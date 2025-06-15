from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QComboBox, QFrame, QGridLayout, QStatusBar,
                             QMenuBar, QMenu, QAction, QShortcut, QMessageBox, QDialog)
from PyQt5.QtCore import Qt, QTimer, QSize, QSettings
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont, QColor, QPalette, QKeySequence
import cv2
import sys
import os
from datetime import datetime
import numpy as np
from settings import Settings, SettingsDialog

class EmotionDetectionGUI(QMainWindow):
    def __init__(self, face_detector, emotion_analyzer):
        super().__init__()
        self.face_detector = face_detector
        self.emotion_analyzer = emotion_analyzer
        self.settings = Settings()
        self.settings.settings_changed.connect(self.apply_settings)
        
        # Initialize camera with settings
        self.camera_index = int(self.settings.get('camera_index', 0))
        self.cap = cv2.VideoCapture(self.camera_index)
        
        # Initialize status bar
        self.statusBar().showMessage("Ready")  # Use the built-in statusBar() method
        
        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()
        self.setup_timer()
        self.apply_settings()
        
    def setup_menu(self):
        """Setup the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        theme_menu = view_menu.addMenu('Theme')
        dark_theme = QAction('Dark', self)
        light_theme = QAction('Light', self)
        dark_theme.triggered.connect(lambda: self.settings.set('theme', 'dark'))
        light_theme.triggered.connect(lambda: self.settings.set('theme', 'light'))
        theme_menu.addAction(dark_theme)
        theme_menu.addAction(light_theme)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        shortcuts_action = QAction('Keyboard Shortcuts', self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Start/Stop detection
        start_shortcut = QShortcut(QKeySequence('Space'), self)
        start_shortcut.activated.connect(self.toggle_detection)
        
        # Capture screenshot
        capture_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        capture_shortcut.activated.connect(self.capture_screenshot)
        
        # Settings
        settings_shortcut = QShortcut(QKeySequence('Ctrl+,'), self)
        settings_shortcut.activated.connect(self.show_settings)
        
        # Exit
        exit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        exit_shortcut.activated.connect(self.close)
        
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_() == QDialog.Accepted:
            self.apply_settings()
            
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Emotion Detection",
            "Real-time Face and Mood Detection System\n\n"
            "Version 1.0\n\n"
            "A powerful tool for real-time emotion analysis using computer vision and deep learning.\n\n"
            "Created by Arpit Jain © 2025 ❤️")
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        shortcuts = {
            'Space': 'Start/Stop detection',
            'Ctrl+S': 'Capture screenshot',
            'Ctrl+,': 'Open settings',
            'Ctrl+Q': 'Exit application'
        }
        
        msg = "Keyboard Shortcuts:\n\n"
        for key, desc in shortcuts.items():
            msg += f"{key}: {desc}\n"
            
        QMessageBox.information(self, "Keyboard Shortcuts", msg)
        
    def apply_settings(self):
        """Apply current settings"""
        # Apply theme
        theme = self.settings.get('theme', 'dark')
        if theme == 'dark':
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #0d47a1;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #1565c0;
                }
                QMenuBar {
                    background-color: #363636;
                    color: white;
                }
                QMenuBar::item:selected {
                    background-color: #0d47a1;
                }
                QMenu {
                    background-color: #363636;
                    color: white;
                }
                QMenu::item:selected {
                    background-color: #0d47a1;
                }
                QStatusBar {
                    background-color: #363636;
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #f5f5f5;
                    color: #000000;
                }
                QLabel {
                    color: #000000;
                }
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                QMenuBar {
                    background-color: #ffffff;
                    color: #000000;
                }
                QMenuBar::item:selected {
                    background-color: #2196f3;
                    color: white;
                }
                QMenu {
                    background-color: #ffffff;
                    color: #000000;
                }
                QMenu::item:selected {
                    background-color: #2196f3;
                    color: white;
                }
                QStatusBar {
                    background-color: #ffffff;
                    color: #000000;
                }
            """)
            
        # Update camera if needed
        new_camera_index = int(self.settings.get('camera_index', 0))
        if new_camera_index != self.camera_index:
            self.camera_index = new_camera_index
            self.cap.release()
            self.cap = cv2.VideoCapture(self.camera_index)
            
        # Update detection interval
        self.timer.setInterval(int(self.settings.get('detection_interval', 30)))
        
    def setup_timer(self):
        """Setup timer for video processing"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_frame)
        self.timer.setInterval(int(self.settings.get('detection_interval', 30)))
        
    def process_frame(self):
        """Process video frame with enhanced visualization"""
        ret, frame = self.cap.read()
        if not ret:
            self.statusBar().showMessage("Error: Cannot read from camera", 3000)
            return
            
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Show FPS if enabled
        if self.settings.get('show_fps') == 'true':
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Detect faces and emotions
        faces, _ = self.face_detector.detect_faces(frame)
        
        for (x, y, w, h) in faces:
            # Extract face region
            face_img = frame[y:y+h, x:x+w]
            
            # Analyze emotion
            emotion, confidence = self.emotion_analyzer.analyze_emotion(face_img)
            
            # Update emotion display
            self.update_emotion_display(emotion, confidence)
            
            # Update statistics
            self.stats_labels[emotion].setText(str(int(self.stats_labels[emotion].text()) + 1))
            
            # Draw face rectangle with emotion color
            color = self.emotion_analyzer.get_emotion_color(emotion)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Add emotion text above face
            text = f"{emotion.upper()} ({confidence:.0%})"
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            
            # Add emoji next to face
            emoji = self.emotion_analyzer.get_emotion_emoji(emotion)
            cv2.putText(frame, emoji, (x+w+10, y+30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 2)
        
        # Convert frame to QImage and display
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Scale image to fit label while maintaining aspect ratio
        scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
            self.video_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.video_label.setPixmap(scaled_pixmap)
        
    def closeEvent(self, event):
        """Clean up resources when closing the application"""
        reply = QMessageBox.question(self, 'Confirm Exit',
                                   "Are you sure you want to exit?",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.cap.release()
            self.statusBar().showMessage("Application closing...", 1000)
            event.accept()
        else:
            event.ignore()
        
    def setup_ui(self):
        """Setup the user interface with modern layout"""
        self.setWindowTitle("Real-time Emotion Detection")
        self.setMinimumSize(1200, 800)
        self.setWindowIcon(QIcon('icons\emotion analysis.png'))
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel for video feed
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(800)
        
        # Video feed label with border
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("""
            QLabel {
                background-color: #1a1a1a;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        left_layout.addWidget(self.video_label)
        
        # Control buttons in a horizontal layout
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Detection")
        self.start_button.setIcon(QIcon('play.png'))
        self.start_button.clicked.connect(self.toggle_detection)
        
        self.capture_button = QPushButton("Capture Screenshot")
        self.capture_button.setIcon(QIcon('camera.png'))
        self.capture_button.clicked.connect(self.capture_screenshot)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.capture_button)
        left_layout.addLayout(button_layout)
        
        # Right panel for stats and emotion display
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Emotion display frame
        emotion_frame = QFrame()
        emotion_frame.setObjectName("emotionFrame")
        emotion_layout = QVBoxLayout(emotion_frame)
        
        # Large emotion emoji
        self.emotion_emoji = QLabel()
        self.emotion_emoji.setAlignment(Qt.AlignCenter)
        self.emotion_emoji.setFont(QFont('Segoe UI', 72))
        emotion_layout.addWidget(self.emotion_emoji)
        
        # Emotion text with confidence
        self.emotion_label = QLabel()
        self.emotion_label.setAlignment(Qt.AlignCenter)
        self.emotion_label.setFont(QFont('Segoe UI', 24, QFont.Bold))
        emotion_layout.addWidget(self.emotion_label)
        
        # Emotion description
        self.emotion_description = QLabel()
        self.emotion_description.setAlignment(Qt.AlignCenter)
        self.emotion_description.setFont(QFont('Segoe UI', 14))
        self.emotion_description.setWordWrap(True)
        emotion_layout.addWidget(self.emotion_description)
        
        right_layout.addWidget(emotion_frame)
        
        # Statistics frame
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        stats_layout = QGridLayout(stats_frame)
        
        # Create stat labels with modern styling
        self.stats_labels = {}
        emotions = ['happy', 'sad', 'angry', 'surprise', 'fear', 'disgust', 'neutral']
        for i, emotion in enumerate(emotions):
            # Emoji label
            emoji_label = QLabel(self.emotion_analyzer.get_emotion_emoji(emotion))
            emoji_label.setFont(QFont('Segoe UI', 20))
            emoji_label.setAlignment(Qt.AlignCenter)
            stats_layout.addWidget(emoji_label, i, 0)
            
            # Emotion name label
            name_label = QLabel(emotion.capitalize())
            name_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
            stats_layout.addWidget(name_label, i, 1)
            
            # Count label
            count_label = QLabel('0')
            count_label.setFont(QFont('Segoe UI', 12))
            stats_layout.addWidget(count_label, i, 2)
            self.stats_labels[emotion] = count_label
        
        right_layout.addWidget(stats_frame)
        right_layout.addStretch()
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 1)
        
        # Initialize emotion display
        self.update_emotion_display('neutral', 0.0)
        
    def update_emotion_display(self, emotion, confidence):
        """Update the emotion display with modern styling"""
        # Update emoji
        self.emotion_emoji.setText(self.emotion_analyzer.get_emotion_emoji(emotion))
        
        # Update emotion text with confidence
        self.emotion_label.setText(f"{emotion.upper()}")
        
        # Update description with confidence
        self.emotion_description.setText(self.emotion_analyzer.get_emotion_description(emotion, confidence))
        
        # Update color based on emotion
        color = self.emotion_analyzer.get_emotion_color(emotion)
        self.emotion_label.setStyleSheet(f"""
            QLabel {{
                color: rgb{color};
                font-weight: bold;
            }}
        """)
        
    def toggle_detection(self):
        """Toggle emotion detection with updated button states and status messages"""
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText("Start Detection")
            self.start_button.setIcon(QIcon('play.png'))
            self.statusBar().showMessage("Detection stopped", 3000)  # Show for 3 seconds
        else:
            self.timer.start()
            self.start_button.setText("Stop Detection")
            self.start_button.setIcon(QIcon('pause.png'))
            self.statusBar().showMessage("Detection started - Analyzing emotions...", 3000)
            
    def capture_screenshot(self):
        """Capture and save screenshot with timestamp and status message"""
        if not self.video_label.pixmap():
            self.statusBar().showMessage("Error: No video feed available", 3000)
            return
            
        # Create screenshots directory if it doesn't exist
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
            
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/emotion_{timestamp}.png"
        
        # Save screenshot
        self.video_label.pixmap().save(filename)
        
        # Show success message with filename
        self.statusBar().showMessage(f"Screenshot saved: {filename}", 3000) 