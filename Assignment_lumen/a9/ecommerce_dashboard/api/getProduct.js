const axios = require("axios");

const BASE_URL = "https://fakestoreapi.com/products";

async function getProducts() {
    try {
        const response = await axios.get(BASE_URL);

        console.log("\n===== ALL PRODUCTS =====\n");

        response.data.forEach(product => {
            console.log("Product ID :", product.id);
            console.log("Title      :", product.title);
            console.log("Price      :", product.price);
            console.log("Category   :", product.category);
            console.log("--------------------------------");
        });

    } catch (error) {
        console.log(error.message);
    }
}

module.exports = getProducts;