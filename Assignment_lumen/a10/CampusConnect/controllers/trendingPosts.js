const api = require("../services/api");

async function trendingPosts() {

    try {

        const response = await api.get("/?_sort=likes&_order=desc&_limit=3");

        console.log("\n===== TOP 3 TRENDING POSTS =====\n");

        response.data.forEach(post => {

            console.log("----------------------------------------");
            console.log("Username :", post.username);
            console.log("Likes    :", post.likes);
            console.log("Content  :", post.content);

        });

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = trendingPosts;