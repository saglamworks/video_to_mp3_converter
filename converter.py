import os
import subprocess
import sys
import platform
import urllib.request
import zipfile

def print_install_message():
    print("\n===============================================")
    print(" Required packages are being installed for the")
    print(" first time. Please wait a moment...")
    print("===============================================\n")

def ffmpeg_exists():
    """FFmpeg kurulu mu kontrol et"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
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
    ffmpeg_path = os.path.join(ffmpeg_bin, "ffmpeg.exe")

    os.remove(zip_path)
    print("FFmpeg downloaded! Using local ffmpeg.")
    return ffmpeg_path

def install_ffmpeg_mac():
    print_install_message()
    print("Checking Homebrew for FFmpeg...")

    brew_check = subprocess.run(["brew", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if brew_check.returncode != 0:
        print("\nHomebrew is not installed! Please install it manually with this command:\n")
        print('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
        sys.exit(1)

    ffmpeg_check = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if ffmpeg_check.returncode != 0:
        print("Installing FFmpeg via Homebrew...")
        subprocess.run(["brew", "install", "ffmpeg"], check=True)

    return "ffmpeg"

def convert_mp4_to_mp3(ffmpeg_path, input_path, output_path):
    command = [
        ffmpeg_path,
        "-i", input_path,
        "-map", "0:a",       # tüm ses akışlarını al
        "-vn",               # video yok
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-y",                # varsa üstüne yaz
        output_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"✔ Converted: {os.path.basename(input_path)} → {os.path.basename(output_path)}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to convert: {os.path.basename(input_path)}")

def main():
    ffmpeg_path = "ffmpeg"  # default

    # FFmpeg kontrolü
    if not ffmpeg_exists():
        system = platform.system()
        if system == "Windows":
            ffmpeg_path = install_ffmpeg_windows()
        elif system == "Darwin":
            ffmpeg_path = install_ffmpeg_mac()
        else:
            print("Unsupported OS!")
            return

    input_folder = "input"
    output_folder = "output"

    if not os.path.exists(input_folder) or not os.listdir(input_folder):
        print("❌ Input folder is empty or does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".mp4")]

    for file in files:
        mp4_path = os.path.join(input_folder, file)
        mp3_name = os.path.splitext(file)[0] + ".mp3"
        mp3_path = os.path.join(output_folder, mp3_name)
        convert_mp4_to_mp3(ffmpeg_path, mp4_path, mp3_path)

    print("\n✔ All MP4 files have been successfully converted to MP3!")

if __name__ == "__main__":
    main()
