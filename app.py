
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
    return "Tamil Live News IPTV Proxy is Running Successfully!"

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

@app.route('/playlist.m3u')
def get_playlist():
    host = request.host_url.rstrip('/')
    
    playlist_content = f"""#EXTM3U x-tvg-url=""

#EXTINF:-1 tvg-id="PolimerNews" tvg-name="Polimer News" tvg-logo="https://yt3.googleusercontent.com/ytc/AIdro_n8-rPqV4qg=s900-c-k-c0x00ffffff-no-rj" group-title="Tamil News",Polimer News
{host}/live/UCskb8P_h_T99z5U83E26v9Q.m3u8

#EXTINF:-1 tvg-id="ThanthiTV" tvg-name="Thanthi TV" tvg-logo="https://yt3.googleusercontent.com/ytc/AIdro_n8h2T_mE3-bF5Q1Y6=s900-c-k-c0x00ffffff-no-rj" group-title="Tamil News",Thanthi TV
{host}/live/UC9_2_fJk-6x6T8kO4u9L4sA.m3u8

#EXTINF:-1 tvg-id="PuthiyaThalaimurai" tvg-name="Puthiya Thalaimurai" tvg-logo="https://yt3.googleusercontent.com/ytc/AIdro_lQ6D5L=s900-c-k-c0x00ffffff-no-rj" group-title="Tamil News",Puthiya Thalaimurai
{host}/live/UCv2_Wk2zW_yH_yU6c5T7F9w.m3u8

#EXTINF:-1 tvg-id="SunNews" tvg-name="Sun News" tvg-logo="https://yt3.googleusercontent.com/ytc/AIdro_mN6x5Q=s900-c-k-c0x00ffffff-no-rj" group-title="Tamil News",Sun News
{host}/live/UCvh_yC7XkM3LgZ6v_4Q9Qvg.m3u8

#EXTINF:-1 tvg-id="News18TamilNadu" tvg-name="News18 Tamil Nadu" tvg-logo="https://yt3.googleusercontent.com/ytc/AIdro_k6T_8M=s900-c-k-c0x00ffffff-no-rj" group-title="Tamil News",News18 Tamil Nadu
{host}/live/UCb0x5L7_yC7yG4R_4u5_6gQ.m3u8

#EXTINF:-1 tvg-id="KalaignarNews" tvg-name="Kalaignar News" tvg-logo="https://yt3.googleusercontent.com/ytc/AIdro_lM8T9P=s900-c-k-c0x00ffffff-no-rj" group-title="Tamil News",Kalaignar News
{host}/live/UCd1Z8j3m9bH6x5G7X4n0M9A.m3u8

#EXTINF:-1 tvg-id="NewsTamil24x7" tvg-name="News Tamil 24x7" tvg-logo="https://yt3.googleusercontent.com/ytc/AIdro_nP9T_k=s900-c-k-c0x00ffffff-no-rj" group-title="Tamil News",News Tamil 24x7
{host}/live/UCTWk2_7k_6fH6M4V8L5Y1qA.m3u8

#EXTINF:-1 tvg-id="SathiyamTV" tvg-name="Sathiyam TV" tvg-logo="https://yt3.googleusercontent.com/ytc/AIdro_mF8L_1=s900-c-k-c0x00ffffff-no-rj" group-title="Tamil News",Sathiyam TV
{host}/live/UCJ4mC0j5G8N3T7X_8l4h0Xg.m3u8
"""
    return Response(playlist_content.strip(), mimetype='application/x-mpegurl')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
