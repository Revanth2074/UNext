const axios = require("axios");

const api = axios.create({
    baseURL: "http://localhost:3000/posts",
    headers: {
        "Content-Type": "application/json"
    }
});

module.exports = api;