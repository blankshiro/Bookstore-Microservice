<template>
    <div class="px-4 pt-5 my-5 text-center border-bottom">
        <h1 class="display-4 fw-bold">Your cart</h1>
        <div class="overflow-hidden">
            <div class="container px-5">
                <table class="table table-secondary" v-if="cartTotalLength">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Total</th>
                            <th></th>
                        </tr>
                    </thead>

                    <tbody>
                        <CartItem v-for="item in cart.items" v-bind:key="item.product.book_id" v-bind:initialItem="item" v-on:removeFromCart="removeFromCart" />
                    </tbody>
                </table>

                <p v-else>You don't have any products in your cart...</p>
            </div>
        </div>

        <div class="col-lg-6 mx-auto">
            <h2 class="subtitle">Summary</h2>
            <p class="lead mb-4">
                <strong>${{ cartTotalPrice.toFixed(2) }}</strong
                >, {{ cartTotalLength }} items
            </p>
        </div>
        <div class="control">
            <router-link to="/cart/checkout" class="button is-success">Proceed to checkout</router-link>
        </div>
    </div>
</template>
<script>
import axios from "axios";
import CartItem from "@/components/CartItem.vue";
export default {
    name: "Cart",
    components: {
        CartItem
    },
    data() {
        return {
            cart: {
                items: []
            }
        };
    },
    mounted() {
        this.cart = this.$store.state.cart;
        document.title = "Cart";
    },
    methods: {
        removeFromCart(item) {
           this.cart.items = this.cart.items.filter((i) => i.product.book_id !== item.product.book_id);
        }
    },
    computed: {
        cartTotalLength() {
            return this.cart.items.reduce((acc, curVal) => {
                return (acc += curVal.quantity);
            }, 0);
        },
        cartTotalPrice() {
            return this.cart.items.reduce((acc, curVal) => {
                return (acc += curVal.product.price * curVal.quantity);
            }, 0);
        }
    }
};
</script>
