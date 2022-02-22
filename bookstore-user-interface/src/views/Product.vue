<template>
    <div class="container">
        <div class="row mt-4">
            <div class="col-sm-4">
                <img v-bind:src="product.image" />
            </div>
            <div class="col-sm-8">
                <h3>{{ product.title }}</h3>
                <hr />
                <p>Author: {{ product.author }}</p>
                <p>Publisher: {{ product.publisher }}</p>
                <p>Genre: {{ product.genre }}</p>
                <hr />
                <p>
                    {{ product.description }}
                </p>
                <hr />
                <p>Price: ${{ product.price }}</p>
                <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3 d-flex" method="post" action="/search">
                    <div class="control">
                        <input type="text" class="form-control form-control-dark" placeholder="price drop test" name="query" />
                    </div>
                    <div class="d-flex ml-2">
                        <button class="btn btn-warning">
                            <span class="icon"><i class="fa fa-arrow-down"></i></span>
                        </button>
                    </div>
                </form>
                <hr />

                <div class="control">
                    <input type="number" class="input" min="1" v-model="quantity" />
                </div>
                <hr />
                <div class="control">
                    <a class="btn btn-primary" @click="addToCart()">Add to Cart</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";
export default {
    name: "Product",
    data() {
        return {
            product: {},
            quantity: 1
        };
    },
    mounted() {
        this.getProduct();
    },
    methods: {
        async getProduct() {
            this.$store.commit("setIsLoading", true);
            // const id = this.$route.params.id
            // await asiox.get("api/$(id)").then(response => {this.product=response.data}).catch(error => {console.log(error)})
            this.product = { id: "1", image: "https://images-na.ssl-images-amazon.com/images/I/41CwwIUSQ4L._SX332_BO1,204,203,200_.jpg", title: "Book Title", author: "Book Author", publisher: "Book Publisher", genre: "Book Genre", description: "Book Description", price: 10 };
            document.title = this.product.title;
            this.$store.commit("setIsLoading", false);
        },
        addToCart() {
            if (isNaN(this.quantity) || this.quantity < 1) {
                this.quantity = 1;
            }

            const item = {
                product: this.product,
                quantity: this.quantity
            };
            this.$store.commit("addToCart", item);
            // toast({
            //     message: "The product was added to the cart",
            //     type: "is-success",
            //     dismissible: true,
            //     pauseOnHover: true,
            //     duration: 2000,
            //     position: "bottom-right"
            // });
        }
    }
};
</script>
