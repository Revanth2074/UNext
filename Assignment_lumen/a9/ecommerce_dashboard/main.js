const getProducts = require("./api/getProduct");
const addProduct = require("./api/addProduct");
const updateProduct = require("./api/updateProduct");
const deleteProduct = require("./api/deleteProduct");

async function main() {

    console.log("==================================");
    console.log(" E-Commerce Product Dashboard");
    console.log("==================================");

    await getProducts();

    await addProduct();

    await updateProduct();

    await deleteProduct();
}

main();