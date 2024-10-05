import subprocess
import re
import os
from typing import List

class VideoSilenceCutter:
    @staticmethod
    def detect_silent_parts(video_file_path: str, ffmpeg_path: str, noise_threshold: float, min_silence_duration: float) -> List[float]:
        silent_segments = []

        # Build FFmpeg command to detect silence
        command = [
            ffmpeg_path,
            "-i", video_file_path,
            "-af", f"silencedetect=noise={noise_threshold}dB:d={min_silence_duration}",
            "-f", "null", "-"
        ]

        # Execute the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Decode output to string
        output = stderr.decode('utf-8')

        # Use regex to find silence start and end
        silence_start_pattern = re.compile(r"silence_start: ([0-9.]+)")
        silence_end_pattern = re.compile(r"silence_end: ([0-9.]+)")

        silence_start = -1
        for line in output.splitlines():
            start_match = silence_start_pattern.search(line)
            end_match = silence_end_pattern.search(line)

            if start_match:
                silence_start = float(start_match.group(1))
            elif end_match and silence_start != -1:
                silence_end = float(end_match.group(1))
                silent_segments.append((silence_start, silence_end))
                silence_start = -1  # Reset for the next detection

        return silent_segments

    @staticmethod
    def trim_video(input_video_path: str, silent_segments: List[float], output_video_path: str, ffmpeg_path: str):
        video_filter = []
        audio_filter = []
        previous_end = 0.0

        # Build filter complex based on silent segments
        for start, end in silent_segments:
            if start > previous_end:
                video_filter.append(f"[0:v]trim=start={previous_end}:end={start},setpts=PTS-STARTPTS[v{len(video_filter) + 2}]")
                audio_filter.append(f"[0:a]atrim=start={previous_end}:end={start},asetpts=PTS-STARTPTS[a{len(audio_filter) + 2}]")
            previous_end = end

        # Handle remaining video/audio after last silent segment
        video_duration = VideoSilenceCutter.get_video_duration(input_video_path, ffmpeg_path)
        if previous_end < video_duration:
            video_filter.append(f"[0:v]trim=start={previous_end},setpts=PTS-STARTPTS[v{len(video_filter) + 2}]")
            audio_filter.append(f"[0:a]atrim=start={previous_end},asetpts=PTS-STARTPTS[a{len(audio_filter) + 2}]")

        # Construct final filter complex
        filter_complex = ";".join(video_filter + audio_filter) + ";"
        concat_video = "".join(f"[v{i}] " for i in range(2, len(video_filter) + 2))
        concat_audio = "".join(f"[a{i}] " for i in range(2, len(audio_filter) + 2))

        final_filter = (
            f"{filter_complex}{concat_video}concat=n={len(video_filter)}:v=1:a=0[outv];"
            f"{concat_audio}concat=n={len(audio_filter)}:v=0:a=1[outa]"
        )

        # Build the FFmpeg command
        ffmpeg_command = [
            ffmpeg_path,
            "-i", input_video_path,
            "-filter_complex", final_filter,
            "-map", "[outv]",
            "-map", "[outa]",
            "-y", output_video_path
        ]

        # Execute the FFmpeg command
        print(f"{GREEN}Executing FFmpeg{RESET}")
        print(f"Executing FFmpeg command: {' '.join(ffmpeg_command)}")
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg process failed with exit code {process.returncode}")

    @staticmethod
    def get_video_duration(input_video_path: str, ffmpeg_path: str) -> float:
        command = [ffmpeg_path, "-i", input_video_path]
        process = subprocess.Popen(command, stderr=subprocess.PIPE)
        stderr = process.communicate()[1].decode('utf-8')

        duration_pattern = re.compile(r"Duration: ([0-9]+):([0-9]+):([0-9.]+)")
        for line in stderr.splitlines():
            match = duration_pattern.search(line)
            if match:
                hours = int(match.group(1))
                minutes = int(match.group(2))
                seconds = float(match.group(3))
                return hours * 3600 + minutes * 60 + seconds

        raise RuntimeError("Unable to retrieve video duration.")
# ANSI color codes
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"

def main():
    ffmpeg_path = "C:\\Users\\gkaar\\Downloads\\ffmpeg-n6.1-latest-win64-gpl-6.1\\bin\\ffmpeg.exe"  # Path to FFmpeg

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Go up two levels

    # Define input and output folders relative to the base directory
    input_folder = os.path.join(base_dir, 'input')
    output_folder = os.path.join(base_dir, 'output')

    # Print to check paths
    print(f"{YELLOW}Base Directory: {RESET}{base_dir}")
    print(f"{YELLOW}Input Folder: {RESET}{input_folder}")
    print(f"{YELLOW}Output Folder: {RESET}{output_folder}")
   # input_video_path = "C:\\Users\\username\\Downloads\\TestVideo.mp4"
    input_video_path = os.path.join(input_folder, "TestVideo.mp4")
    print(input_video_path)
   # output_video_path = "C:\\Users\\username\\Downloads\\Output.mp4"
    output_video_path = os.path.join(output_folder, "Output.mp4")  # Specify the output video file name here

    # Check if input video file exists
    if not os.path.isfile(input_video_path):
        print(f"{RED}Error: Input video file '{input_video_path}' does not exist.")
        return

    noise_threshold = -60  # Configurable silence threshold
    min_silence_duration = 0.5  # Configurable silence duration

    # Detect silent parts
    silent_parts = VideoSilenceCutter.detect_silent_parts(input_video_path, ffmpeg_path, noise_threshold, min_silence_duration)

    # Trim video based on detected silent parts
    VideoSilenceCutter.trim_video(input_video_path, silent_parts, output_video_path, ffmpeg_path)


    print(f"{GREEN}\n############################################################################################################")
    print(f"{GREEN}[INFO] Output video saved successfully at: {output_video_path}{RESET}")
    print(f"{GREEN}[INFO] Video processing complete! Enjoy your trimmed video.{RESET}")
    print(f"{GREEN}\n############################################################################################################")
if __name__ == "__main__":
    main()
