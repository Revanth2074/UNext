const axios = require("axios");

const BASE_URL = "https://fakestoreapi.com/products";

async function deleteProduct() {

    try {

        const response = await axios.delete(`${BASE_URL}/1`);

        console.log("\n===== PRODUCT DELETED =====");
        console.log(response.data);

    } catch (error) {
        console.log(error.message);
    }

}

module.exports = deleteProduct;