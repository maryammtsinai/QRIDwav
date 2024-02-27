import os
import csv
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Function to check if audio contains white noise
def is_white_noise(audio):
    # Calculate the difference between dBFS and max_dBFS
    amplitude_variance = audio.dBFS - audio.max_dBFS
    
    # Adjust this threshold based on your requirements
    threshold = 10  # Example threshold
    
    # If the amplitude variance is below the threshold, consider it as white noise
    return amplitude_variance < threshold

# Set the path to ffmpeg
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin/ffmpeg"

# Path to the Q-Lab folder in OneDrive
onedrive_path = os.path.expanduser("~/Library/CloudStorage/OneDrive-TheMountSinaiHospital/Q-Lab")

# Create a CSV file for reporting
output_csv_path = 'QRIDwavsummary_SR.csv'

with open(output_csv_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write header
    csv_writer.writerow(['Patient_ID', 'Session_ID', 'Wav_File_Path', 'Speech_Status'])
    
    # Iterate through the Q-Lab directory to find .wav files in QRID directories
    for qrid_folder in Path(onedrive_path).iterdir():
        if qrid_folder.is_dir():
            patient_id = qrid_folder.name
            for session_folder in qrid_folder.iterdir():
                if session_folder.is_dir():
                    session_id = session_folder.name
                    for wav_file_path in session_folder.glob('**/*.wav'):
                        try:
                            audio = AudioSegment.from_wav(str(wav_file_path))
                            speech_status = "White Noise" if is_white_noise(audio) else "Normal Speech"
                            row = [patient_id, session_id, str(wav_file_path), speech_status]
                            csv_writer.writerow(row)
                        except Exception as e:
                            print(f"Error processing file {wav_file_path}: {e}")

print(f"Speech status data added to '{output_csv_path}'.")
