import requests
import math

STAT_ORDER = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
MAX_TOTAL_POINTS = 66
MAX_PER_STAT = 32


def fetch_pokepaste(url):
    if not url.endswith("/raw"):
        url = url.rstrip("/") + "/raw"
    r = requests.get(url)
    r.raise_for_status()
    return r.text


def parse_evs(line):
    if not line.startswith("EVs:"):
        return None

    evs = {stat: 0 for stat in STAT_ORDER}
    parts = line.replace("EVs:", "").strip().split("/")

    for part in parts:
        val, stat = part.strip().split()
        evs[stat] = int(val)

    return evs


def evs_to_points(evs):
    points = {}
    total = 0

    for stat in STAT_ORDER:
        p = evs.get(stat, 0) // 4
        p = min(p, MAX_PER_STAT)
        points[stat] = p
        total += p

    if total > MAX_TOTAL_POINTS:
        scale = MAX_TOTAL_POINTS / total
        for stat in points:
            points[stat] = math.floor(points[stat] * scale)

    return points


def points_to_evs(points):
    return {stat: points.get(stat, 0) * 4 for stat in STAT_ORDER}


def format_evs(evs):
    parts = []
    for stat in STAT_ORDER:
        val = evs.get(stat, 0)
        if val > 0:
            parts.append(f"{val} {stat}")
    return "EVs: " + " / ".join(parts)


def convert_line(line):
    evs = parse_evs(line)
    if not evs:
        return line

    points = evs_to_points(evs)
    new_evs = points_to_evs(points)

    return format_evs(new_evs)


def process_team(text):
    return "\n".join(convert_line(line) for line in text.splitlines())