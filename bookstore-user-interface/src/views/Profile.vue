<template>
    <div class="container rounded bg-white mt-5 mb-5">
        <div class="row">
            <div class="col-md-6">
                <div class="d-flex flex-column align-items-center text-center p-3 py-5">
                    <img class="rounded-circle mt-5" src="https://bootdey.com/img/Content/avatar/avatar7.png" style="height:150px" />
                    <span class="font-weight-bold">{{ userInfo["username"] }}</span
                    ><span class="text-black-50"></span><span>{{ userInfo["email"] }} </span>
                </div>
            </div>
            <div class="col-md-6">
                <div class="p-3 py-5">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="text-right">Profile Settings</h4>
                    </div>
                    <div class="row mt-3">
                        <div class="col-md-12 mt-2"><label class="labels">Email</label><input type="text" class="form-control" :placeholder="userInfo['email']" value="" /></div>
                        <div class="col-md-12 mt-2"><label class="labels">Username</label><input type="text" class="form-control" :placeholder="userInfo['username']" value="" /></div>
                        <!-- <div class="col-md-12 mt-2"><label class="labels">Password</label><input type="text" class="form-control" placeholder="password" value="" /></div> -->
                        <div class="row mt-2 mb-2 mt-2">
<!--                            <div class="col-md-6 "><label class="labels">First Name</label><input type="text" class="form-control" placeholder="First Name" value="" /></div>
                            <div class="col-md-6"><label class="labels">Last Name</label><input type="text" class="form-control" value="" placeholder="Last Name" /></div> -->
                        </div>
                    </div>
                    <div class="d-grid gap-2 mt-5 d-md-flex justify-content-md-end">
                        <!--<button class="btn btn-primary profile-button" type="button">Save Profile</button>-->
                        <router-link to="/logout"><button class="btn btn-danger profile-button" type="button">Logout</button></router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";
import UserInfoStore from "../app/user-info-store";
export default {
    name: "Profile",
    data() {
        return {
            userPoolId: process.env.VUE_APP_COGNITO_USERPOOL_ID,
            userInfo: UserInfoStore.state.cognitoInfo
        };
    },
    mounted() {
        document.title = "My Profile";
    },
    methods: {}
};
</script>
