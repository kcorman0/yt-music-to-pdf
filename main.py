import vlc
import pafy

url = "https://www.youtube.com/watch?v=RuHb09rQAxQ"
url = url.split("=")[1]
print(url)
directory = ""

vid = pafy.new(url)
print("Scanning video:", vid.title, "\n")

dl = vid.getbest()
print(dl.resolution, dl.extension)
print(dl.url)

Instance = vlc.Instance()
Player = Instance.media_player_new()
Media = Instance.media_new(dl.url)

Media.get_mrl()
Player.set_media(Media)

Player.play()

while True:
    pass

# time.sleep(5)
# player.pause()
