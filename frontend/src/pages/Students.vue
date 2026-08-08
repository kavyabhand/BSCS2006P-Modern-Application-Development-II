<template>
    <div class="container mt-5">

        <h2>Students</h2>

        <div class="mb-3">
            <input
                class="form-control"
                placeholder="Search by name or roll number"
                v-model="search"
            >
        </div>

        <div class="mb-3 d-flex gap-2 flex-wrap">
            <button class="btn btn-primary" @click="loadStudents">
                Search
            </button>
            <RouterLink class="btn btn-secondary" to="/admin/dashboard">
                Back
            </RouterLink>
        </div>

        <table
            class="table table-bordered"
            v-if="students.length"
        >

            <thead>

                <tr>
                    <th>Name</th>
                    <th>Roll Number</th>
                    <th>Branch</th>
                    <th>CGPA</th>
                    <th>Phone</th>
                    <th>Blacklist</th>
                    <th>Deactivate</th>
                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="student in students"
                    :key="student.id"
                >

                    <td>{{ student.name }}</td>
                    <td>{{ student.roll_number }}</td>
                    <td>{{ student.branch }}</td>
                    <td>{{ student.cgpa }}</td>
                    <td>{{ student.phone }}</td>

                    <td>

                        <button
                            class="btn btn-danger btn-sm"
                            @click="blacklistStudent(student.user_id)"
                        >
                            Blacklist
                        </button>

                    </td>

                    <td>

                        <button
                            class="btn btn-warning btn-sm"
                            @click="deactivateStudent(student.user_id)"
                        >
                            Deactivate
                        </button>

                    </td>

                </tr>

            </tbody>

        </table>

        <p v-else class="text-muted">No students found</p>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const students = ref([])
const search = ref("")

async function loadStudents() {

    const response = await api.get("/admin/students?q=" + search.value)

    students.value = response.data.students

}

async function blacklistStudent(id) {

    const response = await api.put("/admin/blacklist-student/" + id, {})

    alert(response.data.message)

    loadStudents()

}

async function deactivateStudent(id) {

    const response = await api.put("/admin/deactivate-student/" + id, {})

    alert(response.data.message)

    loadStudents()

}

onMounted(() => {
    loadStudents()
})

</script>