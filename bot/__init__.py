import logging
import traceback
from os import listdir, walk
from pathlib import Path
from importlib import import_module

__version__ = "develop"

# Use importlib instead of __import__ for better readability and compatibility with Python 3.
import_module("bot.config.logger")
import_module("bot.filters")
root, folders, files = next(walk("bot", topdown=True))

def force_import(*args):
    for module in args:
        if isinstance(module, tuple):
            force_import(*module)
            continue

        try:
            import_module(module.replace("\\", "."))
        except Exception as e:
            trace = traceback.format_exc()
            logging.error(f"{module}: {trace.splitlines()[-2]}")
            print(trace)
            raise e  # re-raise the exception

def prepare_paths(modules, is_folders=False, folder_name=None, prefix=Path("bot")):
    if is_folders:
        allowed_folders = filter(lambda x: x not in ("__pycache__", "config"), modules)

        return tuple(
            map(
                lambda folder: prepare_paths(listdir(prefix / folder), folder_name=folder),
                allowed_folders
            )
        )

    else:
        allowed_modules = filter(
            lambda file: file.endswith(".py") and not file.startswith("__") and file[:-3] not in ("ban", "ocr"),
            modules
        )

        return tuple(
            map(
            lambda x: str(prefix / Path(folder_name) / Path(x[:-3]) if folder_name else prefix / Path(x[:-3])).replace("/", "."),
                allowed_modules
            )
        )

force_import(*prepare_paths(files))
force_import(*prepare_paths(folders, is_folders=True))
force_import("bot.triggers.ban")
force_import("bot.chat_misc.ocr")