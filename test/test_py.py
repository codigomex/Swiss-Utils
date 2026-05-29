import pytest

from py_utils.py import immutable


def test_immutable_class() -> None:
    @immutable
    class DataConfig:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    obj = DataConfig(10, 20)
    
    # Values are assigned correctly upon init
    assert obj.x == 10
    
    # Mutation raises an error
    with pytest.raises(AttributeError):
        obj.x = 15

    # Deletion raises an error
    with pytest.raises(AttributeError):
        del obj.y