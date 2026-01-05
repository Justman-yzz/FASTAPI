def test_temp() -> None:
    assert 1 + 99 == 100


# 의도된 실패 테스트
def test_temp_false() -> None:
    assert 1 + 1 == 3
