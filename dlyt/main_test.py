from pytube import YouTube
from pytube import Playlist
from tkinter import *
from tkinter import ttk
from dlyt.main import *


def assertion(lb, result):
    result = map(int, lb.curselection())


def test_download_all_button_callback():
    root = Tk()
    some = -1
    lb = Listbox(root, selectmode=EXTENDED)
    lb.insert(END, "hello")
    lb.insert(END, "there")
    lb.pack()
    b = Button(root, text='assert', command=lambda: assertion(lb, some))
    b.pack()
    root.mainloop()
    assert some == [0]


def test_get_titles2():
    url_entry_text = 'https://youtu.be/3frlf4W0KOc?list=PLYyJCobshLZkakaNqSwjRouQ0zHbK0hek'
    # url_entry_text = 'https://www.youtube.com/watch?v=7Wk2v4yzhVo&list=UUhnxLLvzviaR5NeKOevB8iQ'
    urls = get_urls_from_entry_text(url_entry_text)
    yts = [YouTube(url) for url in urls]
    length = len([yt.player_config_args['title'] for yt in yts])
    print(length)
    assert length == 100


def test_get_titles():
    url_entry_text = 'https://www.youtube.com/watch?v=7Wk2v4yzhVo&list=UUhnxLLvzviaR5NeKOevB8iQ'
    urls = get_urls_from_entry_text(url_entry_text)
    # jobs = [YouTube(url) for url in urls]
    jobs = [gevent.spawn(YouTube, url) for url in urls]
    gevent.joinall(jobs)
    # for yt in jobs:
    assert len([job.value.player_config_args['title'] for job in jobs]) == 100
