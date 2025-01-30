<script lang="ts">
    import { errors, messages, clearErrors, clearMessages, removeError,removeMessage } from '$lib/stores/notification';

    function clearAll() {
        clearErrors();
        clearMessages();
    }
</script>

<div class="notification-container">
    {#each $errors as error, index}
        <div class="notification error">
            <span>{error}</span>
            <button on:click={() => removeError(index)}>×</button>
        </div>
    {/each}
    {#each $messages as message, index}
        <div class="notification message">
            <span>{message}</span>
            <button on:click={() => removeMessage(index)}>×</button>
        </div>
    {/each}
    {#if $errors.length > 0 || $messages.length > 0}
        <div class="clear-all">
            <button on:click={clearAll}>Clear All</button>
        </div>
    {/if}
</div>

<style>
    .notification-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.9);
        border-top: 1px solid #e1e1e1;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        max-height: 50vh;
        overflow-y: auto;
    }

    .notification {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        font-size: 0.9rem;
    }

    .error {
        background-color: #ffe6e6;
        color: #cc0000;
        border: 1px solid #cc0000;
    }

    .message {
        background-color: #e6ffe6;
        color: #006600;
        border: 1px solid #006600;
    }

    button {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        color: inherit;
        padding: 0 0.5rem;
    }

    .clear-all {
        text-align: center;
        margin-top: 1rem;
    }

    .clear-all button {
        background-color: #f8f9fa;
        border: 1px solid #e1e1e1;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.9rem;
    }

    .clear-all button:hover {
        background-color: #e1e1e1;
    }
</style>