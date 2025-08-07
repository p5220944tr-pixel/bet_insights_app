import requests
from datetime import datetime, timedelta

BASE_URL = "https://v3.football.api-sports.io"

def get_matches_next_hours(api_key, hours=12):
    now = datetime.utcnow()
    end_time = now + timedelta(hours=hours)
    date_from = now.strftime("%Y-%m-%dT%H:%M:%S")
    date_to = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    headers = {"x-apisports-key": api_key}
    params = {"from": date_from, "to": date_to, "timezone": "Europe/Athens"}

    response = requests.get(f"{BASE_URL}/fixtures", headers=headers, params=params)
    if response.status_code != 200:
        return []

    fixtures = response.json().get("response", [])
    matches = []
    for fixture in fixtures:
        matches.append({
            "id": fixture["fixture"]["id"],
            "date": fixture["fixture"]["date"],
            "time": fixture["fixture"]["date"][11:16],
            "league": fixture["league"]["name"],
            "teams": {
                "home": fixture["teams"]["home"]["name"],
                "away": fixture["teams"]["away"]["name"],
            }
        })
    return matches

def analyze_match(api_key, match_id):
    # ΠΡΟΣΟΧΗ: Αυτή είναι μια απλή ψευδο-ανάλυση.
    # Εδώ μπορείς να προσθέσεις advanced στατιστικά, φόρμα, odds κ.λπ.
    headers = {"x-apisports-key": api_key}
    response = requests.get(f"{BASE_URL}/predictions", headers=headers, params={"fixture": match_id})
    if response.status_code != 200:
        return "Δεν είναι δυνατή η ανάλυση."
    
    data = response.json().get("response", [])
    if not data:
        return "Δεν βρέθηκαν προβλέψεις."

    prediction = data[0]["predictions"]["advice"]
    return prediction
