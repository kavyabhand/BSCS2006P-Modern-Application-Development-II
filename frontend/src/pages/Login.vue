<template>
    <div class="container mt-5" style="max-width:500px">
        <h2 class="mb-4">Login</h2>

        <div class="mb-3">
            <label>Email</label>
            <input type="email" class="form-control" v-model="email">
        </div>

        <div class="mb-3">
            <label>Password</label>
            <input type="password" class="form-control" v-model="password">
        </div>

        <button class="btn btn-primary w-100 mb-3" @click="login">
            Login
        </button>

        <RouterLink to="/register">Register</RouterLink>
        <span class="mx-2">|</span>
        <RouterLink to="/">Back</RouterLink>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const email = ref("")
const password = ref("")

async function login() {

    try {

        const response = await api.post("/auth/login", {
            email: email.value,
            password: password.value
        })

        localStorage.setItem("token", response.data.access_token)
        localStorage.setItem("role", response.data.role)

        if (response.data.role == "student") {
            router.push("/student/dashboard")
        }

        else if (response.data.role == "company") {
            router.push("/company/dashboard")
        }

        else {
            router.push("/admin/dashboard")
        }

    }

    catch (error) {
        alert(error.response.data.message)
    }

}
</script>
