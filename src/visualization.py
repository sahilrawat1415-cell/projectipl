import matplotlib.pyplot as plt 

def plot_top_batsmen(batsmen):
    batsmen.plot(kind='bar')
    plt.title("Top 10 Batsmen (Total Runs)")
    plt.xlabel("Player")
    plt.ylabel("Runs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_strike_rate(sr):
    sr.head(10)['strike_rate'].plot(kind='bar')
    plt.title("Top Strike Rates")
    plt.xlabel("Player")
    plt.ylabel("Strike Rate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_nationality(runs):
    runs.plot(kind='bar')
    plt.title("Runs by Nationality")
    plt.xlabel("Nationality")
    plt.ylabel("Total Runs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()