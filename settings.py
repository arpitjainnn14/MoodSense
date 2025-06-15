from PyQt5.QtCore import QSettings, QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QCheckBox, QPushButton, QSpinBox, QGroupBox

class Settings(QObject):
    """Application settings manager"""
    settings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.settings = QSettings('MoodDetection', 'EmotionDetector')
        self.load_defaults()

    def load_defaults(self):
        """Load default settings if not set"""
        defaults = {
            'theme': 'dark',
            'camera_index': 0,
            'detection_interval': 30,
            'show_fps': True,
            'save_screenshots': True,
            'emotion_smoothing': 2,
            'min_face_size': 30,
            'detection_quality': 'balanced'  # balanced, performance, quality
        }
        
        for key, value in defaults.items():
            if not self.settings.contains(key):
                self.settings.setValue(key, value)

    def get(self, key, default=None):
        """Get setting value"""
        return self.settings.value(key, default)

    def set(self, key, value):
        """Set setting value"""
        self.settings.setValue(key, value)
        self.settings_changed.emit()

    def reset(self):
        """Reset all settings to defaults"""
        self.settings.clear()
        self.load_defaults()
        self.settings_changed.emit()

class SettingsDialog(QDialog):
    """Settings dialog window"""
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setup_ui()

    def setup_ui(self):
        """Setup the settings dialog UI"""
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        # Theme settings
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout()
        
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['dark', 'light'])
        self.theme_combo.setCurrentText(self.settings.get('theme'))
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Camera settings
        camera_group = QGroupBox("Camera")
        camera_layout = QVBoxLayout()
        
        camera_label = QLabel("Camera Index:")
        self.camera_spin = QSpinBox()
        self.camera_spin.setRange(0, 10)
        self.camera_spin.setValue(int(self.settings.get('camera_index')))
        
        camera_layout.addWidget(camera_label)
        camera_layout.addWidget(self.camera_spin)
        camera_group.setLayout(camera_layout)
        layout.addWidget(camera_group)

        # Detection settings
        detection_group = QGroupBox("Detection")
        detection_layout = QVBoxLayout()
        
        quality_label = QLabel("Detection Quality:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(['balanced', 'performance', 'quality'])
        self.quality_combo.setCurrentText(self.settings.get('detection_quality'))
        
        interval_label = QLabel("Detection Interval (ms):")
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(10, 100)
        self.interval_spin.setValue(int(self.settings.get('detection_interval')))
        
        self.show_fps_check = QCheckBox("Show FPS")
        self.show_fps_check.setChecked(self.settings.get('show_fps') == 'true')
        
        detection_layout.addWidget(quality_label)
        detection_layout.addWidget(self.quality_combo)
        detection_layout.addWidget(interval_label)
        detection_layout.addWidget(self.interval_spin)
        detection_layout.addWidget(self.show_fps_check)
        detection_group.setLayout(detection_layout)
        layout.addWidget(detection_group)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        reset_button = QPushButton("Reset to Defaults")
        
        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.reject)
        reset_button.clicked.connect(self.reset_settings)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(reset_button)
        layout.addLayout(button_layout)

    def save_settings(self):
        """Save current settings"""
        self.settings.set('theme', self.theme_combo.currentText())
        self.settings.set('camera_index', self.camera_spin.value())
        self.settings.set('detection_quality', self.quality_combo.currentText())
        self.settings.set('detection_interval', self.interval_spin.value())
        self.settings.set('show_fps', str(self.show_fps_check.isChecked()))
        self.accept()

    def reset_settings(self):
        """Reset settings to defaults"""
        self.settings.reset()
        self.theme_combo.setCurrentText(self.settings.get('theme'))
        self.camera_spin.setValue(int(self.settings.get('camera_index')))
        self.quality_combo.setCurrentText(self.settings.get('detection_quality'))
        self.interval_spin.setValue(int(self.settings.get('detection_interval')))
        self.show_fps_check.setChecked(self.settings.get('show_fps') == 'true') 