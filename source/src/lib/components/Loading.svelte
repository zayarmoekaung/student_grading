<script lang="ts">
    import { loadingStore } from '$lib/stores/loading';
</script>

{#if $loadingStore.length > 0}
    <div class="loading-overlay">
        <div class="spinner"></div>
    </div>
{/if}

<style>
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.9); /* Semi-transparent white background */
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000; /* Ensure it's on top of other elements */
    }

    .spinner {
        border: 4px solid rgba(0, 0, 0, 0.1);
        border-top: 4px solid #007bff; /* Blue color for the spinner */
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
</style>