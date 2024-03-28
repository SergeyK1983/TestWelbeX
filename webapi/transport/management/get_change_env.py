import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
path_file = os.path.join(BASE_DIR, '.env')

GET_INIT = "GET_INIT=do_it"
NEW_GET_INIT = "GET_INIT=do_not"


def change_env():
    with open(path_file, mode='r+', encoding='utf8') as env:
        value = env.readlines()
        if GET_INIT in value:
            value.remove(GET_INIT)

    try:
        os.rename(path_file, os.path.join(BASE_DIR, "old.old"))
    except (FileExistsError, OSError):
        pass

    with open(path_file, mode='w', encoding='utf8') as env:
        env.writelines(value)
        env.write(NEW_GET_INIT)


change_env()
