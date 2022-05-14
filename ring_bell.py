# coding:utf-8
import pygame
import os
import time
import random

bell_time_list = {
"05:30","07:00",
"07:20","08:50",
"09:10","10:40",

"11:00","12:30",
"13:00","14:30",
"14:50","16:20",
"16:40","18:10",

"18:40","20:10",
"20:30","22:00"}

def play_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.stop()   # 如果有上次未停止的播放，则先停止
    pygame.mixer.music.play()

def ringBell():
    file = './1.mp3'
    try:
        play_music(file)
        play_log("ringBell", "succees", file)
    except:
        play_log("ringBell", "fail", file)


def play_log(task_name, status, task):
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('./play.log', 'a+', encoding='utf-8') as fp:
        content = now_time + '\t' + task_name + '\t' + status + '\t' + task + '\n'
        fp.write(content)


def main():
    ringBell()
    while True:
        task_time = time.strftime("%H:%M")
        print("\r 当前系统时间: %s" %task_time, end=" ")
        if task_time in bell_time_list:
            ringBell()
            time.sleep(60 * 10)
        time.sleep(50)

if __name__ == "__main__":
    main()
