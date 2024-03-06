import cv2
import numpy as np

# 이미지 파일 경로
image_path = 'test.jpg'

# OpenCV를 사용하여 이미지 로드
image = cv2.imread(image_path)

# 흑백 이미지로 변환하여 얼굴 탐지를 용이하게 함
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 얼굴 탐지를 위한 Haar Cascade 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 얼굴 탐지 실행
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in faces:
    # 얼굴 영역 추출
    face_img = image[y:y+h, x:x+w]
    # HSV 컬러 공간으로 변환
    hsv = cv2.cvtColor(face_img, cv2.COLOR_BGR2HSV)
    
    # 피부색 HSV 범위 정의
    # 이 범위는 실험을 통해 조정해야 할 수 있음
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # 피부색에 해당하는 마스크 생성
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # 피부색에 해당하는 영역의 평균 색상 계산
    skin = cv2.bitwise_and(face_img, face_img, mask=mask)
    avg_color_per_row = np.average(skin, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    avg_color = np.uint8(avg_color)
    
    # 피부색 출력
    print("피부색 (BGR):", avg_color)

# 결과를 파일로 저장하거나 시각화하려면 cv2.imwrite 또는 cv2.imshow를 사용합니다.
# 예: cv2.imshow('Skin Color', skin)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
