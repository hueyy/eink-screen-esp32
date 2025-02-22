from server.utils import read_from_file, write_to_file
import json
from typing import LiteralString, TypedDict, Literal, Final, Any

JSON_FILE: LiteralString = "server/db.json"

Mode = Literal["static", "dynamic"]

DashboardType = Literal["Home", "News", "iNaturalist"]


class Db(TypedDict):
    mode: Mode
    dashboard_type: DashboardType


DEFAULT_DB: Final[Db] = dict(mode="dynamic", dashboard_type="News")


def db_get_full() -> Db:
    try:
        db: Db = json.loads(read_from_file(JSON_FILE))
        return db
    except Exception as e:
        print("Could not read db: ", e)
        return DEFAULT_DB


def db_get(key: str):
    return db_get_full().get(key)


def db_set(key: str, value: Any):
    db = db_get_full()
    write_to_file(
        JSON_FILE,
        json.dumps(
            {
                **db,
                key: value,
            }
        ),
    )
    return


def db_get_mode() -> Mode:
    return db_get("mode")


def db_set_mode(value: Mode):
    return db_set("mode", value)


def db_get_dashboard_type() -> DashboardType:
    return db_get("dashboard_type")


def db_set_dashboard_type(value: DashboardType):
    return db_set("dashboard_type", value)
