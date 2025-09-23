# CDE-Docker_pipeline-Assignment
A Dockerized ETL pipeline built with Python, Playwright, and PostgreSQL to extract, transform, and load football match data in a reproducible way.

---

# ⚽ Dockerized Python ETL Pipeline with PostgreSQL

## 📌 Project Overview

This project demonstrates a containerized Extract, Transform, Load (ETL) pipeline using **Python, Docker, and PostgreSQL**.
It scrapes football match data, cleans and transforms it, and loads it into a PostgreSQL database — all fully automated using a Bash script.

---

## 🛠️ Tech Stack

* **Python 3.13-slim** – ETL scripts
* **Playwright** – Web scraping (Extract)
* **PostgreSQL 15** – Target database (Load)
* **Docker & Docker Networking** – Container orchestration
* **Bash** – Pipeline automation

---

## 📂 Project Structure

```bash
.
├── scraper.py              # Extract: Scrapes football matches
├── transform.py            # Transform: Cleans & standardizes data
├── load.py                 # Load: Inserts data into Postgres
├── requirement.txt         # Python dependencies
├── Dockerfile              # ETL container definition
├── run_pipeline.sh         # Automates the ETL workflow
└── README.md               # Project documentation
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/<idrisakorede>/<CDE-Docker_pipeline-Assignment>.git
cd <CDE-Docker_pipeline-Assignment>
```

### 2. Ensure Docker is installed

Check Docker installation:

```bash
docker --version
```

### 3. Run the pipeline

The entire ETL pipeline is automated via `run_pipeline.sh`:

```bash
bash run_pipeline.sh
```

### 4. Expected Output

* `scraper.py` generates `raw_matches.json`
* `transform.py` generates `transformed_matches.json`
* `load.py` inserts data into Postgres `matches` table
* The script will query the database and display match records

---

## 🧪 Verify Database

After running the pipeline, you can connect to the Postgres container manually:

```bash
docker exec -it etl_db_container psql -U etl_user -d etl_db
```

Inside Postgres, check data:

```sql
\dt               -- list tables
SELECT * FROM matches;   -- see loaded match data
```

---

## 🧹 Cleanup

The script automatically cleans up containers and network after execution.
If you need to manually clean:

```bash
docker stop etl_db_container && docker rm etl_db_container
docker network rm etl_network
```

---

## 📌 Key Learning Points

* Containerized ETL workflow with Docker
* Web scraping and transformation in Python
* Loading structured data into PostgreSQL
* Automated orchestration using Bash

---
