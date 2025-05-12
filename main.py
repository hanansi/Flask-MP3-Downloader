from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pytubefix import YouTube, exceptions
from pytubefix.cli import on_progress
from pydub import AudioSegment
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


def get_audio_stream(url):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        ys = yt.streams.get_audio_only()
        yt_filename = ys.default_filename

        buffer = BytesIO()
        ys.stream_to_buffer(buffer)
        buffer.seek(0)
        return (buffer, yt_filename)
    except exceptions.RegexMatchError:
        return (None, None)


def convert_m4a_to_mp3(audio_buffer):
    m4a_audio = AudioSegment.from_file(audio_buffer, format="m4a")
    mp3_buffer = BytesIO()
    m4a_audio.export(mp3_buffer, format="mp3")
    mp3_buffer.seek(0)
    return mp3_buffer


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
           m4a_buffer, filename = get_audio_stream(url)
           mp3_buffer = convert_m4a_to_mp3(m4a_buffer)
           mp3_filename = filename.rsplit(".", 1)[0] + ".mp3"

           m4a_buffer.close()  # releases internal buffer memory
           del m4a_buffer      # removes reference so it can be garbage collected

           if mp3_buffer:
                return send_file(mp3_buffer, as_attachment=True, download_name=mp3_filename, mimetype="audio/mp3") 

        return redirect(url_for("index"))  # Redirect to avoid resubmission on refresh

    return render_template("index.html")  # Render template for GET requests


if __name__ == '__main__':
    app.run(debug=True)
    