const axios = require("axios");

const BASE_URL = "https://fakestoreapi.com/products";

async function updateProduct() {

    const updatedProduct = {
        title: "Python Programming Book - Second Edition",
        price: 599,
        description: "Updated edition with FastAPI",
        image: "https://i.pravatar.cc",
        category: "books"
    };

    try {

        const response = await axios.put(
            `${BASE_URL}/1`,
            updatedProduct
        );

        console.log("\n===== PRODUCT UPDATED =====");
        console.log(response.data);

    } catch (error) {
        console.log(error.message);
    }

}

module.exports = updateProduct;