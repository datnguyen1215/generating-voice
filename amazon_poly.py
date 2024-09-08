import argparse
from pathlib import Path
import csv
import boto3
from pydub import AudioSegment
from io import BytesIO
import os  # import os to read environment variables if needed

def synthesize_speech(text, client, voice_id='Joanna'):
    response = client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='neural'
    )
    return response['AudioStream'].read()

def add_silence(duration_ms):
    return AudioSegment.silent(duration=duration_ms)

def main(args):
    # Automatically use credentials from environment variables
    polly_client = boto3.client('polly')

    input_file = args.input_file
    output_dir = args.output_dir
    padding = args.padding
    silence_in_between = args.silence_in_between
    voice_id = args.voice_id

    input_path = Path(input_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(input_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for index, row in enumerate(csvreader):
            audio_parts = []

            # Add padding before
            audio_parts.append(add_silence(padding))
            
            for i, text in enumerate(row):
                if not text.strip():  # Skip empty strings
                    continue
                audio_data = synthesize_speech(text, polly_client, voice_id)
                audio_segment = AudioSegment.from_mp3(BytesIO(audio_data))
                audio_parts.append(audio_segment)

                # Add silence in between texts except the last one
                if i < len(row) - 1:
                  audio_parts.append(add_silence(silence_in_between))
            
            # Add padding after
            audio_parts.append(add_silence(padding))

            # Combine all parts
            combined = AudioSegment.empty()
            for part in audio_parts:
                combined += part
            
            # Export the combined audio
            output_file = output_path / f'{voice_id}_{index+1}.mp3'
            combined.export(output_file, format='mp3')
            print(f"Generated audio: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate audios using Amazon Polly from a CSV input file.")
    parser.add_argument('--padding', type=int, required=True, help='The silence period before and after the audio (in milliseconds)')
    parser.add_argument('--silence-in-between', type=int, required=True, help='The silence in between each text (in milliseconds)')
    parser.add_argument('--input-file', type=str, required=True, help='CSV file containing input texts')
    parser.add_argument('--output-dir', type=str, required=True, help='Directory to save output audios')
    parser.add_argument('--voice-id', type=str, default='Joanna', help='Voice ID to use for TTS')

    args = parser.parse_args()
    main(args)