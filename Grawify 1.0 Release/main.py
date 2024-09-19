import os
import platform
import random
import time
import json
from threading import Thread

from mutagen.mp3 import MP3
from audioplayer import AudioPlayer


audio_player: AudioPlayer | None = None
songs_folder = os.path.join(os.path.dirname(__file__), "Songs")

settings = {
    "currently_selected_mode": "InOrder",
    "delay_between_songs": 1,
    "volume": 100
}

stats = {
    "time_spent_listening": 0,
    "songs_listened_to": 0,
}

state = {
    "current_song_name": "",
    "skip_song": False,
    "paused": False
}


def save_data() -> None:
    with open('Settings.json', 'w') as file:
        json.dump(settings, file, indent=4)

    with open('Stats.json', 'w') as file:
        json.dump(stats, file, indent=4)


def load_data() -> None:
    global settings
    global stats

    with open('Settings.json', 'r') as file:
        data = json.load(file)

        if data:
            settings = data

    with open('Stats.json', 'r') as file:
        data = json.load(file)

        if data:
            stats = data


def convert_seconds_into_hours_minutes_and_seconds(seconds: int) -> str:
    if seconds >= 3600:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        string = f"{h} hours, {m} minutes and {s} seconds"
        return string
    else:
        m = seconds // 60
        s = seconds % 60

        string = f"{m} minutes and {s} seconds"
        return string


def playtime() -> None:
    global stats

    while True:
        time.sleep(1)

        stats["time_spent_listening"] += 1


def get_songs_list():
    return [f for f in os.listdir(songs_folder) if f.endswith(".mp3")]


def play_song(index: int) -> bool:
    global audio_player
    global settings
    global stats
    global state

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
    global settings

    for i in range(len(songs_folder)):
        get_song_name(i)
        display_song_playing()

        output = play_song(i)
        if not output:
            return main()

        time.sleep(settings["delay_between_songs"])

    play_songs_in_order()


def play_random_song() -> None:
    global settings

    while True:
        random_song = random.randint(0, len(songs_folder)-1)

        get_song_name(random_song)
        display_song_playing()

        output = play_song(random_song)
        if not output:
            return main()

        time.sleep(settings["delay_between_songs"])


def play_random_song_you_have_not_played() -> None:
    global settings

    songs_played = list(range(len(songs_folder)))

    while songs_played:
        random_index = random.randint(0, len(songs_played) - 1)
        song_index = songs_played[random_index]

        get_song_name(song_index)
        display_song_playing()

        output = play_song(song_index)
        if not output:
            return main()

        songs_played.pop(random_index)

        time.sleep(settings["delay_between_songs"])


def clear_screen() -> None:
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def get_song_name(index) -> None:
    global state

    songs = get_songs_list()
    file_path = os.path.join(songs_folder, songs[index])
    song_name = os.path.basename(file_path)

    state["current_song_name"] = song_name


def display_song_playing() -> None:
    clear_screen()

    global settings
    global state

    print(f"Currently selected mode: {settings["currently_selected_mode"]}")
    print(f"Currently playing song: {state["current_song_name"]}")


def change_mode(mode: str) -> None:
    global settings

    modes = ["InOrder", "Random", "AdvancedRandom"]

    if mode in modes:
        settings["currently_selected_mode"] = mode


def skip_song() -> None:
    global state

    state["skip_song"] = True


def help_command() -> None:
    print("-"*30 + "Commands" + "-"*30)
    print("skip -- skips a song")
    print("change mode: [ModeName] -- changes the mode")
    print("change delay: [Delay] -- changes delay between songs (whole numbers only)")
    print("change volume: [volume] -- changes volume of a song (numbers between 0 and 100 only)")
    print("stats -- prints your stats")
    print("cls -- clears your screen")


def change_delay_between_songs(user_input) -> None:
    global settings

    if not str.isdigit(user_input):
        return

    if int(user_input) >= 0:
        settings["delay_between_songs"] = int(user_input)


def pause_song(pause: bool) -> None:
    global state

    state["paused"] = pause


def change_volume(number: int) -> None:
    global settings

    if 0 <= number <= 100:
        settings["volume"] = number


def show_stats() -> None:
    global stats

    string = convert_seconds_into_hours_minutes_and_seconds(stats["time_spent_listening"])
    print(f"Your time spent listening to music is: {string}")
    print(f"You have listened to: {stats["songs_listened_to"]} songs")


def show_settings() -> None:
    global settings

    print(f"Currently selected mode: {settings["currently_selected_mode"]}")
    print(f"Delay between songs: {settings["delay_between_songs"]}")
    print(f"Song volume: {settings["volume"]}%")


def check_for_mode() -> None:
    global settings
    mode = settings["currently_selected_mode"]
    thread = Thread(target=play_random_song_you_have_not_played)

    if mode == "Random":
        thread = Thread(target=play_random_song)
    elif mode == "InOrder":
        thread = Thread(target=play_songs_in_order)
    elif mode == "AdvancedRandom":
        thread = Thread(target=play_random_song_you_have_not_played)

    thread.start()


def handle_users_input() -> None:
    inputs = {
        "change mode:": lambda: change_mode(input_part_2),
        "change delay:": lambda: change_delay_between_songs(input_part_2),
        "change volume:": lambda: change_volume(int(input_part_2)),
        "pause": lambda: pause_song(True),
        "resume": lambda: pause_song(False),
        "skip": lambda: skip_song(),
        "stats": lambda: show_stats(),
        "settings": lambda: show_settings(),
        "cls": lambda: display_song_playing(),
        "help": lambda: help_command(),
    }

    users_input = input().split()

    input_part_1 = ""
    input_part_2 = ""

    if len(users_input) > 1:
        input_part_1 = users_input[0]
        input_part_2 = users_input[-1]

        for i in range(len(users_input)-2):
            input_part_1 = input_part_1 + " " + users_input[i+1]

    elif len(users_input) == 1:
        input_part_1 = users_input[0]

    if input_part_1 not in inputs:
        handle_users_input()

    inputs.get(input_part_1, lambda: print("Invalid option. Please try again."))()

    save_data()

    handle_users_input()


def main() -> None:
    load_data()

    playtime_thread = Thread(target=playtime)
    playtime_thread.start()

    check_for_mode()

    handle_users_input()


if __name__ == '__main__':
    main()
