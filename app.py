
import os
import re
import requests
from flask import Flask, redirect, abort

app = Flask(__name__)

# இயல்பான பிரவுசர் போல காட்டிக்கொள்ளும் User-Agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def extract_hls_url(page_url):
    response = requests.get(page_url, headers=HEADERS, timeout=15)
    # பக்கத்தின் சோர்ஸ் கோடில் உள்ள நேரடி HLS m3u8 லிங்க்கை தேடுதல்
    match = re.search(r'(https:\/\/[^"\'\s]+\.m3u8)', response.text)
    if match:
        return match.group(1).replace('\\/', '/')
    return None

@app.route('/')
def home():
    return "Tamil IPTV Proxy is Running!"

# வீடியோ ஐடி மூலம் இயக்குதல் (எ.கா: /video/JWu9MHaz6y8.m3u8)
@app.route('/video/<v_id>.m3u8')
def get_video_stream(v_id):
    try:
        url = f"https://www.youtube.com/watch?v={v_id}"
        hls_url = extract_hls_url(url)
        if hls_url:
            return redirect(hls_url, code=302)
        return "Stream not found", 404
    except Exception as e:
        return f"Error: {e}", 500

# சேனல் ஐடி மூலம் இயக்குதல்
@app.route('/live/<channel_id>.m3u8')
def get_channel_stream(channel_id):
    try:
        url = f"https://www.youtube.com/channel/{channel_id}/live"
        hls_url = extract_hls_url(url)
        if hls_url:
            return redirect(hls_url, code=302)
        return "Stream not found", 404
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
