# 🏏 IPL Data Analysis Dashboard

An interactive data analytics dashboard built with **Streamlit**, analyzing Indian Premier League (IPL) ball-by-ball data from **2008 to 2024**.

---

## 📌 Overview

This project goes beyond basic data visualization — it extracts **actionable cricket insights** from 16 seasons of IPL data covering **1,000+ matches**, **600+ players**, and **200,000+ deliveries**.

The dashboard enables users to:
- Compare players head-to-head
- Analyze match phases (Powerplay, Middle, Death)
- Identify high-scoring venues
- Evaluate team dominance and toss impact
- Discover elite players through Strike Rate vs Consistency analysis

---

## 🚀 Features

| Feature | Description |
|---|---|
| **KPI Overview** | Matches, Runs, Players, Avg Runs/Match at a glance |
| **Player Comparison** | Head-to-head stats (Runs, SR, Avg, Boundaries) with run distribution histogram |
| **Phase-wise Analysis** | Powerplay / Middle / Death overs breakdown for runs and boundaries |
| **Team Dominance** | Top teams by wins + Win Type pie chart (runs vs wickets) |
| **Venue Analysis** | High-scoring vs defensive venues comparison |
| **Player Quality Scatter** | Strike Rate vs Consistency bubble chart with labeled elite players |
| **Top Batsmen & Bowlers** | Leaderboards with sortable data tables |
| **Match Dynamics** | Boundaries, Dot Balls, Fours, and Sixes breakdowns |
| **Toss Impact** | Win percentage when toss is won |
| **Key Takeaways** | Analytical insights explaining patterns in the data |
| **Data Download** | Export the cleaned dataset as CSV |

---

## 🛠️ Tech Stack

- **Python** — Core language
- **Pandas** — Data cleaning, transformation, and analysis
- **Matplotlib** — Custom charts (scatter plots, bar charts, pie charts, histograms)
- **Streamlit** — Interactive web dashboard framework
- **CSV Data Processing** — Ball-by-ball, team, player, and performance datasets

---

## 📊 Key Insights

1. **Toss has moderate impact** — ~50% win rate when toss is won
2. **Death overs are decisive** — Highest run-scoring phase of the match
3. **Boundaries drive scoring** — A significant percentage of deliveries are 4s or 6s
4. **Venue matters** — Some grounds consistently produce 180+ first innings scores
5. **Consistency separates elite players** — Top batsmen maintain high averages across 200+ matches

---

## 📁 Project Structure

```
projectdatasetipl/
│
├── data/
│   └── ipl/
│       ├── IPL_BallByBall2008_2024(Updated).csv
│       ├── team_performance_dataset_2008to2024.csv
│       ├── Players_Info_2024.csv
│       └── ipl_teams_2024_info.csv
│
├── src/
│   ├── app.py              # Main Streamlit dashboard
│   ├── data_loader.py      # Data loading with path resolution
│   ├── data_cleaning.py    # Data cleaning and preprocessing
│   ├── analysis.py         # Analysis functions (top batsmen, bowlers, etc.)
│   └── visualization.py    # Matplotlib plotting utilities
│
├── notebook/               # Jupyter notebooks for exploration
├── output/                 # Generated outputs
└── README.md
```

---

## ▶️ How to Run

### Prerequisites
```bash
pip install streamlit pandas matplotlib
```

### Run the Dashboard
```bash
streamlit run src/app.py
```

The app will open at `http://localhost:8501`

---

## 📸 Dashboard Preview

The dashboard includes:
- **Overview Section** — KPI cards with key stats
- **Player Comparison** — Side-by-side V Kohli vs RG Sharma (configurable)
- **Phase-wise Analysis** — Powerplay / Middle / Death overs charts
- **Team Dominance** — Win charts with pie chart breakdown
- **Venue Analysis** — High vs Low scoring venues (horizontal bar charts)
- **Player Quality** — Strike Rate vs Consistency scatter plot
- **Key Takeaways** — Written analytical insights

---

## 👤 Author

Built as a data analytics portfolio project demonstrating:
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Feature engineering (match phases, boundary detection)
- Interactive dashboard development
- Analytical storytelling with data
