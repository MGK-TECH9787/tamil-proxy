
import os
import subprocess
from flask import Flask, redirect, Response

app = Flask(__name__)

@app.route('/')
def home():
    return "Tamil IPTV Proxy is Running Successfully!"

@app.route('/video/<v_id>.m3u8')
def get_video_stream(v_id):
    try:
        yt_url = f"https://www.youtube.com/watch?v={v_id}"
        cmd = ["yt-dlp", "-g", "--format", "best[ext=mp4]/best", yt_url]
        stream_url = subprocess.check_output(cmd, timeout=30).decode('utf-8').strip().split('\n')[0]
        return redirect(stream_url, code=302)
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/live/<channel_id>.m3u8')
def get_channel_stream(channel_id):
    try:
        yt_url = f"https://www.youtube.com/channel/{channel_id}/live"
        cmd = ["yt-dlp", "-g", "--format", "best[ext=mp4]/best", yt_url]
        stream_url = subprocess.check_output(cmd, timeout=30).decode('utf-8').strip().split('\n')[0]
        return redirect(stream_url, code=302)
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
