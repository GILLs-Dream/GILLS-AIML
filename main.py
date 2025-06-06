import time
from app.downloader import download_video
from app.frame_extractor import extract_frames
from app.ocr import extract_text_from_frames
from pathlib import Path

def save_texts_to_file(texts, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, line in enumerate(texts, 1):
            f.write(f"[Frame {i}]\n{line}\n\n")

def main():
    video_url = input("🎥 유튜브 영상 URL 입력: ")

    # ⏱ 영상 다운로드
    start_time = time.time()
    print("\n⏳ [1/3] 영상 다운로드 중...")
    video_path = download_video(video_url, "data/videos")
    print(f"✅ 다운로드 완료: {video_path}")
    print(f"⏱ 소요 시간: {time.time() - start_time:.2f}초\n")

    # ⏱ 프레임 추출
    start_time = time.time()
    print("⏳ [2/3] 프레임 추출 중...")
    extract_frames(video_path, "data/frames", interval_sec=1)
    print("✅ 프레임 추출 완료!")
    print(f"⏱ 소요 시간: {time.time() - start_time:.2f}초\n")

    # ⏱ OCR 처리
    start_time = time.time()
    print("⏳ [3/3] OCR 처리 중...")
    texts = extract_text_from_frames("data/frames")
    print("✅ OCR 완료!")
    print(f"⏱ 소요 시간: {time.time() - start_time:.2f}초\n")

    # 결과 저장
    output_txt = Path("data/ocr_result.txt")
    save_texts_to_file(texts, output_txt)
    print(f"📝 OCR 결과 저장 완료: {output_txt.resolve()}")

if __name__ == "__main__":
    main()