import { createRouter, createWebHistory } from 'vue-router'

import Home from "../pages/Home.vue"
import Login from "../pages/Login.vue"
import Register from "../pages/Register.vue"

import StudentDashboard from "../pages/StudentDashboard.vue"
import StudentDrives from "../pages/StudentDrives.vue"
import StudentApplications from "../pages/StudentApplications.vue"
import StudentProfile from "../pages/StudentProfile.vue"
import StudentCompanies from "../pages/StudentCompanies.vue"

import CompanyDashboard from "../pages/CompanyDashboard.vue"
import CompanyDrives from "../pages/CompanyDrives.vue"
import CompanyApplications from "../pages/CompanyApplications.vue"
import CompanyProfile from "../pages/CompanyProfile.vue"

import AdminDashboard from "../pages/AdminDashboard.vue"
import PendingCompanies from "../pages/PendingCompanies.vue"
import AdminCompanies from "../pages/AdminCompanies.vue"
import PendingDrives from "../pages/PendingDrives.vue"
import AdminAllDrives from "../pages/AdminAllDrives.vue"
import Students from "../pages/Students.vue"
import AdminApplications from "../pages/AdminApplications.vue"

const routes = [
    {
        path: "/",
        component: Home
    },

    {
        path: "/login",
        component: Login
    },

    {
        path: "/register",
        component: Register
    },

    {
        path: "/student",
        redirect: "/student/dashboard"
    },

    {
        path: "/student/dashboard",
        component: StudentDashboard,
        meta: { role: "student" }
    },

    {
        path: "/student/drives",
        component: StudentDrives,
        meta: { role: "student" }
    },

    {
        path: "/student/applications",
        component: StudentApplications,
        meta: { role: "student" }
    },

    {
        path: "/student/profile",
        component: StudentProfile,
        meta: { role: "student" }
    },

    {
        path: "/student/companies",
        component: StudentCompanies,
        meta: { role: "student" }
    },

    {
        path: "/company",
        redirect: "/company/dashboard"
    },

    {
        path: "/company/dashboard",
        component: CompanyDashboard,
        meta: { role: "company" }
    },

    {
        path: "/company/drives",
        component: CompanyDrives,
        meta: { role: "company" }
    },

    {
        path: "/company/applications",
        component: CompanyApplications,
        meta: { role: "company" }
    },

    {
        path: "/company/profile",
        component: CompanyProfile,
        meta: { role: "company" }
    },

    {
        path: "/admin",
        redirect: "/admin/dashboard"
    },

    {
        path: "/admin/dashboard",
        component: AdminDashboard,
        meta: { role: "admin" }
    },

    {
        path: "/admin/pending-companies",
        component: PendingCompanies,
        meta: { role: "admin" }
    },

    {
        path: "/admin/companies",
        component: AdminCompanies,
        meta: { role: "admin" }
    },

    {
        path: "/admin/pending-drives",
        component: PendingDrives,
        meta: { role: "admin" }
    },

    {
        path: "/admin/all-drives",
        component: AdminAllDrives,
        meta: { role: "admin" }
    },

    {
        path: "/admin/students",
        component: Students,
        meta: { role: "admin" }
    },

    {
        path: "/admin/applications",
        component: AdminApplications,
        meta: { role: "admin" }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token")
    const role = localStorage.getItem("role")
    const publicPaths = ["/", "/login", "/register"]

    if (!publicPaths.includes(to.path) && !token) {
        next("/")
        return
    }

    if (to.meta.role && to.meta.role !== role) {
        next("/")
        return
    }

    if (publicPaths.includes(to.path) && token) {
        if (role === "student") next("/student/dashboard")
        else if (role === "company") next("/company/dashboard")
        else next("/admin/dashboard")
        return
    }

    next()
})

export default router
