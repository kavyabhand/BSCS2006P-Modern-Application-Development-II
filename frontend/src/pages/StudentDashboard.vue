<template>
    <div class="container mt-5">

        <h2>Student Dashboard</h2>

        <RouterLink class="btn btn-outline-primary btn-sm me-2 mb-3" to="/student/drives">Drives</RouterLink>
        <RouterLink class="btn btn-outline-primary btn-sm me-2 mb-3" to="/student/companies">Companies</RouterLink>
        <RouterLink class="btn btn-outline-primary btn-sm me-2 mb-3" to="/student/applications">Applications</RouterLink>
        <RouterLink class="btn btn-outline-primary btn-sm mb-3" to="/student/profile">Profile</RouterLink>

        <div v-if="student">

            <h5>{{ student.student_name }}</h5>
            <p>Branch : {{ student.branch }}</p>
            <p>CGPA : {{ student.cgpa }}</p>
            <p>Total Applications : {{ student.total_applications }}</p>

        </div>

        <hr>

        <button class="btn btn-success mb-3" @click="loadDrives">
            View Placement Drives
        </button>

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

        <hr>

        <button class="btn btn-warning mb-3" @click="loadApplications">
            View Application History
        </button>

        <button class="btn btn-secondary mb-3 ms-2" @click="exportApplications">
            Export Applications
        </button>

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

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const student = ref(null)
const drives = ref([])
const applications = ref([])

async function loadDashboard() {

    try {

        const response = await api.get("/student/dashboard")

        student.value = response.data

    }

    catch (error) {
        alert(error.response.data.message)
    }

}

async function loadDrives() {

    try {

        const response = await api.get("/student/drives")

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
        loadDashboard()

    }

    catch (error) {
        alert(error.response.data.message)
    }

}

async function loadApplications() {

    try {

        const response = await api.get("/student/applications")

        applications.value = response.data.applications

    }

    catch (error) {
        alert(error.response.data.message)
    }

}

async function exportApplications() {

    try {

        const response = await api.post("/student/export", {})

        const taskId = response.data.task_id

        alert(response.data.message)

        const interval = setInterval(async () => {

            const statusRes = await api.get("/student/export/" + taskId)

            if (statusRes.data.status == "done") {

                clearInterval(interval)

                const filename = statusRes.data.filename

                const fileRes = await api.get("/student/export/download/" + filename, {
                    responseType: "blob"
                })

                const url = window.URL.createObjectURL(new Blob([fileRes.data]))
                const link = document.createElement("a")
                link.href = url
                link.setAttribute("download", filename)
                link.click()

                alert("Export downloaded")

            }

            if (statusRes.data.status == "failed") {

                clearInterval(interval)
                alert("Export failed")

            }

        }, 2000)

    }

    catch (error) {
        alert(error.response.data.message)
    }

}

onMounted(() => {
    loadDashboard()
})

</script>
