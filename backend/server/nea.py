import requests
from typing import Final, Literal, TypedDict

NEA_24H_FORECAST_API_URL: Final[str] = (
    "https://api-open.data.gov.sg/v2/real-time/api/twenty-four-hr-forecast"
)

WeatherStr = Literal[
    "Windy",
    "Fair",
    "Fair (Day)",
    "Fair (Night)",
    "Misty",
    "Mist",
    "Hazy",
    "Fair & Warm",
    "Slightly Hazy",
    "Overcast",
    "Cloudy",
    "Partly Cloudy",
    "Partly Cloudy (Day)",
    "Partly Cloudy (Night)",
    "Sunny",
    "Strong Winds",
    "Windy, Cloudy",
    "Windy, Fair",
    "Light Rain",
    "Drizzle",
    "Light Showers",
    "Passing Showers",
    "Showers",
    "Heavy Thundery Showers with Gusty Winds",
    "Heavy Rain",
    "Heavy Showers",
    "Moderate Rain",
    "Strong Winds, Showers",
    "Strong Winds, Rain",
    "Thundery Showers",
    "Windy, Rain",
    "Windy, Showers",
    "Heavy Thundery Showers",
    "Snow",
    "Snow Showers",
]
Forecast = tuple[str, WeatherStr]


class TimePeriod(TypedDict, total=False):
    text: str


class RegionForecast(TypedDict):
    text: WeatherStr


class Regions(TypedDict, total=False):
    central: RegionForecast


class Period(TypedDict, total=False):
    timePeriod: TimePeriod
    regions: Regions


class WeatherForecast(TypedDict):
    temperature: str
    periods: tuple[tuple[str, str], ...]


TIMING_STRINGS: Final = ("6am - 12pm", "12pm - 6pm", "6pm - 12am")


def get_timing_str(timing_text: str):
    timing_text = timing_text.lower()
    if timing_text.startswith("6 am"):
        return TIMING_STRINGS[0]
    elif timing_text.startswith("6 pm"):
        return TIMING_STRINGS[2]
    return TIMING_STRINGS[1]


def get_forecast_emoji(forecast_text: str):
    mappings = (
        (
            "🌬️",
            (
                "Windy",
                "Strong Winds",
                "Windy, Cloudy",
                "Windy, Fair",
            ),
        ),
        ("☀️", ("Fair", "Fair (Day)", "Sunny")),
        (
            "☁️",
            (
                "Overcast",
                "Cloudy",
                "Partly Cloudy",
                "Partly Cloudy (Day)",
                "Partly Cloudy (Night)",
            ),
        ),
        (
            "🌧️",
            (
                "Light Rain",
                "Drizzle",
                "Light Showers",
                "Passing Showers",
                "Showers",
                "Heavy Thundery Showers with Gusty Winds",
                "Heavy Rain",
                "Heavy Showers",
                "Moderate Rain",
                "Strong Winds, Showers",
                "Strong Winds, Rain",
                "Thundery Showers",
                "Windy, Rain",
                "Windy, Showers",
                "Heavy Thundery Showers",
                "Snow",
                "Snow Showers",
            ),
        ),
    )
    for emoji, matches in mappings:
        if forecast_text in matches:
            return emoji
    return "❓"


def get_weather_forecast() -> WeatherForecast | None:
    try:
        response = requests.get(NEA_24H_FORECAST_API_URL)
        response.raise_for_status()

        data = response.json()

        if (
            data["data"]
            and data["data"]["records"]
            and len(data["data"]["records"]) > 0
        ):
            record = data["data"]["records"][0]
            time_periods: list[Period] = record["periods"]
            if len(time_periods) == 3:
                periods = tuple(
                    (
                        get_timing_str(period["timePeriod"]["text"]),
                        get_forecast_emoji(period["regions"]["central"]["text"]),
                    )
                    for period in time_periods
                )
                return dict(
                    temperature=f"{record["general"]["temperature"]["low"]} - {record["general"]["temperature"]["high"]}°C",
                    periods=periods,
                )
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing response: {e}")
        return None
