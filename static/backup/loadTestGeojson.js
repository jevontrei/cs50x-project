// Load and display the GeoJSON file
// fetch() returns a promise
// .then() always returns a promise
fetch('/static/backup/test.geojson')  // load my test geojson file; returns a response object
    .then(response => response.json())  // convert fetch() response object body text to js object (a data structure in memory), not json (a text format); the actual data is still structured according to geojson spec
    .then(data => {
        // geoJSON() parses geojson data / creates a geojson layer
        L.geoJSON(data, {
            style: function (feature) {
                return { color: feature.properties.color };
            }
        }).addTo(map).bindPopup(function (layer) {  // bindPopup() enables clicking behaviour/interactivity; `layer` automatically refers to the individual feature layer that was clicked; the one just created with geoJSON()
            return layer.feature.properties.name;  // this just shows the name of a thing when the user clicks on it
        });
    });