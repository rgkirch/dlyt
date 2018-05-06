from pytube import YouTube
import win32clipboard
from tkinter import *
from tkinter import ttk


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


def get_clipboard():
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


def paste_from_clipboard_to_url_entry():
    url = get_clipboard().strip()
    url_entry.delete(0, END)
    url_entry.insert(0, url)


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


def paste_button_callback():
    pass


def video_selection_listbox_callback(x):
    print(x)


def browse_button_callback():
    pass


def download_all_button_callback():
    pass


def download_selected_button_callback():
    pass


def cancel_all_button_callback():
    pass


def cancel_selected_button_callback():
    pass


if __name__ == '__main__':
    root = Tk()
    root.title('dowload from youtube')
    main_frame = ttk.Frame(root)

    Label(root, text='youtube video url (may link to a single video or a playlist)').pack()
    #  _______   ________________________________
    # | paste | | 'https://youtu.be/dQw4w9WgXcQ' |
    # |_______| |________________________________|
    url_entry_frame = Frame(root)
    paste_button = Button(url_entry_frame, text='paste button',
                          command=paste_button_callback).pack(side=LEFT)
    url_entry = Entry(url_entry_frame).pack(side=LEFT)
    url_entry_frame.pack()

    Label(root, text='videos at url (ctrl + click to select individual videos)').pack()
    #  _______________________
    # | Title1                |
    # | Title2                |
    # | Title3                |
    # | Title4                |
    # |_______________________|
    video_selection_listbox = Listbox(root)
    video_selection_listbox.configure(exportselection=False)
    video_selection_listbox.bind(
        '<<ListboxSelect>>', video_selection_listbox_callback)
    video_selection_listbox.pack()

    Label(root, text='set destination folder for downloaded videos').pack()
    #  ________   _______________________
    # | browse | | C:/Videos/            |
    # |________| |_______________________|
    browse_frame = Frame(root)
    browse_button = Button(browse_frame, text='browse',
                           command=browse_button_callback)
    browse_button.pack(side=LEFT)
    browse_entry = Entry(browse_frame)
    browse_entry.pack(side=LEFT)
    browse_frame.pack()

    Label(root, text='will not overwrite files with the same name').pack()
    #  ______________    ___________________
    # | download all |  | download selected |
    # |______________|  |___________________|
    download_frame = Frame(root)
    download_all_button = Button(download_frame, text='download all',
                                 command=download_all_button_callback)
    download_all_button.pack(side=LEFT)
    download_selected_button = Button(download_frame, text='download selected',
                                      command=download_selected_button_callback)
    download_selected_button.pack(side=LEFT)
    download_frame.pack()

    Label(root, text='video queue (downloads in progress)').pack()
    #  _______________________
    # |                       |
    # |                       |
    # |                       |
    # |                       |
    # |_______________________|
    video_queue_listbox = Listbox(root)
    video_queue_listbox.pack()

    Label(text='cancel video download').pack()
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
    cancel_frame.pack()

    root.mainloop()
