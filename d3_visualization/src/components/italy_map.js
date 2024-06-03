import { FileAttachment } from "components";
import * as d3 from "d3";

// Leggi il file CSV dei terremoti.
const response = await fetch("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson");
if (!response.ok) throw new Error(`fetch failed: ${response.status}`);
const collection = await response.json();

// Convert to an array of objects.
const features = collection.features.map((f) => ({
    magnitude: f.properties.mag,
    longitude: f.geometry.coordinates[0],
    latitude: f.geometry.coordinates[1]
  }));

process.stdout.write(csvFormat(features));
const quakes = FileAttachment("quakes.csv").csv({typed: true});

Plot.plot({
    projection: {
      type: "orthographic",
      rotate: [110, -30]
    },
    marks: [
      Plot.graticule(),
      Plot.sphere(),
      Plot.geo(land, {stroke: "var(--theme-foreground-faint)"}),
      Plot.dot(quakes, {x: "longitude", y: "latitude", r: "magnitude", stroke: "#f43f5e"})
    ]
  })