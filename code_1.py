import tkinter as tk
from tkinter import ttk
import googletrans
import speech_recognition as sr
import gtts
import playsound
import tempfile
import os

def recognize_and_translate():
    # Disable the start button while processing
    start_button.config(state=tk.DISABLED)

    # Clear previous text and translation
    text_entry.delete(0, tk.END)
    translation_entry.delete(0, tk.END)
    status_label.config(text="Listening...", foreground="#1e88e5")

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Start listening
    with sr.Microphone() as source:
        try:
            # Adjust microphone sensitivity
            recognizer.adjust_for_ambient_noise(source)
            voice = recognizer.listen(source, timeout=5)  # Timeout after 5 seconds
            status_label.config(text="Recognition done.", foreground="#43a047")

            # Recognize speech
            text = recognizer.recognize_google(voice, language="en-US")
            text_entry.insert(tk.END, text)

            # Translate the recognized text to selected language
            target_language = language_var.get()
            translator = googletrans.Translator()
            translation = translator.translate(text, dest=target_language)
            translated_text = translation.text
            translation_entry.insert(tk.END, translated_text)

            # Convert translated text to speech
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
                converted_audio = gtts.gTTS(translated_text, lang=target_language)
                converted_audio.write_to_fp(temp_audio)
                audio_file_path = temp_audio.name

            # Play the audio
            playsound.playsound(audio_file_path)

            status_label.config(text="Done", foreground="#43a047")
        except sr.UnknownValueError:
            status_label.config(text="Sorry, could not understand audio.", foreground="#e53935")
        except sr.RequestError as e:
            status_label.config(text="Could not request results, check your internet connection: " + str(e), foreground="#e53935")
        except Exception as e:
            status_label.config(text="An error occurred: " + str(e), foreground="#e53935")
        finally:
            # Enable the start button after processing
            start_button.config(state=tk.NORMAL)

# Create the main window
root = tk.Tk()
root.title("TranslateEase")
root.geometry("500x400")  # Increase size of interface
root.configure(bg="#f0f0f0")  # Set background color

# Set style
style = ttk.Style()
style.theme_use("clam")

# Create UI elements
content_frame = ttk.Frame(root, padding="20")
content_frame.pack(fill="both", expand=True)

start_button = ttk.Button(content_frame, text="Start", command=recognize_and_translate)
start_button.grid(row=0, column=0, columnspan=2, pady=(10, 5), ipadx=10, ipady=5)  # Adjust horizontal padding

language_var = tk.StringVar()
language_var.set("fr")  # Default target language: French

language_label = ttk.Label(content_frame, text="Select Target Language:", font=("Helvetica", 10, "bold"))
language_label.grid(row=1, column=0, padx=5, pady=(5, 2), sticky="w")

language_menu = ttk.Combobox(content_frame, textvariable=language_var, values=["en", "fr", "es", "de"])
language_menu.grid(row=1, column=1, padx=5, pady=(5, 2), sticky="w")

text_label = ttk.Label(content_frame, text="Recognized Text:", font=("Helvetica", 10, "bold"))
text_label.grid(row=2, column=0, padx=5, pady=(2, 2), sticky="w")

text_entry = ttk.Entry(content_frame, width=50, font=("Helvetica", 10))
text_entry.grid(row=2, column=1, padx=5, pady=(2, 2), sticky="w")

translation_label = ttk.Label(content_frame, text="Translation:", font=("Helvetica", 10, "bold"))
translation_label.grid(row=3, column=0, padx=5, pady=(2, 5), sticky="w")

translation_entry = ttk.Entry(content_frame, width=50, font=("Helvetica", 10))
translation_entry.grid(row=3, column=1, padx=5, pady=(2, 5), sticky="w")

status_label = ttk.Label(root, text="", padding=(10, 0))
status_label.pack(side="bottom", fill="x")

# Run the main event loop
root.mainloop()
