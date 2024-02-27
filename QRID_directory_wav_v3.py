import os
import pydub
import csv
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from pydub.silence import split_on_silence

def is_mainly_white_noise(audio):
    # Set the silence threshold
    silence_thresh = -40
    
    # Split the audio by silence
    chunks = pydub.silence.split_on_silence(audio, silence_thresh=silence_thresh)
    
    # Calculate the duration of silence
    silence_duration = sum(chunk.duration_seconds for chunk in chunks)
    
    # Calculate the percentage of silence
    if len(audio) != 0:
        percentage_silence = (silence_duration / len(audio)) * 100
        return percentage_silence > 80  # Adjust the threshold as needed
    else:
        # If the audio duration is zero, consider it as mainly white noise
        return True

# Set the path to ffmpeg
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin/ffmpeg"

# Path to the Q-Lab folder in OneDrive
onedrive_path = os.path.expanduser("~/Library/CloudStorage/OneDrive-TheMountSinaiHospital/Q-Lab")

# Create a CSV file for reporting
output_csv_path = 'QRIDwavsummary_SR_version2.csv'

with open(output_csv_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write header
    csv_writer.writerow(['Patient_ID', 'Session_ID', 'Wav_File_Path', 'Speech_Status', 'White_Noise_Percentage'])
    
    # Iterate through the Q-Lab directory to find .wav files in QRID directories
    for qrid_folder in Path(onedrive_path).iterdir():
        if qrid_folder.is_dir():
            patient_id = qrid_folder.name
            for session_folder in qrid_folder.iterdir():
                if session_folder.is_dir():
                    session_id = session_folder.name
                    for wav_file_path in session_folder.glob('**/*.wav'):
                        audio = AudioSegment.from_wav(str(wav_file_path))
                        is_white_noise = is_mainly_white_noise(audio)
                        
                        # Calculate the white noise percentage
                        silence_duration = sum(end - start for start, end in detect_nonsilent(audio, silence_thresh=-40))
                        total_duration = len(audio)
                        
                        if total_duration > 0:
                            white_noise_percentage = (silence_duration / total_duration) * 100
                        else:
                            white_noise_percentage = 0
                        
                        speech_status = "White Noise" if is_white_noise else "Normal Speech"
                        row = [patient_id, session_id, str(wav_file_path), speech_status, white_noise_percentage]
                        csv_writer.writerow(row)

print(f"Speech status data added to '{output_csv_path}'.")
