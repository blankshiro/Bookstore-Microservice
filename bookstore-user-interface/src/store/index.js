import { createStore } from "vuex";
// state management
export default createStore({
    // variables
    state: {
        cart: {
            items: []
        },
        isAuthenticated: false,
        token: "",
        isLoading: false
    },
    // synchronous actions to change variables
    mutations: {
        initializeStore(state) {
            // check if there is a cart
            if (localStorage.getItem("cart")) {
                state.cart = JSON.parse(localStorage.getItem("cart"));
            } else {
                localStorage.setItem("cart", JSON.stringify(state.cart));
            }

            // check if there is a token
            if (localStorage.getItem("token")) {
                state.token = localStorage.getItem("token");
                state.isAuthenticated = true;
            } else {
                state.token = "";
                state.isAuthenticated = false;
            }
        },
        addToCart(state, item) {
            const exists = state.cart.items.filter((i) => i.product.book_id === item.product.book_id);
            if (exists.length) {
                exists[0].quantity = parseInt(exists[0].quantity) + parseInt(item.quantity);
            } else {
                state.cart.items.push(item);
            }
            localStorage.setItem("cart", JSON.stringify(state.cart));
        },
        setIsLoading(state, status) {
            state.isLoading = status;
        },
        // // used when login
        // setToken(state, token) {
        //     state.token = token;
        //     state.isAuthenticated = true;
        // },
        // // used when logout
        // removeToken(state) {
        //     state.token = "";
        //     state.isAuthenticated = false;
        // },
        clearCart(state) {
            state.cart = { items: [] };

            localStorage.setItem("cart", JSON.stringify(state.cart));
        }
    },
    // asynchronous actions to change variables
    actions: {},
    modules: {}
});
