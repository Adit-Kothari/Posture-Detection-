Posture Detection App
A full-stack application that analyzes posture during squats and desk sitting using computer vision and rule-based logic.
Features
Real-time webcam posture analysis
Video upload processing
Squat & desk sitting evaluation
Visual feedback with pose landmarks
Rule-based bad posture detection
Tech Stack
Frontend: React.js
Backend: Flask, MediaPipe, OpenCV
Deployment: Vercel (Frontend), Render (Backend)
Project Structure
posture-detection-app/
├── backend/                   # Flask backend
│   ├── posture.py             # API and pose analysis
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React frontend
│   ├── public/                # Static assets
│   │   └── index.html         # Main HTML template
│   ├── src/                   # Source code
│   │   ├── posture.js         # Main React component
│   │   ├── api.js             # API service
│   │   ├── index.js           # React entry point
│   │   └── index.css          # Styling
│   └── package.json           # Frontend dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation


