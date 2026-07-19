const api = require("../services/api");

async function sortByLikes() {

    try {

        const response = await api.get("/?_sort=likes&_order=desc");

        console.log("\n===== POSTS SORTED BY LIKES =====\n");

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

module.exports = sortByLikes;