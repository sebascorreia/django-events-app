document.addEventListener("DOMContentLoaded", async function(){
    const radiusSlider=document.getElementById("radius-slider");
    const radiusValue = document.getElementById("radius-value");
    const toggleBtn=document.getElementById("location-filter-btn");
    const dropdown=document.getElementById("location-filter-dropdown");
    const autocompleteContainer = document.getElementById("autocomplete-container");
    const resetBtn = document.getElementById("reset-filter-btn");
    
    let autocompleteEl=null;

    await google.maps.importLibrary("places");
    await google.maps.importLibrary("geometry");

    if (resetBtn) {
    resetBtn.addEventListener("click", resetFilter);
    }

    toggleBtn.addEventListener("click", () =>{
        const isVisible = dropdown.style.display ==="block";
        dropdown.style.display = isVisible ? "none" : "block";

        if (!isVisible && !autocompleteEl){
            autocompleteEl= new google.maps.places.PlaceAutocompleteElement();
          
            autocompleteEl.includedPrimaryTypes = ["locality", "sublocality"];
            autocompleteEl.locationBias = {
                radius: 50000,
                center: { lat: 51.5074, lng: -0.1272 }
            };
        
            autocompleteContainer.appendChild(autocompleteEl);
            
            autocompleteEl.addEventListener('gmp-select', async({placePrediction}) =>{
                const place = placePrediction.toPlace();
                await place.fetchFields({ fields: ['displayName', 'formattedAddress', 'location']});
                const name= place.displayName ?? place.formattedAddress ?? "Unknown";
                const lat = place.location?.lat?.() ?? null;
                const lng = place.location?.lng?.() ?? null;
                const radius = parseFloat(radiusSlider.value);
            
                if (lat && lng){
                    console.log(`City: ${name}, Latitude: ${lat}, Longitude: ${lng}, Radius: ${radius} km`);
                    makeCircle(name, radius, lat,lng);
                    filterEvents(name, radius, lat, lng);
                    closeMenu(dropdown, autocompleteEl);
                    autocompleteEl=null;
                } else{
                    console.log("No valid location returned for place.");
                }
            });
        }
    });

    radiusSlider.addEventListener("input", () => {
        radiusValue.textContent = radiusSlider.value;
    })

    document.addEventListener("click", (event) => {
        const isInsideDropdown = dropdown.contains(event.target);
        const isToggleButton = toggleBtn.contains(event.target);
    
        // If clicked outside both the dropdown and the button, hide it
        if (!isInsideDropdown && !isToggleButton) {
            closeMenu(dropdown, autocompleteEl);
            autocompleteEl=null;
        }
    });
    function filterEvents(city, radiuskm, lat, lng){
        console.log(`Filtering events within the circle centered at ${city} (${lat}, ${lng}) with a radius of ${radiuskm} km.`);
        const center = new google.maps.LatLng(lat,lng);
        const radius = radiuskm *1000;

        const venueMap = window.VENUE_EVENT_OBJ;
        const map = window.ARTIST_MAP;

        if (!venueMap || ! map) return;

        for (const [venueId, venueData] of Object.entries(venueMap)){
            const venueLatLng = new google.maps.LatLng(venueData.lat, venueData.lng);
            const distance = google.maps.geometry.spherical.computeDistanceBetween(center, venueLatLng);
            const isInside = distance <= radius;

            if (venueData.card) {
                venueData.card.style.display = isInside ? "inline-block": "none";
            }
            venueData.events.forEach(({card, marker}) => {
                if (card) card.style.display = isInside ? "inline-block" : "none";
                if (marker) marker.map = isInside ? map : null;
            })

        }
    }
    function closeMenu(dropdown, autocompleteEl){
        dropdown.style.display = "none";
        if (autocompleteEl) autocompleteEl.remove();
        

    }
    function makeCircle(city, radius, lat, lng) {
        console.log(`Making cirlce in ${city} (${lat}, ${lng}) with a radius of ${radius} km.`);
        
        const map = window.ARTIST_MAP;
        const center = {lat, lng};
        const zoom = Math.floor(14 - Math.log2(radius));

        map.panTo(center);
        map.setZoom(zoom);

        if (window.ARTIST_CIRCLE){
            window.ARTIST_CIRCLE.setMap(null);
        }
        window.ARTIST_CIRCLE = new google.maps.Circle({
            strokeColor:"#000000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#000000",   // Black fill
            fillOpacity: 0.10,      // Slightly transparent
            map,
            center,
            radius: radius * 1000, // km → meters
            })
    }
    function resetFilter(){
        const map = window.ARTIST_MAP;
        const venueMap = window.VENUE_EVENT_OBJ;

        if (!map || !venueMap) return;

        for (const venueData of Object.values(venueMap)){
            if (venueData.card) {
                venueData.card.style.display = "inline-block";
            }
            venueData.events.forEach(({ card, marker}) => {
                if (card) card.style.display = "inline-block";
                if (marker) marker.map = map;
            });
        }
        if (window.ARTIST_CIRCLE) {
            window.ARTIST_CIRCLE.setMap(null);
            window.ARTIST_CIRCLE = null;
        }
        const radiusSlider = document.getElementById("radius-slider");
        const radiusValue = document.getElementById("radius-value");
        if (radiusSlider && radiusValue) {
            radiusSlider.value = 10;
            radiusValue.textContent = "10";
        }
    }
    });