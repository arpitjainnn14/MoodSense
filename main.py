import sys
import cv2
from PyQt5.QtWidgets import QApplication
from face_detector import FaceDetector
from emotion_analyzer import EmotionAnalyzer
from gui import EmotionDetectionGUI
from utils import create_directories
from settings import Settings

def main():
    # Create necessary directories
    create_directories()
    
    # Initialize settings
    settings = Settings()
    
    # Initialize components
    face_detector = FaceDetector()
    emotion_analyzer = EmotionAnalyzer()
    
    # Create and show GUI
    app = QApplication(sys.argv)
    app.setApplicationName("Emotion Detection")
    app.setOrganizationName("MoodDetection")
    
    # Set application style
    app.setStyle('Fusion')  # Use Fusion style for consistent look across platforms
    
    window = EmotionDetectionGUI(face_detector, emotion_analyzer)
    window.show()
    
    # Start the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 