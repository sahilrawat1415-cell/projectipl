from data_loader import load_data
from data_cleaning import clean_data
from analysis import (
    top_batsmen, strike_rate, top_bowlers,
    merge_player_info, runs_by_nationality,
    runs_by_role, consistency, death_overs_batsmen,
    toss_impact
)
from visualization import (
    plot_top_batsmen,
    plot_strike_rate,
    plot_nationality
)

def main():
    ball, teams, players, teams_performance = load_data()
    print(players.columns.tolist())   
    print(teams_performance.columns.tolist())
    ball = clean_data(ball)

    merged = merge_player_info(ball, players)

    print("Top Batsmen:\n", top_batsmen(ball))
    print("\nStrike Rate:\n", strike_rate(ball).head())
    print("\nTop Bowlers:\n", top_bowlers(ball))

    print("\nRuns by Nationality:\n", runs_by_nationality(merged))
    print("\nRuns by Role:\n", runs_by_role(merged))
    print("\nConsistency:\n", consistency(ball).head())
    print("\nDeath Overs:\n", death_overs_batsmen(ball))

    print("\nToss Impact (%):\n", toss_impact(teams_performance))

    batsmen = top_batsmen(ball)
    sr = strike_rate(ball)
    nat = runs_by_nationality(merged)

    plot_top_batsmen(batsmen)
    plot_strike_rate(sr)
    plot_nationality(nat)
    

if __name__ == "__main__":
    main()
    