import os
import argparse
import csv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import io

# Fetch the API key from the environment variable or hard-code it
api_key = os.getenv('ELEVEN_LAB_API_KEY', "YOUR_API_KEY")

client = ElevenLabs(
    api_key=api_key,
)

def generate_audio(text, voice_id):
    audio_content = client.text_to_speech.convert(
        voice_id=voice_id,
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        voice_settings=VoiceSettings(
            stability=0.3,
            similarity_boost=0.5
        ),
    )
    return b"".join(audio_content)  # Join the chunks into a single bytes object

def read_texts_from_csv(file_path):
    texts = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            texts.append(row)  # Each row in the CSV is a list of texts
    return texts

def main():
    parser = argparse.ArgumentParser(description='Generate concatenated TTS audio files with ElevenLabs API.')

    parser.add_argument('--voice-id', required=True, help='Voice ID to use for TTS')
    parser.add_argument('--padding', type=int, default=0, help='Padding (in milliseconds) to add at the start and end of each output file')
    parser.add_argument('--in-between-silence', type=int, default=0, help='Silence (in milliseconds) to add between different texts in each combined file')
    parser.add_argument('--input-file', help='CSV file containing texts to convert to speech')
    parser.add_argument('--output-dir', default='.', help='Directory to save the generated audio files')
    parser.add_argument('--output-prefix', default='output_audio', help='Prefix for the generated audio files')
    parser.add_argument('--output-format', default='mp3', choices=['mp3', 'wav'], help='Format of the output audio files')

    args = parser.parse_args()

    if args.input_file:
        texts = read_texts_from_csv(args.input_file)
    else:
        raise ValueError("The --input-file must be provided")

    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for idx, text_line in enumerate(texts):
        combined_audio = AudioSegment.silent(duration=args.padding)
        for i, text in enumerate(text_line):
            text = text.strip()
            if text:  # Skip empty texts
                audio_content = generate_audio(text, args.voice_id)
                if audio_content:
                    audio_segment = AudioSegment.from_file(io.BytesIO(audio_content), format=args.output_format)
                    combined_audio += audio_segment
                    if i < len(text_line) - 1:  # Add in-between silence only if it's not the last text
                        combined_audio += AudioSegment.silent(duration=args.in_between_silence)
        combined_audio += AudioSegment.silent(duration=args.padding)
        output_file = os.path.join(args.output_dir, f"{args.voice_id}_{idx + 1}.{args.output_format}")
        combined_audio.export(output_file, format=args.output_format)
        print(f"Audio generated successfully and saved as {output_file}")

if __name__ == '__main__':
    main()