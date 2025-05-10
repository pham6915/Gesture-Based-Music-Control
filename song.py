import vlc
import time
import msvcrt
import os

# Load song
song_path = r"D:\Perfect Night- Le Sserafim\Perfect Night- Le Sserafim.mp3"
player = vlc.MediaPlayer(song_path)
player.audio_set_volume(70)
player.play()

print("🎵 Playing... (Press 'q' to stop)")

while True:
    state = player.get_state()

    if state in [vlc.State.Ended, vlc.State.Stopped, vlc.State.Error]:
        print("✅ Song finished.")
        break

    # Stop if user presses 'q'
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b'q':
            print("⏹️ Manually stopped.")
            break

    # Read speed from file
    if os.path.exists("speed.txt"):
        with open("speed.txt", "r") as f:
            try:
                speed = float(f.read().strip())
                player.set_rate(speed)
            except ValueError:
                pass  # ignore invalid input

    time.sleep(0.1)

player.stop()

