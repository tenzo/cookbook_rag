from pathlib import Path


def get_root() -> Path:
    return Path(__file__).parent.parent.parent