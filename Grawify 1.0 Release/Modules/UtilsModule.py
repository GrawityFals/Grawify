from threading import Thread

import Modules.DataModule as DataModule
import Modules.PlaySongsModule as PlaySongsModule
import Modules.CommandsModule as CommandsModule


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


def check_for_mode() -> None:
    settings = DataModule.get_settings()

    mode = settings["currently_selected_mode"]
    thread = Thread(target=PlaySongsModule.play_random_song_you_have_not_played)

    if mode == "Random":
        thread = Thread(target=PlaySongsModule.play_random_song)
    elif mode == "InOrder":
        thread = Thread(target=PlaySongsModule.play_songs_in_order)
    elif mode == "AdvancedRandom":
        thread = Thread(target=PlaySongsModule.play_random_song_you_have_not_played)

    thread.start()


def handle_users_input() -> None:
    inputs = {
        "change mode:": lambda: CommandsModule.change_mode(input_part_2),
        "change delay:": lambda: CommandsModule.change_delay_between_songs(input_part_2),
        "change volume:": lambda: CommandsModule.change_volume(int(input_part_2)),
        "pause": lambda: CommandsModule.pause_song(True),
        "resume": lambda: CommandsModule.pause_song(False),
        "skip": lambda: CommandsModule.skip_song(),
        "stats": lambda: CommandsModule.show_stats(),
        "settings": lambda: CommandsModule.show_settings(),
        "cls": lambda: CommandsModule.display_song_playing(),
        "help": lambda: CommandsModule.help_command(),
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

    DataModule.save_data()

    handle_users_input()
