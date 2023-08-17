// Wait for the DOM content to be loaded
document.addEventListener("DOMContentLoaded", function() {
    // Initialize the map
    var map = L.map('map').setView([16, 77], 9);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
        maxZoom: 19
    }).addTo(map);

    // Fetch the Raichur GeoJSON data from Flask and add it to the map
    fetch('/fc/raichur')
        .then(response => response.json())
        .then(data => {
            L.geoJSON(data, {
                style: function () {
                    return {
                        fillColor: 'blue',
                        fillOpacity: 0.0, 
                        color: 'black',
                        weight: 2
                    };
                }
            }).addTo(map);
        })
        .catch(error => {
            console.error("Error fetching GeoJSON:", error);
        });
    
    // display the Raichur CCA boundary in Map
    fetch('/fc/raichurCCA')
        .then(response => response.json())
        .then(data => {
            L.geoJSON(data, {
                style: function () {
                    return {
                        fillColor: 'blue',
                        fillOpacity: 0.4, 
                        color: 'blue',
                        weight: 2
                    };
                }
            }).addTo(map);
        })
        .catch(error => {
            console.error("Error fetching GeoJSON:", error);
        });

    // Fetch the Earth Engine raster URL Raichur LULC from Flask and add to map
    fetch('/image/')
        .then(response => response.json())
        .then(data => {
            L.tileLayer(data.url).addTo(map)
        })
        .catch(error => {
            console.error("Error fetching Earth Engine raster URL:", error);
        });

    // Total Agricultural Area of Raichur
    // fetch(`/area?name=${encodeURIComponent('raichur')}&ctype=${encodeURIComponent('total')}`)
    //     .then(response => response.json())
    //     .then(data => {
    //         // Update the content of the <p> tag with the received data
    //         const paragraph = document.getElementById('ag_area');
    //         total_ag_area = data.area
    //         paragraph.textContent = total_ag_area; // Assuming the backend returns an object with a "message" property
    //     })
    //     .catch(error => {
    //         console.error('Error fetching data:', error);
    //     });

    // function to fetch data for scenarios
    async function scenario_data(name) {
        try{
            let response = await fetch(`/scenario?name=${encodeURIComponent(name)}`);
            let data = await response.json();
            return data;
        } catch(error) {
                console.error('Error fetching data:', error);
                return null;
        };
    }

    // function to reset the display of the central grid
    const reset_content = () => {
        document.getElementById('land-content').style.display = 'none'
        document.getElementById('livestock-content').style.display = 'none'
        document.getElementById('water-content').style.display = 'none'
        document.getElementById('soil-content').style.display = 'none'
    };
    
    // Event listener for Land button
    document.getElementById('land-btn').addEventListener('click', function() {
        const land_ag_content = document.getElementById('land-content')
        reset_content()
        if (land_ag_content.style.display === 'none' || land_ag_content.style.display === ''){
            land_ag_content.style.display = 'block';
        }
    });

    // Event listener for Livestock button
    document.getElementById('livestock-btn').addEventListener('click', function() {
        const land_ag_content = document.getElementById('livestock-content')
        reset_content()
        if (land_ag_content.style.display === 'none' || land_ag_content.style.display === ''){
            land_ag_content.style.display = 'block';
        }
    });

    document.getElementById('water-btn').addEventListener('click', function() {
        const land_ag_content = document.getElementById('water-content')
        reset_content()
        if (land_ag_content.style.display === 'none' || land_ag_content.style.display === ''){
            land_ag_content.style.display = 'block';
        }
    });

    document.getElementById('soil-btn').addEventListener('click', function() {
        const land_ag_content = document.getElementById('soil-content')
        reset_content()
        if (land_ag_content.style.display === 'none' || land_ag_content.style.display === ''){
            land_ag_content.style.display = 'block';
        }
    });

    async function update_data(data) {
        console.log(`${data.hasOwnProperty('k_area')}`);
        const keys = ['k_area', 'r_area'];
        for (const key of keys) {
            console.log(`Key: ${key}`);
            if (data.hasOwnProperty(key)) {
                const value = data[key];
                let ele = document.getElementById(key);
                console.log(`Key: ${key}, Value: ${value}`);
                ele.textContent = value;
            }
        }
    }

    document.getElementById('baseline-btn').addEventListener('click', async function() {
        let data = await scenario_data('baseline');
        console.log(`${data}`);
        update_data(data);
    });
});

