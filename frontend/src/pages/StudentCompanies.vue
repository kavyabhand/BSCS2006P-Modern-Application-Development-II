<template>
    <div class="container mt-5">

        <h2>Search Companies</h2>

        <div class="mb-3">
            <input
                class="form-control"
                placeholder="Search by company name"
                v-model="search"
            >
        </div>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadCompanies">
                Search
            </button>
            <RouterLink class="btn btn-secondary" to="/student/dashboard">
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
                </tr>
            </thead>

            <tbody>

                <tr v-for="company in companies" :key="company.id">

                    <td>{{ company.company_name }}</td>
                    <td>{{ company.industry }}</td>
                    <td>{{ company.location }}</td>
                    <td>{{ company.website }}</td>

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

    const response = await api.get("/student/companies?q=" + search.value)

    companies.value = response.data.companies

}

onMounted(() => {
    loadCompanies()
})

</script>
