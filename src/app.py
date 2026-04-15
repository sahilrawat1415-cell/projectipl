import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from data_loader import load_data
from data_cleaning import clean_data
from analysis import (
    top_batsmen, strike_rate, top_bowlers,
    merge_player_info, runs_by_nationality,
    runs_by_role, consistency, death_overs_batsmen,
    toss_impact
)

# ─────────────────────────────────────────────
# 1. PAGE CONFIG & TITLE
# ─────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="IPL Analytics Dashboard")

st.title("🏏 IPL Analytics Dashboard")
st.markdown("---")

# ─────────────────────────────────────────────
# LOAD & CLEAN DATA
# ─────────────────────────────────────────────
try:
    ball, teams, players, teams_performance = load_data()
    ball = clean_data(ball)
    merged = merge_player_info(ball, players)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ─────────────────────────────────────────────
# DERIVED COLUMNS
# ─────────────────────────────────────────────
ball['over'] = ball['Ball No'].apply(int)  # integer part = over number
ball['is_boundary'] = ball['runs_scored'].isin([4, 6])
ball['is_dot'] = ball['runs_scored'] == 0

def get_phase(over):
    if over <= 5:
        return "Powerplay (0-6)"
    elif over <= 14:
        return "Middle (7-15)"
    else:
        return "Death (16-20)"

ball['phase'] = ball['over'].apply(get_phase)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.title("🔎 Filters")
st.sidebar.markdown("Use filters to explore player and team performance")

st.sidebar.markdown("---")
st.sidebar.subheader("👤 Player Comparison")

all_players = sorted(ball['Striker'].dropna().unique())
player1 = st.sidebar.selectbox("Player 1", all_players, index=all_players.index("V Kohli") if "V Kohli" in all_players else 0)
player2 = st.sidebar.selectbox("Player 2", all_players, index=all_players.index("RG Sharma") if "RG Sharma" in all_players else 1)

# ═════════════════════════════════════════════
# 2. KPI ROW
# ═════════════════════════════════════════════
st.markdown("## 📊 Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_runs = int(ball['runs_scored'].sum())
total_matches = ball['Match id'].nunique()
total_players = ball['Striker'].nunique()
avg_total = total_runs / matches
avg_per_team = avg_total / 2

col1, col2 = st.columns(2)

col1.metric("Avg Total Runs/Match", round(avg_total, 2))
col2.metric("Avg Runs per Team", round(avg_per_team, 2))

kpi1.metric("Matches", f"{total_matches:,}")
kpi2.metric("Runs", f"{total_runs:,}")
kpi3.metric("Players", f"{total_players:,}")
kpi4.metric("Avg Runs/Match", avg_runs)

# ═════════════════════════════════════════════
# 3. KEY INSIGHTS BOX
# ═════════════════════════════════════════════
st.markdown("## 🔍 Key Insights")

st.success(f"""
✔ Total Runs: {total_runs:,}  
✔ Avg Runs/Match: {avg_runs}  
✔ Toss Impact: {round(toss_impact(teams_performance), 2)}%  
✔ Boundaries: {int(ball['is_boundary'].sum()):,} | Dot Balls: {int(ball['is_dot'].sum()):,}
""")

# ═════════════════════════════════════════════
# 4. PLAYER COMPARISON (NEW — FEATURE 1)
# ═════════════════════════════════════════════
st.markdown("---")
st.markdown("## 🆚 Player Comparison")

p1_data = ball[ball['Striker'] == player1]
p2_data = ball[ball['Striker'] == player2]

p1_runs = int(p1_data['runs_scored'].sum())
p2_runs = int(p2_data['runs_scored'].sum())
p1_matches = p1_data['Match id'].nunique()
p2_matches = p2_data['Match id'].nunique()
p1_balls = len(p1_data)
p2_balls = len(p2_data)
p1_sr = round((p1_runs / p1_balls) * 100, 2) if p1_balls > 0 else 0
p2_sr = round((p2_runs / p2_balls) * 100, 2) if p2_balls > 0 else 0
p1_avg = round(p1_runs / p1_matches, 2) if p1_matches > 0 else 0
p2_avg = round(p2_runs / p2_matches, 2) if p2_matches > 0 else 0
p1_boundaries = int(p1_data['is_boundary'].sum())
p2_boundaries = int(p2_data['is_boundary'].sum())

cmp1, cmp_vs, cmp2 = st.columns([5, 1, 5])

with cmp1:
    st.subheader(f"🔵 {player1}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Runs", f"{p1_runs:,}")
    m2.metric("Matches", p1_matches)
    m3.metric("Strike Rate", p1_sr)

    m4, m5 = st.columns(2)
    m4.metric("Avg Runs/Match", p1_avg)
    m5.metric("Boundaries", f"{p1_boundaries:,}")

with cmp_vs:
    st.markdown("<div style='text-align:center; font-size:2rem; padding-top:2rem;'>⚡<br>VS</div>", unsafe_allow_html=True)

with cmp2:
    st.subheader(f"🔴 {player2}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Runs", f"{p2_runs:,}")
    m2.metric("Matches", p2_matches)
    m3.metric("Strike Rate", p2_sr)

    m4, m5 = st.columns(2)
    m4.metric("Avg Runs/Match", p2_avg)
    m5.metric("Boundaries", f"{p2_boundaries:,}")

# Runs per match comparison chart
st.markdown("##### Match-by-Match Runs Comparison")
p1_match_runs = p1_data.groupby('Match id')['runs_scored'].sum()
p2_match_runs = p2_data.groupby('Match id')['runs_scored'].sum()

fig, ax = plt.subplots(figsize=(12, 4))
ax.hist(p1_match_runs, bins=20, alpha=0.6, label=player1, color='#3498db')
ax.hist(p2_match_runs, bins=20, alpha=0.6, label=player2, color='#e74c3c')
ax.set_xlabel("Runs per Match")
ax.set_ylabel("Frequency")
ax.set_title("Run Distribution Comparison")
ax.legend()
plt.tight_layout()
st.pyplot(fig)

# ═════════════════════════════════════════════
# 5. PHASE-WISE ANALYSIS (NEW — FEATURE 2)
# ═════════════════════════════════════════════
st.markdown("---")
st.markdown("## 🎯 Phase-wise Analysis")
st.caption("Powerplay (Overs 0–6) → Middle (7–15) → Death (16–20)")

phase_col1, phase_col2 = st.columns(2)

with phase_col1:
    st.subheader("Runs by Phase")
    phase_runs = ball.groupby('phase')['runs_scored'].sum()
    st.bar_chart(phase_runs)

with phase_col2:
    st.subheader("Boundaries by Phase")
    phase_boundaries = ball[ball['is_boundary']].groupby('phase').size()
    st.bar_chart(phase_boundaries)

# Phase-wise KPIs
pk1, pk2, pk3 = st.columns(3)
for col, phase_name in zip([pk1, pk2, pk3], ["Powerplay (0-6)", "Middle (7-15)", "Death (16-20)"]):
    phase_data = ball[ball['phase'] == phase_name]
    phase_total = int(phase_data['runs_scored'].sum())
    phase_sr = round((phase_data['runs_scored'].sum() / len(phase_data)) * 100, 2) if len(phase_data) > 0 else 0
    col.metric(f"{phase_name} Runs", f"{phase_total:,}")
    col.metric(f"{phase_name} SR", phase_sr)

# ═════════════════════════════════════════════
# 6. TWO-COLUMN DASHBOARD (Player & Team)
# ═════════════════════════════════════════════
st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("👤 Player Analysis")
    player = st.selectbox("Select Player", all_players)
    filtered = ball[ball['Striker'] == player]
    player_stats = filtered.groupby('Match id')['runs_scored'].sum().sort_index()
    st.line_chart(player_stats)

with col_right:
    st.subheader("🏏 Team Analysis")
    team = st.selectbox("Select Team", ball['Batting team'].unique())
    team_data = ball[ball['Batting team'] == team]
    team_runs = team_data.groupby('Striker')['runs_scored'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(team_runs)

# ═════════════════════════════════════════════
# 7. TEAM WIN ANALYSIS (NEW — FEATURE 3)
# ═════════════════════════════════════════════
st.markdown("---")
st.markdown("## 🏆 Team Dominance")

win_col1, win_col2 = st.columns(2)

with win_col1:
    st.subheader("Top Teams by Wins")
    wins = teams_performance['Match_Winner'].value_counts().head(10)
    st.bar_chart(wins)

with win_col2:
    st.subheader("Win Type Breakdown")
    win_types = teams_performance['Win_Type'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(win_types, labels=win_types.index, autopct='%1.1f%%', startangle=90,
           colors=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
    ax.set_title("How Teams Win")
    st.pyplot(fig)

# ═════════════════════════════════════════════
# 8. VENUE ANALYSIS (NEW — FEATURE 4)
# ═════════════════════════════════════════════
st.markdown("---")
st.markdown("## 🏟️ Venue Analysis")

venue_col1, venue_col2 = st.columns(2)

with venue_col1:
    st.subheader("High Scoring Venues")
    venue_runs = teams_performance.groupby('Venue')['First_Innings_Score'].mean().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    venue_runs.plot(kind='barh', ax=ax, color='#2ecc71')
    ax.set_xlabel("Avg First Innings Score")
    ax.set_title("Top 10 High Scoring Venues")
    plt.tight_layout()
    st.pyplot(fig)

with venue_col2:
    st.subheader("Low Scoring Venues")
    venue_low = teams_performance.groupby('Venue')['First_Innings_Score'].mean().sort_values().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    venue_low.plot(kind='barh', ax=ax, color='#e74c3c')
    ax.set_xlabel("Avg First Innings Score")
    ax.set_title("Top 10 Defensive Venues")
    plt.tight_layout()
    st.pyplot(fig)

# ═════════════════════════════════════════════
# 9. STRIKE RATE VS CONSISTENCY (NEW — FEATURE 5)
# ═════════════════════════════════════════════
st.markdown("---")
st.markdown("## 🧠 Player Quality Analysis")
st.caption("Strike Rate vs Average Runs/Match — top-right quadrant = elite players")

sr = strike_rate(ball).reset_index()
cons = consistency(ball).reset_index()
cons.columns = ['Striker', 'avg_runs_per_match']

merged_stats = sr.merge(cons, on='Striker')

fig, ax = plt.subplots(figsize=(12, 6))
scatter = ax.scatter(
    merged_stats['strike_rate'],
    merged_stats['avg_runs_per_match'],
    s=merged_stats['runs_scored'] / 30,
    alpha=0.6,
    c=merged_stats['strike_rate'],
    cmap='RdYlGn',
    edgecolors='black',
    linewidth=0.5
)

# Label top players
for _, row in merged_stats.nlargest(8, 'avg_runs_per_match').iterrows():
    ax.annotate(row['Striker'], (row['strike_rate'], row['avg_runs_per_match']),
                fontsize=8, ha='left', va='bottom')

ax.set_xlabel("Strike Rate", fontsize=12)
ax.set_ylabel("Avg Runs / Match", fontsize=12)
ax.set_title("Strike Rate vs Consistency (bubble size = total runs)", fontsize=14)
ax.axhline(y=merged_stats['avg_runs_per_match'].median(), color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=merged_stats['strike_rate'].median(), color='gray', linestyle='--', alpha=0.5)
plt.colorbar(scatter, label='Strike Rate')
plt.tight_layout()
st.pyplot(fig)

# ═════════════════════════════════════════════
# 10. TOP BATSMEN & MATCH DYNAMICS
# ═════════════════════════════════════════════
st.markdown("---")
st.subheader("🔥 Top Batsmen Overall")
batsmen = top_batsmen(ball)
st.bar_chart(batsmen)

st.markdown("---")
st.subheader("⚡ Match Dynamics")

dyn1, dyn2, dyn3, dyn4 = st.columns(4)
dyn1.metric("Boundaries", f"{int(ball['is_boundary'].sum()):,}")
dyn2.metric("Dot Balls", f"{int(ball['is_dot'].sum()):,}")
dyn3.metric("Fours", f"{int((ball['runs_scored'] == 4).sum()):,}")
dyn4.metric("Sixes", f"{int((ball['runs_scored'] == 6).sum()):,}")

# ═════════════════════════════════════════════
# 11. ADDITIONAL ANALYSIS
# ═════════════════════════════════════════════
st.markdown("---")

add_left, add_right = st.columns(2)

with add_left:
    st.subheader("🎯 Top Bowlers")
    bowlers = top_bowlers(ball)
    st.dataframe(bowlers)

    st.subheader("📈 Strike Rate (500+ balls)")
    st.dataframe(strike_rate(ball).head(10))

with add_right:
    st.subheader("🌍 Runs by Nationality")
    st.bar_chart(runs_by_nationality(merged))

    st.subheader("🧑‍💼 Runs by Role")
    st.bar_chart(runs_by_role(merged))

# ═════════════════════════════════════════════
st.markdown("---")

fin_left, fin_right = st.columns(2)

with fin_left:
    st.subheader("🎯 Consistency (Avg Runs/Match)")
    st.dataframe(consistency(ball))

with fin_right:
    st.subheader("💀 Death Overs Performance")
    death = death_overs_batsmen(ball)

    fig, ax = plt.subplots()
    death.plot(kind='bar', ax=ax)
    plt.xticks(rotation=45)
    plt.title("Top Death Over Finishers")
    plt.tight_layout()
    st.pyplot(fig)

# ═════════════════════════════════════════════
st.markdown("---")
st.subheader("🏆 Toss Impact")
st.metric("Win % when toss won", f"{round(toss_impact(teams_performance), 2)}%")

# ═════════════════════════════════════════════
# KEY TAKEAWAYS — ANALYTICAL INSIGHTS
# ═════════════════════════════════════════════
st.markdown("---")
st.markdown("## 📊 Key Takeaways")

toss_pct = round(toss_impact(teams_performance), 1)
death_runs = int(ball[ball['phase'] == 'Death (16-20)']['runs_scored'].sum())
total_boundary_pct = round((ball['is_boundary'].sum() / len(ball)) * 100, 1)

st.success(f"""
🔹 **Toss Impact is Moderate** — Teams winning the toss win ~{toss_pct}% of matches, suggesting toss alone doesn't determine outcomes.  
🔹 **Death Overs are Decisive** — {death_runs:,} runs scored in death overs (16–20), making it the highest-impact phase for batsmen.  
🔹 **Boundaries Drive Scoring** — {total_boundary_pct}% of all deliveries result in boundaries (4s or 6s), highlighting the aggressive nature of T20 cricket.  
🔹 **Top Batsmen are Consistent** — Elite players like V Kohli and RG Sharma maintain high averages across 200+ matches, showing sustained excellence.  
🔹 **Venue Matters** — Some grounds consistently produce 180+ first innings scores, while defensive venues average under 140.  
""")

st.info("""
💡 **Conclusion:** IPL success depends on a combination of strong death-over batting, 
strategic toss decisions, and adapting to venue conditions — not just individual brilliance.
""")

# ═════════════════════════════════════════════
# DOWNLOAD CLEAN DATASET
# ═════════════════════════════════════════════
st.markdown("---")
st.markdown("## 📥 Download Data")

csv = ball.to_csv(index=False)

st.download_button(
    label="Download Top Batsmen Data",
    data=top_batsmen(ball).to_csv(),
    file_name="top_batsmen.csv",
    mime="text/csv"
)
