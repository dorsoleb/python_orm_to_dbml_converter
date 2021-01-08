import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint, DateTime, Text

AttestationModel = declarative_base()


class ScaleType(AttestationModel):
    """

    Справочник шкал оценки
    task: https://jira.it2g.ru/browse/KISUSS-890

    """
    __tablename__ = 'scale_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(75), nullable=False)
    is_archive = Column(Boolean, nullable=False)


class TestKind(AttestationModel):
    """
       Справочник видов контрольных мероприятий аттестации личного состава
       task: https://jira.it2g.ru/browse/KISUSS-890
    """
    __tablename__ = 'test_kind'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    short_name = Column(String(75), nullable=False)
    scale_type_id = Column(ForeignKey(f'scale_type.id'))
    is_archive = Column(Boolean, nullable=False)


class EducationMethod(AttestationModel):
    """
       Справочник методов проведения занятий по подготовке личного состава
       task: https://jira.it2g.ru/browse/KISUSS-889

    """
    __tablename__ = 'education_method'
    __table_args__ = (
        UniqueConstraint('name', 'short_name', name='_name_and_short_name_uc'),

    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    short_name = Column(String(255), nullable=False)


class AbsenceReason(AttestationModel):
    """
       Справочник причин отсутствия на занятиях по подготовке личного состава
       task: https://jira.it2g.ru/browse/KISUSS-888
    """
    __tablename__ = 'absence_reason'
    __table_args__ = (
        UniqueConstraint('full_name', 'name', name='_full_name_and_name'),

    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)


class PeriodTypes(enum.Enum):
    """
       Типы периодов для справочника
    """
    year = 'год'
    quarter = 'квартал'
    month = 'месяц'
    half_year = 'полугодие'
    arbitrary = 'произвольный'

    def __str__(self):
        return self.value


class Period(AttestationModel):
    """
       Справочник периодов подготовки личного состава
       task: https://jira.it2g.ru/browse/KISUSS-887
    """
    __tablename__ = 'period'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime(True), nullable=False)
    end_date = Column(DateTime(True), nullable=False)
    comment = Column(String(512))
    is_archive = Column(Boolean, default=False)


class ThemePlan(AttestationModel):
    """
       Тематический план
       task: https://jira.it2g.ru/browse/KISUSS-913
       subtask: https://jira.it2g.ru/browse/KISUSS-1047
    """
    __tablename__ = 'theme_plan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    period_id = Column(ForeignKey(f'period.id'))
    start_date = Column(DateTime(True), nullable=False)
    end_date = Column(DateTime(True), nullable=False)
    order_number = Column(String(100), nullable=False)
    order_date = Column(DateTime(True), nullable=False)
    small_division = Column(Boolean, nullable=False)


class BasicThemePlan(AttestationModel):
    """
          Типовой тематический план
          task: https://jira.it2g.ru/browse/KISUSS-913
    """
    __tablename__ = 'basic_theme_plan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    theme_plan_id = Column(ForeignKey(f'theme_plan.id'))
    norm_hours = Column(Integer)
    small_norm_hours = Column(Integer)


class SectionDirectory(AttestationModel):
    """
       Раздел подготовки
       task: https://jira.it2g.ru/browse/KISUSS-1032
    """
    __tablename__ = 'section_directory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    short_name = Column(String(32), nullable=False)
    is_archive = Column(Boolean)


class ThemeDirectoryTypes(enum.Enum):
    """
       Тип темы занятия
    """
    one = 'Норматив по физической подготовке'
    two = 'Норматив по пожарно-строевой и тактико-специальной подготовке'

    def __str__(self):
        return self.value


class ThemeDirectory(AttestationModel):
    """
       Тема занятия
       task: https://jira.it2g.ru/browse/KISUSS-1032
    """
    __tablename__ = 'theme_directory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    section_directory_id = Column(
        ForeignKey(f'section_directory.id'))
    name = Column(String(512))
    is_archive = Column(Boolean)


class Section(AttestationModel):
    """
       Раздел тематического плана
       task: https://jira.it2g.ru/browse/KISUSS-913
    """
    __tablename__ = 'section'

    id = Column(Integer, primary_key=True, autoincrement=True)
    section_directory_id = Column(
        ForeignKey(f'section_directory.id'))
    theme_plan_id = Column(ForeignKey(f'theme_plan.id'))
    order = Column(Integer)  # Нужно реализовать инкремент 10 для каждого значения theme_directory
    add_number = Column(Boolean, default=True)
    count_charge = Column(Boolean)


class Test(AttestationModel):
    """
    Контрольные мероприятия по разделу подготовки
    task: https://jira.it2g.ru/browse/KISUSS-914
    """
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    section_id = Column(ForeignKey(f'section.id'))
    test_kind_id = Column(ForeignKey(f'test_kind.id'))


class Theme(AttestationModel):
    """
          Тема занятия
          task: https://jira.it2g.ru/browse/KISUSS-914
    """
    __tablename__ = 'theme'

    id = Column(Integer, primary_key=True, autoincrement=True)
    section_id = Column(ForeignKey(f'section.id'))
    theme_directory_id = Column(
        ForeignKey(f'theme_directory.id'))
    order = Column(Integer)  # Нужно реализовать инкремент 10 для каждого значения theme_directory


class EducationCharge(AttestationModel):
    """
       Количество часов по теме в разрезе методов проведения занятий
       task: https://jira.it2g.ru/browse/KISUSS-914
    """
    __tablename__ = 'education_charge'

    id = Column(Integer, primary_key=True, autoincrement=True)
    theme_id = Column(ForeignKey(f'theme.id'))
    education_method_id = Column(
        ForeignKey(f'education_method.id'))
    hours = Column(Integer)


class ThemeQuestion(AttestationModel):
    """
       Вопросы темы

       task: https://jira.it2g.ru/browse/KISUSS-915
    """
    __tablename__ = 'theme_question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    theme_id = Column(ForeignKey(f'theme.id'))
    order = Column(Integer)  # Инкремент 10 относительно максимального значения поля order в существующих записях.
    name = Column(Text)
