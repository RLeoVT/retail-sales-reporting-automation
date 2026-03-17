# Retail Sales Reporting Automation

End-to-end pipeline that extracts retail sales data from a SQLite database via SQL, transforms weekly metrics with Pandas, and automatically generates and delivers an interactive HTML report via email.

## Business Problem
Retail commercial teams often rely on manually prepared weekly reports that consume several hours of analytical work. This pipeline automates the full process — from data extraction to report delivery — reducing manual effort to zero.

## Pipeline Architecture
```
CSV → SQLite → SQL Queries → Pandas → HTML Report (Plotly) → Email (Gmail SMTP)
```

## Project Structure
```
├── data/                  # Source dataset (Superstore)
├── db/                    # SQLite database (generated)
├── outputs/               # HTML report (generated)
├── src/
│   ├── queries.py         # SQL extraction functions
│   ├── transform.py       # Pandas transformation functions
│   ├── report.py          # HTML report generation (Jinja2 + Plotly)
│   └── mailer.py          # Automated email delivery (Gmail SMTP)
├── load_db.py             # One-time CSV to SQLite loader
└── main.py                # Pipeline orchestrator
```

## Report Contents
- **Weekly KPIs** — total sales vs prior week with % variance
- **Category Performance** — week-over-week comparison across Furniture, Office Supplies, and Technology
- **Top & Bottom 10 Products** — by weekly revenue
- **Regional Analysis** — current week vs historical weekly average using SQL CTEs

## Tech Stack
- **Python** — Pandas, Plotly, Jinja2, smtplib
- **SQL** — SQLite via sqlite3
- **Data** — [Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) (Kaggle)

## Setup

1. Clone the repository
2. Create and activate a virtual environment
```bash
python3 -m venv retail_env
source retail_env/bin/activate
pip install pandas plotly jinja2 python-dotenv
```
3. Create a `.env` file in the root directory
```
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
RECIPIENT=recipient@gmail.com
```
4. Load the dataset into SQLite
```bash
python load_db.py
```
5. Run the pipeline
```bash
python main.py
```

## Output Preview
The pipeline generates an interactive HTML report with dark theme, delivered as an email attachment. Open in any browser for full Plotly interactivity.