import os
import subprocess
import sys
import platform
import urllib.request
import zipfile
import shutil

def print_install_message():
    print("\n===============================================")
    print(" Required packages are being installed for the")
    print(" first time. Please wait a moment...")
    print("===============================================\n")

def ffmpeg_exists():
    """FFmpeg kurulu mu kontrol et"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def install_ffmpeg_windows():
    print_install_message()
    print("Downloading FFmpeg for Windows...")

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = "ffmpeg.zip"

    urllib.request.urlretrieve(url, zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("ffmpeg_extract")

    extracted_folder = os.listdir("ffmpeg_extract")[0]
    ffmpeg_bin = os.path.join("ffmpeg_extract", extracted_folder, "bin")

    # PATH'e ekliyoruz
    os.environ["PATH"] += os.pathsep + ffmpeg_bin

    print("FFmpeg installed successfully!")

    os.remove(zip_path)

def install_ffmpeg_mac():
    print_install_message()
    print("Installing FFmpeg via Homebrew...")

    # Homebrew kurulu mu?
    brew_check = subprocess.run(["brew", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if brew_check.returncode != 0:
        print("\nHomebrew is not installed! Install it with this command:\n")
        print('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
        sys.exit(1)

    subprocess.run(["brew", "install", "ffmpeg"])

def convert_mp4_to_mp3(input_path, output_path):
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        output_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def main():
    # FFmpeg kontrolü
    if not ffmpeg_exists():
        system = platform.system()

        if system == "Windows":
            install_ffmpeg_windows()
        elif system == "Darwin":  # macOS
            install_ffmpeg_mac()
        else:
            print("Unsupported OS!")
            return

    input_folder = "input"
    output_folder = "output"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = os.listdir(input_folder)

    for file in files:
        if file.lower().endswith(".mp4"):
            mp4_path = os.path.join(input_folder, file)
            mp3_name = os.path.splitext(file)[0] + ".mp3"
            mp3_path = os.path.join(output_folder, mp3_name)

            print(f"Converting: {file} → {mp3_name}")
            convert_mp4_to_mp3(mp4_path, mp3_path)

    print("\n✔ All MP4 files have been successfully converted to MP3!")

if __name__ == "__main__":
    main()
