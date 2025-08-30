class DatabaseInitializationException(Exception):
    """An exception occurred while initializing the database"""


class DatabaseEngineException(Exception):
    """An exception occurred while initializing the database engine"""


class SiteConditionsException(Exception):
    """The site_conditions list was not provided"""


class SnotelDataException(Exception):
    """The snotel_data list was not provided"""
