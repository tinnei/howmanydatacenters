"""Build the globe's static geography from datasets/geo-countries GeoJSON."""

import gzip
import json
import math
from pathlib import Path
import sys

from osgeo import ogr


ROOT = Path(__file__).resolve().parents[1]
LOOKUP = json.loads((ROOT / "data/continents.json").read_text())
NAMES = ("Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America")


def polygons(geometry):
    if geometry.GetGeometryName() == "POLYGON":
        yield geometry
    elif geometry.GetGeometryName() in ("MULTIPOLYGON", "GEOMETRYCOLLECTION"):
        for part in geometry:
            yield from polygons(part)


def ring_coordinates(ring):
    return [(round(x, 5), round(y, 5)) for x, y, *_ in ring.GetPoints()]


def contains(x, y, ring):
    inside = False
    previous = ring[-1]
    for point in ring:
        ax, ay = point
        bx, by = previous
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax:
            inside = not inside
        previous = point
    return inside


def land_points(boundaries):
    for index in range(71):
        lat = -87.5 + 2.5 * index
        step = 2.5 / max(.23, math.cos(math.radians(lat)))
        lon = -180
        while lon < 180:
            for name, rings, (west, east, south, north) in boundaries:
                if (west <= lon <= east and south <= lat <= north
                        and contains(lon, lat, rings[0])
                        and not any(contains(lon, lat, hole) for hole in rings[1:])):
                    yield (round(lon, 5), lat, name)
                    break
            lon += step


def prepare(source):
    countries = ogr.Open(str(source))
    boundaries = []
    country_names = dict(LOOKUP)
    continents = {name: ogr.Geometry(ogr.wkbMultiPolygon) for name in NAMES}
    for feature in countries.GetLayer():
        props = feature.items()
        name = LOOKUP.get((props.get("ISO3166-1-Alpha-2") or "").upper())
        name = name or LOOKUP.get(props.get("name")) or props.get("CONTINENT")
        if name not in continents:
            raise ValueError(f"Missing continent for {props.get('name')}")
        country_names[props["name"]] = name
        geometry = feature.GetGeometryRef()
        for polygon in polygons(geometry):
            boundaries.append((name, [ring.GetPoints() for ring in polygon], polygon.GetEnvelope()))
            if polygon.IsValid():
                continents[name].AddGeometry(polygon)
            else:
                for part in polygons(polygon.MakeValid()):
                    continents[name].AddGeometry(part)

    simplified = {}
    for name, geometry in continents.items():
        dissolved = geometry.UnionCascaded().SimplifyPreserveTopology(.035)
        simplified[name] = [
            [ring_coordinates(ring) for ring in polygon]
            for polygon in polygons(dissolved)
        ]

    return {"polygons": simplified, "points": list(land_points(boundaries)), "countries": country_names}



if __name__ == "__main__":
    ogr.UseExceptions()
    result = prepare(Path(sys.argv[1]))
    payload = json.dumps(result, separators=(",", ":")).encode()
    (ROOT / "data/land-v1.json.gz").write_bytes(gzip.compress(payload, mtime=0))
