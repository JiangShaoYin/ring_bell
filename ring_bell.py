# coding:utf-8
import pygame
import os
import time




def play_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.stop()   # 如果有上次未停止的播放，则先停止
    pygame.mixer.music.play()







if __name__ == "__main__":
    play_music("/Users/jiangshaoyin/code/ring_bell/on_class.mp3")
    time.sleep(10)
