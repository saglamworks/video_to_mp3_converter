=== Installation Instructions ===

This project requires FFmpeg.

----------------------------------------
WINDOWS (AUTO-INSTALL)
----------------------------------------
You do NOT need to manually install anything.

FFmpeg will be downloaded and extracted automatically
the first time you run:

run_windows.bat

After that, the converter will start immediately.


----------------------------------------
MACOS (REQUIRES HOMEBREW)
----------------------------------------
If Homebrew is NOT installed, install it with:

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

After installing Homebrew, run the script again:

./run_mac.command

The converter will automatically install FFmpeg using:

brew install ffmpeg


----------------------------------------
FOLDER STRUCTURE
----------------------------------------
input/   → place your .mp4 files here
output/  → converted .mp3 files will appear here

----------------------------------------
RUNNING THE PROGRAM
----------------------------------------
Windows:   double-click run_windows.bat
MacOS:     run "chmod +x run_mac.command" once,
           then double-click run_mac.command
