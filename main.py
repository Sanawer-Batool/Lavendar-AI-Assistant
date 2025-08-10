import os 
import gradio as gr
import cv2
import platform
import time
from pathlib import Path
from dotenv import load_dotenv
from speech_to_text import record_audio, transcribe_with_groq
from text_to_speech import text_to_speech_with_elevenlabs
from ai_agent import ask_agent

load_dotenv()

# Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Windows-friendly audio file path - use WAV for better compatibility
audio_filepath = "audio_question.wav"  # Changed from MP3 to WAV for better Windows compatibility

# Global variables for camera
camera = None
is_running = False
last_frame = None

def process_audio_and_chat():
    """
    Main audio processing loop with Windows-specific optimizations
    """
    chat_history = []
    
    # Ensure audio directory exists
    audio_dir = Path(audio_filepath).parent
    audio_dir.mkdir(exist_ok=True)
    
    while True:
        try:
            print("🎤 Recording audio...")
            
            # Record audio with error handling
            try:
                record_audio(file_path=audio_filepath)
                
                # Check if file was created successfully
                if not os.path.exists(audio_filepath) or os.path.getsize(audio_filepath) == 0:
                    print("⚠️ Audio file not created or empty, skipping...")
                    time.sleep(0.5)
                    continue
                    
            except Exception as e:
                error_msg = f"Audio recording error: {e}"
                print(error_msg)
                chat_history.append(["🔴 System", error_msg])
                yield chat_history
                time.sleep(1)
                continue
            
            print("🔄 Transcribing audio...")
            
            # Transcribe with error handling
            try:
                user_input = transcribe_with_groq(audio_filepath)
                
                if not user_input or user_input.strip() == "" or len(user_input.strip()) < 2:
                    print("📝 No meaningful transcription, continuing...")
                    time.sleep(0.5)
                    continue
                    
            except Exception as e:
                error_msg = f"Transcription error: {e}"
                print(error_msg)
                chat_history.append(["🔴 System", error_msg])
                yield chat_history
                time.sleep(1)
                continue
            
            print(f"👤 User said: {user_input}")
            
            # Check for exit conditions
            exit_words = ["goodbye", "exit", "quit", "stop", "bye"]
            if any(word in user_input.lower() for word in exit_words):
                farewell_msg = "👋 Goodbye! It was nice talking to you."
                chat_history.append([user_input, farewell_msg])
                yield chat_history
                
                # Generate farewell audio
                try:
                    text_to_speech_with_elevenlabs(
                        input_text=farewell_msg, 
                        output_filepath="farewell.mp3"
                    )
                except Exception as e:
                    print(f"TTS farewell error: {e}")
                
                break
            
            print("🤖 Getting AI response...")
            
            # Get AI response with error handling
            try:
                response = ask_agent(user_query=user_input)
                
                if not response or response.strip() == "":
                    response = "I'm sorry, I couldn't process your request. Could you try again?"
                    
            except Exception as e:
                response = f"I encountered an error: {e}. Please try again."
                print(f"AI Agent error: {e}")
            
            print(f"🤖 AI Response: {response}")
            
            # Create Windows-friendly response audio path
            response_audio_dir = Path("responses")
            response_audio_dir.mkdir(exist_ok=True)
            response_audio_path = response_audio_dir / "final.mp3"
            
            print("🔊 Converting response to speech...")
            
            # Generate TTS with error handling
            try:
                text_to_speech_with_elevenlabs(
                    input_text=response, 
                    output_filepath=str(response_audio_path)
                )
            except Exception as e:
                print(f"TTS error: {e}")
                # Continue without TTS if it fails
            
            # Update chat history
            chat_history.append([user_input, response])
            yield chat_history
            
            # Small delay to prevent system overload
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("🛑 Stopping audio processing...")
            break
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            print(error_msg)
            chat_history.append(["🔴 System Error", error_msg])
            yield chat_history
            time.sleep(2)  # Longer delay after unexpected errors

def initialize_camera():
    """Initialize the camera with Windows-optimized settings"""
    global camera
    
    if camera is None:
        print("📹 Initializing camera...")
        
        # Try different backends for Windows compatibility
        backends_to_try = [
            (cv2.CAP_DSHOW, "DirectShow"),      # Best for Windows
            (cv2.CAP_MSMF, "Media Foundation"), # Windows 10+
            (cv2.CAP_ANY, "Auto-detect")        # Fallback
        ]
        
        for backend_id, backend_name in backends_to_try:
            try:
                print(f"Trying {backend_name} backend...")
                camera = cv2.VideoCapture(0, backend_id)
                
                if camera.isOpened():
                    # Test if we can actually read frames
                    ret, test_frame = camera.read()
                    if ret and test_frame is not None:
                        # Configure camera for Windows
                        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        camera.set(cv2.CAP_PROP_FPS, 30)
                        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                        
                        # Additional Windows-specific settings
                        if platform.system() == "Windows":
                            camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
                        
                        print(f"✅ Camera initialized successfully with {backend_name}")
                        return True
                
                camera.release()
                camera = None
                
            except Exception as e:
                print(f"❌ Failed with {backend_name}: {e}")
                if camera:
                    camera.release()
                    camera = None
                continue
        
        print("❌ Failed to initialize camera with any backend")
        return False
    
    return camera.isOpened()

def start_webcam():
    """Start the webcam feed"""
    global is_running, last_frame
    
    print("🎥 Starting webcam...")
    is_running = True
    
    if not initialize_camera():
        print("❌ Camera initialization failed")
        return None
    
    try:
        ret, frame = camera.read()
        if ret and frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            last_frame = frame
            print("✅ Webcam started successfully")
            return frame
    except Exception as e:
        print(f"❌ Error starting webcam: {e}")
        
    return last_frame

def stop_webcam():
    """Stop the webcam feed with proper cleanup"""
    global is_running, camera
    
    print("⏹️ Stopping webcam...")
    is_running = False
    
    if camera is not None:
        try:
            camera.release()
            print("✅ Camera released successfully")
        except Exception as e:
            print(f"❌ Error releasing camera: {e}")
        finally:
            camera = None
    
    # Clean up any OpenCV windows (Windows-specific)
    if platform.system() == "Windows":
        try:
            cv2.destroyAllWindows()
        except:
            pass
    
    return None

def get_webcam_frame():
    """Get current webcam frame with Windows optimizations"""
    global camera, is_running, last_frame
    
    if not is_running or camera is None:
        return last_frame
    
    try:
        # Windows-specific buffer management
        if platform.system() == "Windows":
            # Grab frame without retrieving to clear buffer
            if hasattr(camera, 'grab'):
                camera.grab()
        
        ret, frame = camera.read()
        if ret and frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            last_frame = frame
            return frame
            
    except Exception as e:
        print(f"❌ Error getting webcam frame: {e}")
        
    return last_frame

# Create necessary directories
def setup_directories():
    """Create required directories for Windows"""
    directories = ["responses", "temp", "audio"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

# Setup UI with Windows-friendly styling
def create_ui():
    with gr.Blocks(
        title="Lavendar AI Assistant",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        """
    ) as demo:
        
        gr.Markdown("""
        <h1 style='color: orange; text-align: center; font-size: 4em; margin-bottom: 20px;'> 
        👧🏼 Lavendar – Your Personal AI Assistant
        </h1>
        <p style='text-align: center; color: #666; font-size: 1.2em;'>
        Windows-Optimized Version
        </p>
        """)

        with gr.Row():
            # Left column - Webcam
            with gr.Column(scale=1):
                gr.Markdown("## 📹 Webcam Feed")
                
                with gr.Row():
                    start_btn = gr.Button("🎥 Start Camera", variant="primary", size="sm")
                    stop_btn = gr.Button("⏹️ Stop Camera", variant="secondary", size="sm")
                
                webcam_output = gr.Image(
                    label="Live Feed",
                    streaming=True,
                    show_label=False,
                    width=640,
                    height=480
                )
                
                # Optimized timer for Windows (10 FPS for stability)
                webcam_timer = gr.Timer(0.1)
            
            # Right column - Chat
            with gr.Column(scale=1):
                gr.Markdown("## 💬 Chat Interface")
                
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=400,
                    show_label=False,
                    avatar_images=("user_13984171.png", "cancan_9702934.png"),
                    bubble_full_width=False
                )
                
                gr.Markdown("""
                *🎤 Continuous listening mode is active - speak anytime!*  
                *💡 Say 'goodbye', 'exit', or 'quit' to stop the conversation*  
                *🖥️ Optimized for Windows systems*
                """)
                
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary", size="sm")
        
        # Event handlers
        start_btn.click(fn=start_webcam, outputs=webcam_output)
        stop_btn.click(fn=stop_webcam, outputs=webcam_output)
        webcam_timer.tick(fn=get_webcam_frame, outputs=webcam_output, show_progress=False)
        clear_btn.click(fn=lambda: [], outputs=chatbot)
        
        # Auto-start continuous mode when the app loads
        demo.load(fn=process_audio_and_chat, outputs=chatbot)
        
        return demo

# Main execution
if __name__ == "__main__":
    print("🚀 Starting Lavendar AI Assistant...")
    print(f"💻 Running on: {platform.system()} {platform.release()}")
    
    # Setup directories
    setup_directories()
    
    # Create and launch UI
    demo = create_ui()
    
    try:
        print("🌐 Launching web interface...")
        demo.launch(
            server_name="127.0.0.1",  # Windows-friendly (instead of 0.0.0.0)
            server_port=7860,
            share=False,  # Set to True if you need external access
            debug=True,
            show_error=True,
            quiet=False,
            prevent_thread_lock=False
        )
    except Exception as e:
        print(f"❌ Failed to launch on port 7860: {e}")
        print("🔄 Trying alternative port...")
        try:
            demo.launch(
                server_name="127.0.0.1",
                server_port=0,  # Let system choose available port
                share=False,
                debug=True,
                show_error=True
            )
        except Exception as e2:
            print(f"❌ Failed to launch on any port: {e2}")
            print("💡 Try running as administrator or check your firewall settings")