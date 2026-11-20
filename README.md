# How Many Data Centers?

A minimal, interactive white globe of publicly mapped data center locations, built with [Three.js](https://threejs.org/).

## Deploy on Render

1. In Render, select **New → Static Site**.
2. Connect `tinnei/howmanydatacenters`.
3. Branch: `main`; Build command: `echo "No build required"`; Publish directory: `.`.
4. Deploy. The `render.yaml` also describes these settings for Render Blueprint deployment.

## Data

The page fetches [Data Center Atlas](https://github.com/kiankyars/datacenter-atlas) `sites.geojson` from its publicly hosted latest download when a visitor opens the page. Site names and location markers come from that dataset; its authored data is licensed CC BY 4.0, with third-party materials retaining their respective terms. Atlas documentation explains the data's source coverage and varying coordinate precision. Country outlines are from [datasets/geo-countries](https://github.com/datasets/geo-countries).

The number at upper right is **mapped site records loaded**, not the world's total operating data centers. Dataset includes records spanning multiple development stages, and coverage is incomplete. No sample points are fabricated if the source is unavailable.

## Local use

Serve the repository with any static HTTP server (for example `python3 -m http.server 8000`), then open `http://localhost:8000`. Three.js, country outlines and site data load over the internet.

## Interface

Drag to rotate, scroll/pinch to zoom, click a data-center dot to see its public name and location. This first release deliberately avoids dashboards and filters.
