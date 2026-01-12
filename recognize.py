import cv2
import face_recognition
import os
import numpy as np
import pandas as pd
from datetime import datetime
import time

class FaceRecognizer:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()
        
    def load_known_faces(self):
        """Load all known faces from the folder"""
        print("Loading known faces...")
        
        if not os.path.exists("known_faces"):
            print("No 'known_faces' folder found!")
            return
        
        for filename in os.listdir("known_faces"):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                # Extract name from filename (assumes format: name_number.jpg)
                name = "_".join(filename.split("_")[:-1])
                
                # Load image
                image_path = os.path.join("known_faces", filename)
                image = face_recognition.load_image_file(image_path)
                
                try:
                    # Get face encoding
                    encoding = face_recognition.face_encodings(image)[0]
                    self.known_face_encodings.append(encoding)
                    self.known_face_names.append(name)
                    print(f"  ✓ Loaded: {name}")
                except:
                    print(f"  ✗ Couldn't process: {filename}")
        
        print(f"Loaded {len(self.known_face_names)} known faces\n")
    
    def mark_attendance(self, name):
        """Mark attendance in CSV file"""
        # Create attendance folder if it doesn't exist
        if not os.path.exists("attendance_records"):
            os.makedirs("attendance_records")
        
        # Get current date for filename
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"attendance_records/attendance_{today}.csv"
        
        # Get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")
        
        # Create or load attendance file
        if os.path.exists(filename):
            df = pd.read_csv(filename)
        else:
            df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
        
        # Check if already marked today
        if name in df[df["Date"] == current_date]["Name"].values:
            print(f"  ⚠ {name} already marked today")
            return False
        
        # Add new entry
        new_entry = {
            "Name": name,
            "Date": current_date,
            "Time": current_time,
            "Status": "Present"
        }
        
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(filename, index=False)
        
        print(f"  ✅ Attendance marked for {name} at {current_time}")
        return True
    
    def run_recognition(self):
        """Main recognition loop"""
        print("\n" + "="*50)
        print("FACE RECOGNITION ATTENDANCE SYSTEM")
        print("="*50)
        print("\nStarting camera... Press 'q' to quit\n")
        
        # Initialize video capture
        video_capture = cv2.VideoCapture(0)
        
        # Variables for tracking
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        
        last_recognized = {}
        
        while True:
            # Grab single frame
            ret, frame = video_capture.read()
            
            if not ret:
                print("Failed to grab frame")
                break
            
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
            # Convert BGR to RGB (face_recognition uses RGB)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Process every other frame to save time
            if process_this_frame:
                # Find all faces in current frame
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                face_names = []
                for face_encoding in face_encodings:
                    # See if face matches any known faces
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    
                    # Use the known face with the smallest distance
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        
                        # Check if we should mark attendance (not recognized in last 10 seconds)
                        current_time = time.time()
                        if name not in last_recognized or (current_time - last_recognized[name]) > 10:
                            self.mark_attendance(name)
                            last_recognized[name] = current_time
                    
                    face_names.append(name)
            
            process_this_frame = not process_this_frame
            
            # Display results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations (since we scaled down)
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # Draw box around face
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                
                # Draw label
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            
            # Display attendance stats
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"attendance_records/attendance_{today}.csv"
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                present_count = len(df)
                cv2.putText(frame, f"Present Today: {present_count}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Display frame
            cv2.imshow('Face Recognition Attendance System', frame)
            
            # Break loop with 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        video_capture.release()
        cv2.destroyAllWindows()
        print("\nSystem stopped")

if __name__ == "__main__":
    recognizer = FaceRecognizer()
    if len(recognizer.known_face_names) > 0:
        recognizer.run_recognition()
    else:
        print("No faces found in 'known_faces' folder!")
        print("Please run enroll.py first to add faces.")