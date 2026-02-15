from __future__ import annotations

import csv
from typing import List
from scenario_schema import StationInput


def load_stations_from_csv(csv_path: str) -> List[StationInput]:
    stations: List[StationInput] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Expected columns: Station Code,Station Name,Platform Count,Track Availability,Halt Time (mins)
            code = row.get("Station Code") or row.get("code") or ""
            name = row.get("Station Name") or code
            platform_count = int(row.get("Platform Count", 0) or 0)
            halt_time_str = row.get("Halt Time (mins)") or row.get("halt") or "0"
            try:
                halt_time = float(halt_time_str)
            except ValueError:
                halt_time = 0.0
            stations.append(
                StationInput(
                    station_id=name,
                    platform_count=platform_count,
                    platform_length_m=600.0,
                    halt_time_min=halt_time,
                    station_priority="major_junction" if platform_count >= 8 else "small_station",
                )
            )
    return stations




