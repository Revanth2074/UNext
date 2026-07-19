const api = require("../services/api");

async function createPost() {

    const newPost = {
        username: "sophia",
        content: "Node.js APIs are awesome!",
        category: "Programming",
        likes: 0,
        hashtags: "#nodejs"
    };

    try {

        const response = await api.post("/", newPost);

        console.log("\nPost Created Successfully\n");
        console.log(response.data);

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = createPost;