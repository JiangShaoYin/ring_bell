# coding:utf-8
import pygame
import os
import time
import random

schedules = {
  "workday":[
    ["05:20","06:20"],
    ["06:30","08:00"],

    ["08:40","09:40"],

    ["09:55","12:10"],

    ["13:00","14:40"],
    ["15:00","16:30"],
    ["16:50","18:20"],

    ["19:00","20:00"],
    ["20:10","21:15"],
  ],

  "Saturday":[
    ["05:20","06:20"],

    ["06:30","08:00"],
    ["08:20","09:50"],
    ["10:10","11:40"],

    ["12:10","13:40"],
    ["14:00","15:30"],
    ["15:50","17:25"],
  ],

  "Sunday":[
    ["05:20","06:20"],
    
    ["06:30","08:00"],
    ["08:20","09:50"],
    ["10:10","11:40"],

    # ["17:55","19:25"],
    # ["19:45","21:15"],

    ["09:10","10:40"],
    ["11:00","12:30"],
    
    ["12:50","14:20"],
    ["14:40","16:10"],
    ["16:30","18:00"],

    ["18:30","20:00"],
    ["20:10","21:15"],
  ],
} 


def play_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.stop()   # 如果有上次未停止的播放，则先停止
    pygame.mixer.music.play()

def ringBell(filename):
    try:
        play_music(filename)
        play_log("ringBell", "success", filename)
    except:
        play_log("ringBell", "fail", filename)


def play_log(task_name, status, task):
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('./play.log', 'a+', encoding='utf-8') as fp:
        content = now_time + '\t' + task_name + '\t' + status + '\t' + task + '\n'
        fp.write(content)

def show_desktop_notification(title, message):
    try:
        # 使用plyer库
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name='Clocker',
            timeout=10
        )
    except ImportError:
        play_log("desktop_notification", "fail", "plyer library not installed")

def show_popup():
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        messagebox.showinfo("Clocker", "Time's up!")
        root.destroy()
    except ImportError:
        play_log("show_popup", "fail", "tkinter library not installed")



def main():
    # ringBell("/Users/jiangshaoyin/code/ring_bell/on_class.mp3")
    show_popup()

    while True:
        # get the weekday of today in human readable format
        weekday = time.strftime("%A")
        weekday = weekday if weekday == "Sunday" or weekday == "Saturday" else "workday"

        on_class = {time[0] for time in schedules[weekday]}
        off_class = {time[1] for time in schedules[weekday]}
        print(on_class)
        print(off_class)

        task_time = time.strftime("%H:%M")
        print("\r 当前系统时间: %s" %task_time, end=" ")
        if task_time in on_class:
            ringBell("/Users/jiangshaoyin/code/ring_bell/on_class.mp3")
            time.sleep(60 * 10)
        if task_time in off_class:
            ringBell("/Users/jiangshaoyin/code/ring_bell/off_class.mp3")
            time.sleep(60 * 10)
        time.sleep(50)


if __name__ == "__main__":
    main()
