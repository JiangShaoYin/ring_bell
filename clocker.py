# coding:utf-8
import pygame
import time
import os
import argparse

def play_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.stop()   # 如果有上次未停止的播放，则先停止
    pygame.mixer.music.play()

def ringBell(filename):
    filename = os.path.expanduser(filename)
    try:
        play_music(filename)
    except:
        play_log("ringBell", "fail", filename)


def play_log(task_name, status, task):
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    content = now_time + '\t' + task_name + '\t' + status + '\t' + task + '\n'
    print(content)

def parse_duration(duration):
    if duration is None:
        return 0
    if duration.endswith("h"):
        return int(duration[:-1]) * 60 * 60
    if duration.endswith("m"):
        return int(duration[:-1]) * 60
    if duration.endswith("s"):
        return int(duration[:-1])
    return int(duration)

def clocker(duration):
    seconds = parse_duration(duration)
    print(f"\n\nClocker will ring bell after {seconds} seconds")
    time.sleep(seconds)

    ringBell("~/code/ring_bell/on_class.mp3")
    # wait the music to finish
    time.sleep(5)



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="gar /path/to/dir # py |: gen arch of a give dir or file")

  parser.add_argument("duration", type=str, default=None, help="duration of the clocker, end with h/m/s")
  args = parser.parse_args()

  clocker(args.duration)


