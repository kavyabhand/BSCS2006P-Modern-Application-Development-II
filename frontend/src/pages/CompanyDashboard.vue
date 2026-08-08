<template>
    <div class="container mt-5">

        <h2>Company Dashboard</h2>

        <RouterLink class="btn btn-outline-primary btn-sm me-2 mb-3" to="/company/drives">Drives</RouterLink>
        <RouterLink class="btn btn-outline-primary btn-sm me-2 mb-3" to="/company/applications">Applications</RouterLink>
        <RouterLink class="btn btn-outline-primary btn-sm mb-3" to="/company/profile">Profile</RouterLink>

        <div v-if="dashboard">

            <h5>{{ dashboard.company_name }}</h5>
            <p>Approval Status : {{ dashboard.approval_status }}</p>
            <p>Total Drives : {{ dashboard.total_drives }}</p>
            <p>Total Applications : {{ dashboard.total_applications }}</p>

        </div>

        <hr>

        <div v-if="dashboard && dashboard.approval_status != 'approved'" class="alert alert-warning">
            Waiting for admin approval before you can create drives.
        </div>

        <div v-else>
        <h4>Create Placement Drive</h4>

        <div class="mb-2">
            <input class="form-control" placeholder="Job Title *" v-model="job_title">
        </div>

        <div class="mb-2">
            <textarea class="form-control" placeholder="Job Description" v-model="job_description"></textarea>
        </div>

        <div class="mb-2">
            <input class="form-control" placeholder="Required Skills" v-model="required_skills">
        </div>

        <div class="mb-2">
            <input class="form-control" placeholder="Minimum CGPA" v-model="minimum_cgpa">
        </div>

        <div class="mb-2">
            <input class="form-control" placeholder="Eligible Branch" v-model="eligible_branch">
        </div>

        <div class="mb-2">
            <input class="form-control" placeholder="Eligible Year" v-model="eligible_year">
        </div>

        <div class="mb-2">
            <input class="form-control" placeholder="Salary LPA" v-model="salary_lpa">
        </div>

        <div class="mb-2">
            <label class="form-label">Application Deadline *</label>
            <input class="form-control" type="date" v-model="application_deadline">
        </div>

        <button class="btn btn-success mb-4" @click="createDrive">
            Create Drive
        </button>
        </div>

        <hr>

        <button class="btn btn-warning mb-3" @click="loadDrives">
            View My Drives
        </button>

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

        <hr>

        <button class="btn btn-info mb-3" @click="loadApplications">
            View Applications
        </button>

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

const dashboard = ref(null)
const drives = ref([])
const applications = ref([])

const job_title = ref("")
const job_description = ref("")
const required_skills = ref("")
const minimum_cgpa = ref("")
const eligible_branch = ref("")
const eligible_year = ref("")
const salary_lpa = ref("")
const application_deadline = ref("")

async function loadDashboard() {

    const response = await api.get("/company/dashboard")

    dashboard.value = response.data

}

async function createDrive() {

    if (!job_title.value) {
        alert("Job title is required")
        return
    }

    if (!application_deadline.value) {
        alert("Application deadline is required")
        return
    }

    try {

        const response = await api.post("/company/drives", {
            job_title: job_title.value,
            job_description: job_description.value,
            required_skills: required_skills.value,
            minimum_cgpa: minimum_cgpa.value,
            eligible_branch: eligible_branch.value,
            eligible_year: eligible_year.value,
            salary_lpa: salary_lpa.value,
            application_deadline: application_deadline.value
        })

        alert(response.data.message)

        job_title.value = ""
        job_description.value = ""
        required_skills.value = ""
        minimum_cgpa.value = ""
        eligible_branch.value = ""
        eligible_year.value = ""
        salary_lpa.value = ""
        application_deadline.value = ""

        loadDashboard()
        loadDrives()

    }

    catch (error) {
        const msg = error.response?.data?.message || error.message || "Failed to create drive"
        alert(msg)
    }

}

async function loadDrives() {

    const response = await api.get("/company/drives")

    drives.value = response.data.drives

}

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
    loadDashboard()
})

</script>
