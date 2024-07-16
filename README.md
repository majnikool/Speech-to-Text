```markdown
# Real-time Speech-to-Text Translator

This Python application utilizes Google Cloud's Speech-to-Text and Translation APIs to create a real-time speech translation system. The program captures audio input from the microphone, performs speech recognition, and then translates the recognized text into a specified target language. It features a console-based UI that updates dynamically to show the translation process in real-time.

## Prerequisites

- Python 3.6+
- PyAudio
- Google Cloud Platform account
- Enabled Google Speech-to-Text API
- Enabled Google Translate API
- API key for Google Cloud

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/real-time-translator.git
   cd real-time-translator
   ```

2. **Install dependencies:**

   Make sure you have Python installed, then run:

   ```bash
   pip install pyaudio google-cloud-speech google-cloud-translate six
   ```

3. **Set up Google Cloud credentials:**

   Place your Google Cloud credentials JSON file in the root directory of the project or specify its path in the environment variables:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
   ```

## Usage

To start the application, run:

```bash
python -m curses_wrapper.py
```

Once started, the application will guide you through an animated introduction. Speak into your microphone, and the translations will appear on your terminal screen. Press `q` to quit the application at any time.

## Configuration

To change the source or target language, modify the `language_code` and `target_language` parameters in the `listen_and_translate` function within the script.


