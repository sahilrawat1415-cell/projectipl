def clean_data(ball):
    ball['type of extras'] = ball['type of extras'].fillna("None")
    ball['Player Out'] = ball['Player Out'].fillna("None")
    ball['wicket_type'] = ball['wicket_type'].fillna("None")
    
    return ball