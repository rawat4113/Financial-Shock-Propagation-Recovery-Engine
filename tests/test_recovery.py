from src.recovery.recovery_prediction import recovery_days

def test_recovery():
    assert recovery_days([(0,.8),(1,.99)])==1
