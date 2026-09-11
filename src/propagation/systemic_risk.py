def systemic_risk(shocks):
    vals=list(shocks.values())
    return 100*sum(vals)/len(vals) if vals else 0.0
