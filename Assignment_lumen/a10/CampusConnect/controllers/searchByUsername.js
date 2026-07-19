const api = require("../services/api");

async function searchByUsername(username) {

    try {

        const response = await api.get(`/?username=${username}`);

        console.log(`\n===== POSTS BY ${username.toUpperCase()} =====\n`);

        response.data.forEach(post => {
            console.log("----------------------------------------");
            console.log("Username :", post.username);
            console.log("Content  :", post.content);
            console.log("Category :", post.category);
            console.log("Likes    :", post.likes);
            console.log("Hashtag  :", post.hashtags);
        });

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = searchByUsername;