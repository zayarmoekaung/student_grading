import { writable } from 'svelte/store';
import { Course } from '$lib/types/course.type';

export const course = writable<Course| null>(null);
export const currentcourse = writable<Course| null>(null);
export function makeCourse() {
    course.set(new Course)
}
export function clearCourse() {
    course.set(null)
}
export function setCurrentCourse(c : Course) {
    currentcourse.set(c)
}
export function clearCurrentCourse() {
    currentcourse.set(null)
}