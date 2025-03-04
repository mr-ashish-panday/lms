import os
import cv2
import time
import numpy as np
import mediapipe as mp

# Initialize Mediapipe Holistic
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Define class names
CLASSES = ["Accident", "Disaster", "First aid", "Help me", "Hungry", "Toilet"]
MP_DATA_PATH = "D:\Minor\GD"

def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, lh, rh])

def get_next_video_number(class_path):
    existing_videos = [int(folder.split('_')[-1]) for folder in os.listdir(class_path) if folder.startswith("video")]
    return max(existing_videos) + 1 if existing_videos else 0

def capture_videos():
    cap = cv2.VideoCapture(0)
    
    with mp_holistic.Holistic(static_image_mode=False) as holistic:
        
        for class_name in CLASSES:
            class_path = os.path.join(MP_DATA_PATH, class_name)
            os.makedirs(class_path, exist_ok=True)
            
            for video_num in range(30):
                video_index = get_next_video_number(class_path)
                video_path = os.path.join(class_path, f"video_{video_index}")
                os.makedirs(video_path, exist_ok=True)
                
                for countdown in range(3, 0, -1):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    cv2.putText(frame, f"Starting capture in {countdown}...", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Capture', frame)
                    if cv2.waitKey(1000) & 0xFF == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                
                paused = False
                frame_count = 0
                
                while frame_count < 30:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = holistic.process(image)
                    
                    # Draw styled landmarks
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                              landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                    mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                              landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style())
                    mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                              landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style())
                    
                    keypoints = extract_keypoints(results)
                    frame_path = os.path.join(video_path, f"frame_{frame_count}.npy")
                    np.save(frame_path, keypoints)
                    
                    frame_count += 1
                    cv2.putText(frame, "Recording... Press 'p' to pause, 'r' to retake, 'q' to quit", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Capture', frame)
                    
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('r'):
                        print("Retake selected. Restarting capture...")
                        os.system(f"rm -rf {video_path}")
                        os.makedirs(video_path, exist_ok=True)
                        break
                    elif key == ord('p'):
                        paused = True
                        while paused:
                            ret, frame = cap.read()
                            cv2.putText(frame, "Paused. Press 'c' to continue, 'q' to quit.", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.imshow('Capture', frame)
                            key = cv2.waitKey(1) & 0xFF
                            if key == ord('c'):
                                paused = False
                            elif key == ord('q'):
                                cap.release()
                                cv2.destroyAllWindows()
                                return
                    elif key == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                
            cv2.putText(frame, f"30 videos for {class_name} collected. Move to next class? (Press any key, 'q' to quit)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Capture', frame)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return
    
    cap.release()
    cv2.destroyAllWindows()


capture_videos()
print("Data collection complete!")
