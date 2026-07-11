import re
import sys
import os

# Adjust path to import app package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app.models.user import User
from app.models.student import Student
from app.models.profile import UserProfile
from app.models.portfolio import PortfolioCustomization

def sanitize_name(name):
    if not name:
        return ""
    return re.sub(r'[^a-z0-9]', '', name.lower())

def main():
    dry_run = "--run" not in sys.argv
    if dry_run:
        print("=" * 60)
        print("DRY RUN MODE - NO CHANGES WILL BE APPLIED TO THE DATABASE")
        print("To apply changes, run: python scripts/generate_kce_emails.py --run")
        print("=" * 60)

    db = SessionLocal()
    try:
        # Keep track of assigned emails in this run to avoid internal duplicates
        assigned_emails = set()

        # Step 1: Process Student Users
        print("\n--- Processing Students ---")
        students = db.query(Student).all()
        for student in students:
            base_email = sanitize_name(student.name)
            if not base_email:
                base_email = f"student{student.id}"
            
            email = f"{base_email}@kce.ac.in"
            
            # Check duplicate
            if email in assigned_emails:
                reg_suffix = sanitize_name(student.register_no)
                email = f"{base_email}{reg_suffix}@kce.ac.in"
            
            if email in assigned_emails:
                email = f"{base_email}{student.id}@kce.ac.in"
                
            assigned_emails.add(email)
            old_email = student.email
            print(f"Student {student.register_no} ({student.name}): {old_email} -> {email}")
            
            if not dry_run:
                # Update Student
                student.email = email
                # Update User
                user = db.query(User).filter(User.id == student.user_id).first()
                if user:
                    user.email = email
                # Update Portfolio Customization
                port = db.query(PortfolioCustomization).filter(PortfolioCustomization.student_id == student.id).first()
                if port:
                    port.email = email

        # Step 2: Process Non-Student Users
        print("\n--- Processing Staff/Admin ---")
        users = db.query(User).filter(User.role != "student").all()
        for user in users:
            # Try to get profile name
            profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
            
            # Special override for the mentor:
            if user.role == "mentor":
                if not dry_run and profile:
                    profile.full_name = "Dr. Monisha R"
                name = "Dr. Monisha R"
                email = "monisha.r@kce.ac.in"
            else:
                name = profile.full_name if profile else user.username
                base_email = sanitize_name(name)
                if not base_email:
                    base_email = f"user{user.id}"
                email = f"{base_email}@kce.ac.in"
                
                if email in assigned_emails:
                    email = f"{base_email}{user.id}@kce.ac.in"
                
            assigned_emails.add(email)
            old_email = user.email
            print(f"{user.role.upper()} ({name}): {old_email} -> {email}")
            
            if not dry_run:
                # Update User
                user.email = email
                # Update User Profile
                if profile:
                    profile.email = email

        if not dry_run:
            db.commit()
            print("\nDatabase changes committed successfully!")
        else:
            print("\nDry run completed. No database changes were made.")

    except Exception as e:
        db.rollback()
        print(f"\nError: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
