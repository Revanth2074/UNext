const api = require("../services/api");

async function popularPosts() {

    try {

        const response = await api.get("/?likes_gte=100");

        console.log("\n===== POPULAR POSTS =====\n");

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

module.exports = popularPosts;