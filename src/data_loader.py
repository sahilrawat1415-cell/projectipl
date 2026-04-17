import pandas as pd
import os

# Resolve project root (parent of src/)
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def load_data():
    data_dir = os.path.join(_PROJECT_ROOT, "data", "ipl")
    ball = pd.read_csv(
    os.path.join(data_dir, "IPL_BallByBall2008_2024(Updated).csv"),
    dtype={"Season": str},
    low_memory=False
)

    ball["Season"] = ball["Season"].str[:4]
    teams_performance = pd.read_csv(os.path.join(data_dir, "team_performance_dataset_2008to2024.csv"))
    players = pd.read_csv(os.path.join(data_dir, "Players_Info_2024.csv"))
    teams = pd.read_csv(os.path.join(data_dir, "ipl_teams_2024_info.csv"))
    return ball, teams, players, teams_performance


# if __name__ == "__main__":
#     print(players.columns.tolist())
#     ball, teams, players, teams_performance = load_data()

#     # print(ball.head())
#     # print(ball.shape)
#     # print(ball.columns)
#     # print(ball.info())
#     # print(ball.columns.tolist())
#     # print(ball.columns.tolist())
#     # Example cleaning
    
# #     ball = pd.read_csv(
# #     "data/ipl/IPL_BallByBall2008_2024(Updated).csv",
# #     low_memory=False
# # )    
#     ball['type of extras'] = ball['type of extras'].fillna("None")
#     ball['Player Out'] = ball['Player Out'].fillna("None")
#     print(ball.isnull().sum())
#     top_batsmen = ball.groupby('Striker')['runs_scored'].sum().sort_values(ascending=False).head(10)
#     print(top_batsmen)