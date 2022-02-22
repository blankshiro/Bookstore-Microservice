<template>
    <div id="wrapper">
        <nav class="p-3 bg-dark text-white">
            <div class="container">
                <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
                    <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 me-2 text-white text-decoration-none">
                        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="32" fill="currentColor" class="bi bi-book" viewBox="0 0 16 16">
                            <path
                                d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811V2.828zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492V2.687zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783z"
                            />
                        </svg>
                    </a>

                    <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
                        <li><router-link to="/" class="nav-link px-2 text-white">Books</router-link></li>
                        <li><router-link to="/orders" class="nav-link px-2 text-white">Past Orders</router-link></li>
                        <li><router-link to="/wishlist" class="nav-link px-2 text-white">Wishlist</router-link></li>
                    </ul>

                    <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3 d-flex" method="get" action="/search">
                        <div class="control">
                            <input type="text" class="form-control form-control-dark" placeholder="Search for a book!" name="query" />
                        </div>
                        <div class="d-flex">
                            <button class="btn btn-success">
                                <span class="icon"><i class="fa fa-search"></i></span>
                            </button>
                        </div>
                    </form>

                    <div class="text-end ">
                        <router-link to="/profile" class="btn btn-outline-light me-2">My Account</router-link>
                        <router-link to="/cart" class="btn btn-outline-light me-2"
                            ><span class="icon"><i class="fas fa-shopping-cart"></i></span><span> Cart ({{ cartTotalLength }})</span></router-link
                        >
                    </div>
                </div>
            </div>
        </nav>
        <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
            <div class="lds-dual-ring"></div>
        </div>
        <router-view />
    </div>
</template>

<script>
import axios from "axios"
export default {
    data() {
        return {
            cart: {
                items: []
            }
        };
    },
    mounted() {
        this.cart = this.$store.state.cart;
    },
    computed: {
        cartTotalLength() {
            let totalLength = 0;
            for (let i = 0; i < this.cart.items.length; i++) {
                totalLength += this.cart.items[i].quantity;
            }
            return totalLength;
        }
    }
};
</script>

<style lang="scss">
@import "../node_modules/bulma";
.lds-dual-ring {
    display: inline-block;
    width: 80px;
    height: 80px;
}
.lds-dual-ring:after {
    content: " ";
    display: block;
    width: 64px;
    height: 64px;
    margin: 8px;
    border-radius: 50%;
    border: 6px solid #ccc;
    border-color: #ccc transparent #ccc transparent;
    animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
.is-loading-bar {
    height: 0;
    overflow: hidden;
    -webkit-transition: all 0.3s;
    transition: all 0.3s;
    &.is-loading {
        height: 80px;
    }
}
</style>
