
from flask import Flask, redirect
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "Tamil IPTV Proxy is Running!"

# வீடியோ ID அல்லது லைவ் URL மூலம் இயக்கும் வழி
@app.route('/video/<v_id>.m3u8')
def get_video_stream(v_id):
    try:
        yt_url = f"https://www.youtube.com/watch?v={v_id}"
        # ஆடியோ மற்றும் வீடியோ இணைந்த மிகச் சிறந்த HLS லிங்க்கை எடுக்கும்
        cmd = ["yt-dlp", "-g", "-f", "best", yt_url]
        stream_url = subprocess.check_output(cmd, timeout=25).decode('utf-8').strip()
        return redirect(stream_url, code=302)
    except Exception as e:
        return f"Error: {e}", 500

# சேனல் ID மூலம் இயக்கும் வழி
@app.route('/live/<channel_id>.m3u8')
def get_channel_stream(channel_id):
    try:
        yt_url = f"https://www.youtube.com/channel/{channel_id}/live"
        cmd = ["yt-dlp", "-g", "-f", "best", yt_url]
        stream_url = subprocess.check_output(cmd, timeout=25).decode('utf-8').strip()
        return redirect(stream_url, code=302)
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
