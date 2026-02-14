import subprocess
import os
import json

INPUT = "video.mp4"          # file name
OUTPUT_FOLDER = "audio_out" 
MP3_BITRATE = "192k"         

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def get_audio_codec(video_path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=codec_name",
        "-of", "json",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
        codec = data["streams"][0]["codec_name"]
        return codec
    except (KeyError, IndexError, json.JSONDecodeError):
        return None


def extract_audio(video_path, output_folder, mp3_bitrate="192k"):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    codec = get_audio_codec(video_path)

    if not codec:
        print(f"[ERROR] Не вдалося визначити аудіо кодек у {video_path}")
        return


    if codec.lower() in ["mp3"]:
        output_audio = os.path.join(output_folder, f"{base_name}.mp3")
        cmd = [
            "ffmpeg", "-i", video_path, "-vn", "-ab", mp3_bitrate,
            "-y", output_audio
        ]

    elif codec.lower() in ["aac", "opus", "flac"]:
        ext = codec.lower()
        output_audio = os.path.join(output_folder, f"{base_name}.{ext}")
        cmd = [
            "ffmpeg", "-i", video_path, "-vn", "-acodec", "copy",
            "-y", output_audio
        ]
    else:

        output_audio = os.path.join(output_folder, f"{base_name}.mp3")
        cmd = [
            "ffmpeg", "-i", video_path, "-vn", "-ab", mp3_bitrate,
            "-y", output_audio
        ]

    try:
        subprocess.run(cmd, check=True)
        print(f"[OK] {video_path} → {output_audio}")
    except subprocess.CalledProcessError:
        print(f"[ERROR] Не вдалося витягти аудіо з {video_path}")



extract_audio(INPUT, OUTPUT_FOLDER, MP3_BITRATE)

# for filename in os.listdir("."):
#     if filename.lower().endswith(".mp4"):
#         extract_audio(filename, OUTPUT_FOLDER, MP3_BITRATE)
