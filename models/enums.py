from enum import Enum


class PlanEnum(str, Enum):
    EMPRENDEDOR = 'Emprendedor'
    EMPRESARIO = 'Empresario'
    EMPRESARIO_PLUS = 'Empresario Plus'


class RiskLevelEnum(str, Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'


class ChannelEnum(str, Enum):
    EMAIL = 'Email'
    WEB = 'Web'
    Mobile = 'Mobile'


class PartOfDayEnum(str, Enum):
    MORNING = 'Morning'
    MIDDAY = 'Midday'
    AFTERNOON = 'Afternoon'
    NIGHT = 'Night'


class ProductTypeEnum(str, Enum):
    SOFTWARE = 'Software'
    HARDWARE = 'Hardware'
    SERVICE = 'Service'
    OTHER = 'Other'


class DayOfWeekEnum(str, Enum):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'


class ScalingLevelEnum(int, Enum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5
    LEVEL_6 = 6
    LEVEL_7 = 7
    LEVEL_8 = 8
    LEVEL_9 = 9
    LEVEL_10 = 10
