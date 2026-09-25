"""Select the score and upcoming-fixture windows shown on the public site."""
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
import os


PARIS = ZoneInfo("Europe/Paris")
SATURDAY_SWITCH = time(9, 0)


def paris_now():
    """Return Paris time, with an optional deterministic override for tests."""
    raw = os.environ.get("PHB_NOW", "").strip()
    if not raw:
        return datetime.now(PARIS)
    value = datetime.fromisoformat(raw)
    if value.tzinfo is None:
        value = value.replace(tzinfo=PARIS)
    return value.astimezone(PARIS)


def score_week_bounds(now=None):
    """Return the displayed score week and whether Saturday's switch is active."""
    now = (now or paris_now()).astimezone(PARIS)
    current_monday = now.date() - timedelta(days=now.weekday())
    switch_at = datetime.combine(
        current_monday + timedelta(days=5), SATURDAY_SWITCH, tzinfo=PARIS
    )
    active = now >= switch_at
    start = current_monday if active else current_monday - timedelta(days=7)
    return start, start + timedelta(days=7), active


def select_score_and_upcoming(matches, now=None):
    """Move the current weekend to scores from Saturday 09:00 Paris time."""
    now = (now or paris_now()).astimezone(PARIS)
    score_start, score_end, switch_active = score_week_bounds(now)
    scores = []
    upcoming = []
    for match in matches:
        kick_off = datetime.fromisoformat(match["date"]).astimezone(PARIS)
        if score_start <= kick_off.date() < score_end:
            scores.append(match)
            continue
        if match["played"]:
            continue
        if switch_active:
            if kick_off.date() >= score_end:
                upcoming.append(match)
        elif kick_off >= now:
            upcoming.append(match)
    scores.sort(key=lambda match: match["date"], reverse=True)
    upcoming.sort(key=lambda match: match["date"])
    return scores, upcoming, switch_active


def first_calendar_week(matches):
    """Keep every fixture in the first available Monday-to-Sunday week."""
    if not matches:
        return []
    first_day = datetime.fromisoformat(matches[0]["date"]).astimezone(PARIS).date()
    next_monday = first_day + timedelta(days=7 - first_day.weekday())
    return [
        match for match in matches
        if datetime.fromisoformat(match["date"]).astimezone(PARIS).date() < next_monday
    ]
