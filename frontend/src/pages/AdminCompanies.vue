<template>
    <div class="container mt-5">

        <h2>Search Companies</h2>

        <div class="mb-3">
            <input
                class="form-control"
                placeholder="Search by name or industry"
                v-model="search"
            >
        </div>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadCompanies">
                Search
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
                    <th>Status</th>
                    <th>HR</th>
                    <th>Blacklist</th>
                    <th>Deactivate</th>
                </tr>
            </thead>

            <tbody>

                <tr v-for="company in companies" :key="company.id">

                    <td>{{ company.company_name }}</td>
                    <td>{{ company.industry }}</td>
                    <td>{{ company.location }}</td>
                    <td>{{ company.approval_status }}</td>
                    <td>{{ company.hr_name }}</td>

                    <td>
                        <button class="btn btn-danger btn-sm" @click="blacklistCompany(company.user_id)">
                            Blacklist
                        </button>
                    </td>

                    <td>
                        <button class="btn btn-warning btn-sm" @click="deactivateCompany(company.user_id)">
                            Deactivate
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

const companies = ref([])
const search = ref("")

async function loadCompanies() {

    const response = await api.get("/admin/companies?q=" + search.value)

    companies.value = response.data.companies

}

async function blacklistCompany(id) {

    const response = await api.put("/admin/blacklist-company/" + id, {})

    alert(response.data.message)

    loadCompanies()

}

async function deactivateCompany(id) {

    const response = await api.put("/admin/deactivate-company/" + id, {})

    alert(response.data.message)

    loadCompanies()

}

onMounted(() => {
    loadCompanies()
})

</script>
