import json
from pathlib import Path

import numpy as np


HSV_STORE_PATH = Path(__file__).with_name("hsv_presets.json")


def _read_store():
    if not HSV_STORE_PATH.exists():
        return {}

    try:
        with HSV_STORE_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    except (json.JSONDecodeError, OSError):
        pass

    return {}


def _write_store(data):
    with HSV_STORE_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _validate_triplet(values, max_values):
    if not isinstance(values, list) or len(values) != 3:
        return None

    parsed = []
    for idx, item in enumerate(values):
        if not isinstance(item, int):
            return None
        if item < 0 or item > max_values[idx]:
            return None
        parsed.append(item)

    return parsed


def load_hsv_range(profile_name, default_lower, default_upper):
    data = _read_store()
    profile = data.get(profile_name, {})

    lower = _validate_triplet(profile.get("lower"), [179, 255, 255])
    upper = _validate_triplet(profile.get("upper"), [179, 255, 255])
    clicked = _validate_triplet(profile.get("clicked_hsv"), [179, 255, 255])

    if lower is None or upper is None:
        return default_lower.copy(), default_upper.copy(), None

    clicked_hsv = tuple(clicked) if clicked is not None else None
    return np.array(lower, dtype=np.uint8), np.array(upper, dtype=np.uint8), clicked_hsv


def save_hsv_range(profile_name, lower_hsv, upper_hsv, clicked_hsv=None):
    data = _read_store()

    profile_data = {
        "lower": [int(v) for v in lower_hsv],
        "upper": [int(v) for v in upper_hsv],
    }

    if clicked_hsv is not None:
        profile_data["clicked_hsv"] = [int(v) for v in clicked_hsv]

    data[profile_name] = profile_data
    _write_store(data)
