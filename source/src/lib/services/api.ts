import { get } from 'svelte/store';
import axios from 'axios';
import { Course } from '$lib/types/course.type';
import { authToken, clearAuth } from '../stores/auth'; // Import clearAuth
import { goto } from '$app/navigation'; // Import goto for navigation
import type { Student } from '$lib/types/students.type';

const API_URL = 'http://localhost:5000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
});

// Request interceptor to add the auth token to headers
api.interceptors.request.use((config) => {
    const token = get(authToken);
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response && error.response.status === 401) {
          
            clearAuth();
            goto('/'); 
        }
      
        return Promise.reject(error);
    }
);

// Login function
export async function login(email: string, password: string) {
    const response = await api.post('/api/login', { email, password });
    return response.data;
}

// Fetch Courses function
export async function fetchCourses(
    page: number = 1,
    per_page: number = 10,
    semester: string = "",
) {
    const params = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString(),
    });
    if (semester) {
        params.append('semester', semester);
    }
    const url = `/api/courses?${params.toString()}`;
    const response = await api.get(url);
    return response;
}

// Fetch Students function
export async function fetchStudents(
    page: number = 1,
    per_page: number = 10,
    course_id: number,
) {
    const params = new URLSearchParams({
        page: page.toString(),
        per_page: per_page.toString(),
        course_id: course_id.toString(),
    });
    const url = `/api/course/students?${params.toString()}`;
    const response = await api.get(url);
    return response;
}

// Create Course function
export async function createCourse(course: Course) {
    const url = `/api/course/create`;
    const response = await api.post(url, course);
    return response;
}
export async function addStudent(student: Student) {
    const url = `/api/student/create`;
    const response = await api.post(url, student);
    return response;
}
export async function enrollStudent(enrollment: {student_id: string, course_id: string}) {
    const url = `/api/course/enroll`;
    const response = await api.post(url, enrollment);
    return response;
}