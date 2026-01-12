import pandas as pd
import os
import glob

def view_all_attendance():
    """View all attendance records"""
    records = glob.glob("attendance_records/*.csv")
    
    if not records:
        print("No attendance records found!")
        return
    
    print("\n📊 ALL ATTENDANCE RECORDS")
    print("="*60)
    
    for record in sorted(records):
        date = record.split("_")[-1].replace(".csv", "")
        df = pd.read_csv(record)
        print(f"\n📅 Date: {date}")
        print(f"   Total Present: {len(df)}")
        print("   Present:", ", ".join(df["Name"].unique()))

if __name__ == "__main__":
    view_all_attendance()