import subprocess

def run_command(command):
    cmd = command
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def setup_ffmpeg():
    try:
        cmd1 = "ffmpeg -version"
        run_command(command)
        print("ffmpeg already installed!")
    except:
        try:
            print("Setting up ffmpeg (SUDO)...")
            update = "ffmpeg -version"
            run_command(update)
            command = "sudo apt-get install ffmpeg"
            run_command(command)
            print("ffmpeg setup complete!")
        except:
            print("Setting up ffmpeg (SUDO)...")
            command = "apt-get install ffmpeg"
            run_command(command)
            print("ffmpeg setup complete!")

def setup_streamlink():
    try:
        command = "streamlink -version"
        run_command(command)
        print("streamlink already installed!")
    except:
        try:
            print("Setting up streamlink (SUDO)...")
            command = "sudo apt-get install -y streamlink"
            run_command(command)
            print("streamlink setup complete!")
        except:
            print("Setting up streamlink...")
            command = "apt-get install -y streamlink"
            run_command(command)
            print("streamlink setup complete!")