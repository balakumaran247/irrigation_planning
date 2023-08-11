// Wait for the DOM content to be loaded
document.addEventListener("DOMContentLoaded", function() {
    // Initialize the map
    var map = L.map('map').setView([16, 77], 9);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
        maxZoom: 19
    }).addTo(map);

    // Fetch the GeoJSON data from Flask and add it to the map
    fetch('/fc/raichur')
        .then(response => response.json())
        .then(data => {
            L.geoJSON(data).addTo(map);
        })
        .catch(error => {
            console.error("Error fetching GeoJSON:", error);
        });

    // Fetch the Earth Engine raster URL from Flask and add it to the map
    fetch('/image/')
        .then(response => response.json())
        .then(data => {
            L.tileLayer(data.url).addTo(map)
        })
        .catch(error => {
            console.error("Error fetching Earth Engine raster URL:", error);
        });

    fetch(`/area?name=${encodeURIComponent('raichur')}&ctype=${encodeURIComponent('total')}`)
        .then(response => response.json())
        .then(data => {
            // Update the content of the <p> tag with the received data
            const paragraph = document.getElementById('ag_area');
            total_ag_area = data.area
            paragraph.textContent = total_ag_area; // Assuming the backend returns an object with a "message" property
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    // Reference to the content <div> element
    var contentDisplay = document.getElementById('content-display');

    async function ag_area(name, ctype) {
        try{
            let response = await fetch(`/area?name=${encodeURIComponent(name)}&ctype=${encodeURIComponent(ctype)}`);
            let data = await response.json();
            let val = data.area;
            let ele = document.getElementById(ctype)
            ele.textContent = val
        } catch(error) {
                console.error('Error fetching data:', error);
                let ele = document.getElementById(ctype);
                ele.textContent = 'Failed'
        };
    }

    const reset_content = () => {
        document.getElementById('land-content').style.display = 'none'
        document.getElementById('livestock-content').style.display = 'none'
        document.getElementById('water-content').style.display = 'none'
        document.getElementById('soil-content').style.display = 'none'
    };
    
    // Event listener for Button 1
    document.getElementById('land-btn').addEventListener('click', function() {
        const land_ag_content = document.getElementById('land-content')
        reset_content()
        if (land_ag_content.style.display === 'none' || land_ag_content.style.display === ''){
            land_ag_content.style.display = 'block';
        }
    });

    for (const param of ['single', 'double', 'triple', 'total']) {
        ag_area('', param)
    }

    // Event listener for Button 2
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

});

document.addEventListener("DOMContentLoaded", function() {
    // Previous code ...

    var ctx = document.getElementById('myChart').getContext('2d');
    
    var chart = new Chart(ctx, {
        type: 'bar', // You can change the type to 'line', 'pie', etc.
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

