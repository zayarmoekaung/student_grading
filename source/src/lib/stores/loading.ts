import { writable } from 'svelte/store';

interface LoadingObject {
    id: string; 
    stop_loading: () => void; 
}

const loadings = writable<LoadingObject[]>([]);

export function startLoading(): LoadingObject {
    const loadingObject: LoadingObject = {
        id: Math.random().toString(36).substring(2, 9), 
        stop_loading: () => {
            loadings.update((currentLoadings) =>
                currentLoadings.filter((loading) => loading.id !== loadingObject.id)
            );
        },
    };

    loadings.update((currentLoadings) => [...currentLoadings, loadingObject]);

    return loadingObject;
}

export function isLoading(): boolean {
    let loading = false;
    loadings.subscribe((currentLoadings) => {
        loading = currentLoadings.length > 0;
    })();
    return loading;
}

export const loadingStore = {
    subscribe: loadings.subscribe,
    startLoading,
    isLoading,
};