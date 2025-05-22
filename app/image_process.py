import cv2
import numpy as np
import os

def preprocess_image_for_ocr(img_path, save_path=None):
    """
    이미지 전처리: OCR 성능 향상을 위한 기본 전처리 수행
    - 그레이스케일 변환
    - 가우시안 블러로 노이즈 제거
    - Adaptive Threshold 이진화
    - 모폴로지 연산(팽창)으로 텍스트 영역 강조
    - 윤곽선 기반 텍스트 영역 후보 추출 및 ROI 반환

    :param img_path: 원본 이미지 경로
    :param save_path: 전처리 이미지 저장 경로 (선택사항)
    :return: 전처리된 이미지 리스트 (각각 텍스트 영역 후보)
    """

    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {img_path}")

    # 1. 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 가우시안 블러 (노이즈 제거)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Adaptive Threshold (이진화)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    # 4. 모폴로지 연산 (팽창) — 텍스트 영역 연결
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=2)

    # 5. 윤곽선 찾기
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rois = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # 너무 작거나 너무 큰 영역 필터링 (텍스트 영역 후보만)
        if w < 50 or h < 15:
            continue
        if w > img.shape[1] * 0.9 and h > img.shape[0] * 0.9:
            continue

        roi = gray[y:y + h, x:x + w]

        # Optional: ROI 이미지 저장
        if save_path:
            os.makedirs(save_path, exist_ok=True)
            cv2.imwrite(os.path.join(save_path, f"roi_{x}_{y}.png"), roi)

        rois.append(roi)

    # 전처리된 전체 이미지도 저장 가능 (텍스트가 잘 보이도록)
    if save_path:
        os.makedirs(save_path, exist_ok=True)
        cv2.imwrite(os.path.join(save_path, "preprocessed.png"), dilated)

    # 후보 영역 없으면 원본 그레이스케일 반환
    if not rois:
        return [gray]

    return rois