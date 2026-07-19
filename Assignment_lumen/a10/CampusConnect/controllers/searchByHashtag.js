const api = require("../services/api");

async function searchByHashtag(hashtag) {

    try {

        const response = await api.get(`/?hashtags=${hashtag}`);

        console.log(`\n===== POSTS WITH ${hashtag} =====\n`);

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

module.exports = searchByHashtag;