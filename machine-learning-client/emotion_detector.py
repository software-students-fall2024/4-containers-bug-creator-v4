"""
Emotion detection module that captures images from camera,
detects emotions, and stores results in MongoDB.
"""
from datetime import datetime
import cv2
from fer import FER
from pymongo import MongoClient

def connect_to_mongodb():
    """
    Establishes connection to MongoDB and returns the emotions collection.
    
    Returns:
        MongoDB collection object for emotions data
    """
    client = MongoClient('mongodb://admin:password@localhost:27017/')
    db = client['emotions_db']
    return db['emotions']

def capture_and_detect():
    """
    Captures video from camera, detects emotions in faces,
    and stores results in MongoDB. Press SPACE to capture,
    ESC to exit.
    """
    cap = cv2.VideoCapture(0)
    detector = FER(mtcnn=True)
    emotions_collection = connect_to_mongodb()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Emotion Detection', frame)
        
        key = cv2.waitKey(1)
        if key == 32:  # 空格键的ASCII码
            result = detector.detect_emotions(frame)
            
            if result:
                emotions = result[0]['emotions']
                dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
                
                record = {
                    'timestamp': datetime.now(),
                    'dominant_emotion': dominant_emotion,
                    'all_emotions': emotions
                }
                emotions_collection.insert_one(record)
                
                print(f"Detected emotion: {dominant_emotion}")
                print("Results saved to MongoDB")
        
        elif key == 27:  # ESC键的ASCII码
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_detect()
