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
    async function scenario_data(scenario, name) {
        try{
            let response = await fetch(`/scenario?name=${encodeURIComponent(name)}&scenario=${encodeURIComponent(scenario)}`);
            let data = await response.json();
            return data;
        } catch(error) {
                console.error('Error fetching data:', error);
                return null;
        };
    }

    // function to reset the display of the central grid
    const reset_content = () => {
        document.getElementById('default-main').style.display = 'none'
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

    function table_updation(id_name, list_items){
        const tableBody = document.getElementById(id_name);
        tableBody.innerHTML = '';
        for (const [key_element, value_element] of list_items) {
            const row = document.createElement('tr');
            const keyCell = document.createElement('td');
            const valueCell = document.createElement('td');

            keyCell.textContent = key_element;
            valueCell.textContent = value_element;

            row.appendChild(keyCell);
            row.appendChild(valueCell);
            tableBody.appendChild(row);
        }
    }

    async function update_data(data) {
        for (const key in data) {
            if (data.hasOwnProperty(key)) {
                const value = data[key];
                try{
                    if (key === 'k_crops') {
                        table_updation('kharifAreaTableBody', data.k_crops)
                    } else if (key === 'r_crops') {
                        table_updation('rabiAreaTableBody', data.r_crops)
                    } else if (key === 'k_iwr_list') {
                        table_updation('kharifWaterTableBody', data.k_iwr_list)
                    } else if (key === 'r_iwr_list') {
                        table_updation('rabiWaterTableBody', data.r_iwr_list)
                    } else {
                        let ele = document.getElementById(key);
                        ele.textContent = value;
                    }
                } catch(error) {
                    console.error(`Error identifying the key: ${key}`);
                };
            }
        }
    }

    document.getElementById('baseline-btn').addEventListener('click', async function() {
        let data = await scenario_data('baseline', 'raichurCCA');
        update_data(data);
    });
    document.getElementById('scenario1-btn').addEventListener('click', async function() {
        let data = await scenario_data('scenario1', 'raichurCCA');
        update_data(data);
    });
});

