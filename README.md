# AIStyling

## 최종 목표
웹 서비스 개시

## 프로세스
1. 사용자가 전신 사진을 업로드
   - 가이드가 있어야 함.
   - 사진의 밝기, 채도도 중요 (A4 용지를 배경으로 권장)
2. 얼굴형, 퍼스널컬러, 체형을 분석
   - 퍼스널컬러 분석법: 사진의 크기를 1080X1080 픽셀에 맞게 조정, OpenCV를 이용하여 얼굴을 추출, 랜드마크를 기준으로 볼 부분만을 추출, YCbCr 컬러 공간을 이용해 피부색을 검출, 모폴로지 연산을 적용하여 피부 영역 정제, 피부 영역에서 RGB 채널의 제1사분위수(Q1)부터 제3사분위수(Q3)까지의 픽셀 값들의 평균 RGB 값을 계산
4. 분석한 결과를 라벨링
5. 라벨링 데이터를 토대로 패션 추천
   - 패션 또한 라벨링 되어 있어야 함 (데이터 존재함)
   - 라벨링 데이터 간의 최적의 조합도 존재해야 함

## 개발 언어
- 백엔드: Spring
- 프론트엔드: React
- 알고리즘: 파이썬

## 필요 모델
https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat

# 팀원
- 김태훈 [github](https://github.com/minchoCoin)
- 이성훈 [github](https://github.com/NextrPlue)

## Reference
https://koreascience.kr/article/CFKO200928451820293.pdf
