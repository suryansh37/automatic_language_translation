import speech_recognition as sr
import concurrent.futures

def recognize_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        transcripts = recognizer.recognize_google(audio_data, show_all=True)
        return transcripts
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service: {e}")
        return None

# List of audio files
audio_files = ["C:/Users/EVERVITAL/Desktop/MP VI/ALT MP/Countfrom1to10inSpanish_audio.wav"]  # Replace with your audio files

# Process audio files concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(recognize_audio, audio_files)

# Print recognized transcripts
for audio_file, result in zip(audio_files, results):
    if result:
        print(f"Transcripts for {audio_file}:")
        for alternative in result:
            transcript = alternative['alternative'][0]['transcript']
            confidence = alternative['alternative'][0]['confidence']
            print(f" - {transcript} (confidence: {confidence})")
    else:
        print(f"Failed to transcribe {audio_file}")
