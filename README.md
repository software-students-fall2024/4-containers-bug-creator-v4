![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Emotion Detection System

![ML Client Build Status](https://github.com/software-students-fall2024/4-containers-bug-creator-v4/actions/workflows/ml-client.yml/badge.svg)
![Web App Build Status](https://github.com/software-students-fall2024/4-containers-bug-creator-v4/actions/workflows/webapp.yml/badge.svg)

## Project Description

A machine learning-based emotion detection system that analyzes facial expressions in images. The system consists of three main components:
- ML Client: Uses DeepFace for emotion recognition
- Web App: Provides user interface for image upload and real-time camera capture
- MongoDB: Stores user data and detection results

### Key Features
- Upload images for emotion detection
- Real-time camera capture and analysis
- View detection history
- User authentication system

### Tech Stack
- ML: TensorFlow, DeepFace, OpenCV
- Backend: Flask, PyMongo
- Frontend: Bootstrap
- Database: MongoDB
- Containerization: Docker, Docker Compose

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Python 3.10+ (for local development)

### Option 1: Using Docker 

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create `.env` file in root directory:
```bash
MONGODB_USERNAME=admin
MONGODB_PASSWORD=password
MONGODB_HOST=mongodb
MONGODB_PORT=27017
MONGODB_DATABASE=emotion_detection
ML_CLIENT_URL=http://ml-client:5001
```

3. Start services:
```bash
docker-compose up -d
```

Access:
- Web App: http://localhost:5000
- MongoDB Express: http://localhost:8081 (admin/pass)

### Option 2: Local Development

1. Start MongoDB:
```bash
docker-compose up mongodb -d
```

2. Set up ML Client:
```bash
cd machine-learning-client
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python api.py
```

3. Set up Web App:
```bash
cd web-app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## System Architecture

### ML Client
- Endpoint: `/detect`
- Method: POST
- Input: Image file
- Output: Emotion analysis results

### Database Schema

1. users
   - user_id
   - email
   - password_hash

2. pictures
   - user_id
   - image (binary)
   - timestamp

3. detection_results
   - user_id
   - picture_id
   - emotions (object)
   - timestamp

## Development

### Code Style
- Black formatter
- Pylint linter
- PEP 8 standards

### Testing
```bash
cd machine-learning-client
pytest

cd ../web-app
pytest
```

## Environment Variables
Required environment variables in `.env`:
```
MONGODB_USERNAME=admin
MONGODB_PASSWORD=password
MONGODB_HOST=mongodb
MONGODB_PORT=27017
MONGODB_DATABASE=emotion_detection
ML_CLIENT_URL=http://ml-client:5001
```

## Contributors:

[**Bowen Ma**](https://github.com/mabowen1013)

[**Hanlin He**](https://github.com/Alpha-He)

[**Junqi Zhao**](https://github.com/JunqiZhao888)

[**Andrew Qin**](https://github.com/Andrewqin1)
