<template>
    <div class="container mt-5">

        <h2>Pending Drives</h2>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadDrives">
                Load Drives
            </button>
            <RouterLink class="btn btn-secondary" to="/admin/dashboard">
                Back
            </RouterLink>
        </div>

        <table
            class="table table-bordered"
            v-if="drives.length"
        >

            <thead>

                <tr>
                    <th>Company</th>
                    <th>Job</th>
                    <th>CGPA</th>
                    <th>Salary</th>
                    <th>Deadline</th>
                    <th>Approve</th>
                    <th>Reject</th>
                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="drive in drives"
                    :key="drive.id"
                >

                    <td>{{ drive.company_name }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.minimum_cgpa }}</td>
                    <td>{{ drive.salary_lpa }}</td>
                    <td>{{ drive.deadline }}</td>

                    <td>

                        <button
                            class="btn btn-success btn-sm"
                            @click="approveDrive(drive.id)"
                        >
                            Approve
                        </button>

                    </td>

                    <td>

                        <button
                            class="btn btn-danger btn-sm"
                            @click="rejectDrive(drive.id)"
                        >
                            Reject
                        </button>

                    </td>

                </tr>

            </tbody>

        </table>

        <p v-else class="text-muted">No pending drives</p>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const drives = ref([])

async function loadDrives() {

    const response = await api.get("/admin/pending-drives")

    drives.value = response.data.drives

}

async function approveDrive(id) {

    const response = await api.put("/admin/approve-drive/" + id, {})

    alert(response.data.message)

    loadDrives()

}

async function rejectDrive(id) {

    const response = await api.put("/admin/reject-drive/" + id, {})

    alert(response.data.message)

    loadDrives()

}

onMounted(() => {
    loadDrives()
})

</script>