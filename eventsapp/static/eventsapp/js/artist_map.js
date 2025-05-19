document.addEventListener("DOMContentLoaded", async function() {
    const map_element = document.getElementById("artist-events-map")
    const markers = window.ARTIST_EVENTS;
    window.VENUE_EVENT_OBJ = {}; 
    
    
    if (!map_element || !markers || markers.length === 0) return;

    const { Map} = await google.maps.importLibrary("maps");
    const {AdvancedMarkerElement} = await google.maps.importLibrary("marker")
    const bounds = new google.maps.LatLngBounds();
    const infoWindow = new google.maps.InfoWindow({
        content:""
    });
    const map = new Map(map_element, {  //map set up centered in the UK
        zoom:5,
        center: { lat: 54.5, lng: -3.4 },
        mapId:"5cc32464b18b967d5f101816"
    });
    window.ARTIST_MAP = map;
    window.ARTIST_CIRCLE = null;

    markers.forEach(({ lat, lng, title, venue, date, price, image,id, venue_id, artist_ids}) => {
        const position = {lat, lng}; 
        bounds.extend(position); // expand bounds to include marker
        const eventDate = new Date(date);
        const formattedDate = eventDate.toISOString().split("T")[0]; //formatting date and time to be more legible 
        const formattedTime = eventDate.toTimeString().split(":").slice(0, 2).join(":");


        const marker = new AdvancedMarkerElement({  //marker creation
            map,
            position, 
            gmpClickable: true,
            title: `${title} @ ${venue} (${date})`
        });
        const artistCards = []; //Selecting the cards
        artist_ids.forEach(artist_id => {
            const card = document.querySelector(`.artist-card[data-artist-id="${artist_id}"]`);
            if (card) {
                artistCards.push(card);
            }
        });
        const eventCard = document.querySelector(`.event-card[data-event-id="${id}"]`);
        const venueCard = document.querySelector(`.venue-card[data-venue-id="${venue_id}"]`);

        if (!window.VENUE_EVENT_OBJ[venue_id]){ //Defining the object that associates venues with events, markers and artists
            window.VENUE_EVENT_OBJ[venue_id] ={// This is done to help with filtering
                lat,
                lng,
                card: venueCard,
                events:[]
            };
        }
        window.VENUE_EVENT_OBJ[venue_id].events.push({
            eventCard: eventCard,
            artistCards: artistCards,
            marker:marker
        });

        if (!window.ARTIST_MARKERS) window.ARTIST_MARKERS = []; // events can have multiple artists
            window.ARTIST_MARKERS.push(marker);
        
        marker.addEventListener("gmp-click", () => { //adding an infowindow for when you click on a marker
            
            map.panTo(position);
            map.setZoom(12);
            const content = `
                <a href="${EVENT_DETAIL_URL}${id}" class="event-card-link">
                <div class="event-card">
                ${image ? `<img src="${image}" alt="${title}" class="info-window-image">` : ""}
                    <h3>${title}</h3>
                    <p> ${venue}</p>
                    <p>${formattedDate} ${formattedTime}</p>
                    <p> £${price} </p>
                </div>
                </a>
            `;
            console.log("Info Window Content:", content);
            infoWindow.setContent(content); // Set the content of the info window
            infoWindow.open(map, marker); // Open the info window on the marker
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