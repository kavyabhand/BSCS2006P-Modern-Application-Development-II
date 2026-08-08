<template>
    <div class="container mt-5" style="max-width:500px">
        <h2 class="mb-4">Register</h2>

        <div class="mb-3">
            <label>Role</label>
            <select class="form-control" v-model="role">
                <option value="student">Student</option>
                <option value="company">Company</option>
            </select>
        </div>

        <div class="mb-3">
            <label>Email</label>
            <input type="email" class="form-control" v-model="email">
        </div>

        <div class="mb-3">
            <label>Password</label>
            <input type="password" class="form-control" v-model="password">
        </div>

        <div v-if="role == 'student'">
            <div class="mb-3">
                <label>Full Name</label>
                <input class="form-control" v-model="full_name">
            </div>
            <div class="mb-3">
                <label>Roll Number</label>
                <input class="form-control" v-model="roll_number">
            </div>
            <div class="mb-3">
                <label>Branch</label>
                <input class="form-control" v-model="branch">
            </div>
            <div class="mb-3">
                <label>Year</label>
                <input type="number" class="form-control" v-model="year">
            </div>
            <div class="mb-3">
                <label>CGPA</label>
                <input type="number" step="0.01" class="form-control" v-model="cgpa">
            </div>
        </div>

        <div v-if="role == 'company'">
            <div class="mb-3">
                <label>Company Name</label>
                <input class="form-control" v-model="company_name">
            </div>
            <div class="mb-3">
                <label>Industry</label>
                <input class="form-control" v-model="industry">
            </div>
            <div class="mb-3">
                <label>Location</label>
                <input class="form-control" v-model="location">
            </div>
            <div class="mb-3">
                <label>Website</label>
                <input class="form-control" v-model="website">
            </div>
            <div class="mb-3">
                <label>HR Name</label>
                <input class="form-control" v-model="hr_name">
            </div>
            <div class="mb-3">
                <label>HR Email</label>
                <input class="form-control" v-model="hr_email">
            </div>
        </div>

        <button class="btn btn-primary w-100 mb-3" @click="register">
            Register
        </button>

        <RouterLink to="/login">Login</RouterLink>
        <span class="mx-2">|</span>
        <RouterLink to="/">Back</RouterLink>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const role = ref("student")
const email = ref("")
const password = ref("")
const full_name = ref("")
const roll_number = ref("")
const branch = ref("")
const year = ref("")
const cgpa = ref("")
const company_name = ref("")
const industry = ref("")
const location = ref("")
const website = ref("")
const hr_name = ref("")
const hr_email = ref("")

async function register() {

    if (!email.value || !password.value) {
        alert("Email and password are required")
        return
    }

    if (role.value == "student") {
        if (!full_name.value || !roll_number.value || !branch.value || !year.value || !cgpa.value) {
            alert("All student fields are required")
            return
        }

        const yearNum = parseInt(year.value)
        const cgpaNum = parseFloat(cgpa.value)

        if (isNaN(yearNum) || isNaN(cgpaNum)) {
            alert("Year and CGPA must be valid numbers")
            return
        }
    }

    if (role.value == "company") {
        if (!company_name.value) {
            alert("Company name is required")
            return
        }
    }

    try {

        const data = {
            email: email.value,
            password: password.value,
            role: role.value
        }

        if (role.value == "student") {
            data.full_name = full_name.value
            data.roll_number = roll_number.value
            data.branch = branch.value
            data.year = parseInt(year.value)
            data.cgpa = parseFloat(cgpa.value)
        }

        else {
            data.company_name = company_name.value
            data.industry = industry.value
            data.location = location.value
            data.website = website.value
            data.hr_name = hr_name.value
            data.hr_email = hr_email.value
        }

        const response = await api.post("/auth/register", data)

        alert(response.data.message)
        router.push("/login")

    }

    catch (error) {
        alert(error.response?.data?.message || "Registration failed")
    }

}
</script>
