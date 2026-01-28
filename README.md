Face Recognition Attendance System

An AI-powered system that automatically tracks attendance using facial recognition.

  Features
- Real-time recognition - Identifies people instantly via webcam
- Automatic logging - Saves attendance with timestamps to CSV files
- One-shot learning - Learns from just 1 photo per person
- No database needed - Uses simple CSV files
- Works offline - All processing happens on your computer

 Quick Start

 1. Install Requirements
pip install opencv-python face-recognition numpy pandas

 2. Enroll People (Teach the AI)
Run `enroll.py`, enter a name, and press SPACEBAR to capture face images.

 3. Start Attendance System
Run `recognize.py` - the AI will automatically recognize people and log attendance.

 4. Check Records
Attendance is saved in `attendance_records/attendance_YYYY-MM-DD.csv`

 📁 Project Structure

├── enroll.py           
├── recognize.py         
├── known_faces/         
└── attendance_records/  


  How It Works
1. Enrollment: Takes photos → Converts faces to 128-number "fingerprints"
2. Recognition: Camera sees face → Compares with known fingerprints → Identifies person
3. Logging: Saves name + timestamp to CSV → Creates daily reports

  Key Settings
- Similarity threshold: 60% (0.6) required for recognition
- Processing speed: 25% frame size for real-time performance
- Duplicate prevention: 10-second cooldown between logs

 ⚠️Requirements
- Python 3.8+
- Webcam
- 4GB+ RAM

  Tips
- Ensure good lighting for best accuracy
- Use frontal face images during enrollment
- Green box = Recognized, Red box = Unknown

  Output Format
CSV files contain: `Name, Date, Time, Status`
Example: `John, 2024-01-15, 09:30:15, Present`

