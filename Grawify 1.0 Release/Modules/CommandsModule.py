import os
import platform

import Modules.DataModule as DataModule
import Modules.UtilsModule as UtilsModule


def clear_screen() -> None:
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def change_mode(mode: str) -> None:
    settings = DataModule.get_settings()

    modes = ["InOrder", "Random", "AdvancedRandom"]

    if mode in modes:
        settings["currently_selected_mode"] = mode


def skip_song() -> None:
    state = DataModule.get_state()

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
    settings = DataModule.get_settings()

    if not str.isdigit(user_input):
        return

    if int(user_input) >= 0:
        settings["delay_between_songs"] = int(user_input)


def pause_song(pause: bool) -> None:
    DataModule.change_state("paused", pause)


def change_volume(number: int) -> None:
    if 0 <= number <= 100:
        DataModule.change_settings("volume", number)


def show_stats() -> None:
    stats = DataModule.get_stats()

    string = UtilsModule.convert_seconds_into_hours_minutes_and_seconds(stats["time_spent_listening"])
    print(f"Your time spent listening to music is: {string}")
    print(f"You have listened to: {stats["songs_listened_to"]} songs")


def show_settings() -> None:
    settings = DataModule.get_settings()

    print(f"Currently selected mode: {settings["currently_selected_mode"]}")
    print(f"Delay between songs: {settings["delay_between_songs"]}")
    print(f"Song volume: {settings["volume"]}%")


def display_song_playing() -> None:
    settings = DataModule.get_settings()
    state = DataModule.get_state()

    clear_screen()

    print(f"Currently selected mode: {settings["currently_selected_mode"]}")
    print(f"Currently playing song: {state["current_song_name"]}")
