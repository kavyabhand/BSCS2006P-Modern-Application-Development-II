<template>
    <div class="container mt-5">

        <h2>Placement Drives</h2>

        <div class="mb-3">
            <input class="form-control" placeholder="Search by job title" v-model="search">
        </div>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadDrives">
                Search
            </button>
            <RouterLink class="btn btn-secondary" to="/student/dashboard">
                Back
            </RouterLink>
        </div>

        <table class="table table-bordered" v-if="drives.length">

            <thead>
                <tr>
                    <th>Company</th>
                    <th>Job</th>
                    <th>CGPA</th>
                    <th>Salary</th>
                    <th>Deadline</th>
                    <th>Eligible</th>
                    <th>Apply</th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="drive in drives" :key="drive.id">

                    <td>{{ drive.company_name }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.minimum_cgpa }}</td>
                    <td>{{ drive.salary_lpa }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>{{ drive.eligible ? "Yes" : "No" }}</td>

                    <td>

                        <button
                            class="btn btn-primary btn-sm"
                            @click="applyDrive(drive.id)"
                            :disabled="drive.already_applied || !drive.eligible">

                            {{ drive.already_applied ? "Applied" : (drive.eligible ? "Apply" : "Not Eligible") }}

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

    try {

        const response = await api.get("/student/drives?q=" + search.value)

        drives.value = response.data.drives

    }

    catch (error) {
        alert(error.response.data.message)
    }

}

async function applyDrive(id) {

    try {

        const response = await api.post("/student/apply/" + id, {})

        alert(response.data.message)

        loadDrives()

    }

    catch (error) {
        alert(error.response.data.message)
    }

}

onMounted(() => {
    loadDrives()
})

</script>
