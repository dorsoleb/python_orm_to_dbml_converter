from typing import Type, List

from sqlalchemy import Table, Column, ForeignKey

from interfaces import ISqlAlchemyDBMLMaker


class SqlAlchemyDBMLMaker(ISqlAlchemyDBMLMaker):
    """
    Служит для конвертации Таблиц и их связей из алхимии в формат DBML
    Что такое DBML? https://www.dbml.org/home
    """

    def __init__(self, model: Type[Table]):
        self.model = self._validate_model(model)

    @staticmethod
    def _validate_model(model: Type[Table]):

        check_hasattr = ['__table__', '__tablename__']
        result = all([hasattr(model, x) for x in check_hasattr])

        if not result:
            raise AttributeError(f"Model has no {' '.join(check_hasattr)} attrs")

        return model

    def _all_columns(self, model: Type[Table] = None) -> List[Column]:
        """
        Для получения всех колонок в модели


        Пример:
        [ Column('id', Integer(), table=<absence_reason>, primary_key=True, nullable=False),
         Column('name', String(length=100), table=<absence_reason>, nullable=False) ]
        """
        if model is None:
            model = self.model

        result = model.__table__._columns._all_columns

        return result

    @staticmethod
    def _get_child_relation(foreign_key: ForeignKey) -> str:
        """
        Отдает связь на которую ссылается таблица

        Пример:
        'theme_plan.id'
        ^^^ от поля basic_theme_plan.theme_plan_id ведет связь на theme_plan.id
        """
        result = f'{foreign_key.target_fullname}'
        return result

    @staticmethod
    def _get_parent_relation(foreign_key: ForeignKey) -> str:
        """
        Отдает связь от которой исходит связь

        Пример:
        'basic_theme_plan.theme_plan_id'
        """
        result = f'{foreign_key.parent.table.name}.{foreign_key.parent.name}'
        return result

    @classmethod
    def _create_ref(cls, foreign_key: ForeignKey) -> str:
        """
        Конструктор для _get_parent_relation и _get_parent_relation

        Пример:
        'Ref: basic_theme_plan.theme_plan_id > theme_plan.id \n'
        """

        result = f'Ref: {cls._get_parent_relation(foreign_key)} > {cls._get_child_relation(foreign_key)} \n'

        return result

    def _foreign_keys(self, model: Type[Table] = None) -> List[ForeignKey]:
        """
        Отдает список всех внешних ключей у таблицы

        Пример:
        [ForeignKey('theme_plan.id')]
        """
        if model is None:
            model = self.model
        result = list(model.__table__.foreign_keys)
        return result

    def create_ref(self, foreign_keys: List[ForeignKey] = None) -> str:
        """
        Конструктор для множестенного создания связей между таблицами

        Пример:
        'Ref: basic_theme_plan.theme_plan_id > theme_plan.id \n'
        """

        if foreign_keys is None:
            foreign_keys = self._foreign_keys()

        result = '\n'.join([self._create_ref(x) for x in foreign_keys])

        return result

    @staticmethod
    def create_column(column: Column) -> str:
        """
        Основной компонент создания колонок в таблице
        Типизация идет от типов на питоне

        Пример:
            id int
            full_name str
            name str
        """

        result = f'{column.name} {column.type.python_type.__name__}'

        return result

    def create_table(self) -> str:
        """
        Собирает конструктором название таблицы
        Потом пихает внутрь название и типы колонок

        Пример:
        Table absence_reason {
             id int
             full_name str
             name str
         }
        """
        all_columns: List[Column] = self._all_columns()
        model: Type[Table] = self.model

        table_header = f'Table {model.__tablename__}'

        table_body = '\n'.join([f' {self.create_column(x)} ' for x in all_columns])

        result = ''.join([table_header, ' { \n', table_body, '\n } \n \n'])

        return result


class ExtractSqlAlchemyModel:
    """
    Служит для получения моделей алхимии целиком из модуля
    """

    @staticmethod
    def _is_model_class(model_class) -> bool:
        """
        Валидирует на то, что перед нами класс алхимии
        """
        check_hasattr = ['__table__', '__tablename__']
        result = all([hasattr(model_class, x) for x in check_hasattr])

        return result

    @classmethod
    def extract_sqlalchemy_models(cls, imported_module):
        module_name = imported_module

        def _extract_module(class_str, _module_name=module_name):
            return getattr(_module_name, class_str)

        all_sqlalchemy_models = [
            _extract_module(model_class_str)
            for model_class_str in dir(module_name)
            if cls._is_model_class(_extract_module(model_class_str))
        ]

        return all_sqlalchemy_models