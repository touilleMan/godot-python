import pytest


@pytest.fixture
def current_node():
    # `conftest.py` is imported weirdly by pytest so we cannot just put a
    # global variable in it and set it from `Main._ready`
    from main import get_current_node

    return get_current_node()
