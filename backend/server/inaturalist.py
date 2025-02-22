import requests
import os
import logging
from typing import TypedDict, Optional, Final
import re
from random import choice
import traceback

INAT_API_URL: Final[str] = os.environ.get("INAT_API_URL", "")


class Observation(TypedDict):
    common_name: Optional[str]
    scientific_name: Optional[str]
    location: str
    timestamp: Optional[str]
    photo_url: str
    licence_str: str


def parse_observation(raw_observation) -> Optional[Observation]:
    scientific_name = raw_observation["taxon"].get("name", None)
    common_name_obj = raw_observation["taxon"].get("common_name", {})
    common_name = common_name_obj.get("name", None) if common_name_obj else None
    observation_photos = raw_observation["photos"]

    if len(observation_photos) == 0:
        return None

    return dict(
        common_name=common_name,
        scientific_name=scientific_name,
        location=raw_observation["place_guess"],
        timestamp=raw_observation["observed_on_string"] or None,
        photo_url=re.sub(
            r"large(\.jpe?g)$", r"original\1", observation_photos[0]["large_url"]
        ),
        licence_str=f"©️ {raw_observation["user_login"]}, {raw_observation["license"]}",
    )


def get_observations() -> list[Observation]:
    try:
        if len(INAT_API_URL) == 0:
            raise ValueError("INAT_API_URL not specified")

        response = requests.get(INAT_API_URL)
        response.raise_for_status()

        data = response.json()

        if len(data) > 0:
            return [
                obs
                for obs in (
                    parse_observation(raw_observation) for raw_observation in data
                )
                if obs is not None
            ]
        else:
            raise ValueError("No observations retrieved")

    except Exception as e:
        logging.error(
            f"Error fetching from iNaturalist API: {e} {traceback.format_exc()}"
        )
        return []


def get_random_observation() -> Observation:
    all_observations = get_observations()
    return choice(all_observations)
