// Wait for the DOM content to be loaded
document.addEventListener("DOMContentLoaded", function() {
    // Initialize the map
    var map = L.map('map').setView([16, 77], 9);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
        maxZoom: 19
    }).addTo(map);

    // Fetch the GeoJSON data from Flask and add it to the map
    fetch('/fc/')
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

    // Reference to the content <div> element
    var contentDisplay = document.getElementById('content-display');
    
    // Event listener for Button 1
    document.getElementById('btn1').addEventListener('click', function() {
        contentDisplay.innerHTML = `
            <form>
                <label for="input1-1">Label 1:</label>
                <input type="text" id="input1-1" name="input1-1">
                <!-- Add more input fields as needed -->
                <input type="submit" value="Submit">
            </form>
        `;
    });

    // Event listener for Button 2
    document.getElementById('btn2').addEventListener('click', function() {
        contentDisplay.innerHTML = `
            <form>
                <label for="input2-1">Label A:</label>
                <input type="text" id="input2-1" name="input2-1">
                <!-- Add more input fields as needed -->
                <input type="submit" value="Submit">
            </form>
        `;
    });

    // Add similar event listeners for Button 3 and Button 4 with different form structures if needed...
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

