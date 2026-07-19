const api = require("../services/api");

async function filterByCategory(category) {

    try {

        const response = await api.get(`/?category=${category}`);

        console.log(`\n===== ${category.toUpperCase()} POSTS =====\n`);

        response.data.forEach(post => {

            console.log("----------------------------------------");
            console.log("Username :", post.username);
            console.log("Content  :", post.content);
            console.log("Likes    :", post.likes);

        });

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = filterByCategory;