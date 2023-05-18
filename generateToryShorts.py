import os
import shutil
import random
from moviepy.editor import *
import requests
#dataset.py에서 불러옴
import dataset


# Load intro video and audio
intro_dir = "./intro"
intro_file = os.path.join(intro_dir, "Intro.mov")
intro = VideoFileClip(intro_file)

only_music_file = "only.mp3"
intro_music_file = os.path.join(intro_dir, only_music_file)
intro_music = AudioFileClip(intro_music_file)
intro = intro.set_audio(intro_music)

# Load outro video
outro_dir = "./outro"
outro_file = os.path.join(outro_dir, "Outro.mp4")
outro = VideoFileClip(outro_file)

#다운로드가 잘 이루어졌는 지 확인하는 코드
download_dir = "./drive/"
if not os.path.exists(download_dir):    #drive 디렉토리가 있는 지 확인 -> 코드 맨 마지막에 drive 디렉토리 삭제
    asset_dir  = "./asset"              #없으면 기존의 에셋 활용
else:
    asset_dir  = "./drive"              #있으면 drive의 영상 활용

# Load random video file and trim to 9 seconds
video_files = [f for f in os.listdir(asset_dir) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
random_video_file = random.choice(video_files)

video_file = os.path.join(asset_dir, random_video_file)
video = VideoFileClip(video_file)

if video.duration > 9:
    start_time = random.uniform(0, video.duration - 9)
    end_time = start_time + 9
    video = video.subclip(start_time, end_time)

# Load random image file and resize to 1280x1280
name_dir = "./"
name_image_file = "name.png"

name_file = os.path.join(name_dir, name_image_file)
image_name = ImageClip(name_file).resize((2000, 778)).set_pos((80, 2578))



#생성 AI를 통해 문제 이미지 생성
try:
  data = dataset.chooseData()
  print(data)

  API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
  headers = {"Authorization": "Bearer " + os.getenv("API_KEY")}

  def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content
  image_bytes = query({
    "inputs": data,
  })
  # You can access the image with PIL.Image for example
  import io
  from PIL import Image
  image = Image.open(io.BytesIO(image_bytes))
  image.save('./generate/quiz.png', 'png')

  image_dir = "./generate/"
except:
  image_dir  = "./image"   
  print("생성AI 실패")


# Load random image file and resize to 1280x1280
image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
random_image_file = random.choice(image_files)

image_file = os.path.join(image_dir, random_image_file)
image = ImageClip(os.path.join(image_dir, random_image_file)).resize((1000, 1000)).set_pos((580, 302))


# Load random music file
music_dir = "./music"
music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
random_music_file = random.choice(music_files)

music_file = os.path.join(music_dir, random_music_file)
music = AudioFileClip(music_file)


# Combine video, image and music
video_with_image = CompositeVideoClip([video, image.set_duration(video.duration), image_name.set_duration(video.duration)])
final_clip = concatenate_videoclips([video_with_image, outro])

if music.duration < final_clip.duration:
    music = music.loop_to_duration(final_clip.duration)
else:
    music = music.subclip(0, final_clip.duration)

final_clip = final_clip.set_audio(music)

#Intro + final_clip(playing video + outro)
final_clip = concatenate_videoclips([intro,final_clip])


# Export final video
final_clip.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")

#drive 디렉토리 삭제 -> 커밋할 수 있는 파일 크기 때문에
if os.path.exists("./drive/"):
    shutil.rmtree("./drive/") # -> 디렉토리 안의 비었을 때 : os.removedir(dir), 디렉토리 안에 파일이 있을 때 : shutil.rmtree(dir)
else:
    print("drive 영상 다운로드 실패! 기존 에셋 영상을 통한 제작 진행")