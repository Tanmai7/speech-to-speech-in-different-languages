import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import subprocess

# Mapping of full language names to gTTS language codes
LANGUAGE_CODES = {
    'afrikaans': 'af', 'albanian': 'sq', 'arabic': 'ar', 'armenian': 'hy', 'bengali': 'bn', 'bosnian': 'bs', 'catalan': 'ca',
    'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et',
    'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht',
    'hindi': 'hi', 'hungarian': 'hu', 'icelandic': 'is', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja',
    'javanese': 'jw', 'kannada': 'kn', 'khmer': 'km', 'korean': 'ko', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt',
    'macedonian': 'mk', 'malay': 'ms', 'malayalam': 'ml', 'marathi': 'mr', 'myanmar': 'my', 'nepali': 'ne', 'norwegian': 'no',
    'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'serbian': 'sr', 'sinhala': 'si',
    'slovak': 'sk', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tamil': 'ta', 'telugu': 'te',
    'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh',
    'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
}

# Function to extract text from audio file
def extract_text_from_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

# Function to translate text to user-defined language
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=LANGUAGE_CODES[target_language])
    return translation.text

# Function to save translated text to a file
def save_translated_text(text, target_language):
    folder_path = 'translated_texts'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f'translated_{target_language}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Translated text saved to {file_path}")
    return file_path

# Function to convert text to speech and save as audio file
def text_to_speech(text, target_language):
    lang_code = LANGUAGE_CODES.get(target_language.lower())
    if not lang_code:
        raise ValueError(f"Language not supported: {target_language}")
    tts = gTTS(text=text, lang=lang_code)
    audio_file_path = f'translated_texts/translated_{target_language}.mp3'
    tts.save(audio_file_path)
    print(f"Audio saved to {audio_file_path}")
    return audio_file_path

# Function to replace audio in video with translated audio using ffmpeg
def replace_audio_in_video(video_file, audio_file, output_file):
    command = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        output_file
    ]
    subprocess.run(command, check=True)
    print(f"Video saved to {output_file}")

# Main function
def main():
    audio_file = input("Enter the path to the audio file (e.g., 'C:\\speech\\story_eng.wav'): ")
    target_language = input("Enter the target language (e.g., 'Spanish'): ").lower()
    video_file = input("Enter the path to the video file (e.g., 'C:\\speech\\video.mp4'): ")
    output_file = input("Enter the path for the output video file (e.g., 'C:\\speech\\output_video.mp4'): ")

    text = extract_text_from_audio(audio_file)
    print(f"Extracted Text: {text}")

    translated_text = translate_text(text, target_language)
    print(f"Translated Text: {translated_text}")

    save_translated_text(translated_text, target_language)
    translated_audio_file = text_to_speech(translated_text, target_language)
    replace_audio_in_video(video_file, translated_audio_file, output_file)

if __name__ == "__main__":
    main()