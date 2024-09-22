import time
from threading import Thread

import Modules.DataModule as DataModule
import Modules.UtilsModule as UtilsModule


def playtime() -> None:
    stats = DataModule.get_stats()

    while True:
        time.sleep(1)

        stats["time_spent_listening"] += 1


def main() -> None:
    DataModule.load_data()

    playtime_thread = Thread(target=playtime)
    playtime_thread.start()

    UtilsModule.check_for_mode()

    UtilsModule.handle_users_input()

    input()


if __name__ == '__main__':
    main()
