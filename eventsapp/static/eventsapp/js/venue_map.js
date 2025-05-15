document.addEventListener("DOMContentLoaded", async function (){
    const map_element = document.getElementById("map");
    if (!map_element) return;

    const lat = parseFloat(map_element.dataset.lat);
    const lng = parseFloat(map_element.dataset.lng);
    const title = map_element.dataset.title
    position = { lat, lng };

    if (isNaN(lat) || isNaN(lng)) return;
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    map = new Map(map_element, {
        zoom: 11,
        center: position,
        mapId:"5cc32464b18b967d5f101816"
    });
    const marker = new AdvancedMarkerElement({
        map:map,
        position: position,
        title: title
    });

});