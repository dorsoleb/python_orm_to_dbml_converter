import pytest

from models import ScaleType


@pytest.fixture
def model_fixture():
    return ScaleType


@pytest.fixture
def model_columns_fixture():
    return ['id', 'name', 'is_archive']
