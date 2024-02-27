import os
import csv
from pathlib import Path
from pydub import AudioSegment

AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"

# Function to calculate amplitude statistics
def calculate_amplitude_statistics(audio):
    # Get amplitude values
    amplitudes = audio.get_array_of_samples()

    if not amplitudes:
        # Return None for all statistics if no valid audio data
        return None, None, None, None

    # Calculate statistics
    min_amplitude = min(amplitudes)
    max_amplitude = max(amplitudes)
    mean_amplitude = sum(amplitudes) / len(amplitudes)
    std_dev_amplitude = (sum((a - mean_amplitude) ** 2 for a in amplitudes) / len(amplitudes)) ** 0.5

    return min_amplitude, max_amplitude, mean_amplitude, std_dev_amplitude

# Set the path to ffmpeg
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin/ffmpeg"

# Path to the Q-Lab folder in OneDrive
onedrive_path = os.path.expanduser("~/Library/CloudStorage/OneDrive-TheMountSinaiHospital/Q-Lab")

# Create a CSV file for reporting
output_csv_path = 'QRIDwavampsummary.csv'

with open(output_csv_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header
    csv_writer.writerow(['PATIENT_ID', 'SESSION_ID', 'WAV_FILE_PATH', 'MIN_AMPLITUDE', 'MAX_AMPLITUDE', 'MEAN_AMPLITUDE', 'STD_DEV_AMPLITUDE'])

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
                            # Calculate amplitude statistics
                            min_amp, max_amp, mean_amp, std_dev_amp = calculate_amplitude_statistics(audio)

                            if min_amp is not None:
                                # Write to CSV only if valid audio data
                                row = [patient_id, session_id, str(wav_file_path), min_amp, max_amp, mean_amp, std_dev_amp]
                                csv_writer.writerow(row)
                            else:
                                # Report that the file contains no valid audio data
                                row = [patient_id, session_id, str(wav_file_path), "No Valid Audio Data", "", "", ""]
                                csv_writer.writerow(row)
                        except Exception as e:
                            print(f"Error processing file {wav_file_path}: {e}")

print(f"Amplitude statistics data added to '{output_csv_path}'.")
