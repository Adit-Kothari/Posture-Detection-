
from flask import Flask, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
import base64

app = Flask(__name__)
mp_pose = mp.solutions.pose

# Rule-based analysis functions
def analyze_squat(landmarks):
    feedback = []
    # Knee beyond toe check
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    if knee.x < ankle.x: 
        feedback.append("BAD: Knee beyond toes")
    
    # Back angle check
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    back_angle = calculate_angle(shoulder, hip, knee)
    if back_angle < 150: 
        feedback.append(f"BAD: Back angle too shallow ({back_angle:.1f}°)")
    
    return feedback or ["Good posture"]

def analyze_sitting(landmarks):
    feedback = []
    # Neck bend check
    ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    neck_angle = calculate_angle(ear, shoulder, (shoulder.x, shoulder.y+0.1))
    if neck_angle > 30: 
        feedback.append(f"BAD: Neck bend too extreme ({neck_angle:.1f}°)")
    
    # Back straightness check
    shoulder_center = midpoint(
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    )
    hip_center = midpoint(
        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    )
    back_angle = calculate_angle(shoulder_center, hip_center, (hip_center.x, hip_center.y+0.1))
    if abs(back_angle - 180) > 15: 
        feedback.append(f"BAD: Back not straight ({back_angle:.1f}°)")
    
    return feedback or ["Good posture"]

# Helper functions
def calculate_angle(a, b, c):
    # Calculate angle between three points
    ba = np.array([a.x - b.x, a.y - b.y])
    bc = np.array([c.x - b.x, c.y - b.y])
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(cosine))

def midpoint(a, b):
    return mp.solutions.pose.PoseLandmark(
        x=(a.x + b.x)/2,
        y=(a.y + b.y)/2,
        visibility=(a.visibility + b.visibility)/2
    )

# API Endpoints
@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.json
    img_data = base64.b64decode(data['image'].split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    with mp_pose.Pose() as pose:
        results = pose.process(img)
        if results.pose_landmarks:
            feedback = analyze_squat(results.pose_landmarks.landmark) \
                if data['activity'] == 'squat' \
                else analyze_sitting(results.pose_landmarks.landmark)
            
            return jsonify({
                'feedback': feedback,
                'landmarks': [
                    {'x': lm.x, 'y': lm.y} 
                    for lm in results.pose_landmarks.landmark
                ]
            })
    
    return jsonify({'feedback': ['No pose detected'], 'landmarks': []})

@app.route('/process_video', methods=['POST'])
def process_video():
    # Video processing logic (similar to frame processing but for all frames)
    # Returns aggregated feedback
    return jsonify({'feedback': ['Video processed']})

if __name__ == '__main__':
    app.run(debug=True)