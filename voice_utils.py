import os
import asyncio
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
from groq import Groq
import edge_tts
from dotenv import load_dotenv

load_dotenv()
client = Groq()

async def record_audio_until_stop():
    """Records audio and transcribes using Groq Whisper."""
    print("\n🔴 Recording... (Press ENTER to stop)")
    fs = 16000
    data = []
    recording = True

    def callback(indata, frames, time, status):
        if recording:
            data.append(indata.copy())

    # Record
    stream = sd.InputStream(samplerate=fs, channels=1, callback=callback)
    with stream:
        await asyncio.to_thread(input)
        recording = False
    
    print("⚡ Transcribing...")
    
    # Save to temp file
    my_recording = np.concatenate(data, axis=0)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        write(tmp.name, fs, my_recording)
        tmp_path = tmp.name

    # API Call
    try:
        with open(tmp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3", 
                file=audio_file,
                language="te" # Force Telugu
            )
        text = transcription.text
    except Exception as e:
        print(f"Error in STT: {e}")
        text = ""
    finally:
        os.remove(tmp_path)
        
    print(f"🎤 Heard: {text}")
    return text

async def play_audio(text: str):
    """Generates Telugu speech using Edge TTS."""
    print(f"🤖 Speaking: {text}")
    if not text: return

    # Telugu Voice (Male)
    voice = "te-IN-MohanNeural" 
    communicate = edge_tts.Communicate(text, voice)
    
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        await communicate.save(tmp.name)
        tmp_path = tmp.name

    # Play Audio
    if os.name == 'nt': # Windows
        os.system(f'start {tmp_path}')
    else: # Mac/Linux
        os.system(f'afplay {tmp_path}' if os.system(f'afplay {tmp_path}') == 0 else f'mpg123 {tmp_path}')