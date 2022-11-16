from pytube import YouTube
from simple_term_menu import TerminalMenu
from progress.spinner import Spinner
from pyfiglet import Figlet

# TODO: think of smarter way to show progress - maybe it is possible to use another bar
# TODO: use command line arguments. Eg. File with links to multiple videos. Handle downloading a whole playlist. Set download location.
# TODO: is it possible to merge DASH video and audio streams in Python? If so - implement :)

def resolution_menu(streams):
    options = [stream.resolution for stream in streams]
    terminal_menu = TerminalMenu(options, title="Choose resolution")
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")
    return options[menu_entry_index], menu_entry_index

def main():

    f = Figlet(font='slant')
    print(f.renderText('YT Downloader'))

    bar = Spinner('KB left... ')
    def progress_callback(*args):
        bar.next()
        bar.message = "KB left: " + str(args[2]/1000) + " "

    def complete_callback(*args):
        bar.finish()
        print("Download complete")

    video_url = input('\nEnter YouTube video URL: ')

    yt = YouTube(video_url, on_progress_callback=progress_callback, on_complete_callback=complete_callback)

    print("\nQuerying for available resolution options...")

    streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    chosen_res = resolution_menu(streams)
    streams[chosen_res[1]].download()

if __name__ == '__main__':
    main()
