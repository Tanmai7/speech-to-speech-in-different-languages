import speech_recognition as sr
from googletrans import Translator
import os

# Function to extract text from audio file
def extract_text_from_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

# Function to translate text to user-defined language
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function to save translated text to a file
def save_translated_text(text, target_language):
    folder_path = 'translated_texts'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f'translated_{target_language}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Translated text saved to {file_path}")

# Main function
def main():
    audio_file = input("Enter the path to the audio file (e.g., 'C:\\speech\\story_eng.wav'): ")
    target_language = input("Enter the target language (e.g., 'es' for Spanish): ")

    text = extract_text_from_audio(audio_file)
    print(f"Extracted Text: {text}")

    translated_text = translate_text(text, target_language)
    print(f"Translated Text: {translated_text}")

    save_translated_text(translated_text, target_language)

if __name__ == "__main__":
    main()