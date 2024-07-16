import curses
import os
import pyaudio
from six.moves import queue
from google.cloud import speech
from google.cloud import translate_v2 as translate
import time
import sys


# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/Majid/whisper_real_time/studied-groove-345512-189a0dfb04be.json'

# Initialize Google Cloud clients
speech_client = speech.SpeechClient()
translate_client = translate.Client()

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Generate the audio chunks from the buffer."""
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)

def display_intro(stdscr):
    """Displays an introduction animation with enhanced formatting."""
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)  # Text: Black, Background: Green
    stdscr.bkgd(' ', curses.color_pair(1))  # Apply the color pair to the background

    messages = ["Initializing...", "Welcome to the Real-time Translator!", "You can start speaking now."]
    for message in messages:
        stdscr.clear()
        # Center the message and apply bold and color
        stdscr.addstr(curses.LINES // 2, (curses.COLS - len(message)) // 2, message, curses.A_BOLD | curses.color_pair(1))
        stdscr.refresh()
        time.sleep(1)  # Wait a second for each part of the intro

def listen_and_translate(stdscr, rate=16000, chunk=1024, language_code='fi-FI', target_language='en'):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.curs_set(0)
    stdscr.nodelay(1)
    display_intro(stdscr)
    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.scrollok(True)
    y = 0

    max_stream_duration = 295

    while True:
        start_time = time.time()

        with MicrophoneStream(rate, chunk) as stream:
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=rate,
                language_code=language_code,
            )

            streaming_config = speech.StreamingRecognitionConfig(
                config=config,
                interim_results=True
            )

            responses = speech_client.streaming_recognize(streaming_config, requests)

            stdscr.addstr(0, 0, "Listening...", curses.A_BOLD)
            stdscr.refresh()

            for response in responses:
                if stdscr.getch() == ord('q'):
                    break

                if time.time() - start_time > max_stream_duration:
                    break

                for result in response.results:
                    transcript = result.alternatives[0].transcript.strip()
                    update_transcript_display(stdscr, transcript, y, final=result.is_final)
                    if result.is_final:
                        y += 1
                        if y >= curses.LINES - 2:  # Adjust for screen height
                            stdscr.scroll(1)
                            y -= 1
                        translation = translate_client.translate(transcript, target_language=target_language)
                        translation_text = "Translation: " + translation['translatedText']
                        # Ensure the translation text fits in one line
                        max_width = curses.COLS - 1
                        if len(translation_text) > max_width:
                            translation_text = translation_text[:max_width-3] + "..."
                        stdscr.addstr(y, 0, translation_text)
                        stdscr.refresh()
                        y += 2  # Leave a blank line after translation

            time.sleep(1)


def update_transcript_display(stdscr, transcript, y, final=False):
    max_y = curses.LINES - 1  # Maximum y-coordinate based on current terminal size

    # If y is out of bounds, adjust it to stay within the window.
    # This is a basic fix; you may need to refine this based on your application's needs.
    if y > max_y:
        y = max_y
    elif y < 0:
        y = 0

    # Now we can safely move the cursor and update the display.
    stdscr.move(y, 0)
    stdscr.clrtoeol()
    if final:
        stdscr.attron(curses.A_BOLD)
    else:
        stdscr.attron(curses.A_DIM)
    stdscr.addstr(y, 0, transcript)
    if final:
        stdscr.attroff(curses.A_BOLD)
    else:
        stdscr.attroff(curses.A_DIM)
    stdscr.refresh()

def main(stdscr):
    # Initialize colors if terminal supports them
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)  # Define a color pair if needed

    # Set background and foreground if needed, using the defined color pair
    stdscr.bkgd(' ', curses.color_pair(1))  # This is optional and depends on your terminal's capability

    # Execute the main function of the script
    listen_and_translate(stdscr)

if __name__ == '__main__':
    curses.wrapper(main)