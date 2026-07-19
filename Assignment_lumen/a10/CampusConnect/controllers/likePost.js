const api = require("../services/api");

async function likePost(id) {

    try {

        // Fetch post
        const response = await api.get(`/${id}`);

        const post = response.data;

        console.log("\n===== LIKE POST =====");
        console.log("Before Likes :", post.likes);

        // Increase likes
        post.likes++;

        // Update post
        await api.put(`/${id}`, post);

        console.log("After Likes  :", post.likes);

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = likePost;