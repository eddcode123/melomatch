fetch('http://localhost:3000/api/top-artists')
    .then(response => response.json())
    .then(data => {
        // Process the fetched data
        console.log(data); // Example: Log data to console
        // Update UI or perform actions with fetched data
        // Example: Update DOM elements with fetched data
    })
    .catch(error => console.error('Error fetching data:', error));