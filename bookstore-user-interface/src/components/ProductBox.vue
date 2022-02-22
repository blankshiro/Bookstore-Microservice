<template>
    <div class="col">
        <div class="card shadow-sm">
            <!-- <img :src="product.image" width="245" height="340" /> -->
            <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fedit.org%2Fimages%2Fcat%2Fbook-covers-big-2019101610.jpg&f=1&nofb=1" style="width:100%;height:345px" />
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <p class="card-text">{{ product.title }}</p>
                    <button class="button far fa-bookmark mb-3" @click="addToWishlist()" style="outline: none;border: 0;box-shadow: none;background-color: transparent;"></button>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                    <div class="control">
                        <button type="button" @click="addToCart()" class="btn btn-sm btn-primary">Add to cart</button>
                      <!--  <router-link v-bind:to="product.book_id" class="btn btn-sm btn-secondary ms-4">View details</router-link>-->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// Reusable component to display products
import axios from "axios";
import { toast } from "bulma-toast";
export default {
    name: "ProductBox",
    props: {
        product: Object,
        quantity: Number
    },
    methods: {
        addToCart() {
            const item = {
                product: this.product,
                quantity: 1
            };
            this.$store.commit("addToCart", item);
            toast({
                message: "The product was added to the cart",
                type: "is-success",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
            });
        },
        addToWishlist() {
            var axios = require('axios');
            var data = JSON.stringify({"user_id": userId,"book_id":this.product.book_id});
            axios({method: 'post', url: 'https://yjnonj3tqg.execute-api.ap-southeast-1.amazonaws.com/prod/wishlist', headers: { 'Content-Type': 'application/json' }, data : data})
            .then(function (response) {
                console.log(JSON.stringify(response.data));
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }
};
</script>
