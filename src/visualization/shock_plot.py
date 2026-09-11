import matplotlib.pyplot as plt

def plot_shock(dates, scores):
    plt.figure(figsize=(10,5))
    plt.plot(dates,scores)
    plt.xlabel("Date")
    plt.ylabel("Shock score")
    plt.title("Financial Shock Score")
    return plt.gca()
