import { browser } from '$app/environment';
import { goto } from '$app/navigation';
import { authToken } from '$lib/stores/auth';
import { startLoading } from '$lib/stores/loading';
import { addError } from '$lib/stores/notification';
import type { Course } from '$lib/types/course.type';
export const load = async () => {
    let token = null
     if (browser) {
         token = localStorage.getItem('authToken');
     }
    if (!token) {
        goto('/'); 
    }
    let courses = <Course[]>[]
    const loading = startLoading();
    try {
        const res = ''
    } catch (error) {
        addError(error as string)
    }
    
};