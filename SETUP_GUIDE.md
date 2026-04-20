# Git Repository Setup - FFmpeg Exclusion Guide

## Problem
The FFmpeg binary bundle (~100+ MB) was included in the repository, making it impossible to push to GitHub due to file size restrictions.

## Solution Implemented
FFmpeg has been **excluded from the Git repository** using `.gitignore`. Users must download it separately.

## Files Created/Modified

### 1. ✅ `.gitignore` (NEW)
Created to exclude large files from Git:
- `ffmpeg-n6.1-latest-win64-gpl-6.1/` - FFmpeg directory
- `__pycache__/` and Python cache files
- Virtual environments (`venv/`, `ENV/`, `env/`)
- IDE files (`.idea/`, `.iml`)
- Video input/output files (to save space)

### 2. ✅ `README.md` (UPDATED)
Enhanced with:
- Clear installation steps in 3 parts
- FFmpeg setup options (manual, automatic, or system-wide)
- Updated folder structure documentation with note about downloading FFmpeg
- New troubleshooting section
- Explanations for why FFmpeg isn't in the repo

### 3. ✅ `setup_ffmpeg.py` (NEW)
Helper script for users to:
- Automatically download and extract FFmpeg
- Get manual setup instructions
- Configure to use system FFmpeg instead
- Interactive menu-based setup

## Repository Size Reduction
- **Before**: ~100+ MB (due to FFmpeg binary)
- **After**: <1 MB (just source code and documentation)

## For Users Cloning the Repository

### Quick Start:
```bash
# 1. Clone the repository
git clone https://github.com/aathigk/VideoSilenceCutter.git
cd VideoSilenceCutter

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Setup FFmpeg (choose one):
# Option A: Auto-download
python setup_ffmpeg.py

# Option B: Manual download
# Follow README.md instructions

# Option C: Use system FFmpeg
# Follow README.md instructions and edit VideoSilenceCutter.py

# 4. Run the application
python VideoSilenceCutter.py
```

## Next Steps for GitHub Push

1. **Remove the FFmpeg folder locally** (if not already done):
   ```bash
   git rm -r --cached ffmpeg-n6.1-latest-win64-gpl-6.1/
   ```

2. **Commit and push**:
   ```bash
   git add -A
   git commit -m "Remove FFmpeg binary and add gitignore - users now download separately"
   git push origin main
   ```

3. **Verify the repo is now small**:
   ```bash
   git count-objects -v
   ```

## Benefits
✅ Dramatically reduced repository size (can now push to GitHub)
✅ Faster cloning for users
✅ Better user experience with automated setup script
✅ Flexible FFmpeg configuration options
✅ Clear documentation for new users
