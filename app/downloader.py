import os
import hashlib
import yt_dlp

def sanitize_filename(title, ext):
    hash_object = hashlib.sha256(title.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return f"{hex_dig}.{ext}"

def download_video(url, output_dir='data/videos'):
    os.makedirs(output_dir, exist_ok=True)

    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', 'video')
        video_id = info_dict.get('id')
        ext = 'mp4'
        hashed_name = sanitize_filename(title, ext)
        final_path = os.path.join(output_dir, hashed_name)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_path = os.path.join(output_dir, f"{info['id']}.mp4")

    if os.path.exists(downloaded_path):
        os.rename(downloaded_path, final_path)

    return final_path