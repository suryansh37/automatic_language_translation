from tkinter import *
import os
import tkinter.messagebox as tkMessageBox
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import threading as td
import random
import string

main = Tk()
main.title("Voiceprint Translator")
main.geometry("940x570")
main.config(bg="#F5F5F5")

# Define the dictionary of languages and their language codes
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Russian": "ru",
    "Hindi": "hi",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Bengali": "bn",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Odia": "or"
}

lt = list(languages.keys())

v1 = StringVar(main)
v1.set(lt[0])
v2 = StringVar(main)
v2.set(lt[1])


# Function to generate a random filename
def generate_random_filename():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(10)) + ".mp3"

# Function to speak the translated text
def speak():
    global txtbx2
    tx = txtbx2.get("1.0", END)
    
    # Check if the selected language exists in the languages dictionary
    selected_language = v2.get()
    if selected_language in languages:
        language_code = languages[selected_language]
        
        # Specify the folder path where you want to save the MP3 file
        folder_path = "C:/Users/EVERVITAL/Desktop/MP VI/ALT MP"  
        
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Generate a random filename for the temporary audio file
        file_name = generate_random_filename()
        file_path = os.path.join(folder_path, file_name)
    
        myobj = gTTS(text=tx, lang=language_code, slow=False)
        
        # Save the audio to the random filename
        myobj.save(file_path)
        
        # Play the audio
        song = AudioSegment.from_mp3(file_path)
        play(song)
        
        # Remove the temporary audio file after playing
        os.remove(file_path)
    else:
        tkMessageBox.showinfo("Warning", "Selected language is not supported.")

# Function to translate text
def translate():
    global txtbx, txtbx2
    txtbx2.delete("1.0", "end-1c")
    tx = txtbx.get("1.0", END)
    
    # Define the language codes and corresponding languages
    code = ["en", "hi", "ta", "gu", "mr", "es", "fr", "de", "ja", "ru", "bn", "te", "kn", "ml", "pa", "ur", "or"]
    languages = ["English", "Hindi", "Tamil", "Gujarati", "Marathi", "Spanish", "French", "German", 
                 "Japanese", "Russian", "Bengali", "Telugu", "Kannada", "Malayalam", "Punjabi", 
                 "Urdu", "Odia"]
    
    # Check if the selected language exists in the languages list
    if v2.get() in languages:
        lang = code[languages.index(v2.get())]
        translated = GoogleTranslator(source='auto', target=lang).translate(tx)
        txtbx2.insert("end-1c", translated)
    else:
        tkMessageBox.showinfo("Warning", "Selected language is not supported.")


# Function to detect voice input
def detect():
    global flag, txtbx
    r = sr.Recognizer()  # Define the recognizer here
    while True:
        if flag == True:
            print("breaked")
            break
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            txtbx.insert("end-1c", MyText)
        except sr.RequestError as e:
            tkMessageBox.showinfo("warning", "Could not request results; {0}".format(e))
            break
        except sr.UnknownValueError:
            tkMessageBox.showinfo("warning", "unknown error occurred")
            break
# Function to start voice detection
def start():
    global flag, b1
    flag = False
    b1["text"] = "Stop Speaking"
    b1["command"] = stop
    td.Thread(target=detect).start()

# Function to stop voice detection
def stop():
    global flag, b1
    b1["text"] = "Give Voice Input"
    b1["command"] = start
    flag = True

# UI Elements
Label(main, text="Translate Language via Voice Commands or Text Input", font=("Arial", 18, "bold"), bg="#F5F5F5", fg="#333333").place(x=240, y=20)

can1 = Canvas(main, width=400, height=450, bg="#FFFFFF", relief="solid", bd=2, highlightthickness=0)
can1.place(x=30, y=80)

Label(main, text="Input Box:", font=("Arial", 14, "bold"), bg="#FFFFFF", fg="#333333").place(x=44, y=70)

can2 = Canvas(main, width=400, height=450, bg="#FFFFFF", relief="solid", bd=2, highlightthickness=0)
can2.place(x=490, y=80)

Label(main, text="Output Box:", font=("Arial", 14, "bold"), bg="#FFFFFF", fg="#333333").place(x=780, y=60)

txtbx = Text(main, width=40, height=7, font=("Arial", 12), relief="solid", bd=0, highlightthickness=0)
txtbx.place(x=50, y=100)

txtbx2 = Text(main, width=40, height=7, font=("Arial", 12), relief="solid", bd=0, highlightthickness=0)
txtbx2.place(x=510, y=100)

b1 = Button(main, text="Give Voice Input", font=("Arial", 12, "bold"), width=35, height=1, bg="#FFC107", fg="#333333", command=start, relief="solid", bd=4, highlightthickness=0)
b1.place(x=50, y=250)

Button(main, text="Speak Text", font=("Arial", 12, "bold"), width=35, height=1, bg="#FFC107", fg="#333333", command=speak, relief="solid", bd=4, highlightthickness=0).place(x=510, y=250)

Button(main, text="Translate", font=("Arial", 15, "bold"), width=71, height=3, bg="#4CAF50", fg="#FFFFFF", command=translate, relief="solid", bd=3, highlightthickness=0).place(x=30, y=446)

Label(main, text="Select Language:", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#333333").place(x=50, y=300)
Label(main, text="Select Language:", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#333333").place(x=510, y=300)

o1 = OptionMenu(main, v1, *lt)
o1.config(font=("Arial", 12, "bold"), width=36, bg="#FFFFFF", fg="#333333", relief="solid", bd=1, highlightthickness=0)
o1.place(x=50, y=340)

o2 = OptionMenu(main, v2, *lt)
o2.config(font=("Arial", 12, "bold"), width=36, bg="#FFFFFF", fg="#333333", relief="solid", bd=1, highlightthickness=0)
o2.place(x=510, y=340)

main.mainloop()
