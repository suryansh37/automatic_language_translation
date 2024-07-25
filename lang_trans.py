import tkinter as tk
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
    status_label.config(text="Listening...")

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Start listening
    with sr.Microphone() as source:
        try:
            # Adjust microphone sensitivity
            recognizer.adjust_for_ambient_noise(source)
            voice = recognizer.listen(source, timeout=5)  # Timeout after 5 seconds
            status_label.config(text="Recognition done.")

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

            status_label.config(text="Done")
        except sr.UnknownValueError:
            status_label.config(text="Sorry, could not understand audio.")
        except sr.RequestError as e:
            status_label.config(text="Could not request results, check your internet connection: " + str(e))
        except Exception as e:
            status_label.config(text="An error occurred: " + str(e))
        finally:
            # Enable the start button after processing
            start_button.config(state=tk.NORMAL)

# Create the main window
root = tk.Tk()
root.title("Speech Recognition and Translation")

# Create UI elements
start_button = tk.Button(root, text="Start", command=recognize_and_translate)
start_button.grid(row=0, column=0, padx=10, pady=10)

language_var = tk.StringVar()
language_var.set("fr")  # Default target language: French

language_label = tk.Label(root, text="Select Target Language:")
language_label.grid(row=0, column=1, padx=10, pady=10)

language_menu = tk.OptionMenu(root, language_var, "en", "fr", "es", "de")
language_menu.grid(row=0, column=2, padx=10, pady=10)

text_label = tk.Label(root, text="Recognized Text:")
text_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

text_entry = tk.Entry(root, width=50)
text_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

translation_label = tk.Label(root, text="Translation:")
translation_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

translation_entry = tk.Entry(root, width=50)
translation_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

status_label = tk.Label(root, text="")
status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

# Run the main event loop
root.mainloop()
