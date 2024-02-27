import os
import csv
from pathlib import Path
import glob
import openpyxl
from pydub import AudioSegment

# Function to check if the audio is white noise
def is_white_noise(audio):
    # Define a threshold for amplitude variance (adjust as needed)
    amplitude_threshold = 1000

    # Ensure the length is a whole number of frames
    frame_width = audio.frame_width
    length_in_frames = len(audio.raw_data) // frame_width * frame_width
    adjusted_audio = audio[:length_in_frames]

    # Calculate the amplitude variance
    amplitude_variance = adjusted_audio.dBFS - adjusted_audio.max_dBFS

    # If the variance is below the threshold, consider it white noise
    return amplitude_variance < amplitude_threshold

# Function to transcribe speech from a .wav file
def transcribe_wav_file(wav_file_path):
    # Load the audio file using pydub
    audio = AudioSegment.from_wav(wav_file_path)
    
    # Check if the audio is white noise
    if is_white_noise(audio):
        return "White noise detected"
    else:
        return "Normal audio"

# Path to the Q-Lab folder in my OneDrive
onedrive_path = os.path.expanduser("~/Library/CloudStorage/OneDrive-TheMountSinaiHospital/Q-Lab")

# Prefix for patient folders
patient_prefix = 'QRID'

# Create a new Excel workbook
workbook = openpyxl.Workbook()

# Create a new sheet for CSV data
csv_sheet = workbook.create_sheet(title='CSV Data')

# Write header to the CSV sheet
csv_sheet.append(['Patient_ID', 'Session_ID', 'Wav_File_Path', 'Audio_Status'])

# Iterate through the folders in 'Q-Lab' directory
for patient_folder in Path(onedrive_path).iterdir():
    # Check if the folder is a patient folder and has the specified prefix
    if patient_folder.is_dir() and patient_folder.name.startswith(patient_prefix):
        # Iterate through session folders within each patient folder
        for session_folder in patient_folder.glob('*/**/'):
            # Use glob to find all .wav files within the Session folder recursively
            wav_files = glob.glob(str(session_folder / '**' / '*.wav'), recursive=True)

            # Check if .wav files were found
            if wav_files:
                # Extract Patient_ID and Session_ID from folder names
                patient_id = patient_folder.name
                session_id = session_folder.name

                # Iterate through found .wav files and append to the CSV sheet
                for wav_file in wav_files:
                    # Check if the audio is white noise or normal
                    audio_status = transcribe_wav_file(wav_file)

                    csv_sheet.append([patient_id, session_id, str(wav_file), audio_status])
            else:
                print(f"No .wav files found in Session folder: {session_folder}")

# Remove the default sheet created with the workbook
workbook.remove(workbook.active)

# Save the workbook to an XLSX file
output_xlsx_path = 'summary_report_white_noise.xlsx'
workbook.save(output_xlsx_path)
print(f"XLSX file '{output_xlsx_path}' created successfully.")
