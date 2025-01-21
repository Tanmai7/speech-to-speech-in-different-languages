import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()

def record_text_from_audio_file(audio_file):
    try:
        with sr.AudioFile(audio_file) as source:
            print("Processing audio file...")
            audio = r.record(source)
            text = r.recognize_google(audio)
            print("Extracted text: ", text)
            return text
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("Unknown error occurred")
    return None

def write_text_to_file(text):
    with open("text.txt", "a") as f:
        f.write(text)
        f.write("\n")

if __name__ == "__main__":
    audio_file = "story_eng.wav"  # Replace with your audio file path
    text = record_text_from_audio_file(audio_file)
    if text:
        write_text_to_file(text)