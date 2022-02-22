import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";


const cors = require("cors")


// axios.defaults.baseURL = "";

createApp(App)
    .use(cors)
    .use(store)
    .use(router)
    .mount("#app");
