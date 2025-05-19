//do after content is loaded
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
    // Reset button
    if (resetBtn) {
    resetBtn.addEventListener("click", resetFilter);
    }
    // Filter by location and radius button
    toggleBtn.addEventListener("click", () =>{
        //make it appear and disappear
        const isVisible = dropdown.style.display ==="block";
        dropdown.style.display = isVisible ? "none" : "block";

        if (!isVisible && !autocompleteEl){
            autocompleteEl= new google.maps.places.PlaceAutocompleteElement();
          
            autocompleteEl.includedPrimaryTypes = ["locality", "sublocality"]; //include cities and boroughs
            //bias towards places close to London
            autocompleteEl.locationBias = {
                radius: 50000,
                center: { lat: 51.5074, lng: -0.1272 }
            };
        
            autocompleteContainer.appendChild(autocompleteEl); //adding the autocomplete search to the autocomplete div container
            
            autocompleteEl.addEventListener('gmp-select', async({placePrediction}) =>{
                // google map's autocomplete functionality
                const place = placePrediction.toPlace();
                await place.fetchFields({ fields: ['displayName', 'formattedAddress', 'location']});
                const name= place.displayName ?? place.formattedAddress ?? "Unknown";
                const lat = place.location?.lat?.() ?? null;
                const lng = place.location?.lng?.() ?? null;
                const radius = parseFloat(radiusSlider.value);
            
                if (lat && lng){ //make sure location exists just in case
                    console.log(`City: ${name}, Latitude: ${lat}, Longitude: ${lng}, Radius: ${radius} km`);
                    makeCircle(name, radius, lat,lng); // make filter circle
                    filterEvents(name, radius, lat, lng); // filter by location
                    closeMenu(dropdown, autocompleteEl); //close the menu when filter has been chosen
                    autocompleteEl=null; //clear the search bar
                } else{
                    console.log("No valid location returned for place.");
                }
            });
        }
    });

    radiusSlider.addEventListener("input", () => { //radius slider for the circle filter
        radiusValue.textContent = radiusSlider.value;
    })

    document.addEventListener("click", (event) => {
        const isInsideDropdown = dropdown.contains(event.target);
        const isToggleButton = toggleBtn.contains(event.target);
    
        // closes the filter menu if pressed the button or the main page
        if (!isInsideDropdown && !isToggleButton) {
            closeMenu(dropdown, autocompleteEl);
            autocompleteEl=null;
        }
    });
    
    function filterEvents(city, radiuskm, lat, lng){
        console.log(`Filtering out venues outside the circle centered at ${city} (${lat}, ${lng}) with a radius of ${radiuskm} km.`);
        const center = new google.maps.LatLng(lat,lng);
        const radius = radiuskm *1000;

        const venueMap = window.VENUE_EVENT_OBJ; //window to the object that associates Venue with events and markers
        const map = window.ARTIST_MAP;

        if (!venueMap || ! map) return; //hide everything
        document.querySelectorAll(".event-card, .venue-card, .artist-card").forEach(el => {
            el.style.display = "none";
        });
        if (window.ARTIST_MARKERS){
            window.ARTIST_MARKERS.forEach(marker => marker.map = null);
        }

        for (const  venueData of Object.values(venueMap)){ 
            const venueLatLng = new google.maps.LatLng(venueData.lat, venueData.lng);
            const distance = google.maps.geometry.spherical.computeDistanceBetween(center, venueLatLng); //distance between center of the circle and venue
            const isInside = distance <= radius;
            if (!isInside) continue; //if not inside ignore

            if (venueData.card) { //only show cards and markers within the circle
                venueData.card.style.display = "inline-block";
            }
            venueData.events.forEach(({eventCard, artistCards, marker}) => {
                if (eventCard) eventCard.style.display = "inline-block";
                if (marker) marker.map = window.ARTIST_MAP;
                artistCards.forEach(artistCard =>{
                    if(artistCard) artistCard.style.display="inline-block";
                });
            })

        }
    }
    function closeMenu(dropdown, autocompleteEl){ 
        dropdown.style.display = "none";
        if (autocompleteEl) autocompleteEl.remove();
        

    }
    function makeCircle(city, radius, lat, lng) { //make filter circle in map
        console.log(`Making cirlce in ${city} (${lat}, ${lng}) with a radius of ${radius} km.`);
        
        const map = window.ARTIST_MAP;
        const center = {lat, lng};
        const zoom = Math.floor(14 - Math.log2(radius));//zoom is relative to radius input by the user

        map.panTo(center);
        map.setZoom(zoom);

        if (window.ARTIST_CIRCLE){
            window.ARTIST_CIRCLE.setMap(null);
        }
        window.ARTIST_CIRCLE = new google.maps.Circle({
            strokeColor:"#000000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#000000",    
            fillOpacity: 0.10,      
            map,
            center,
            radius: radius * 1000, 
            })
    }
    function resetFilter() {
        const map = window.ARTIST_MAP;
        const venueMap = window.VENUE_EVENT_OBJ;
    
        if (!map || !venueMap) return;
    
        // Restore all cards
        document.querySelectorAll(".event-card, .venue-card, .artist-card").forEach(el => {
            el.style.display = "inline-block";
        });
    
        // Restore all markers
        if (window.ARTIST_MARKERS) {
            window.ARTIST_MARKERS.forEach(marker => marker.map = map);
        }
    
        // Delete circle
        if (window.ARTIST_CIRCLE) {
            window.ARTIST_CIRCLE.setMap(null);
            window.ARTIST_CIRCLE = null;
        }
    
        // Reset radius slider
        const radiusSlider = document.getElementById("radius-slider");
        const radiusValue = document.getElementById("radius-value");
        if (radiusSlider && radiusValue) {
            radiusSlider.value = 10;
            radiusValue.textContent = "10";
        }
    }
    });