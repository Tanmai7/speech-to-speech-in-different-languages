from flask import Flask, request, render_template, send_file, redirect, url_for, send_from_directory
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import subprocess

app = Flask(__name__)

# Ensure directories exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('translated_texts', exist_ok=True)
os.makedirs('translated_videos', exist_ok=True)

# Configure static folders
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TRANSLATED_VIDEOS_FOLDER'] = 'translated_videos'

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

# Function to convert audio file to WAV format
def convert_to_wav(input_file, output_file):
    command = [
        'ffmpeg',
        '-i', input_file,
        output_file
    ]
    subprocess.run(command, check=True)

# Function to extract text from audio file using speech_recognition library
def extract_text_from_audio(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return None
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
        return None

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
    return file_path

# Function to convert text to speech and save as audio file
def text_to_speech(text, target_language):
    lang_code = LANGUAGE_CODES.get(target_language.lower())
    if not lang_code:
        raise ValueError(f"Language not supported: {target_language}")
    audio_file_path = f'translated_texts/translated_{target_language}.mp3'
    tts = gTTS(text=text, lang=lang_code)
    tts.save(audio_file_path)
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    video_file = request.files['video_file']
    target_language = request.form['target_language'].lower()

    video_file_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    video_file.save(video_file_path)

    # Extract audio from video
    audio_file_path = os.path.splitext(video_file_path)[0] + '.wav'
    convert_to_wav(video_file_path, audio_file_path)

    text = extract_text_from_audio(audio_file_path)
    if text is None:
        return "Error: Could not extract text from audio. Please try again with a different file."

    translated_text = translate_text(text, target_language)
    save_translated_text(translated_text, target_language)
    translated_audio_file = text_to_speech(translated_text, target_language)

    translated_video_file = os.path.join(app.config['TRANSLATED_VIDEOS_FOLDER'], f'translated_{target_language}.mp4')
    replace_audio_in_video(video_file_path, translated_audio_file, translated_video_file)

    return redirect(url_for('result', original_video=video_file.filename, translated_video=f'translated_{target_language}.mp4'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/translated_videos/<filename>')
def translated_file(filename):
    return send_from_directory(app.config['TRANSLATED_VIDEOS_FOLDER'], filename)

@app.route('/result')
def result():
    original_video = request.args.get('original_video')
    translated_video = request.args.get('translated_video')
    return render_template('result.html', original_video=original_video, translated_video=translated_video)

if __name__ == '__main__':
    app.run(debug=True)