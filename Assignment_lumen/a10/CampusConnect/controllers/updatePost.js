const api = require("../services/api");

async function updatePost(id) {

    try {

        const currentPost = await api.get(`/${id}`);

        const updatedPost = {
            ...currentPost.data,
            content: "Morning workout completed successfully!",
            category: "Health & Fitness",
            likes: currentPost.data.likes + 10
        };

        await api.put(`/${id}`, updatedPost);

        console.log("\nPost Updated Successfully");

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = updatePost;