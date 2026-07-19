const getAllPosts = require("./controllers/getAllPosts");
const getSinglePost = require("./controllers/getSinglePost");
const createPost = require("./controllers/createPost");
const updatePost = require("./controllers/updatePost");
const deletePost = require("./controllers/deletePost");

const searchByUsername = require("./controllers/searchByUsername");
const searchByHashtag = require("./controllers/searchByHashtag");
const filterByCategory = require("./controllers/filterByCategory");
const sortByLikes = require("./controllers/sortByLikes");
const trendingPosts = require("./controllers/trendingPosts");

const searchContent = require("./controllers/searchContent");
const popularPosts = require("./controllers/popularPosts");
const latestPosts = require("./controllers/latestPosts");
const likePost = require("./controllers/likePost");
const searchAndFilter = require("./controllers/searchAndFilter");

async function main() {

    console.log("=================================");
    console.log(" CampusConnect ");
    console.log("=================================");

    // Activity 1
    await getAllPosts();

    // Activity 2
    await getSinglePost(3);

    // Activity 3
    await createPost();

    // Activity 4
    await updatePost(2);

    // Activity 5
    await deletePost(4);

    // Activity 6
    await searchByUsername("john");

    // Activity 7
    await searchByHashtag("#AI");

    // Activity 8
    await filterByCategory("Programming");

    // Activity 9
    await sortByLikes();

    // Activity 10
    await trendingPosts();

    // Activity 11
    await searchContent("JavaScript");

    // Activity 12
    await popularPosts();

    // Activity 13
    await latestPosts();

    // Activity 14
    await likePost(1);

    // Activity 15
    await searchAndFilter("john", "Programming");

}

main();