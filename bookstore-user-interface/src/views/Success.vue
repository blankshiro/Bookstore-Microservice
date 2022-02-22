<template>
    <div class="px-4 py-5 my-5 text-center">
        <h1 class="display-5 fw-bold">Thank you</h1>
        <div class="col-lg-6 mx-auto">
            <p class="lead mb-4">Your order will be processed within 48 hours</p>
        </div>
    </div>
</template>

<script>
export default {
    name: "Success",
    mounted() {
        document.title = "Success";
    }
};
</script>
