const api = require("../services/api");

async function getAllPosts() {
    try {
        const response = await api.get("/");

        console.log("\n========== ALL POSTS ==========\n");

        response.data.forEach(post => {
            console.log("----------------------------------------");
            console.log("Username :", post.username);
            console.log("Content  :", post.content);
            console.log("Category :", post.category);
            console.log("Likes    :", post.likes);
            console.log("Hashtag  :", post.hashtags);
        });

        console.log("----------------------------------------");

    } catch (error) {
        console.log("Error :", error.message);
    }
}

module.exports = getAllPosts;