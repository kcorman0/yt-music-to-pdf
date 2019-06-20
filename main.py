import vlc
import pafy
import os
import time

# Constants (might need to change)
url = "https://www.youtube.com/watch?v=RuHb09rQAxQ"
directory = "temp/"

# Make temporary directory for screenshots
try:
    os.mkdir("temp")
except:
    pass


url = url.split("=")[1]

vid = pafy.new(url)
print("Scanning video:", vid.title, "\n")

dl = vid.getbest()
# print(dl.resolution, dl.extension)
# print(dl.url)

Instance = vlc.Instance()
Player = Instance.media_player_new()
Events = Player.event_manager()
Media = Instance.media_new(dl.url)

Media.get_mrl()
Player.set_media(Media)
Player.audio_set_volume(0)

Player.play()
time.sleep(5)
jump = 3000
Player.set_time(0)
Player.pause()
t = Player.get_time()
while Player.get_state() != 'Finished':
    t += jump
    Player.set_time(t)
    Player.play()
    if Player.get_state() == 'Playing':
        Player.pause()
    time.sleep(1)
    print("Screenshot at time:", t / 1000)
    Player.video_take_snapshot(0, directory + str(t) + ".png", 0, 0)