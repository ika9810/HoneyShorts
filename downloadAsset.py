import gdown
import os
import random

# 다운로드 받을 Google Drive 파일의 ID를 랜덤으로 선택해서 변수에 저장합니다.
file_list = ["1UXDZ7wUAH56cjU9iauLWeMbaVGiti6K2",]
file_id = random.choice(file_list)

# 다운로드 받을 디렉토리 경로를 설정합니다.
#drive 디렉토리를 만들어서 구글 드라이브 영상을 저장할 디렉토리를 설정합니다.
download_dir = "./drive/"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Google Drive 파일의 ID를 기반으로 파일을 다운로드합니다.
url = f"https://drive.google.com/uc?id={file_id}"
output = os.path.join(download_dir, "output_video.mp4")
try:
  gdown.download(url, output, quiet=False)
except:
  print("영상 다운로드 실패!") 
print("영상 다운로드 완료!")