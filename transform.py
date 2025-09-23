import json
from datetime import datetime, timezone

def transform(data):
    transformed = []
    for match in data:

        # Convert "Sunday, 8 September 2024" to datetime (YYYY-MM-DD)
        parsed_date = datetime.strptime(match["date"], "%A, %d %B %Y").date()

        transformed.append({
            "gameweek": match["gameweek"],
            "date": parsed_date.isoformat(), # transformed to "YYYY-MM-DD"
            "home_team": match["home_team"].title(),
            "away_team": match["away_team"].title(),
            "home_score": int(match["home_score"]),
            "away_score": int(match["away_score"]),
            "scraped_at": datetime.now(timezone.utc).isoformat()
        })
    return transformed

if __name__ == "__main__":
    with open("results.json", "r") as f:
        raw_data = json.load(f)

    cleaned = transform(raw_data)

    with open("transformed_matches.json", "w") as f:
        json.dump(cleaned, f, indent=2)

    print("✅ Transformed data saved to transformed_matches.json")
