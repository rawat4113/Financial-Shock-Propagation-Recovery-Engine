import matplotlib.pyplot as plt

def plot_recovery(days, values):
    plt.figure(figsize=(10,5))
    plt.plot(days,values)
    plt.xlabel("Days")
    plt.ylabel("Recovery level")
    plt.title("Recovery Simulation")
    return plt.gca()
