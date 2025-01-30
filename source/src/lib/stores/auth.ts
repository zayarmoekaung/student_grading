import { browser } from '$app/environment';
import { writable } from 'svelte/store';

interface User {
    id: string;
    email: string;
    name?: string;
    role: string;
    active: boolean;
}

export const authToken = writable<string | null>(browser ? localStorage.getItem('authToken') || null : null);

export const user = writable<User | null>(null);
export const authed = writable<Boolean>(false);
export function setAuth(token: string, userData: User) {
    if (browser) {
        localStorage.setItem('authToken', token);
    }
    authToken.set(token);
    user.set(userData);
    console.log(user);
    authed.set(true)
}

export function clearAuth() {
    if (browser) {
        localStorage.removeItem('authToken');
    }
    authToken.set(null);
    user.set(null);
    authed.set(false);
}