# MoodSense: Real-Time Emotion Detection System

A powerful Python-based application that performs real-time facial emotion detection and analysis using computer vision and deep learning. This system provides an intuitive graphical user interface for monitoring and analyzing human emotions through webcam feed.

## 🌟 Features

- **Real-time Face Detection**: Utilizes OpenCV for robust face detection and tracking.
- **Advanced Emotion Analysis**: Implements DeepFace for accurate emotion recognition with enhanced preprocessing and temporal smoothing.
- **Modern GUI Interface**: Built with PyQt5, featuring a sleek, dark-themed, and user-friendly design.
- **Comprehensive Emotion Tracking**: Detects 7 distinct emotions:
  - 😊 Happy
  - 😢 Sad
  - 😡 Angry
  - 😮 Surprise
  - 😨 Fear
  - 🤢 Disgust
  - 😐 Neutral
- **Live Statistics**: Tracks and displays emotion frequency in real-time.
- **Visual Feedback**: 
  - Color-coded emotion indicators.
  - Emoji representations.
  - Confidence scores.
  - Detailed emotion descriptions displayed on the screen.
- **Screenshot Capability**: Capture detection moments with timestamp and clear status messages.
- **Customizable Settings**: 
  - Adjust camera index.
  - Control detection interval.
  - Toggle FPS display.
  - Switch between Dark and Light themes.
- **Keyboard Shortcuts**: Streamlined control with shortcuts for starting/stopping detection, taking screenshots, and opening settings.
- **Status Updates**: Real-time feedback through a dedicated status bar.
- **Responsive Design**: Adapts to different screen sizes while maintaining aspect ratio.

## 🛠️ Technical Stack

- **Python 3.x**
- **OpenCV**: For real-time video processing and face detection.
- **DeepFace**: For advanced emotion analysis.
- **PyQt5**: For building the rich graphical user interface.
- **NumPy**: For efficient numerical operations.
- **Pandas**: For data logging and analysis (emotion_log.csv).
- **Matplotlib**: For generating emotion reports.

## 🚀 Getting Started

### Requirements

- Python 3.8 or higher
- Webcam
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/MoodSense.git
   cd MoodSense
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Ensure your webcam is connected and accessible.
2. Run the main application:
   ```bash
   python main.py
   ```
3. **Controls:**
   - Press `Space` to start/stop emotion detection.
   - Press `Ctrl+S` to capture a screenshot.
   - Press `Ctrl+,` to open the settings dialog.
   - Press `Ctrl+Q` to exit the application.

4. **Additional Features:**
   - Emotion logs are automatically saved to `logs/emotion_log.csv`.
   - Screenshots are saved in the `screenshots/` directory.
   - Generate emotion reports from the `logs/` directory using utility functions (can be expanded).

## 📂 Project Structure

- `main.py`: Main application entry point, initializes the GUI and core components.
- `face_detector.py`: Handles real-time face detection using OpenCV.
- `emotion_analyzer.py`: Performs emotion analysis using DeepFace, including preprocessing and smoothing.
- `gui.py`: Implements the PyQt5 graphical user interface, including all visual elements and interactions.
- `settings.py`: Manages application settings and provides a settings dialog.
- `utils.py`: Contains helper functions for directory creation, screenshot saving, and emotion logging.
- `requirements.txt`: Lists all Python dependencies and their versions.
- `README.md`: Project description and setup instructions (this file).
- `logs/`: Directory for saved emotion logs (automatically created).
- `screenshots/`: Directory for captured screenshots (automatically created).
- `icons/`: Directory for application icons (automatically created or custom added).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Developed by Arpit Jain © 2025 ❤️
- OpenCV for robust computer vision capabilities.
- DeepFace for powerful facial attribute analysis.
- PyQt5 for the intuitive and modern GUI framework. 