from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
import os
from moviepy.editor import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    file_type = request.form['file_type']
    download_path = request.form['path']

    try:
        yt = YouTube(url)
        if file_type == 'mp4':
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=download_path)
            file_path = os.path.join(download_path, stream.default_filename)
        else:
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(output_path=download_path)
            file_path = os.path.join(download_path, stream.default_filename)

            mp4_path = file_path
            mp3_path = mp4_path.replace('.mp4', '.mp3')
            video = AudioFileClip(mp4_path)
            video.write_audiofile(mp3_path)
            video.close()

            os.remove(mp4_path)

            file_path = mp3_path

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
