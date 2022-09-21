from pytube import YouTube
import pytube
import os

def main():
    video_url = input('Enter YouTube video URL: ')

    if os.name == 'nt':
        path = os.getcwd() + '\\'
    else:
        path = os.getcwd() + '/'

    name = pytube.extract.video_id(video_url)

    YouTube(video_url).streams.first().download(filename=name)
    yt = YouTube(video_url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

if __name__ == '__main__':
    main()