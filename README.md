# Voice Generation Project

This project allows you to generate voice audio files using Amazon Polly and ElevenLabs Text-to-Speech (TTS) services.

## Project Structure

- `amazon_poly.py`: Script for generating audio using Amazon Polly
- `eleven_lab.py`: Script for generating audio using ElevenLabs
- `.gitignore`: Specifies files to be ignored by version control (all MP3 files)

## Prerequisites

- Python 3.x
- AWS account with Polly access (for Amazon Polly)
- ElevenLabs API key (for ElevenLabs)

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/voice-generation-project.git cd voice-generation-project

2. Install the required dependencies:

pip install boto3 pydub elevenlabs


3. Set up your credentials:
- For Amazon Polly: Configure your AWS credentials using AWS CLI or environment variables
- For ElevenLabs: Set the `ELEVEN_LAB_API_KEY` environment variable with your API key

## Usage

### Amazon Polly

Run the script with the following command:

python amazon_poly.py --padding --silence-in-between --input-file --output-dir --voice-id <voice_id>


Arguments:
- `--padding`: Silence period before and after the audio (in milliseconds)
- `--silence-in-between`: Silence between each text (in milliseconds)
- `--input-file`: CSV file containing input texts
- `--output-dir`: Directory to save output audios
- `--voice-id`: Voice ID to use for TTS (default: Joanna)

### ElevenLabs

Run the script with the following command:

python eleven_lab.py --voice-id <voice_id> --padding --in-between-silence --input-file --output-dir --output-prefix --output-format


Arguments:
- `--voice-id`: Voice ID to use for TTS (required)
- `--padding`: Padding to add at the start and end of each output file (in milliseconds, default: 0)
- `--in-between-silence`: Silence to add between different texts in each combined file (in milliseconds, default: 0)
- `--input-file`: CSV file containing texts to convert to speech (required)
- `--output-dir`: Directory to save the generated audio files (default: current directory)
- `--output-prefix`: Prefix for the generated audio files (default: output_audio)
- `--output-format`: Format of the output audio files (choices: mp3, wav; default: mp3)

## Input File Format

Both scripts expect a CSV file as input, where each row contains the text to be converted to speech. Multiple columns in a row will be treated as separate phrases to be combined into a single audio file.

## Output

The scripts will generate MP3 or WAV files (depending on the chosen format) in the specified output directory. Each file will be named using the pattern: `<voice_id>_<index>.<format>`.