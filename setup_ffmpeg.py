import subprocess

def run_command(command):
    cmd = command
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def setup_ffmpeg():
    try:
        command = "ffmpeg -version"
        run_command(command)
        print("ffmpeg already installed!")
    except:
        try:
            print("Setting up ffmpeg (SUDO)...")
            command = "sudo apt-get install ffmpeg"
            run_command(command)
            print("ffmpeg setup complete!")
        except:
            print("Setting up ffmpeg (SUDO)...")
            command = "apt-get install ffmpeg"
            run_command(command)
            print("ffmpeg setup complete!")
