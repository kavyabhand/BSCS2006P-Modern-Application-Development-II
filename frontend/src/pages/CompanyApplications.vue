<template>
    <div class="container mt-5">

        <h2>Applications</h2>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadApplications">
                Load Applications
            </button>
            <RouterLink class="btn btn-secondary" to="/company/dashboard">
                Back
            </RouterLink>
        </div>

        <table class="table table-bordered" v-if="applications.length">

            <thead>

                <tr>
                    <th>Student</th>
                    <th>Roll No</th>
                    <th>Branch</th>
                    <th>CGPA</th>
                    <th>Job</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>

            </thead>

            <tbody>

                <tr v-for="application in applications" :key="application.application_id">

                    <td>{{ application.student_name }}</td>
                    <td>{{ application.roll_number }}</td>
                    <td>{{ application.branch }}</td>
                    <td>{{ application.cgpa }}</td>
                    <td>{{ application.job_title }}</td>
                    <td>{{ application.status }}</td>

                    <td>

                        <select
                            class="form-select"
                            @change="updateStatus(application.application_id, $event.target.value)">

                            <option value="">Update</option>
                            <option value="shortlisted">Shortlisted</option>
                            <option value="interview">Interview</option>
                            <option value="selected">Selected</option>
                            <option value="rejected">Rejected</option>

                        </select>

                    </td>

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

    const response = await api.get("/company/applications")

    applications.value = response.data.applications

}

async function updateStatus(id, status) {

    if (status == "") return

    const response = await api.put("/company/application/" + id + "/status", {
        status: status
    })

    alert(response.data.message)

    loadApplications()

}

onMounted(() => {
    loadApplications()
})

</script>
