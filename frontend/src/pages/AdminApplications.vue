<template>
    <div class="container mt-5">

        <h2>All Applications</h2>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadApplications">
                Load Applications
            </button>
            <RouterLink class="btn btn-secondary" to="/admin/dashboard">
                Back
            </RouterLink>
        </div>

        <table class="table table-bordered" v-if="applications.length">

            <thead>
                <tr>
                    <th>Student</th>
                    <th>Roll No</th>
                    <th>Company</th>
                    <th>Job</th>
                    <th>Status</th>
                    <th>Applied At</th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="application in applications" :key="application.id">

                    <td>{{ application.student_name }}</td>
                    <td>{{ application.roll_number }}</td>
                    <td>{{ application.company_name }}</td>
                    <td>{{ application.job_title }}</td>
                    <td>{{ application.status }}</td>
                    <td>{{ application.applied_at }}</td>

                </tr>

            </tbody>

        </table>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const applications = ref([])

async function loadApplications() {

    const response = await api.get("/admin/applications")

    applications.value = response.data.applications

}

onMounted(() => {
    loadApplications()
})

</script>
