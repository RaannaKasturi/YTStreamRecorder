import gradio as gr
from main import main
import subprocess

def get_stream(channel_id, email, nyberman):
    emails = email.split(" ")
    file_url = main(channel_id, emails, nyberman)
    if not file_url:
        return "No Live Streams Currently."
    return file_url

def setup():
    command = f'apt update && apt install -y ffmpeg'
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def app():
    with gr.Blocks(title="Youtube Stream Downloader") as webui:
        with gr.Row():
            with gr.Column():
                channel_id = gr.Textbox(label="Enter Channel ID", placeholder="UCzGnQARnZqgfB37xPBCgw8g", type="text", interactive=True)
                is_nyberman = gr.Checkbox(label="Is Nyberman Stream?", value=False)
            email_id = gr.Textbox(label="Enter your Email ID", placeholder="nayankasturi@gmail.com", type="text", interactive=True)
        btn = gr.Button(value="Record & Download Stream")
        file_url = gr.Textbox(label="File URL", type="text", interactive=False, show_copy_button=True)
        btn.click(get_stream, inputs=[channel_id, email_id, is_nyberman], outputs=file_url)
    try:
        webui.queue(default_concurrency_limit=15).launch()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":

    app()
