<template>
    <div class="container">
        <div class="column is-12">
            <h2 class="subtitle">My Wishlist</h2>
            <table class="table is-fullwidth">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Price</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="item in wishlist" v-bind:key="item.book_id">
                        <td>{{ item.title }}</td>
                        <td>${{ item.price }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
    name: "Wishlist",
    data() {
        return {
            wishlist: []
        };
    },
    mounted() {
        document.title = "My Wishlist";
        this.getWishlist();
    },
    methods: {
        async getProducts(bookId) {
        await axios
            .get('https://yjnonj3tqg.execute-api.ap-southeast-1.amazonaws.com/prod/products/' + bookId)
            .then(response => {
                this.wishlist.push(response.data.data);
            })
            .catch(error => {
                console.log(error)
            })
        },
        async getWishlist() {
            this.$store.commit("setIsLoading", true);
            await axios
                .get("https://yjnonj3tqg.execute-api.ap-southeast-1.amazonaws.com/prod/wishlist?user=" + userId)
                .then((response) => {
                    var itemList = response.data.data.items
                    for (var i = 0 ; i < itemList.length ; i++){
                        this.getProducts(itemList[i].book_id)
                    }
                    this.orders = response.data;
                })
                .catch((error) => {
                    console.log(error);
                });
            this.$store.commit("setIsLoading", false);
        }
    }
};
</script>
