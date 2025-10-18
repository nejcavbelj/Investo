"""
Cleanup script for generated reports
"""

import os
from pathlib import Path
from config.settings import PROJECT_ROOT

def cleanup_old_reports(days_old=7):
    """Clean up reports older than specified days"""
    reports_dir = PROJECT_ROOT / "reports" / "generated"
    
    if not reports_dir.exists():
        print("No reports directory found")
        return
    
    import time
    current_time = time.time()
    cutoff_time = current_time - (days_old * 24 * 60 * 60)
    
    deleted_count = 0
    for file_path in reports_dir.glob("*.html"):
        if file_path.stat().st_mtime < cutoff_time:
            try:
                file_path.unlink()
                deleted_count += 1
                print(f"Deleted: {file_path.name}")
            except Exception as e:
                print(f"Error deleting {file_path.name}: {e}")
    
    print(f"Cleanup complete. Deleted {deleted_count} old reports.")

def cleanup_all_reports():
    """Clean up all reports (use with caution)"""
    reports_dir = PROJECT_ROOT / "reports" / "generated"
    
    if not reports_dir.exists():
        print("No reports directory found")
        return
    
    deleted_count = 0
    for file_path in reports_dir.glob("*.html"):
        try:
            file_path.unlink()
            deleted_count += 1
            print(f"Deleted: {file_path.name}")
        except Exception as e:
            print(f"Error deleting {file_path.name}: {e}")
    
    print(f"Cleanup complete. Deleted {deleted_count} reports.")

if __name__ == "__main__":
    print("Report Cleanup Utility")
    print("1. Clean reports older than 7 days")
    print("2. Clean all reports")
    print("3. Exit")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        cleanup_old_reports()
    elif choice == "2":
        confirm = input("Are you sure you want to delete ALL reports? (y/N): ").strip().lower()
        if confirm == 'y':
            cleanup_all_reports()
        else:
            print("Cancelled")
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice")
