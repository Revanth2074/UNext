const api = require("../services/api");

async function getSinglePost(id) {

    try {

        const response = await api.get(`/${id}`);

        const post = response.data;

        console.log("\n========== SINGLE POST ==========\n");

        console.log("ID       :", post.id);
        console.log("Username :", post.username);
        console.log("Content  :", post.content);
        console.log("Category :", post.category);
        console.log("Likes    :", post.likes);
        console.log("Hashtag  :", post.hashtags);

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = getSinglePost;