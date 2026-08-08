<template>
    <div class="container mt-5">

        <h2>Pending Companies</h2>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadCompanies">
                Load Companies
            </button>
            <RouterLink class="btn btn-secondary" to="/admin/dashboard">
                Back
            </RouterLink>
        </div>

        <table class="table table-bordered" v-if="companies.length">

            <thead>

                <tr>
                    <th>Company</th>
                    <th>Industry</th>
                    <th>Location</th>
                    <th>Website</th>
                    <th>HR</th>
                    <th>Email</th>
                    <th>Approve</th>
                    <th>Reject</th>
                </tr>

            </thead>

            <tbody>

                <tr v-for="company in companies" :key="company.id">

                    <td>{{ company.company_name }}</td>
                    <td>{{ company.industry || "-" }}</td>
                    <td>{{ company.location || "-" }}</td>
                    <td>{{ company.website || "-" }}</td>
                    <td>{{ company.hr_name }}</td>
                    <td>{{ company.hr_email }}</td>

                    <td>

                        <button
                            class="btn btn-success btn-sm"
                            @click="approveCompany(company.id)"
                        >
                            Approve
                        </button>

                    </td>

                    <td>

                        <button
                            class="btn btn-danger btn-sm"
                            @click="rejectCompany(company.id)"
                        >
                            Reject
                        </button>

                    </td>

                </tr>

            </tbody>

        </table>

        <p v-else class="text-muted">No pending companies</p>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const companies = ref([])

async function loadCompanies() {

    const response = await api.get("/admin/pending-companies")

    companies.value = response.data.companies

}

async function approveCompany(id) {

    const response = await api.put("/admin/approve-company/" + id, {})

    alert(response.data.message)

    loadCompanies()

}

async function rejectCompany(id) {

    const response = await api.put("/admin/reject-company/" + id, {})

    alert(response.data.message)

    loadCompanies()

}

onMounted(() => {
    loadCompanies()
})

</script>
