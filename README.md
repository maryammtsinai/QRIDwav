# QRIDwav
Analyzing the wav files found in the QRID Patient folders to see which files are missing/corrupted

Differences b/w code:
QRID_directory_localpath10wav.py: creates 'summary_report_white_noise.xlsx'; facing issues

QRID_directory_wav_amplitudes.py: creates 'QRIDwavampsummary.csv'

QRID_directory_wav_v2.py: creates 'QRIDwavsummary_SR.csv'; uses SpeechRecognition; NOT ACCURATE because it says most content is 'White Noise' when it truly isn't

QRID_directory_wav.v3.py: creates 'QRIDwavsummary_SR_version2.csv'
