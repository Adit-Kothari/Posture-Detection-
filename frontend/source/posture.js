 
import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';

function App() {
  const [mode, setMode] = useState('webcam'); // 'webcam' or 'upload'
  const [activity, setActivity] = useState('squat'); // 'squat' or 'sitting'
  const [feedback, setFeedback] = useState([]);
  const [file, setFile] = useState(null);
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);

  // Process video frame
  const processFrame = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    const response = await fetch('http://localhost:5000/process_frame', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ image: imageSrc, activity })
    });
    const data = await response.json();
    setFeedback([...feedback, data.feedback]);
    drawLandmarks(data.landmarks);
  };

  // Draw pose landmarks on canvas
  const drawLandmarks = (landmarks) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    landmarks.forEach(point => {
      ctx.beginPath();
      ctx.arc(point.x * canvas.width, point.y * canvas.height, 5, 0, 2 * Math.PI);
      ctx.fillStyle = '#FF0000';
      ctx.fill();
    });
  };

  // Handle file upload
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('video', file);
    formData.append('activity', activity);
    
    const response = await fetch('http://localhost:5000/process_video', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    setFeedback(data.feedback);
  };

  return (
    <div className="App">
      <h1>Posture Detection</h1>
      <div>
        <button onClick={() => setMode('webcam')}>Webcam</button>
        <button onClick={() => setMode('upload')}>Upload Video</button>
        <select onChange={(e) => setActivity(e.target.value)}>
          <option value="squat">Squat</option>
          <option value="sitting">Desk Sitting</option>
        </select>
      </div>

      {mode === 'webcam' ? (
        <div>
          <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg" />
          <button onClick={processFrame}>Analyze Frame</button>
          <canvas ref={canvasRef} width={640} height={480} />
        </div>
      ) : (
        <div>
          <input type="file" accept="video/*" onChange={handleUpload} />
        </div>
      )}

      <div className="feedback">
        {feedback.map((msg, i) => (
          <p key={i} style={{ color: msg.includes('BAD') ? 'red' : 'green' }}>
            {msg}
          </p>
        ))}
      </div>
    </div>
  );
}

export default App;