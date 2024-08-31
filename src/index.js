const express = require("express");
const path = require("path");
const collection = require("./config");
const bcrypt = require('bcryptjs');
const axios = require('axios'); // Import axios
const qs = require('querystring'); // For formatting data

const app = express();

// Convert data into JSON format
app.use(express.json());
// Serve static files from the "public" directory
app.use(express.static("public"));

// Parse URL-encoded bodies
app.use(express.urlencoded({ extended: false }));
// Use EJS as the view engine
app.set("view engine", "ejs");

app.get("/", (req, res) => {
    res.render("login", { message: null });
});

app.get("/signup", (req, res) => {
    res.render("signup");
});

// Register User
app.post("/signup", async (req, res) => {
    const data = {
        name: req.body.username,
        password: req.body.password
    };

    const existingUser = await collection.findOne({ name: data.name });

    if (existingUser) {
        res.send('User already exists. Please choose a different username.');
    } else {
        const saltRounds = 10;
        const hashedPassword = await bcrypt.hash(data.password, saltRounds);

        data.password = hashedPassword;
        await collection.insertMany([data]); // Corrected to insert as an array
        res.render("login", { message: "User registered successfully!" });
    }
});

// Login User
app.post("/login", async (req, res) => {
    try {
        const check = await collection.findOne({ name: req.body.username });
        if (!check) {
            return res.send("Username not found");
        }

        const isPasswordMatch = await bcrypt.compare(req.body.password, check.password);
        if (!isPasswordMatch) {
            return res.send("Wrong password");
        } else {
            res.redirect('/top_links');
        }
    } catch (error) {
        console.error(error);
        res.send("Error occurred while processing your request.");
    }
});

// Define a route to render the top_links.ejs page
app.get('/top_links', (req, res) => {
    res.render('top_links', { top_links: [], suggested_keywords: [], error: null });
});

app.post('/top_links', async (req, res) => {
    const { website_url, interest_keyword } = req.body;

    try {
        // Make a POST request to the Flask backend
        const response = await axios.post('http://localhost:8000/', qs.stringify({
            website_url,
            interest_keyword
        }), {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        const top_links = response.data.top_links;
        const suggested_keywords = response.data.suggested_keywords;

        // Render the top_links.ejs page with the fetched data
        res.render('top_links', { top_links, suggested_keywords, error: null });
    } catch (error) {
        console.error('Error fetching data from Flask backend:', error.response ? error.response.data : error.message);
        res.render('top_links', { top_links: [], suggested_keywords: [], error: "Error fetching data from the backend." });
    }
});

// Define Port for Application
const port = 5000;
app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
