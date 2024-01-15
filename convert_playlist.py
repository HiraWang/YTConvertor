import os
import ssl
import shutil
from pytube import Playlist, YouTube

ssl._create_default_https_context = ssl._create_stdlib_context

root = 'C:/Users/cy.wang/MET/Alan/Music'
playlist = 'https://youtube.com/playlist?list=PLFdgdNMl_r3Ks7Au7SFJiRaMXwWrdikxR&si=ejV4p3yJ2QZpbaW4'
shutil.rmtree(root, ignore_errors=True)
os.mkdir(root)
os.chdir(root)
playlist = Playlist(playlist)

print('download...')
cnt = 0
tot_cnt = len(playlist.video_urls)
for i in playlist.video_urls:
    yt = YouTube(i)
    print(i, cnt, tot_cnt, yt.author, yt.title)
    fn = str(cnt) + ' ' + str(yt.author) + ' ' + str(yt.title) + '.mp3'
    yt.streams.filter().get_audio_only().download(filename=fn)
    cnt += 1
print('ok!')
