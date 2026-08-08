<template>
    <div class="container mt-5">

        <h2>Company Profile</h2>

        <div class="mb-3">
            <label>Industry</label>
            <input v-model="industry" class="form-control">
        </div>

        <div class="mb-3">
            <label>Location</label>
            <input v-model="location" class="form-control">
        </div>

        <div class="mb-3">
            <label>Website</label>
            <input v-model="website" class="form-control">
        </div>

        <div class="mb-3">
            <label>HR Phone</label>
            <input v-model="hr_phone" class="form-control">
        </div>

        <div class="mb-3">
            <label>HR Position</label>
            <input v-model="hr_position" class="form-control">
        </div>

        <div class="mb-3">
            <label>Description</label>
            <textarea v-model="description" class="form-control"></textarea>
        </div>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="updateProfile">
                Update Profile
            </button>
            <RouterLink class="btn btn-secondary" to="/company/dashboard">
                Back
            </RouterLink>
        </div>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const industry = ref("")
const location = ref("")
const website = ref("")
const hr_phone = ref("")
const hr_position = ref("")
const description = ref("")

async function loadProfile() {
    try {
        const response = await api.get("/company/profile")
        industry.value = response.data.industry
        location.value = response.data.location
        website.value = response.data.website
        hr_phone.value = response.data.hr_phone
        hr_position.value = response.data.hr_position
        description.value = response.data.description
    }
    catch (error) {
        alert(error.response.data.message)
    }
}

async function updateProfile() {

    try {

        const response = await api.put("/company/profile", {
            industry: industry.value,
            location: location.value,
            website: website.value,
            hr_phone: hr_phone.value,
            hr_position: hr_position.value,
            description: description.value
        })

        alert(response.data.message)

    }

    catch (error) {
        alert(error.response.data.message)
    }

}

onMounted(() => {
    loadProfile()
})

</script>
