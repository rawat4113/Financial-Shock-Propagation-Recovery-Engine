def contagion_step(shock, exposure, recovery_rate=0.05):
    return max(0.0, min(1.0, shock*exposure*(1-recovery_rate)))
