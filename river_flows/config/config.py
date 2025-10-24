import os


env = os.getenv("APP_ENV", "test")

DATABASE_URL = f"postgresql://postgres:postgres@postgres-local:5432/river_flows-{env}"
ALEMBIC_DB_URL = f"postgresql://postgres:postgres@localhost:5432/river_flows-{env}"

USGS_URL = "https://waterservices.usgs.gov/nwis/iv"
USGS_EWRSD_SITE = "09067020"

SITE_MAPPING = {
    "09067020": {"SNOTEL": "842:CO:SNTL"},
    "09067020": {"SNOTEL": "842:CO:SNTL"},
    "09065500": {"SNOTEL": "842:CO:SNTL"},
}

ONI_MAPPING = {
    1: "djf",
    2: "jfm",
    3: "fma",
    4: "mam",
    5: "amj",
    6: "mjj",
    7: "jja",
    8: "jas",
    9: "aso",
    10: "son",
    11: "ond",
    12: "ndj",
}
# SITE_MAPPING = {
#     "09067020": {
#         "SNOTEL": ["1040:CO:SNTL", "842:CO:SNTL", "485:CO:SNTL"]
#     },
#     "09067020": {
#         "SNOTEL": ["1040:CO:SNTL", "842:CO:SNTL", "485:CO:SNTL"]
#     },
#     "09065500": {
#         "SNOTEL": ["1040:CO:SNTL", "842:CO:SNTL", "485:CO:SNTL"]
#     },
# }
