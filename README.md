# Real-time Speech Translation with Google Cloud

This project provides a real-time speech translation system using Google Cloud's Speech-to-Text and Translation APIs, with a terminal interface for displaying live transcriptions and translations. The terminal interface is enhanced using the `curses` library to provide a more interactive and visually appealing user experience.

## Features
- Real-time speech recognition using Google Cloud Speech-to-Text API.
- Translation of recognized speech into a target language using Google Cloud Translation API.
- Interactive terminal interface with introductory animations and live updates.

## Requirements
- Python 3.6+
- Google Cloud SDK
- `pyaudio` for audio stream handling
- `curses` for terminal interface
- `google-cloud-speech` and `google-cloud-translate` for Google Cloud services
- `six` for compatibility

## Setup

### Google Cloud Setup
1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on the project dropdown and create a new project.

2. **Enable APIs**:
   - In the Google Cloud Console, go to the API Library.
   - Enable the [Cloud Speech-to-Text API](https://console.cloud.google.com/apis/library/speech.googleapis.com).
   - Enable the [Cloud Translation API](https://console.cloud.google.com/apis/library/translate.googleapis.com).

3. **Set Up Authentication**:
   - In the Google Cloud Console, go to the "IAM & Admin" section and click on "Service Accounts".
   - Create a new service account and download the JSON key file.
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to this file:

    ```sh
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
    ```

### Python Environment
- Install the required Python packages using pip:

    ```sh
    pip install pyaudio google-cloud-speech google-cloud-translate six
    ```

## Usage

1. **Run the Script**:
    - Execute the script from the terminal.

    ```sh
    python your_script_name.py
    ```

2. **Interactive Terminal**:
    - The script will start with an introductory animation and then begin listening for speech input.
    - Speak into the microphone, and the terminal will display the live transcription and translation.

3. **Quit the Application**:
    - Press `q` in the terminal to quit the application.

## Configuration

To change the source or target language, modify the `language_code` and `target_language` parameters in the `listen_and_translate` function within the script.


