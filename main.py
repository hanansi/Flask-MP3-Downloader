from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pytubefix import YouTube, exceptions
from pytubefix.cli import on_progress
from io import BytesIO

app = Flask(__name__)
app.secret_key = b'\x1c\x8a\xbf\x88\xd07\xfa\x91\xb0\x9fU\x9c\xee\xaf\x01\x95D\xdf\xba\x83\xf7\xea\x8f7'


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
        flash("Input a YouTube Link.")
        return (None, None)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
           buffer, filename = get_audio_stream(url)
        
           if buffer:
                return send_file(buffer, as_attachment=True, download_name=filename, mimetype="audio/mp4") 

        return redirect(url_for("index"))  # Redirect to avoid resubmission on refresh

    return render_template("index.html")  # Render template for GET requests


if __name__ == '__main__':
    app.run(debug=True, host="192.168.58.154")
    