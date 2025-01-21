from pydub import AudioSegment
import subprocess

# Convert video to audio using ffmpeg
subprocess.call(['ffmpeg', '-i', 'story_eng.mp4', 'story_eng.wav'])

# Load the audio file
audio = AudioSegment.from_file("story_eng.wav", format="wav")

# Export the audio file
audio.export("story_eng.wav", format="wav")