from deepface import DeepFace
import numpy as np
import cv2
import logging
from collections import Counter, deque

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionAnalyzer:
    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        # Use a smaller window for faster response
        self.emotion_history = deque(maxlen=3)
        self.confidence_history = deque(maxlen=3)
        
        # Optimized emotion weights
        self.emotion_weights = {
            'happy': 1.2,     # Increase sensitivity to happiness
            'surprise': 1.2,   # Increase sensitivity to surprise
            'angry': 1.0,      # Keep anger as baseline
            'fear': 1.0,       # Keep fear as baseline
            'sad': 1.0,        # Keep sadness as baseline
            'disgust': 1.0,    # Keep disgust as baseline
            'neutral': 0.8     # Slightly decrease neutral
        }
        
        # Simplified confidence thresholds
        self.confidence_thresholds = {
            'happy': 0.20,     # Lower threshold for happiness
            'surprise': 0.20,  # Lower threshold for surprise
            'neutral': 0.30,   # Higher threshold for neutral
            'default': 0.25    # Default threshold for other emotions
        }
        
    def enhance_contrast(self, img):
        """Fast contrast enhancement for real-time processing."""
        if len(img.shape) == 3:
            # Convert to LAB color space
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Quick CLAHE
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            
            # Merge and convert back
            return cv2.cvtColor(cv2.merge((cl,a,b)), cv2.COLOR_LAB2BGR)
        return img

    def preprocess_face(self, face_img):
        """Fast face preprocessing for real-time detection."""
        # Quick resize if needed
        if face_img.shape[0] < 96 or face_img.shape[1] < 96:
            face_img = cv2.resize(face_img, (96, 96))
        
        # Basic contrast enhancement
        face_img = self.enhance_contrast(face_img)
        
        return face_img

    def analyze_emotion(self, face_img):
        """
        Fast emotion analysis optimized for real-time performance.
        
        Args:
            face_img: Face image (BGR format)
            
        Returns:
            tuple: (dominant_emotion, confidence)
        """
        try:
            # Basic validation
            if face_img is None or face_img.size == 0:
                return 'neutral', 0.0

            # Quick preprocessing
            processed_face = self.preprocess_face(face_img)
            
            # Single fast analysis with opencv backend
            try:
                result = DeepFace.analyze(
                    processed_face,
                    actions=['emotion'],
                    enforce_detection=False,
                    detector_backend='opencv',  # Fastest backend
                    silent=True
                )
                emotions = result[0]['emotion']
            except Exception as e:
                logger.debug(f"Analysis failed: {str(e)}")
                return 'neutral', 0.0

            # Apply emotion weights
            weighted_emotions = {
                emo: emotions[emo] * self.emotion_weights.get(emo, 1.0)
                for emo in self.emotions
            }
            
            # Get dominant emotion
            dominant_emotion = max(weighted_emotions.items(), key=lambda x: x[1])
            confidence = emotions[dominant_emotion[0]] / 100.0
            
            # Check confidence threshold
            threshold = self.confidence_thresholds.get(
                dominant_emotion[0], 
                self.confidence_thresholds['default']
            )
            
            if confidence < threshold:
                # Look for next best emotion that meets threshold
                sorted_emotions = sorted(weighted_emotions.items(), key=lambda x: x[1], reverse=True)
                for emotion, _ in sorted_emotions[1:]:
                    conf = emotions[emotion] / 100.0
                    if conf >= self.confidence_thresholds.get(emotion, self.confidence_thresholds['default']):
                        dominant_emotion = (emotion, weighted_emotions[emotion])
                        confidence = conf
                        break
            
            # Update history
            self.emotion_history.append(dominant_emotion[0])
            self.confidence_history.append(confidence)
            
            # Simple temporal smoothing
            if len(self.emotion_history) >= 2:
                # If last two emotions are the same, use that
                if self.emotion_history[-1] == self.emotion_history[-2]:
                    return dominant_emotion[0], confidence
            
            return dominant_emotion[0], confidence
            
        except Exception as e:
            logger.error(f"Error in emotion analysis: {str(e)}")
            return 'neutral', 0.1
    
    def get_emotion_color(self, emotion):
        """
        Get color for emotion visualization.
        
        Args:
            emotion: Emotion name
            
        Returns:
            tuple: BGR color values
        """
        color_map = {
            'happy': (0, 255, 255),     # Yellow
            'sad': (255, 128, 0),       # Orange
            'angry': (0, 0, 255),       # Red
            'surprise': (255, 255, 0),   # Cyan
            'fear': (255, 0, 255),      # Magenta
            'disgust': (0, 255, 0),     # Green
            'neutral': (255, 255, 255),  # White
            'unknown': (128, 128, 128)   # Gray
        }
        return color_map.get(emotion, (128, 128, 128))
    
    def get_emotion_emoji(self, emotion):
        """
        Get emoji for emotion visualization.
        
        Args:
            emotion: Emotion name
            
        Returns:
            str: Emoji character
        """
        emoji_map = {
            'happy': '😄',
            'sad': '😢',
            'angry': '😡',
            'surprise': '😮',
            'fear': '😨',
            'disgust': '🤢',
            'neutral': '😐',
            'unknown': '❓'
        }
        return emoji_map.get(emotion, '❓')
    
    def get_emotion_description(self, emotion, confidence):
        """
        Get a description of the emotion.
        
        Args:
            emotion: Emotion name
            confidence: Confidence score
            
        Returns:
            str: Description of the emotion
        """
        descriptions = {
            'happy': f"Happy ({confidence:.0%} confidence)",
            'sad': f"Sad ({confidence:.0%} confidence)",
            'angry': f"Angry ({confidence:.0%} confidence)",
            'surprise': f"Surprised ({confidence:.0%} confidence)",
            'fear': f"Afraid ({confidence:.0%} confidence)",
            'disgust': f"Disgusted ({confidence:.0%} confidence)",
            'neutral': f"Neutral ({confidence:.0%} confidence)",
            'unknown': "Unable to determine emotion"
        }
        return descriptions.get(emotion, "Unable to determine emotion") 