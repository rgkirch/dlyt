from pytube import YouTube
from pytube import Playlist
import win32clipboard
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import gevent


def lb_single_selection(list_box) -> str:
    cur_sel = list_box.curselection()
    if cur_sel:
        return str(list_box.get(cur_sel))
    else:
        return ''


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


def listbox_select_callback(lb):
    print(lb_single_selection(lb))


def download(url):
    print('downloading url')


def is_playlist_url(url):
    return 'list=' in url

    # def populate_videolist():
    #     clear_listbox(listbox)
    #     url = url_entry.get()
    #     if is_playlist_url(url):
    #         pass
    #     else:
    #         yt = YouTube(url_entry.get())
    #     for item in yt:
    #         lb.insert(END, item)


def sequence(f, g):
    f()
    g()


def construct_playlist_url(url):
    base_url = 'https://www.youtube.com/playlist?list='
    playlist_code = url.split('&list=')[1]
    return base_url + playlist_code


def get_urls_from_entry_text(url_entry_text):
    urls = []
    if 'list' in url_entry_text:
        url = construct_playlist_url(url_entry_text)
        pl = Playlist(url)
        pl.populate_video_urls()
        return pl.video_urls
    else:
        return [url_entry_text]


def paste_button_callback():
    url = get_clipboard_contents().strip()
    url_entry.delete(0, END)
    url_entry.insert(0, url)


def video_selection_listbox_callback(x):
    print(x)


def browse_button_callback():
    s = filedialog.askdirectory().strip()
    if s:
        browse_entry.delete(0, END)
        browse_entry.insert(0, s)


def download_all_button_callback(video_selection_listbox):
    items = map(int, video_selection_listbox.curselection())
    print(video_selection_listbox)
    print([str(item) for item in video_selection_listbox])


def download_selected_button_callback():
    pass


def cancel_all_button_callback():
    pass


def cancel_selected_button_callback():
    pass


def go_button_callback(yt_data):
    def f(url):
        yt = YouTube(url)
        title = yt.player_config_args['title']
        return (title, yt)
    url_entry_text = url_entry.get().strip()
    video_selection_listbox.delete(0, END)
    urls = get_urls_from_entry_text(url_entry_text)
    jobs = [gevent.spawn(f, url) for url in urls]
    gevent.joinall(jobs)
    # gevent.wait(jobs)
    for job in jobs:
        title, yt = job.value
        yt_data[title] = yt
        video_selection_listbox.insert(END, title)
        root.update()


if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_all()

    yt_data = {}
    root = Tk()
    root.title('dowload from youtube')
    main_frame = ttk.Frame(root)

    Label(root, text='youtube video url (may link to a single video or a playlist)').pack(
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
    go_button = Button(url_entry_frame, text='go',
                       command=lambda: go_button_callback(yt_data))
    go_button.pack(side=LEFT)
    url_entry_frame.pack(anchor='w', fill=X)

    Label(root, text='videos at url (ctrl + click to select individual videos)').pack(anchor='w')
    #  _______________________
    # | Title1                |
    # | Title2                |
    # | Title3                |
    # | Title4                |
    # |_______________________|
    video_selection_listbox = Listbox(root, selectmode=EXTENDED)
    video_selection_listbox.configure(exportselection=False)
    video_selection_listbox.bind(
        '<<ListboxSelect>>', video_selection_listbox_callback)
    video_selection_listbox.pack(fill=BOTH, expand=1)

    Label(root, text='set destination folder for downloaded videos').pack(anchor='w')
    #  ________   _______________________
    # | browse | | C:/Videos/            |
    # |________| |_______________________|
    browse_frame = Frame(root)
    browse_button = Button(browse_frame, text='browse',
                           command=browse_button_callback)
    browse_button.pack(side=LEFT)
    browse_entry = Entry(browse_frame)
    browse_entry.pack(side=LEFT, fill=BOTH, expand=1)
    browse_frame.pack(anchor='w', fill=X)

    Label(root, text='will not overwrite files with the same name').pack(anchor='w')
    #  ______________    ___________________
    # | download all |  | download selected |
    # |______________|  |___________________|
    download_frame = Frame(root)
    download_all_button = Button(download_frame, text='download all',
                                 command=lambda: download_all_button_callback(video_selection_listbox))
    download_all_button.pack(side=LEFT)
    download_selected_button = Button(download_frame, text='download selected',
                                      command=download_selected_button_callback)
    download_selected_button.pack(side=LEFT)
    download_frame.pack(anchor='w', fill=X)

    Label(root, text='video queue (downloads in progress)').pack(anchor='w')
    #  _______________________
    # |                       |
    # |                       |
    # |                       |
    # |                       |
    # |_______________________|
    video_queue_listbox = Listbox(root, selectmode=EXTENDED)
    video_queue_listbox.pack(fill=BOTH, expand=1)

    Label(text='cancel video download').pack(anchor='w')
    #  ____________    _________________
    # | cancel all |  | cancel selected |
    # |____________|  |_________________|
    cancel_frame = Frame(root)
    cancel_all_button = Button(cancel_frame, text='cancel all',
                               command=cancel_all_button_callback)
    cancel_all_button.pack(side=LEFT)
    cancel_selected_button = Button(cancel_frame, text='cancel selected',
                                    command=cancel_selected_button_callback)
    cancel_selected_button.pack(side=LEFT)
    cancel_frame.pack(anchor='w', fill=X)

    root.mainloop()
