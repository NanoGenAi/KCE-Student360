from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter()

@router.get("/overview")
async def get_admin_overview():
    """Skeleton route for retrieving administrative system overview statistics."""
    return {
        "total_students": 0,
        "total_faculty": 0,
        "total_mentors": 0,
        "total_users": 0,
        "total_scores_uploaded": 0
    }

# Students CRUD
@router.get("/students")
async def admin_get_students():
    return []

@router.post("/students")
async def admin_create_student(payload: Dict[str, Any]):
    return {"success": True}

@router.put("/students/{id}")
async def admin_update_student(id: int, payload: Dict[str, Any]):
    return {"success": True}

@router.delete("/students/{id}")
async def admin_delete_student(id: int):
    return {"success": True}

# Faculty CRUD
@router.get("/faculty")
async def admin_get_faculty():
    return []

@router.post("/faculty")
async def admin_create_faculty(payload: Dict[str, Any]):
    return {"success": True}

@router.put("/faculty/{id}")
async def admin_update_faculty(id: int, payload: Dict[str, Any]):
    return {"success": True}

@router.delete("/faculty/{id}")
async def admin_delete_faculty(id: int):
    return {"success": True}

# Mentors CRUD
@router.get("/mentors")
async def admin_get_mentors():
    return []

@router.post("/mentors")
async def admin_create_mentor(payload: Dict[str, Any]):
    return {"success": True}

@router.put("/mentors/{id}")
async def admin_update_mentor(id: int, payload: Dict[str, Any]):
    return {"success": True}

@router.delete("/mentors/{id}")
async def admin_delete_mentor(id: int):
    return {"success": True}

# Users CRUD
@router.get("/users")
async def admin_get_users():
    return []

@router.post("/users")
async def admin_create_user(payload: Dict[str, Any]):
    return {"success": True}

@router.put("/users/{id}")
async def admin_update_user(id: int, payload: Dict[str, Any]):
    return {"success": True}

@router.delete("/users/{id}")
async def admin_delete_user(id: int):
    return {"success": True}

# Mentor Assignments CRUD
@router.get("/mentor-assignments")
async def admin_get_assignments():
    return []

@router.post("/mentor-assignments")
async def admin_create_assignment(payload: Dict[str, Any]):
    return {"success": True}

@router.delete("/mentor-assignments/{id}")
async def admin_delete_assignment(id: int):
    return {"success": True}
