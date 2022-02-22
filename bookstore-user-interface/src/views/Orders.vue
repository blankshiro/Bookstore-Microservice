<template>
    <div class="container">
        <div class="column is-12">
            <h2 class="subtitle">My orders</h2>

            <OrderSummary v-for="order in orders" v-bind:key="order.id" v-bind:order="order" />
        </div>
    </div>
</template>

<script>
import axios from "axios";
import OrderSummary from "@/components/OrderSummary";
export default {
    name: "Orders",
    components: {
        OrderSummary
    },
    data() {
        return {
            orders: []
        };
    },
    mounted() {
        document.title = "My Orders";
        this.getOrders();
    },
    methods: {
        async getOrders() {
            this.$store.commit("setIsLoading", true);
             await axios
                 .get("https://yjnonj3tqg.execute-api.ap-southeast-1.amazonaws.com/prod/ordersbyuserid/" + userId)
                 .then((response) => {
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
