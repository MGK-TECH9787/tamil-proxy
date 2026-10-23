from flask import Flask, redirect, abort
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "Tamil IPTV Proxy is Running!"

@app.route('/live/<channel_id>.m3u8')
def get_stream(channel_id):
    try:
        yt_url = f"https://www.youtube.com/channel/{channel_id}/live"
        cmd = ["yt-dlp", "-g", "-f", "best", yt_url]
        stream_url = subprocess.check_output(cmd, timeout=20).decode('utf-8').strip()
        return redirect(stream_url, code=302)
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
