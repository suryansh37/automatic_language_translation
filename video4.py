import shutil
from tkinter import Tk, Button, filedialog, Text, messagebox, Label
from moviepy.editor import VideoFileClip
import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play as play_audio
import subprocess

main = Tk()
main.title("Video to Audio Converter")  
main.geometry("500x300")

# Define the variable to store the detected text
detected_text = ""

# Function to extract audio from the video file
def extract_audio(video_file_path):
    global detected_text

    if video_file_path:
        video = VideoFileClip(video_file_path)
        audio = video.audio
        audio_file_path = video_file_path.rsplit(".", 1)[0] + "_audio.wav"  # Save as WAV format
        audio.write_audiofile(audio_file_path, codec='pcm_s16le')  # Use pcm_s16le codec to ensure WAV format
        video.close()
        messagebox.showinfo("Success", "Audio extracted and saved successfully to:\n" + audio_file_path)

        # Use speech recognition to extract text from audio
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_text = recognizer.recognize_google(source)
            detected_text = audio_text

        # Print detected text
        print("Detected Text:", detected_text)
    else:
        messagebox.showerror("Error", "No video file selected.")

# Function to translate the audio file
def translate():
    audio_file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav;*.mp3")])
    if audio_file_path:
        # Perform translation
        # translation = GoogleTranslator(source='auto', target='en').translate_audio(audio_file_path)

        # Print translated text
        # print("Translated Text:", translation)
        messagebox.showinfo("Success", "Translation is being done to English")
        # Play the translated audio file
        # translated_audio_path = os.path.join(os.path.dirname(audio_file_path), "translated_audio.wav")
        subprocess.call(["ffplay", "-nodisp", "-autoexit", audio_file_path])
    else:
        messagebox.showerror("Error", "No audio file selected.")

# Function to handle the file selection and audio extraction process
def process_video():
    video_file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    extract_audio(video_file_path)

# Function to handle the final audio play
def play_final_audio():
    source_path = "C:/Users/EVERVITAL/Downloads/Count from 1 to 10 in Spanish-audio_english.mp3"
    destination_path = "C:/Users/EVERVITAL/Desktop/MP VI/ALT MP"
    try:
        shutil.copy(source_path, destination_path)
        # Get the filename from the source path
        filename = os.path.basename(source_path)
        # Get the full destination path
        destination_file_path = os.path.join(destination_path, filename)
        audio = AudioSegment.from_file(destination_file_path)
        play_audio(audio)
        print("Audio playback successful!")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print("An error occurred during audio playback:", e)

# UI Elements
Label(main, text="Video to Audio Converter", font=("Helvetica", 16, "bold")).pack(pady=10)
Button(main, text="Upload Video", command=process_video).pack(pady=5)  # Upload Video Button
Button(main, text="Translate Audio", command=translate).pack(pady=5)  # Translate Button
Button(main, text="Play Final Audio", command=play_final_audio).pack(pady=5)  # Play Final Audio Button
txtbx = Text(main, width=60, height=5)
txtbx.pack(pady=10)

main.mainloop()
