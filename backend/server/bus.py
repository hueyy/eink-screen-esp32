import requests
from datetime import datetime
from typing import Literal, Final
import os
import logging

LTA_API_URL: Final[str] = (
    "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival"
)

ETASource = Literal[
    # whether based on bus schedule or bus location
    "Estimated",
    "Location",
]


def get_relative_arrival_timing(timestamp: str) -> int:
    estimated_time = datetime.fromisoformat(timestamp)
    current_time = datetime.now(estimated_time.tzinfo)
    minutes = int((estimated_time - current_time).total_seconds() / 60)
    return minutes


def get_bus_arrival_timings(
    bus_stop_code: str, service_number: str
) -> tuple[int, ETASource] | tuple[None, None]:
    params = {"BusStopCode": bus_stop_code, "ServiceNo": service_number}
    headers = {"AccountKey": os.environ.get("LTA_API_KEY")}

    try:
        response = requests.get(LTA_API_URL, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        if data["Services"] and len(data["Services"]) > 0:
            next_bus = data["Services"][0]["NextBus"]
            estimated_arrival: str = next_bus["EstimatedArrival"]
            relative_estimated_arrival = get_relative_arrival_timing(estimated_arrival)
            monitored: Literal[0, 1] = next_bus["Monitored"]
            eta_source: ETASource = "Estimated" if monitored == 0 else "Location"

            return relative_estimated_arrival, eta_source
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error making request: {e}")
        return None, None
    except KeyError as e:
        logging.error(f"Error parsing response: {e}")
        return None, None


BUS_NUMBER: Final[str] = os.environ.get("BUS_NUMBER", "")
BUS_STOP_1: Final[str] = os.environ.get("BUS_STOP_1_ID", "")
BUS_STOP_2: Final[str] = os.environ.get("BUS_STOP_2_ID", "")


def get_bus_data():
    return dict(
        bus_number=BUS_NUMBER,
        bus_stop_1=get_bus_arrival_timings(BUS_STOP_1, BUS_NUMBER),
        bus_stop_2=get_bus_arrival_timings(BUS_STOP_2, BUS_NUMBER),
    )
