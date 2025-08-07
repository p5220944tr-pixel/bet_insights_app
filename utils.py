import requests
from datetime import datetime, timedelta

BASE_URL = "https://v3.football.api-sports.io"

def get_matches_next_24h(api_key):
    """
    Επιστρέφει ματς για σήμερα και αύριο (ώρα Ελλάδας).
    """
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    headers = {"x-apisports-key": api_key}

    all_matches = []

    for date in [today, tomorrow]:
        params = {
            "date": date.strftime("%Y-%m-%d"),
            "timezone": "Europe/Athens"
        }

        response = requests.get(f"{BASE_URL}/fixtures", headers=headers, params=params)
        print(f"Ζητάμε αγώνες για: {date}")
        print("API response JSON:", response.json())

        if response.status_code != 200:
            continue

        fixtures = response.json().get("response", [])
        for fixture in fixtures:
            match_time = fixture["fixture"]["date"][11:16]
            all_matches.append({
                "id": fixture["fixture"]["id"],
                "date": fixture["fixture"]["date"],
                "time": match_time,
                "league": fixture["league"]["name"],
                "teams": {
                    "home": fixture["teams"]["home"]["name"],
                    "away": fixture["teams"]["away"]["name"],
                }
            })

    return all_matches

def analyze_match(api_key, match_id):
    """
    Κάνει απλή ανάλυση για το ματς με το match_id (προβλέψεις από API).
    """
    headers = {"x-apisports-key": api_key}
    response = requests.get(f"{BASE_URL}/predictions", headers=headers, params={"fixture": match_id})
    if response.status_code != 200:
        return "Δεν είναι δυνατή η ανάλυση."
    
    data = response.json().get("response", [])
    if not data:
        return "Δεν βρέθηκαν προβλέψεις."

    prediction = data[0]["predictions"]["advice"]
    return prediction
