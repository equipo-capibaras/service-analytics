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


class ScalingLevelEnum(int, Enum):
    SCALED_1 = 1
    SCALED_2 = 2
    SCALED_3 = 3
    SCALED_4 = 4
    SCALED_5 = 5
    SCALED_6 = 6
    SCALED_7 = 7
    SCALED_8 = 8
    SCALED_9 = 9
    SCALED_10 = 10
