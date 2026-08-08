<template>
    <div class="container mt-5">

        <h2>Student Profile</h2>

        <div class="mb-3">
            <label>Full Name</label>
            <input v-model="full_name" class="form-control">
        </div>

        <div class="mb-3">
            <label>Phone</label>
            <input v-model="phone" class="form-control">
        </div>

        <div class="mb-3">
            <label>Skills</label>
            <input v-model="skills" class="form-control">
        </div>

        <div class="mb-3">
            <label>Experience</label>
            <textarea v-model="experience" class="form-control"></textarea>
        </div>

        <div class="mb-3">
            <label>About</label>
            <textarea v-model="about" class="form-control"></textarea>
        </div>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="updateProfile">
                Update Profile
            </button>
            <RouterLink class="btn btn-secondary" to="/student/dashboard">
                Back
            </RouterLink>
        </div>

        <hr>

        <h4>Upload Resume</h4>

        <div class="mb-3">
            <input type="file" class="form-control" @change="onFileChange">
        </div>

        <button class="btn btn-success" @click="uploadResume">
            Upload Resume
        </button>

        <p v-if="resume_filename" class="mt-3">Current resume : {{ resume_filename }}</p>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const full_name = ref("")
const phone = ref("")
const skills = ref("")
const experience = ref("")
const about = ref("")
const resume_filename = ref("")
const resume_file = ref(null)

async function loadProfile() {
    try {
        const response = await api.get("/student/profile")
        full_name.value = response.data.full_name
        phone.value = response.data.phone
        skills.value = response.data.skills
        experience.value = response.data.experience
        about.value = response.data.about
        resume_filename.value = response.data.resume_filename
    }
    catch (error) {
        alert(error.response.data.message)
    }
}

function onFileChange(event) {
    resume_file.value = event.target.files[0]
}

async function updateProfile() {

    try {

        const response = await api.put("/student/profile", {
            full_name: full_name.value,
            phone: phone.value,
            skills: skills.value,
            experience: experience.value,
            about: about.value
        })

        alert(response.data.message)

    }

    catch (error) {
        alert(error.response.data.message)
    }

}

async function uploadResume() {

    if (!resume_file.value) {
        alert("Select a file first")
        return
    }

    try {

        const formData = new FormData()
        formData.append("resume", resume_file.value)

        const response = await api.post("/student/resume", formData)

        resume_filename.value = response.data.filename

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
