import cv2
import os
import sys

def enroll_person():
    """Capture and save face for a new person"""
    
    print("\n" + "="*50)
    print("FACE ENROLLMENT SYSTEM")
    print("="*50)
    

    name = input("\nEnter person's name: ").strip()
    if not name:
        print("Name cannot be empty!")
        return
    
    
    if not os.path.exists("known_faces"):
        os.makedirs("known_faces")
    
    
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Press SPACE to capture, ESC to quit")
     
    print(f"\nEnrolling: {name}")
    print("Instructions:")
    print("1. Look directly at the camera")
    print("2. Ensure good lighting")
    print("3. Press SPACEBAR to capture")
    print("4. Press ESC to cancel")
    
    img_counter = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Show the video feed
        cv2.imshow("Press SPACE to capture, ESC to quit", frame)
        
        k = cv2.waitKey(1)
        
        # ESC pressed
        if k % 256 == 27:
            print("\nEnrollment cancelled!")
            break
        
        # SPACE pressed
        elif k % 256 == 32:
            # Save the captured image
            img_name = f"known_faces/{name}_{img_counter}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"✓ Image saved as {img_name}")
            img_counter += 1
            
            # Show confirmation
            cv2.imshow("Captured Image", frame)
            cv2.waitKey(2000)
            cv2.destroyWindow("Captured Image")
            
            more = input("\nCapture another image? (y/n): ").lower()
            if more != 'y':
                break
    
    cam.release()
    cv2.destroyAllWindows()
    
    if img_counter > 0:
        print(f"\n✅ Successfully enrolled {name} with {img_counter} image(s)")
    else:
        print("\n❌ No images captured")

if __name__ == "__main__":
    enroll_person()