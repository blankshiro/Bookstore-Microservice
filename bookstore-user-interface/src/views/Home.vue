<template>
    <div class="home">
        <section class="hero is-small is-dark mb-6">
            <div class="hero-body has-text-centered">
                <p class="title mb-6">Welcome, {{ userInfo["username"] }}!</p>
                <p class="subtitle">
                    “Today a reader, tomorrow a leader.” – Margaret Fuller
                </p>
            </div>
        </section>
        <main role="main">
            <div class="album py-5 bg-light">
                <div class="container">
                    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-5 g-3">
                        <ProductBox v-for="product in Products" v-bind:key="product.book_id" v-bind:product="product" />
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import axios from 'axios'
import ProductBox from '@/components/ProductBox'
import UserInfoStore from "../app/user-info-store";
export default {
  name: 'Home',
  data() {
    return {
        Products: [],
        userPoolId: process.env.VUE_APP_COGNITO_USERPOOL_ID,
        userInfo: UserInfoStore.state.cognitoInfo
    }
  },
  components: {
    ProductBox
  },
  mounted() {
    this.getProducts()
    this.getUserId()
    document.title = 'Home'
  },
  methods: {
    async getProducts() {
      await axios
        .get('https://yjnonj3tqg.execute-api.ap-southeast-1.amazonaws.com/prod/products')
        .then(response => {
            this.Products = response.data.data.books;
        })
        .catch(error => {
          console.log(error)
        })
    },
    getUserId() {
        axios
            .get('https://yjnonj3tqg.execute-api.ap-southeast-1.amazonaws.com/prod/users/find/' + this.userInfo.username)
            .then(response => {
                    global.userId = response.data.id
            })
            .catch(error => {
                console.log(error)
            })
        }
  }
}
</script>
