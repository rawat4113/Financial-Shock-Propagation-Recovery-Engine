from src.shock_detection.shock_score import shock_score

def test_score_range():
    assert 0 <= shock_score(2,0.5,0.2) <= 100
