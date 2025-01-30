import { writable } from 'svelte/store';

export const errors =  writable<string[]>([]);
export const messages =  writable<string[]>([]);

export function addError(error: string) {
    errors.update((currentErrors) => [...currentErrors, error]);
}
export function removeError(index: number) {
    errors.update((currentErrors) => currentErrors.filter((_, i) => i !== index));
}
export function clearErrors() {
    errors.set([]);
}
export function addMessage(message: string) {
    messages.update((currentMessages) => [...currentMessages, message]);
}
export function removeMessage(index: number) {
    messages.update((currentMessages) => currentMessages.filter((_, i) => i !== index));
}
export function clearMessages() {
    messages.set([]);
}