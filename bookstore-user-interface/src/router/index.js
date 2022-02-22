import { createRouter, createWebHistory } from "vue-router";
import store from "../store";
import Home from "../views/Home.vue";
import Product from "../views/Product.vue";
import Search from "../views/Search.vue";
import Cart from "../views/Cart.vue";
import Profile from "../views/Profile.vue";
import Orders from "../views/Orders.vue";
import Wishlist from "../views/Wishlist.vue";
import Checkout from "../views/Checkout.vue";
import Success from "../views/Success.vue";
import Entry from "@/components/Entry";
import auth from "../app/auth";
import LogoutSuccess from "@/components/LogoutSuccess";
import UserInfoStore from "../app/user-info-store";
import UserInfoApi from "../app/user-info-api";
import ErrorComponent from "@/components/Error";

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
        beforeEnter: requireAuth
    },
    // {
    //     path: "/home",
    //     name: "Home",
    //     component: Home,
    //     beforeEnter: requireAuth
    // },
    {
        path: "/about",
        name: "About",
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ "../views/About.vue")
    },
    {
        path: "/profile",
        name: "Profile",
        component: Profile,
        beforeEnter: requireAuth
    },
    {
        path: "/orders",
        name: "Orders",
        component: Orders,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/wishlist",
        name: "Wishlist",
        component: Wishlist,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/search",
        name: "Search",
        component: Search,
        beforeEnter: requireAuth
    },
    {
        path: "/cart",
        name: "Cart",
        component: Cart,
        beforeEnter: requireAuth
    },
    {
        path: "/cart/checkout",
        name: "Checkout",
        component: Checkout,
        beforeEnter: requireAuth
    },
    {
        path: "/cart/success",
        name: "Success",
        component: Success,
        beforeEnter: requireAuth
    },
    {
        path: "/:id",
        name: "Product",
        component: Product,
        beforeEnter: requireAuth
    },
    {
        path: "/login",
        beforeEnter(to, from, next) {
            auth.auth.getSession();
        }
    },
    {
        path: "/login/oauth2/code/cognito",
        beforeEnter(to, from, next) {
            var currUrl = window.location.href;
            auth.auth.parseCognitoWebResponse(currUrl);
            next();
        }
    },
    {
        path: "/logout",
        component: LogoutSuccess,
        beforeEnter(to, from, next) {
            auth.logout();
            next();
        }
    }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

function requireAuth(to, from, next) {
    if (!auth.auth.isUserSignedIn()) {
        UserInfoStore.setLoggedIn(false);
        next({
            path: "/login",
            query: { redirect: to.fullPath }
        });
    } else {
        UserInfoApi.getUserInfo().then((response) => {
            UserInfoStore.setLoggedIn(true);
            UserInfoStore.setCognitoInfo(response);
            next();
        });
    }
}
export default router;
