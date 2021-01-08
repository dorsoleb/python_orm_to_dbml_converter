from main import SqlAlchemyDBMLMaker
from tests.test_fixtures import *


def test_all_columns(model_fixture, model_columns_fixture):
    all_columns_name = [x.name for x in SqlAlchemyDBMLMaker(model_fixture)._all_columns()]
    assert all([x for x in all_columns_name if x in model_columns_fixture])
