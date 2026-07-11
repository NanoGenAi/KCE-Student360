import os
import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException
from app.config import settings

# Attempt to import Supabase client dynamically if keys exist
supabase_client = None
if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
    try:
        from supabase import create_client
        supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
    except Exception as e:
        print(f"Warning: Failed to initialize Supabase client: {e}")

ALLOWED_EXTENSIONS = {
    "profile": {".jpg", ".jpeg", ".png", ".webp"},
    "resumes": {".pdf", ".doc", ".docx"},
    "projects": {".jpg", ".jpeg", ".png", ".webp", ".pdf"},
    "certificates": {".jpg", ".jpeg", ".png", ".webp", ".pdf"},
    "achievements": {".jpg", ".jpeg", ".png", ".webp", ".pdf"}
}

def get_safe_filename(original_filename: str) -> str:
    """Generates a clean filename using timestamp and a random UUID."""
    ext = os.path.splitext(original_filename)[1].lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_id = uuid.uuid4().hex[:8]
    return f"{timestamp}_{random_id}{ext}"

async def save_upload_file(file: UploadFile, folder: str) -> str:
    """
    Saves an uploaded file either to Supabase Storage or to the local filesystem.
    
    Args:
        file (UploadFile): The uploaded file object.
        folder (str): Target subfolder name ('profile', 'resumes', 'projects', 'certificates', 'achievements').
        
    Returns:
        str: The accessible URL/path of the saved file.
    """
    if folder not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid upload category: '{folder}'")
        
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS[folder]:
        raise HTTPException(
            status_code=400, 
            detail=f"Extension '{ext}' not allowed for category '{folder}'. Allowed: {list(ALLOWED_EXTENSIONS[folder])}"
        )

    filename = get_safe_filename(file.filename)
    
    # Read file content bytes
    content = await file.read()
    
    # Reset file cursor just in case it is read again
    await file.seek(0)

    # 1. Supabase Storage Option
    if supabase_client and settings.SUPABASE_STORAGE_BUCKET:
        try:
            bucket = settings.SUPABASE_STORAGE_BUCKET
            # Path inside the bucket: folder/filename (e.g. profile/20260709_100000_abcd.png)
            path_in_bucket = f"{folder}/{filename}"
            
            # Perform upload using supabase storage client
            content_type = file.content_type or "application/octet-stream"
            response = supabase_client.storage.from_(bucket).upload(
                path=path_in_bucket,
                file=content,
                file_options={"content-type": content_type}
            )
            
            # Obtain the public URL
            public_url = supabase_client.storage.from_(bucket).get_public_url(path_in_bucket)
            return public_url
        except Exception as e:
            # Fallback to local save if Supabase upload fails
            print(f"Supabase Storage upload failed, falling back to local storage. Error: {e}")

    # 2. Local Storage Fallback
    local_folder_path = os.path.join(settings.UPLOAD_DIR, folder)
    os.makedirs(local_folder_path, exist_ok=True)
    
    local_file_path = os.path.join(local_folder_path, filename)
    with open(local_file_path, "wb") as f:
        f.write(content)
        
    # Return path compatible with static route mapping
    return f"/uploads/{folder}/{filename}"
