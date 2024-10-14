import subprocess

def run_command(command):
    cmd = command
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def setup_ffmpeg():
    try:
        fcmd1 = "ffmpeg -version"
        run_command(fcmd1)
        print("ffmpeg already installed!")
    except:
        try:
            print("Setting up ffmpeg (SUDO)...")
            fupdate = "sudo apt-get update"
            run_command(fupdate)
            fcmd2 = "sudo apt-get install -y ffmpeg"
            run_command(fcmd2)
            print("ffmpeg setup complete!")
        except:
            print("Setting up ffmpeg...")
            fupdate = "sudo apt-get update"
            run_command(fupdate)
            fcmd3 = "apt-get install -y ffmpeg"
            run_command(fcmd3)
            print("ffmpeg setup complete!")

def setup_streamlink():
    try:
        scmd = "streamlink -version"
        run_command(scmd)
        print("streamlink already installed!")
    except:
        try:
            supdate = "sudo apt-get update"
            run_command(supdate)
            print("Setting up streamlink (SUDO)...")
            scmd1 = "sudo apt-get install -y streamlink"
            run_command(scmd1)
            print("streamlink setup complete!")
        except:
            supdate = "sudo apt-get update"
            run_command(supdate)
            print("Setting up streamlink...")
            scmd2 = "apt-get install -y streamlink"
            run_command(scmd2)
            print("streamlink setup complete!")

def setup_environ():
    setup_ffmpeg()
    setup_streamlink()