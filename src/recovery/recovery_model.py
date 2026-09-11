from sklearn.ensemble import RandomForestRegressor

def train_recovery_model(X,y):
    model=RandomForestRegressor(n_estimators=300,random_state=42,n_jobs=-1)
    model.fit(X,y)
    return model
