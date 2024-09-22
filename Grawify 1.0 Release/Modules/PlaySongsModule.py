import os
import time
import random
from mutagen.mp3 import MP3
from audioplayer import AudioPlayer

import Modules.DataModule as DataModule
import Modules.CommandsModule as CommandsModule
import main as main

songs_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Songs'))


def get_songs_list():
    return [f for f in os.listdir(songs_folder) if f.endswith(".mp3")]


def get_song_name(index) -> None:
    state = DataModule.get_state()

    songs = get_songs_list()
    file_path = os.path.join(songs_folder, songs[index])
    song_name = os.path.basename(file_path)

    state["current_song_name"] = song_name


def play_song(index: int) -> bool:
    settings = DataModule.get_settings()
    state = DataModule.get_state()
    stats = DataModule.get_stats()

    local_settings = settings.copy()

    songs = get_songs_list()
    file_path = os.path.join(songs_folder, songs[index])

    audio_player = AudioPlayer(file_path)
    audio_player.play(block=False)

    audio = MP3(file_path)
    length = audio.info.length

    for i in range(int(length)*10):
        if local_settings["currently_selected_mode"] != settings["currently_selected_mode"]:
            AudioPlayer.stop(audio_player)
            return False
        if state["skip_song"]:
            state["skip_song"] = False
            AudioPlayer.stop(audio_player)
            return True
        if state["paused"]:
            audio_player.pause()

            while state["paused"]:
                time.sleep(0.1)

            audio_player.resume()

        audio_player.volume = settings["volume"]

        time.sleep(0.1)

    stats["songs_listened_to"] += 1

    return True


def play_songs_in_order() -> None:
    settings = DataModule.get_settings()

    folder_length = len(os.listdir(songs_folder))

    for i in range(folder_length):
        get_song_name(i)
        CommandsModule.display_song_playing()

        output = play_song(i)
        if not output:
            return main.main()

        time.sleep(settings["delay_between_songs"])

    play_songs_in_order()


def play_random_song() -> None:
    while True:
        settings = DataModule.get_settings()

        folder_length = len(os.listdir(songs_folder))

        random_song = random.randint(0, folder_length-1)

        get_song_name(random_song)
        CommandsModule.display_song_playing()

        output = play_song(random_song)
        if not output:
            return main.main()

        time.sleep(settings["delay_between_songs"])


def play_random_song_you_have_not_played() -> None:
    print(os.path.abspath(songs_folder))
    folder_length = len(os.listdir(songs_folder))

    songs_played = list(range(folder_length))

    while songs_played:
        settings = DataModule.get_settings()

        random_index = random.randint(0, len(songs_played) - 1)

        song_index = songs_played[random_index]

        get_song_name(song_index)
        CommandsModule.display_song_playing()

        output = play_song(song_index)
        if not output:
            return main.main()

        songs_played.pop(random_index)

        time.sleep(settings["delay_between_songs"])

    play_random_song_you_have_not_played()
