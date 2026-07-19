const api = require("../services/api");

async function latestPosts() {

    try {

        const response = await api.get("/?_sort=id&_order=desc&_limit=5");

        console.log("\n===== LATEST POSTS =====\n");

        response.data.forEach(post => {

            console.log("----------------------------------------");
            console.log("ID       :", post.id);
            console.log("Username :", post.username);
            console.log("Content  :", post.content);

        });

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = latestPosts;