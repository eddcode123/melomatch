const apiKey = 'afa8075b695333e63279bf9ab0bf8be8';
const url = `https://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key=${apiKey}&format=json`;

async function getTopFive() {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Request to API failed with code ${response.status}`);
        }
        const data = await response.json();

        if (data.artists && data.artists.artist) {
            const artists = data.artists.artist.slice(0, 5).map(artist => artist.name);
            return artists;
        } else {
            throw new Error("Invalid Data format");
        }
    } catch (error) {
        console.error(`Fetch error: ${error}`);
    }
}

async function getArtistImage(artists) {
    try {
        const clientId = "89d183fbb7b24c1c903a9578228937b5";
        const clientSecret = "05a876d25d5741e9a9a9a275c18df22e";
        const basicAuth = btoa(`${clientId}:${clientSecret}`);
        const tokenEndpoint = 'https://accounts.spotify.com/api/token';

        // Obtain access token
        const response = await fetch(tokenEndpoint, {
            method: 'POST',
            headers: {
                'Authorization': `Basic ${basicAuth}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'grant_type=client_credentials'
        });

        if (!response.ok) {
            throw new Error(`Failed to get the access token with code: ${response.status}`);
        }

        const tokenData = await response.json();
        let accessToken = tokenData.access_token;
        let imageUrl = [];

        // Fetch artist data from an array of artist names
        for (let i = 0; i < artists.length; i++) {
            let artistResponse = await fetch(`https://api.spotify.com/v1/search?type=artist&q=${encodeURIComponent(artists[i])}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });
            if (!artistResponse.ok) {
                console.error(`Failed to get artist data for ${artists[i]} with code: ${artistResponse.status}`);
                continue;
            }
            let artistData = await artistResponse.json();

            if (artistData.artists && artistData.artists.items.length > 0) {
                const artist = artistData.artists.items[0];
                if (artist.images && artist.images.length > 0) {
                    imageUrl.push({
                        'name': artist.name,
                        'imgURL': artist.images[0].url // Corrected image property name
                    });
                } else {
                    console.warn(`No image found for ${artist.name}`);
                }
            } else {
                console.warn(`No data found for ${artists[i]}`);
            }
        }

        return imageUrl;
    } catch (error) {
        console.error(`Fetch error: ${error}`);
    }
}

// Call function
getTopFive().then(data => {
    if (data) {
        getArtistImage(data).then(ImageData => {
           let myImages = ImageData.map(artist => artist.imgURL)
           console.log(myImages)
        });
    }
});
