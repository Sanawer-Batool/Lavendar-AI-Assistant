import os 
import elevenlabs
from elevenlabs.client import ElevenLabs
import subprocess # to handle audio playback across different OS
import platform # to determine the OS type
from dotenv import load_dotenv

load_dotenv()
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Function to convert text to speech using ElevenLabs API
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Converts text to speech using ElevenLabs API and saves it to a file.
    
    Args:
        input_text (str): The text to convert to speech.
        output_filepath (str): The path where the audio file will be saved.
    """
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="jqcCZkN6Knx8BJ5TBdYR",
        model_id="eleven_multilingual_v2",
        output_format="mp3_22050_32"
    )
    
    # Save the audio data to file - audio is already bytes data
    with open(output_filepath, 'wb') as f:
        for chunk in audio:
            f.write(chunk)
    
    print(f"Audio saved to: {output_filepath}")
    
    # Play the audio file
    os_name = platform.system()
    try: 
        if os_name == "Darwin":  # macOS
            subprocess.run(["afplay", output_filepath])
        elif os_name == "Windows":  # Windows
            # Use a simpler approach for Windows
            os.startfile(output_filepath)
        elif os_name == "Linux":  # Linux
            subprocess.run(["mpg123", output_filepath])  # or use 'ffplay'
        else:
            raise OSError(f"Unsupported OS: {os_name}")
    except Exception as e:
        print(f"Error playing audio: {e}")


## -----------# Free Alternative text-to-speech using gTTS (Google Text-to-Speech)
# Uncomment the following code to use gTTS instead of ElevenLabs

# from gtts import gTTS

# def text_to_speech_with_gtts(input_text, output_filepath):
#     """
#     Converts text to speech using gTTS and saves it to a file.
    
#     Args:
#         input_text (str): The text to convert to speech.
#         output_filepath (str): The path where the audio file will be saved.
#     """
#     language = "en"

#     audioobj = gTTS(
#         text=input_text,
#         lang=language,
#         slow=False
#     )
#     audioobj.save(output_filepath)
#     print(f"Audio saved to: {output_filepath}")
    
#     # Play the audio file
#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":  # macOS
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":  # Windows
#             # Option 1: Use os.startfile (simplest - opens with default player)
#             os.startfile(output_filepath)
            
#             # Option 2: Use Windows Media Player command line
#             # subprocess.run(['wmplayer', output_filepath])
            
#             # Option 3: Use PowerShell with Windows Media Format SDK
#             # subprocess.run(['powershell', '-c', f'Add-Type -AssemblyName presentationCore; $player = New-Object system.windows.media.mediaplayer; $player.open("{output_filepath}"); $player.Play(); Start-Sleep 5'])
            
#         elif os_name == "Linux":  # Linux
#             # Use mpg123 for MP3 files (install with: sudo apt-get install mpg123)
#             subprocess.run(['mpg123', output_filepath])
#             # Alternative: subprocess.run(['ffplay', '-nodisp', '-autoexit', output_filepath])
#         else:
#             raise OSError(f"Unsupported operating system: {os_name}")
#     except FileNotFoundError as e:
#         print(f"Audio player not found: {e}")
#         print("On Linux, try installing: sudo apt-get install mpg123")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")


# # Test the function
# if __name__ == "__main__":
#     input_text = "Hi, I am Lavender, your AI assistant. Testing text to speech functionality"
#     output_filepath = "testing_tts.mp3"
#     # text_to_speech_with_elevenlabs(input_text, output_filepath)
#     # Use the standard gTTS approach with fixed playback
#     #text_to_speech_with_gtts(input_text, output_filepath)

