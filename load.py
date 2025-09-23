import json
import psycopg2
from datetime import datetime

def load(data):
    conn = psycopg2.connect(
        dbname="etl_db",
        user="etl_user",
        password="etl_pass",
        host="etl_db_container",  # must match DB container name
        port="5432"
    )
    cur = conn.cursor()

    # Create table with date as DATE type
    cur.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id SERIAL PRIMARY KEY,
            gameweek INT,
            date DATE,
            home_team TEXT,
            away_team TEXT,
            home_score INT,
            away_score INT,
            scraped_at TIMESTAMPTZ
        )
    """)

    for m in data:
        cur.execute("""
            INSERT INTO matches (gameweek, date, home_team, away_team, home_score, away_score, scraped_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            m["gameweek"],
            datetime.fromisoformat(m["date"]).date(),  # ensure proper DATE
            m["home_team"],
            m["away_team"],
            m["home_score"],
            m["away_score"],
            datetime.fromisoformat(m["scraped_at"])    # TIMESTAMPTZ
        ))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    with open("transformed_matches.json", "r") as f:
        transformed_data = json.load(f)

    load(transformed_data)
    print("✅ Data loaded into Postgres")
