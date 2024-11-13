import cv2
import numpy as np
from fer import FER
from pymongo import MongoClient
from datetime import datetime

def connect_to_mongodb():
    # 连接到MongoDB
    client = MongoClient('mongodb://admin:password@localhost:27017/')
    db = client['emotions_db']
    return db['emotions']

def capture_and_detect():
    # 初始化摄像头
    cap = cv2.VideoCapture(0)
    
    # 初始化情绪检测器
    detector = FER(mtcnn=True)
    
    # 连接MongoDB
    emotions_collection = connect_to_mongodb()
    
    while True:
        # 捕获画面
        ret, frame = cap.read()
        if not ret:
            break
            
        # 显示画面
        cv2.imshow('Emotion Detection', frame)
        
        # 按空格键拍照并检测
        key = cv2.waitKey(1)
        if key == 32:  # 空格键的ASCII码
            # 进行情绪检测
            result = detector.detect_emotions(frame)
            
            if result:
                # 获取检测结果
                emotions = result[0]['emotions']
                dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
                
                # 保存到MongoDB
                record = {
                    'timestamp': datetime.now(),
                    'dominant_emotion': dominant_emotion,
                    'all_emotions': emotions
                }
                emotions_collection.insert_one(record)
                
                print(f"Detected emotion: {dominant_emotion}")
                print("Results saved to MongoDB")
        
        # 按ESC退出
        elif key == 27:  # ESC键的ASCII码
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_detect()
