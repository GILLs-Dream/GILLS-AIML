import os
import easyocr
from app.image_process import preprocess_image_for_ocr

def extract_text_from_frames(frame_dir: str, lang=["ko", "en"], preprocessed_dir=None):
    texts = []
    os.makedirs(preprocessed_dir, exist_ok=True) if preprocessed_dir else None

    reader = easyocr.Reader(lang, gpu=True)  # GPU 사용 가능

    for file in sorted(os.listdir(frame_dir)):
        if file.endswith('.jpg'):
            img_path = os.path.join(frame_dir, file)

            rois = preprocess_image_for_ocr(img_path, save_path=preprocessed_dir)

            for i, roi_img in enumerate(rois):
                result = reader.readtext(roi_img, detail=0)  # detail=0이면 텍스트만 반환
                for line in result:
                    line = line.strip()
                    if line:
                        texts.append(f"[{file} ROI {i}]: {line}")

    return texts