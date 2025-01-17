# 🔊 Video Surveillance System Using Deep Learning 🔍🔥🛡️

## Overview  
This **Video Surveillance System** leverages cutting-edge deep learning techniques to detect **violence**, **fire**, and **weapons** in real-time. It ensures proactive threat detection to enhance security in various environments, such as public spaces, offices, and industrial areas. 🚨  

### Key Features  
- **Violence Detection**: Utilizes RCNN to identify violent activities in monitored areas. 🥊  
- **Fire Detection**: Identifies fire outbreaks with RCNN, ensuring timely alerts for fire safety. 🔥  
- **Weapon Detection**: Employs Faster RCNN to recognize firearms and other weapons, ensuring enhanced security. 🔫  
- **Real-Time Monitoring**: Connects to network cameras and processes video streams with minimal latency. 🕒  
- **Mobile Notifications**: Sends instant alerts to a connected Flutter-based mobile application. 📱  

---

## 🛠️ System Architecture  
1. **Models**:  
   - **RCNN** for violence and fire detection.  
   - **Faster RCNN** for weapon detection.  

2. **Deployment**:  
   - Three models deployed separately on different systems (e.g., laptops or AWS EC2 instances).  
   - Each model processes video feeds from network cameras.  

3. **Communication**:  
   - Detected events are communicated to a central mobile application using APIs.  

---

## 🚀 Installation  

### Prerequisites  
- Python 3.8+  
- TensorFlow / PyTorch (for model loading)  
- OpenCV (for video stream handling)  
- Flask (for API development)  
- Flutter (for mobile app interface)  

---

## ⚙️ Customization  
- **Camera Settings**: Modify `camera_config.json` to add multiple RTSP streams.  
- **Alert Configuration**: Customize thresholds for detection sensitivity in `config.py`.  
- **Mobile Notifications**: Use the `flutter_local_notifications` package for Android notifications.  

---

## 📊 Results  
- Achieved **high accuracy** for violence, fire, and weapon detection in diverse environments.  
- The system demonstrates **low latency** even with continuous real-time processing.  

---

## 🛡️ Security and Privacy  
The system is designed with privacy in mind. All video streams are processed locally, ensuring sensitive data remains secure. 🔒  

---

## 💬 Feedback  
Feel free to report issues or suggest features by creating a GitHub issue. Contributions are always welcome!  

---

## 🏆 Credits  
- **Deep Learning Models**: RCNN, Faster RCNN
- **Frameworks**: TensorFlow, PyTorch, OpenCV
- **Mobile App**: Flutter
