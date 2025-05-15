document.addEventListener("DOMContentLoaded", async function() {
    const map_element = document.getElementById("artist-events-map")
    const markers = window.ARTIST_EVENTS;

    if (!map_element || !markers || markers.length === 0) return;

    const { Map} = await google.maps.importLibrary("maps");
    const {AdvancedMarkerElement} = await google.maps.importLibrary("marker")
    const bounds = new google.maps.LatLngBounds();
    const map = new Map(map_element, {
        zoom:5,
        center: { lat: 54.5, lng: -3.4 },
        mapId:"5cc32464b18b967d5f101816"
    });

    markers.forEach(({ lat, lng, title, venue, date }) => {
        const position = {lat, lng};
        bounds.extend(position);

        new AdvancedMarkerElement({
            map,
            position, 
            title: `${title} @ ${venue} (${date})`
        });
    });
    if (markers.length === 1) {
        const { lat, lng } = markers[0];
        map.setCenter({ lat, lng });
        map.setZoom(10);
      } else {
        map.fitBounds(bounds, { top: 50, bottom: 50, left: 50, right: 50 });
      }
});