from sklearn.ensemble import IsolationForest


def fit_isolation_forest(
    X,
    contamination=0.02,
    random_state=42
):
    model = IsolationForest(
        contamination=contamination,
        random_state=random_state
    )

    model.fit(X)

    return model