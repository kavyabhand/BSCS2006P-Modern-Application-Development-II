<template>
    <div class="container mt-5">

        <h2>Admin Dashboard</h2>

        <div v-if="dashboard">

            <p>Total Students : {{ dashboard.total_students }}</p>
            <p>Total Companies : {{ dashboard.total_companies }}</p>
            <p>Total Drives : {{ dashboard.total_drives }}</p>
            <p>Total Selected : {{ dashboard.total_selected }}</p>

        </div>

        <hr>

        <RouterLink class="btn btn-success me-2 mb-2" to="/admin/pending-companies">
            Pending Companies
        </RouterLink>

        <RouterLink class="btn btn-warning me-2 mb-2" to="/admin/pending-drives">
            Pending Drives
        </RouterLink>

        <RouterLink class="btn btn-outline-success me-2 mb-2" to="/admin/companies">
            Search Companies
        </RouterLink>

        <RouterLink class="btn btn-outline-warning me-2 mb-2" to="/admin/all-drives">
            All Drives
        </RouterLink>

        <RouterLink class="btn btn-info me-2 mb-2" to="/admin/students">
            Students
        </RouterLink>

        <RouterLink class="btn btn-primary me-2 mb-2" to="/admin/applications">
            Applications
        </RouterLink>

        <button class="btn btn-secondary me-2 mb-2" @click="triggerReport">
            Generate Report
        </button>

        <button class="btn btn-dark mb-2" @click="triggerReminders">
            Send Reminders
        </button>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const dashboard = ref(null)

async function loadDashboard() {

    const response = await api.get("/admin/dashboard")

    dashboard.value = response.data

}

async function triggerReport() {

    const response = await api.get("/admin/report")

    alert(response.data.message)

}

async function triggerReminders() {

    const response = await api.get("/admin/reminders")

    alert(response.data.message)

}

onMounted(() => {
    loadDashboard()
})

</script>
