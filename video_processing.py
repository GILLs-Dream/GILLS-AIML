import os
import yt_dlp
import hashlib
import shutil

def sanitize_filename(title, ext):
    """제목을 SHA256으로 해시해서 고유한 파일명 생성"""
    hash_object = hashlib.sha256(title.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return f"{hex_dig}.{ext}"

def download_video(url, output_dir='videos'):
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # 영상 정보만 먼저 추출
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', 'video')
        video_id = info_dict.get('id')
        ext = 'mp4'  # 우리가 강제할 확장자
        hashed_name = sanitize_filename(title, ext)
        final_path = os.path.join(output_dir, hashed_name)

    # 실제 다운로드
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_path = os.path.join(output_dir, f"{info['id']}.mp4")

    # 해시 기반 이름으로 변경
    os.rename(downloaded_path, final_path)

    # 파일 경로 기록
    with open("video_path.txt", "w") as f:
        f.write(final_path)

    print(f"✅ 다운로드 완료! 저장 위치: {final_path}")
    return final_path

# 사용 예시
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=AMcaJvP3Gpk"
    downloaded_path = download_video(video_url)
    print(f"📁 사용할 영상 경로: {downloaded_path}")