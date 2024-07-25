from tkinter import Tk, Button, filedialog, messagebox, Text, END
from moviepy.editor import VideoFileClip
import os
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect as detect_language

main = Tk()
main.title("Video to Audio Converter")
main.geometry("400x400")

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
        messagebox.showinfo("Success", "Audio extracted and saved successfully to: " + audio_file_path)

        # Set the detected text to an empty string initially
        detected_text = ""
        return audio_file_path
    else:
        messagebox.showerror("Error", "No video file selected.")
        return None

# Function to translate the detected text
def translate():
    global detected_text
    print("Translated")

    # Detect the language of the text
    detected_language = detect_language(detected_text)

    # Offer options for translation
    # messagebox.showinfo("Translate Options", f"Detected language: {detected_language}\nPlease select the language to translate to.")
    # Add code here to prompt user for translation language and translate the text

# Function to handle the file selection and audio extraction process
def process_video():
    video_file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    audio_file_path = extract_audio(video_file_path)
    
    if audio_file_path:
        translate_button.config(state="normal")
    else:
        translate_button.config(state="disabled")

# UI Elements
Button(main, text="Upload Video", command=process_video).pack()  # Upload Video Button
translate_button = Button(main, text="Translate", command=translate)
translate_button.pack()
translate_button.config(state="disabled")  # Disable initially until text is detected

txtbx = Text(main, width=50, height=5)
txtbx.pack()

main.mainloop()
