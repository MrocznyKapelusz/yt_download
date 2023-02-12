from pytube import YouTube, Playlist
from typing import List
from simple_term_menu import TerminalMenu
from progress.spinner import Spinner
from pyfiglet import Figlet
import os

# TODO: is it possible to merge DASH video and audio streams in Python? If so - implement :)

f = Figlet(font="slant")

bar = Spinner("KB left... ")


def progress_callback(*args):
    bar.next()
    bar.message = "KB left: " + str(args[2] / 1000) + " "


def complete_callback(*args):
    bar.finish()
    print("Download complete")


def option_menu():
    options = ["Video download", "Playlist download"]
    terminal_menu = TerminalMenu(options, title="Choose optio")
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")
    return options[menu_entry_index]


def download_video(video: YouTube, path=".", prefix=None):
    print(f"Downloading {video.title}... into directory {path}")
    stream = (
        video.streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()[0]
    )
    filename = stream.default_filename.replace(" ", "_").replace("-", "")

    stream.download(output_path=path, filename=filename, filename_prefix=prefix)


def download_playlist(playlist: Playlist):
    print(f"Downloading {playlist.title}...")
    # TODO: use getcwd to navigate, download somwhere else
    try:
        path = f"./{playlist.title.replace(' ','_')}"
        os.mkdir(path)
    except FileExistsError:
        pass

    for num, video in enumerate(playlist.videos):
        video.register_on_progress_callback(progress_callback)
        video.register_on_complete_callback(complete_callback)
        download_video(video, path, prefix=f"{num+1:02}_")


def main():
    print(f.renderText("YT Downloader"))
    chosen_opt = option_menu()
    if chosen_opt == "Video download":
        video_url = input("\nEnter YouTube video URL: ")
        video = YouTube(
            video_url,
            on_progress_callback=progress_callback,
            on_complete_callback=complete_callback,
        )
        download_video(video)

    elif chosen_opt == "Playlist download":
        playlist_url = input("\nEnter YouTube playlist URL: ")
        playlist = Playlist(playlist_url)
        download_playlist(playlist)

    else:
        raise NameError(f"Chosen option '{chosen_opt}' not available")


if __name__ == "__main__":
    main()
