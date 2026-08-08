<template>
    <div class="container mt-5">

        <h2>My Drives</h2>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadDrives">
                Load Drives
            </button>
            <RouterLink class="btn btn-secondary" to="/company/dashboard">
                Back
            </RouterLink>
        </div>

        <table class="table table-bordered" v-if="drives.length">

            <thead>
                <tr>
                    <th>Job</th>
                    <th>Status</th>
                    <th>Deadline</th>
                    <th>Applicants</th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="drive in drives" :key="drive.id">

                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.status }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>{{ drive.applicants }}</td>

                </tr>

            </tbody>

        </table>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const drives = ref([])

async function loadDrives() {

    const response = await api.get("/company/drives")

    drives.value = response.data.drives

}

onMounted(() => {
    loadDrives()
})

</script>
