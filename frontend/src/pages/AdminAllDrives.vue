<template>
    <div class="container mt-5">

        <h2>All Drives</h2>

        <div class="mb-3">
            <input
                class="form-control"
                placeholder="Search by job title"
                v-model="search"
            >
        </div>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadDrives">
                Search
            </button>
            <RouterLink class="btn btn-secondary" to="/admin/dashboard">
                Back
            </RouterLink>
        </div>

        <table class="table table-bordered" v-if="drives.length">

            <thead>
                <tr>
                    <th>Company</th>
                    <th>Job</th>
                    <th>CGPA</th>
                    <th>Deadline</th>
                    <th>Status</th>
                    <th>Applicants</th>
                    <th>Close</th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="drive in drives" :key="drive.id">

                    <td>{{ drive.company_name }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.minimum_cgpa }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>{{ drive.status }}</td>
                    <td>{{ drive.applicants }}</td>

                    <td>
                        <button
                            class="btn btn-dark btn-sm"
                            @click="closeDrive(drive.id)"
                            :disabled="drive.status == 'closed'">
                            Close
                        </button>
                    </td>

                </tr>

            </tbody>

        </table>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const drives = ref([])
const search = ref("")

async function loadDrives() {

    const response = await api.get("/admin/all-drives?q=" + search.value)

    drives.value = response.data.drives

}

async function closeDrive(id) {

    const response = await api.put("/admin/close-drive/" + id, {})

    alert(response.data.message)

    loadDrives()

}

onMounted(() => {
    loadDrives()
})

</script>
