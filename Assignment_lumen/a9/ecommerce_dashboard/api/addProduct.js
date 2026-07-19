const axios = require("axios");

const BASE_URL = "https://fakestoreapi.com/products";

async function addProduct() {

    const product = {
        title: "Python Programming Book",
        price: 499,
        description: "Learn Python from beginner to advanced",
        image: "https://i.pravatar.cc",
        category: "books"
    };

    try {

        const response = await axios.post(BASE_URL, product);

        console.log("\n===== PRODUCT ADDED =====");
        console.log(response.data);

    } catch (error) {
        console.log(error.message);
    }

}

module.exports = addProduct;