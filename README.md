# How Many Data Centers?

A minimal, interactive white globe of publicly mapped data center locations, built with [Three.js](https://threejs.org/).

## Deploy on Render

1. In Render, select **New → Static Site**.
2. Connect `tinnei/howmanydatacenters`.
3. Branch: `main`; Build command: `echo "No build required"`; Publish directory: `.`.
4. Deploy. The `render.yaml` also describes these settings for Render Blueprint deployment.

## Data

The page fetches [Data Center Atlas](https://github.com/kiankyars/datacenter-atlas) `sites.geojson` when the page opens. The browser can reuse the response according to the publisher's cache headers. Site names and location markers come from that dataset; its authored data is licensed CC BY 4.0, with third-party materials retaining their respective terms. Atlas documentation explains the data's source coverage and varying coordinate precision.

The globe loads a precomputed, compressed asset built from [datasets/geo-countries](https://github.com/datasets/geo-countries). To regenerate it, run `python scripts/prepare-land.py countries.geojson` with Python GDAL bindings installed. Bump the version in the asset filename, the script, and the page's fetch URL when publishing a replacement so returning visitors get the new asset.

The number at upper right is **mapped site records loaded**, not the world's total operating data centers. Dataset includes records spanning multiple development stages, and coverage is incomplete. No sample points are fabricated if the source is unavailable.

## Local use

Serve the repository with any static HTTP server (for example `python3 -m http.server 8000`), then open `http://localhost:8000`. Three.js and present-day site data load over the internet.

## Interface

Drag to rotate, scroll/pinch to zoom, and click a dot to see its name, reported lifecycle status and observation date (when provided). Press Escape to dismiss. Automatic rotation is disabled when the visitor prefers reduced motion. Rotate toward a continent to explore its sites, or use the list icon to browse them.

Blue markers mean at least one project at the site is reported operational; pale blue means a reported pre-operational project stage; gray-blue means no supported classification. These are **last reported statuses**, not live operational verification. A campus with multiple projects is counted once. Completed projects are not assumed operational, and research leads are not treated as construction. The displayed number is the count of mapped site records loaded, not the world's total.
