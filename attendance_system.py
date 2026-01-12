import os
import sys
import subprocess

def show_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("        FACE RECOGNITION ATTENDANCE SYSTEM")
    print("="*60)
    print("\nMain Menu:")
    print("1. Enroll New Person")
    print("2. Start Attendance Marking")
    print("3. View Today's Attendance")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    return choice

def view_attendance():
    """Display today's attendance records"""
    from datetime import datetime
    import pandas as pd
    
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"attendance_records/attendance_{today}.csv"
    
    if os.path.exists(filename):
        print(f"\n📋 Attendance for {today}:")
        print("-"*40)
        
        df = pd.read_csv(filename)
        print(df.to_string(index=False))
        
        print(f"\nTotal Present: {len(df)}")
    else:
        print(f"\nNo attendance records found for {today}")
    
    input("\nPress Enter to continue...")

def main():
    """Main program loop"""
    while True:
        choice = show_menu()
        
        if choice == "1":
            print("\nLaunching Enrollment System...")
            subprocess.run([sys.executable, "enroll.py"])
        
        elif choice == "2":
            print("\nLaunching Recognition System...")
            subprocess.run([sys.executable, "recognize.py"])
        
        elif choice == "3":
            view_attendance()
        
        elif choice == "4":
            print("\nThank you for using the Attendance System!")
            print("Goodbye! 👋")
            break
        
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()