const api = require("../services/api");

async function searchContent(keyword) {

    try {

        const response = await api.get(`/?q=${keyword}`);

        console.log(`\n===== SEARCH RESULT : ${keyword} =====\n`);

        response.data.forEach(post => {

            console.log("----------------------------------------");
            console.log("Username :", post.username);
            console.log("Content  :", post.content);
            console.log("Category :", post.category);
            console.log("Likes    :", post.likes);

        });

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = searchContent;