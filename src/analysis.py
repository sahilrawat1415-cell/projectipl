def top_batsmen(ball):
    return ball.groupby('Striker')['runs_scored'].sum().sort_values(ascending=False).head(10)
def strike_rate(ball):
    sr = ball.groupby('Striker').agg({
        'runs_scored': 'sum',
        'Ball No': 'count'
    })
    sr['strike_rate'] = (sr['runs_scored'] / sr['Ball No']) * 100
    return sr[sr['Ball No'] > 500].sort_values(by='strike_rate', ascending=False)

def top_bowlers(ball):
    wickets = ball[ball['Player Out'] != "None"]
    return wickets.groupby('Bowler')['Player Out'].count().sort_values(ascending=False).head(10)

def merge_player_info(ball, players):
    # Clean names before merging
    ball['Striker'] = ball['Striker'].str.strip()
    players['Player Name'] = players['Player Name'].str.strip()
    
    merged = ball.merge(players, left_on='Striker', right_on='Player Name', how='left')
    return merged

def runs_by_nationality(merged):
    return merged.groupby('Player Nationality')['runs_scored'].sum().sort_values(ascending=False)


def runs_by_role(merged):
    return merged.groupby('Player Role')['runs_scored'].sum().sort_values(ascending=False)

def consistency(ball):
    runs_per_match = ball.groupby(['Striker', 'Match id'])['runs_scored'].sum().reset_index()
    return runs_per_match.groupby('Striker')['runs_scored'].mean().sort_values(ascending=False).head(10)

def death_overs_batsmen(ball):
    # Approximate death overs using innings progression
    death = ball[ball['Ball No'] >= 16]  # last balls of overs (imperfect but usable)
    return death.groupby('Striker')['runs_scored'].sum().sort_values(ascending=False).head(10)

def toss_impact(teams_performance):
    df = teams_performance.copy()
    df['toss_win_match'] = df['Toss_Winner'] == df['Match_Winner']
    return df['toss_win_match'].mean() * 100
