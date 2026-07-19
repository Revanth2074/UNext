const api = require("../services/api");

async function deletePost(id) {

    try {

        await api.delete(`/${id}`);

        console.log("\nPost Deleted Successfully");

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = deletePost;