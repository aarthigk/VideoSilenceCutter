#!/usr/bin/env python3
"""
Setup script to help users download and configure FFmpeg
Run this after cloning the repository to set up FFmpeg
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

def download_ffmpeg():
    """Download FFmpeg for Windows"""
    print("=" * 60)
    print("FFmpeg Setup Helper")
    print("=" * 60)
    print("\nThis script will help you download and setup FFmpeg.")
    print("Note: FFmpeg is a large file (~100+ MB). The download may take a few minutes.\n")

    # Check if already exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_dir = os.path.join(base_dir, "ffmpeg-n6.1-latest-win64-gpl-6.1")

    if os.path.exists(ffmpeg_dir):
        print(f"✓ FFmpeg already exists at: {ffmpeg_dir}")
        return True

    # Provide options
    print("Options:")
    print("1. Download FFmpeg automatically (requires internet)")
    print("2. Manual setup (you'll download FFmpeg yourself)")
    print("3. Use system FFmpeg from PATH\n")

    choice = input("Select option (1/2/3): ").strip()

    if choice == "1":
        return auto_download_ffmpeg(base_dir, ffmpeg_dir)
    elif choice == "2":
        manual_setup_instructions(ffmpeg_dir)
        return True
    elif choice == "3":
        use_system_ffmpeg()
        return True
    else:
        print("Invalid choice.")
        return False

def auto_download_ffmpeg(base_dir, ffmpeg_dir):
    """Automatically download and extract FFmpeg"""
    try:
        print("\nDownloading FFmpeg (this may take a few minutes)...")
        print("Downloading from: https://github.com/BtbN/FFmpeg-Builds/releases")

        # Download URL for FFmpeg Windows build
        url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-N-114433-g8c426e3-win64-gpl.zip"
        zip_path = os.path.join(base_dir, "ffmpeg_temp.zip")

        # Download
        print("Downloading...")
        urllib.request.urlretrieve(url, zip_path)
        print("✓ Download complete!")

        # Extract
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(base_dir)
        print("✓ Extraction complete!")

        # Find extracted folder and rename it
        extracted_folders = [d for d in os.listdir(base_dir) if d.startswith("ffmpeg-N-")]
        if extracted_folders:
            extracted_path = os.path.join(base_dir, extracted_folders[0])
            shutil.move(extracted_path, ffmpeg_dir)
            print(f"✓ FFmpeg set up successfully at: {ffmpeg_dir}")

        # Cleanup
        os.remove(zip_path)

        print("\n✓ Setup complete! You can now run VideoSilenceCutter.py")
        return True

    except Exception as e:
        print(f"\n✗ Error downloading FFmpeg: {e}")
        print("\nPlease download FFmpeg manually:")
        manual_setup_instructions(ffmpeg_dir)
        return False

def manual_setup_instructions(ffmpeg_dir):
    """Print manual setup instructions"""
    print("\n" + "=" * 60)
    print("Manual FFmpeg Setup Instructions")
    print("=" * 60)
    print("""
1. Download FFmpeg from one of these sources:
   - https://ffmpeg.org/download.html
   - https://github.com/BtbN/FFmpeg-Builds/releases (Recommended)

2. Extract the downloaded zip file

3. Move/rename the extracted folder to:
   """)
    print(f"   {ffmpeg_dir}")
    print("""
4. Ensure the structure looks like:
   ffmpeg-n6.1-latest-win64-gpl-6.1/
   ├── bin/
   │   ├── ffmpeg.exe
   │   ├── ffplay.exe
   │   └── ffprobe.exe
   └── ...

5. After setup, run: python VideoSilenceCutter.py
""")

def use_system_ffmpeg():
    """Guide user to use system FFmpeg"""
    print("\n" + "=" * 60)
    print("Using System FFmpeg")
    print("=" * 60)
    print("""
To use FFmpeg from your system PATH:

1. Install FFmpeg:
   Windows (Chocolatey): choco install ffmpeg
   Linux: sudo apt install ffmpeg
   macOS: brew install ffmpeg

2. Modify VideoSilenceCutter.py:
   Change this line:
   ffmpeg_path = os.path.join(base_dir, "ffmpeg-n6.1-latest-win64-gpl-6.1", "bin", "ffmpeg.exe")
   
   To this:
   ffmpeg_path = "ffmpeg"

3. Run: python VideoSilenceCutter.py
""")

if __name__ == "__main__":
    success = download_ffmpeg()
    sys.exit(0 if success else 1)
