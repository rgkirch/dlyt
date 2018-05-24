import os
from pytube import YouTube
from pytube import Playlist
import win32clipboard
from tkinter import filedialog
from tkinter import *
from tkinter import ttk


def clear_listbox(lb):
    lb.delete(0, END)


def append_to_text_box(text_box, text):
    state = text_box['state']
    text_box['state'] = 'normal'
    text_box.insert(END, text)
    text_box['state'] = state


def get_clipboard_contents():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def paste_button_callback():
    url = get_clipboard_contents().strip()
    url_entry.delete(0, END)
    url_entry.insert(0, url)


def audio_button_callback():
    url = url_entry.get().strip()
    yt = YouTube(url)
    stream = yt.streams.filter(type='audio', subtype='mp4').order_by(
        'bitrate').desc().first()
    stream.default_filename
    stream.download()
    os.rename(stream.default_filename, stream.default_filename[:-1] + '3')


def video_button_callback():
    url = url_entry.get().strip()
    yt = YouTube(url)
    yt.streams.filter(progressive=True,
                      subtype='mp4').order_by('resolution').first().download()


if __name__ == '__main__':

    root = Tk()
    root.title('dowload from youtube')
    main_frame = ttk.Frame(root)

    Label(root, text='youtube video url').pack(
        anchor='w')
    #  _______   ________________________________
    # | paste | | 'https://youtu.be/dQw4w9WgXcQ' |
    # |_______| |________________________________|
    url_entry_frame = Frame(root)
    paste_button = Button(url_entry_frame, text='paste button',
                          command=paste_button_callback)
    paste_button.pack(side=LEFT)
    url_entry = Entry(url_entry_frame)
    url_entry.pack(side=LEFT, fill=BOTH, expand=1)
    url_entry_frame.pack(anchor='w', fill=X)

    #  _______   _______
    # | video | | audio |
    # |_______| |_______|
    button_frame = Frame(root)
    video_button = Button(button_frame, text='video',
                          command=video_button_callback)
    video_button.pack(side=LEFT)
    audio_button = Button(button_frame, text='audio',
                          command=audio_button_callback)
    audio_button.pack(side=LEFT)
    button_frame.pack(anchor='w', fill=X)

    root.mainloop()
