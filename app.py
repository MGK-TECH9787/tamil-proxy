
import os
import re
import requests
from flask import Flask, redirect, Response, request

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def extract_hls_url(page_url):
    response = requests.get(page_url, headers=HEADERS, timeout=15)
    match = re.search(r'(https:\/\/[^"\'\s]+\.m3u8)', response.text)
    if match:
        return match.group(1).replace('\\/', '/')
    return None

@app.route('/')
def home():
    return "Tamil IPTV Proxy is Running!"

# வீடியோ ஐடி ஸ்ட்ரீம்
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

# சேனல் ஐடி ஸ்ட்ரீம்
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

# TiviMate-ல் நேரடியாக M3U URL ஆகக் கொடுக்க இது உதவும்
@app.route('/playlist.m3u')
def get_playlist():
    host = request.host_url.rstrip('/')
    content = f"""#EXTM3U
#EXTINF:-1 tvg-id="PolimerLive" tvg-name="Polimer News" tvg-logo="https://yt3.googleusercontent.com/ytc/AIdro_n8-rPqV4qg=s900-c-k-c0x00ffffff-no-rj" group-title="Tamil News",Polimer News Live
{host}/live/UCskb8P_h_T99z5U83E26v9Q.m3u8
"""
    return Response(content, mimetype='application/x-mpegurl')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
