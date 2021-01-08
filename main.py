import models
from utils import SqlAlchemyDBMLMaker, ExtractSqlAlchemyModel


def main():
    all_models = ExtractSqlAlchemyModel.extract_sqlalchemy_models(models)

    all_tables = [SqlAlchemyDBMLMaker(x).create_table() for x in all_models]
    all_refs = [SqlAlchemyDBMLMaker(x).create_ref() for x in all_models]

    filename = 'database.dbml'
    with open(filename, 'w+') as the_file:
        for table in all_tables:
            the_file.write(table)
        for table_ref in all_refs:
            the_file.write(table_ref)

    print("Successfully done")


if __name__ == '__main__':
    main()
