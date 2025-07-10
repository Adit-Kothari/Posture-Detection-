 // frontend/src/api.js
import axios from 'axios';

const API_BASE = process.env.NODE_ENV === 'production' 
  ? process.env.REACT_APP_API_URL 
  : 'http://localhost:5000';

export const processFrame = async (imageSrc, activity) => {
  try {
    const response = await axios.post(`${API_BASE}/process_frame`, {
      image: imageSrc,
      activity
    });
    return response.data;
  } catch (error) {
    console.error('Error processing frame:', error);
    return { feedback: ['Connection failed'], landmarks: [] };
  }
};

export const processVideo = async (videoFile, activity) => {
  try {
    const formData = new FormData();
    formData.append('video', videoFile);
    formData.append('activity', activity);
    
    const response = await axios.post(`${API_BASE}/process_video`, formData, {
      headers: {'Content-Type': 'multipart/form-data'}
    });
    return response.data;
  } catch (error) {
    console.error('Error processing video:', error);
    return { feedback: ['Connection failed'] };
  }
};