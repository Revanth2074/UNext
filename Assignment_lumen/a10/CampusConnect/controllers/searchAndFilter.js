const api = require("../services/api");

async function searchAndFilter(username, category) {

    try {

        const response = await api.get(
            `/?username=${username}&category=${category}`
        );

        console.log(
            `\n===== ${username.toUpperCase()} - ${category.toUpperCase()} POSTS =====\n`
        );

        response.data.forEach(post => {

            console.log("----------------------------------------");
            console.log("Username :", post.username);
            console.log("Category :", post.category);
            console.log("Content  :", post.content);
            console.log("Likes    :", post.likes);

        });

    } catch (error) {

        console.log("Error :", error.message);

    }

}

module.exports = searchAndFilter;