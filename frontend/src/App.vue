<template>
    <div v-if="showNav" class="container mt-3">
        <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
    </div>
    <router-view />
</template>

<script setup>
import { computed } from "vue"
import { useRoute, useRouter } from "vue-router"

const route = useRoute()
const router = useRouter()

const showNav = computed(() => {
    return route.path !== "/" && route.path !== "/login" && route.path !== "/register"
})

function logout() {
    localStorage.removeItem("token")
    localStorage.removeItem("role")
    router.push("/")
}
</script>
