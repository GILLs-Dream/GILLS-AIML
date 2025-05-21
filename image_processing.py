import cv2
import numpy as np
import os

# 텍스트 후보 영역 추출 함수
def selectWords(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Sobel 연산으로 수직 방향 엣지 강조 (자막 텍스트에 유리)
    grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3)
    abs_grad_x = cv2.convertScaleAbs(grad_x)

    # 이진화
    _, binary = cv2.threshold(abs_grad_x, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 커널 크기: 가로로 긴 텍스트 형태 추출
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 5))
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

    # 외곽선 찾기
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    roi_list = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 50 and h > 15:  # 너무 작으면 제외
            roi = img[y:y + h, x:x + w]
            roi_list.append(roi)

    return roi_list


# 동영상 프레임 처리 및 ROI 추출
def process_video(video_path, output_dir='output', frame_interval=30):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"❌ 영상 파일을 열 수 없습니다: {video_path}")
    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            roi_list = selectWords(frame)
            for idx, roi in enumerate(roi_list):
                filename = f"{output_dir}/frame{frame_count}_roi{idx}.png"
                cv2.imwrite(filename, roi)
                saved_count += 1

        frame_count += 1

    cap.release()
    print(f"[완료] 총 {saved_count}개의 ROI가 저장되었습니다.")

# 예시 사용
if __name__ == "__main__":
    with open("video_path.txt", "r") as f:
        video_path = f.read().strip()
    process_video(video_path, output_dir='text_frames', frame_interval=30)

