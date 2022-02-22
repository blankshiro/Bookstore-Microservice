<template>
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-body">
                <div class="px-4 py-2">
                    <h4 class="mt-5 fw-bold fs-3 mb-5">Credit Card Detail</h4>
                    <div class="card-body">
                        <form>
                            <div class="row mb-4">
                                <div class="col">
                                    <div class="form-outline">
                                        <input type="text" class="form-control" v-model="name" required />
                                        <label class="form-label">Name on card</label>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="form-outline">
                                        <input type="text" class="form-control" v-model="card" required />
                                        <label class="form-label">Credit card number</label>
                                    </div>
                                </div>
                            </div>

                            <div class="row mb-4">
                                <div class="col-3">
                                    <div class="form-outline">
                                        <input type="text" class="form-control" v-model="month" required />
                                        <label class="form-label">Expiry Month</label>
                                    </div>
                                </div>
                                <div class="col-3">
                                    <div class="form-outline">
                                        <input type="text" class="form-control" v-model="year" required />
                                        <label class="form-label">Expiry Year</label>
                                    </div>
                                </div>
                                <div class="col-3">
                                    <div class="form-outline">
                                        <input type="text" class="form-control" v-model="cvv" required />
                                        <label class="form-label">CVV</label>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                  <div class="control float-end"><button class="button is-success" @click="checkout">Pay with Stripe</button></div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
    name: "Checkout",
    data() {
        return {
            cart: {
                items: []
            },
            name: "",
            card: "",
            month: "",
            year: "" ,
            cvv: ""  
            };
    },
    mounted() {
        this.cart = this.$store.state.cart;
        document.title = "Checkout";
    },
    methods: {
        checkout() {
            var a = {"user_id": userId, "card_details" : { "cardNumber" : this.card , "expiryMonth" : parseInt(this.month), expiryYear : parseInt(this.year), "cvv" : this.cvv}}
            a["product_list"] = []

            for (var i = 0 ; i < this.cart.items.length ; i++)
                a["product_list"].push({product_id : this.cart.items[i].product.book_id , quantity : this.cart.items[i].quantity});
            var data = JSON.stringify(a);
            console.log(accessToken)
            axios({ method: 'post', url: 'https://yjnonj3tqg.execute-api.ap-southeast-1.amazonaws.com/prod/createorder', headers: {'Content-Type': 'application/json','Authorization': accessToken}, data : data})
            .then(response => {
                if (response.data.message === "Order placed."){
                    this.$store.commit("clearCart");
                    this.$router.push("/cart/success");
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }
};
</script>
