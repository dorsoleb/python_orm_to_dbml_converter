from abc import abstractstaticmethod, abstractmethod, abstractclassmethod, ABC
from typing import List

from sqlalchemy import ForeignKey, Column


class ISqlAlchemyDBMLMaker:

    def create_ref(self, foreign_keys: List[ForeignKey] = None) -> str:
        """
        Конструктор для множестенного создания связей между таблицами
        """

    @staticmethod
    def create_column(column: Column) -> str:
        """
        Основной компонент создания колонок в таблице
        Типизация идет от типов на питоне
        """

    def create_table(self) -> str:
        """
        Собирает конструктором название таблицы
        Потом пихает внутрь название и типы колонок
        """


