<template>
    <div class="container mt-5">

        <h2>My Applications</h2>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadApplications">
                Load Applications
            </button>
            <RouterLink class="btn btn-secondary" to="/student/dashboard">
                Back
            </RouterLink>
        </div>

        <table class="table table-bordered" v-if="applications.length">

            <thead>
                <tr>
                    <th>Company</th>
                    <th>Job</th>
                    <th>Status</th>
                    <th>Applied At</th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="application in applications" :key="application.applied_at">

                    <td>{{ application.company }}</td>
                    <td>{{ application.job_title }}</td>
                    <td>{{ application.status }}</td>
                    <td>{{ application.applied_at }}</td>

                </tr>

            </tbody>

        </table>

        <hr>

        <h4>Placement History</h4>

        <table class="table table-bordered" v-if="placements.length">

            <thead>
                <tr>
                    <th>Company</th>
                    <th>Job</th>
                    <th>Package</th>
                    <th>Placed At</th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="placement in placements" :key="placement.placed_at">

                    <td>{{ placement.company }}</td>
                    <td>{{ placement.job_title }}</td>
                    <td>{{ placement.offered_package }}</td>
                    <td>{{ placement.placed_at }}</td>

                </tr>

            </tbody>

        </table>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const applications = ref([])
const placements = ref([])

async function loadApplications() {

    const response = await api.get("/student/applications")

    applications.value = response.data.applications

    const placementRes = await api.get("/student/placements")

    placements.value = placementRes.data.placements

}

onMounted(() => {
    loadApplications()
})

</script>
