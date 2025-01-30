<script lang="ts">
  import '../styles/app.css';
  import { user, clearAuth } from '$lib/stores/auth';
  import { goto } from '$app/navigation';
  import Notification from '$lib/components/Notification.svelte';

  function handleLogout() {
      clearAuth(); 
      goto('/'); 
  }
</script>

{#if $user}
  <header class="navbar">
      <section class="navbar-section">
          <span class="navbar-brand mr-2">Student Grading</span>
      </section>
      <section class="navbar-section">
          <span>{$user.name} ({$user.role})</span>
          <button class="btn btn-link" on:click={handleLogout}>Logout</button>
      </section>
  </header>
{/if}

<main class="container">
  <slot />
  <Notification />
</main>

<style>
  .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background-color: #f8f9fa;
      border-bottom: 1px solid #e1e1e1;
  }

  .navbar-section {
      display: flex;
      align-items: center;
      gap: 1rem;
  }

  .navbar-brand {
      font-weight: bold;
      font-size: 1.25rem;
  }

  .btn-link {
      color: #007bff;
      text-decoration: none;
      background: none;
      border: none;
      cursor: pointer;
      padding: 0;
  }

  .btn-link:hover {
      text-decoration: underline;
  }
</style>