<template>
    <div class="search">
        <main role="main">
            <div class="column is-12">
                <h1 class="title">Search</h1>

                <h2 class="is-size-5 has-text-grey">Search term: "{{ query }}"</h2>
            </div>
            <div class="album py-5 bg-light">
                <div class="container">
                    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5 g-3">
                        <ProductBox v-for="product in products" v-bind:key="product.book_id" v-bind:product="product" />
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import axios from "axios";
import ProductBox from "@/components/ProductBox";
export default {
    name: "Search",
    components: {
        ProductBox
    },
    data() {
        return {
            products: [],
            query: ""
        };
    },
    mounted() {
        document.title = "Searching for ...";
        let uri = window.location.search.substring(1);
        let params = new URLSearchParams(uri);
        if (params.get("query")) {
            this.query = params.get("query");
            this.performSearch();
        }
    },
    methods: {
        async performSearch() {
            this.$store.commit("setIsLoading", true);

            // await axios
            //     .post("/api/v1/products/search/", { query: this.query })
            //     .then((response) => {
            //         this.products = response.data;
            //     })
            //     .catch((error) => {
            //         console.log(error);
            //     });

            this.$store.commit("setIsLoading", false);
        }
    }
};
</script>
