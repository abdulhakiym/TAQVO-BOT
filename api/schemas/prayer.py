"""Pydantic schemas for prayer time responses."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PrayerTimings(BaseModel):
    """Daily prayer times."""

    fajr: str
    dhuhr: str
    asr: str
    maghrib: str
    isha: str
    sunrise: str | None = None


class PrayerCoordinates(BaseModel):
    """Geographical coordinates."""

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class PrayerMetadata(BaseModel):
    """Prayer calculation metadata."""

    calculation_method: dict[str, Any] = Field(
        default_factory=dict
    )
    madhhab: str
    madhhab_name: str
    asr_school: str
    source: str
    updated_at: str


class PrayerTimesResponse(BaseModel):
    """Complete daily prayer times response."""

    model_config = ConfigDict(extra="ignore")

    success: bool
    date: str
    timezone: str
    coordinates: PrayerCoordinates
    timings: PrayerTimings
    sunrise: str | None = None
    hijri: dict[str, Any] = Field(default_factory=dict)
    meta: PrayerMetadata
