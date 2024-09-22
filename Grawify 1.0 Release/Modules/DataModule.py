import json


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


def save_data() -> None:
    with open('Settings.json', 'w') as file:
        json.dump(settings, file, indent=4)

    with open('Stats.json', 'w') as file:
        json.dump(stats, file, indent=4)


def get_stats() -> {str: int}:
    return stats


def change_stats(child: str, value: int) -> None:
    global stats

    stats[child] = value


def get_settings() -> {str: str | int}:
    return settings


def change_settings(child: str, value: str | int) -> None:
    global settings

    settings[child] = value


def get_state() -> {str: str | bool}:
    return state


def change_state(child: str, value: str | bool) -> None:
    global state

    state[child] = value
