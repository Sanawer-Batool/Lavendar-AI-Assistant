import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# Configures logging to show time, level (INFO/ERROR), and message.
logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to record audio from the microphone and save it as an MP3 file
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Function to record audio from the microphone and save it as an MP3 file.
    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for the user to start speaking.(in seconds)
    phrase_time_limit (int): Maximum length of the recorded audio (in seconds).
    """
    # This object will handle listening and processing audio.
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source: # Use the default microphone as the audio source
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start Speaking Now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete. Processing audio...")

            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate = "128k")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occured: {e}")

# file_path = "testing_stt.mp3"
# record_audio(file_path)

def transcribe_with_groq(audio_filepath):
   GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
   client = Groq(api_key=GROQ_API_KEY)
   stt_model = "whisper-large-v3"
   audio_file=open(audio_filepath, "rb")
   transcription = client.audio.transcriptions.create(
       model=stt_model,
       file=audio_file,
       language="en"
   )
   return transcription.text

# audio_filepath = "testing_stt.mp3"
# print(transcribe_with_groq(audio_filepath))

