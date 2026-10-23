
import os
import re
import requests
from flask import Flask, redirect, Response, request

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def extract_hls_url(page_url):
    try:
        res = requests.get(page_url, headers=HEADERS, timeout=12)
        match = re.search(r'(https:\/\/[^"\'\s]+\.m3u8)', res.text)
        if match:
            return match.group(1).replace('\\/', '/')
    except Exception:
        pass
    return None

@app.route('/')
def home():
    return "All-in-One Tamil IPTV & Multi-Sports Live Proxy is Running 24/7!"

# --- YouTube Endpoints ---
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

# --- FanCode API Dynamic Resolver ---
@app.route('/fancode/<match_id>.m3u8')
def get_fancode_stream(match_id):
    try:
        fc_api = f"https://www.fancode.com/api-craft/v1/event/{match_id}"
        res = requests.get(fc_api, headers=HEADERS, timeout=8)
        data = res.json()
        stream_url = data.get('event', {}).get('stream_url') or data.get('stream_url')
        if stream_url:
            return redirect(stream_url, code=302)
        return redirect(f"https://dai.google.com/linear/hls/event/{match_id}/master.m3u8", code=302)
    except Exception as e:
        return f"Error: {e}", 500

# --- Tamil News Playlist ---
@app.route('/playlist.m3u')
def get_news_playlist():
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

#EXTINF:-1 tvg-id="NewsTamil24x7" tvg-name="News Tamil 24x7" tvg-logo="https://yt3.googleusercontent.com/ytc/AIdro_nP9T_k=s900-c-k-c0x00ffffff-no-rj" group-title="Tamil News",News Tamil 24x7
{host}/live/UCTWk2_7k_6fH6M4V8L5Y1qA.m3u8
"""
    return Response(playlist_content.strip(), mimetype='application/x-mpegurl')

# --- All Sports & Live Events Playlist ---
@app.route('/sports.m3u')
def get_all_sports_playlist():
    host = request.host_url.rstrip('/')
    lines = ['#EXTM3U x-tvg-url=""']

    # 1. DD Sports (தேசிய & சர்வதேச போட்டிகள் - Free HLS)
    lines.append(f'#EXTINF:-1 tvg-id="DDSports" tvg-name="DD Sports HD" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/2/23/DD_Sports_logo.png" group-title="National Sports",DD Sports HD\nhttps://d2q8p4pe5spbak.cloudfront.net/bpk-tv/DDSportsHD/default/index.m3u8')

    # 2. Sony Sports Networks
    lines.append(f'#EXTINF:-1 tvg-id="SonyTen1" tvg-name="Sony Ten 1 HD" tvg-logo="https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/india/sony-ten-1-in.png" group-title="Sony Sports",Sony Ten 1 HD\nhttps://dai.google.com/linear/hls/event/U3y74V2WRvG-881J72V5bg/master.m3u8')
    lines.append(f'#EXTINF:-1 tvg-id="SonyTen2" tvg-name="Sony Ten 2 HD" tvg-logo="https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/india/sony-ten-2-in.png" group-title="Sony Sports",Sony Ten 2 HD\nhttps://dai.google.com/linear/hls/event/y7p_Zc80SCqXqW6N9x2P2w/master.m3u8')
    lines.append(f'#EXTINF:-1 tvg-id="SonyTen5" tvg-name="Sony Ten 5 HD" tvg-logo="https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/india/sony-ten-5-in.png" group-title="Sony Sports",Sony Ten 5 HD\nhttps://dai.google.com/linear/hls/event/fUeA2sYxTVG49i_hD1n_4A/master.m3u8')

    # 3. Red Bull TV (சர்வதேச அதிரடி விளையாட்டுகள் & ரேசிங்)
    lines.append(f'#EXTINF:-1 tvg-id="RedBullTV" tvg-name="Red Bull TV" tvg-logo="https://resources.redbull.com/logos/redbulltv/v1/redbulltv-logo.png" group-title="Global Sports",Red Bull TV\nhttps://rbmn-live.akamaized.net/hls/live/590964/BoRB-AT/master.m3u8')

    # 4. FanCode நேரடி போட்டிகள் (Auto Fetch)
    try:
        fc_matches_api = "https://www.fancode.com/api-craft/v1/matches?status=LIVE"
        f_res = requests.get(fc_matches_api, headers=HEADERS, timeout=5)
        if f_res.status_code == 200:
            matches = f_res.json().get('matches', [])
            for m in matches:
                m_id = m.get('id')
                m_name = m.get('name', 'Live Match')
                lines.append(f'#EXTINF:-1 tvg-id="{m_id}" tvg-name="{m_name}" tvg-logo="https://images.fancode.com/eyJrZXkiOiJmYW5jb2RlLWxvZ28ucG5nIn0=" group-title="FanCode Events",{m_name}\n{host}/fancode/{m_id}.m3u8')
    except Exception:
        lines.append(f'#EXTINF:-1 tvg-id="FanCodeLive" tvg-name="FanCode Live Cricket" group-title="FanCode Events",FanCode Live Cricket\n{host}/fancode/live.m3u8')

    # 5. Cricbuzz நேரலை உரையாடல் & போட்டி கவரேஜ்
    lines.append(f'#EXTINF:-1 tvg-id="CricbuzzLive" tvg-name="Cricbuzz Live Analysis" tvg-logo="https://www.cricbuzz.com/images/cb_logo.svg" group-title="Cricket Analysis",Cricbuzz Live\n{host}/live/UCszBHXKg_4B3_Y69xS_Hn7Q.m3u8')

    return Response("\n\n".join(lines), mimetype='application/x-mpegurl')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
