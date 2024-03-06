import cv2
import dlib
import numpy as np

# 미리 학습된 모델과 이미지 파일 경로 설정
PREDICTOR_PATH = 'shape_predictor_68_face_landmarks.dat'
image_path = 'test.jpg'

# dlib의 얼굴 탐지기와 랜드마크 탐지기 초기화
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

# 이미지 로드 및 흑백 변환
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 얼굴 탐지 및 랜드마크 추출
faces = detector(gray)
for face in faces:
    landmarks = predictor(gray, face)

    # 볼 영역과 입술 영역에 대한 랜드마크 포인트
    cheek_points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(1, 16)]
    lip_points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(48, 68)]
    
    # 볼 영역에 대한 마스크 생성
    cheek_mask = np.zeros_like(gray)
    cv2.fillPoly(cheek_mask, [np.array(cheek_points, dtype=np.int32)], (255))
    cv2.fillPoly(cheek_mask, [np.array(lip_points, dtype=np.int32)], (0))

# 이미지를 YCbCr 컬러 공간으로 변환 및 피부색 마스크 생성
ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
lower_skin = np.array([0, 133, 77], dtype=np.uint8)
upper_skin = np.array([255, 173, 127], dtype=np.uint8)
skin_mask = cv2.inRange(ycbcr, lower_skin, upper_skin)

# 모폴로지 연산 적용
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
skin_mask = cv2.erode(skin_mask, kernel, iterations=20)

# 겹치는 부분의 마스크 선택
combined_mask = cv2.bitwise_and(cheek_mask, skin_mask)

# 결합된 마스크 적용하여 피부 영역 추출
final_skin = cv2.bitwise_and(image, image, mask=combined_mask)

# 피부 영역 픽셀에서 RGB 채널의 사분위수 계산 및 평균 계산
masked_pixels = image[combined_mask != 0]
Q1 = np.percentile(masked_pixels, 25, axis=0)
Q3 = np.percentile(masked_pixels, 75, axis=0)

# 사분위수 범위 내의 픽셀들만 선택하여 평균 계산
interquartile_range_mask = (masked_pixels >= Q1) & (masked_pixels <= Q3)
filtered_pixels = masked_pixels[np.all(interquartile_range_mask, axis=-1)]
average_color_IQR = np.mean(filtered_pixels, axis=0)

print("제1사분위수(Q1)부터 제3사분위수(Q3)까지 피부 영역 픽셀의 평균 RGB 값:", average_color_IQR)

# 결과 시각화
cv2.imshow('Final Skin Area with Morphology (YCbCr)', final_skin)
cv2.waitKey(0)
cv2.destroyAllWindows()
