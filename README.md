# VideoSilenceCutter

## Overview
**VideoSilenceCutter** is a Python tool designed to automatically trim silent segments from video files, streamlining the video editing process. This project utilizes FFmpeg for audio processing, making it efficient and effective for content creators who spend excessive time manually editing videos.

## Features
- Detects silent parts of a video based on a configurable noise threshold and minimum silence duration.
- Trims the video automatically, outputting a new file without the silent segments.
- User-friendly, with clear instructions and customizable parameters.

## Requirements
- Python 3.x
- FFmpeg
- `moviepy` library

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/aathigk/VideoSilenceCutter.git
   cd VideoSilenceCutter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download and extract FFmpeg:
   - Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Extract the folder and rename it to `ffmpeg-n6.1-latest-win64-gpl-6.1` (or update the path in VideoSilenceCutter.py)
   - Place it in the project root directory

## Usage
1. Place your input video files in the `input/` folder.
2. Run the script:
   ```bash
   python VideoSilenceCutter.py
   ```
3. The output video will be saved in the `output/` folder.

## Folder Structure
The project is organized as follows:

```
VideoSilenceCutter/
│
├── input/                                      # Folder for input video files
│   └── TestIP.mp4                              # Example input video
│
├── output/                                     # Folder for output video files
│
├── ffmpeg-n6.1-latest-win64-gpl-6.1/          # FFmpeg installation folder
│   └── bin/
│       └── ffmpeg.exe                          # FFmpeg executable
│
├── VideoSilenceCutter.py                       # The main Python script
├── requirements.txt                            # List of Python dependencies
├── README.md                                   # Project documentation
└── VideoSilenceCutter.iml                      # IDE configuration file
```
## Configuration
You can adjust the `noise_threshold` and `min_silence_duration` variables in the VideoSilenceCutter.py script to customize the silence detection criteria.

- **noise_threshold**: The audio level below which is considered silence (in dBFS)
- **min_silence_duration**: The minimum duration (in seconds) of silence required to trim

## Troubleshooting

### FFmpeg Not Found Error
If you get an error saying `ffmpeg.exe` not found:
1. Verify you've downloaded and extracted FFmpeg to the project directory
2. Check the folder path matches: `ffmpeg-n6.1-latest-win64-gpl-6.1/bin/ffmpeg.exe`
3. Alternatively, update the `ffmpeg_path` in `VideoSilenceCutter.py` to point to your FFmpeg installation

### Large Files Not in Repository
If you're seeing `.gitignore` file and wondering where FFmpeg is:
- This is intentional! FFmpeg is excluded from git to keep the repository size small
- You must download it separately as instructed in the Installation section

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for suggestions and improvements.

## Acknowledgments
Special thanks to FFmpeg for providing powerful multimedia processing capabilities.

![License](https://img.shields.io/badge/license-MIT-blue)
