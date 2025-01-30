<script lang="ts">
    import { setAuth } from '$lib/stores/auth';
    import { login } from '$lib/services/api';
    import { goto } from '$app/navigation';
    import { addError, addMessage } from '$lib/stores/notification';
    import { startLoading } from '$lib/stores/loading';
    let email = '';
    let password = '';

    async function handleLogin() {
        const loading = startLoading();
        try {
            const { access_token, user_info } = await login(email, password);
            setAuth(access_token, user_info);
            goto('/dashboard'); 
            addMessage('Login Success')
        } catch (err :any) {
           const error = err.response?.data?.message || 'Login failed';
           addError(error)
        } finally {
            loading.stop_loading();
        }
    }
</script>

<div class="container grid-lg">
    <div class="columns">
        <div class="column col-6 col-mx-auto">
            <div class="card">
                <div class="card-header">
                    <div class="card-title h3">Login</div>
                </div>
                <div class="card-body">
                    <form on:submit|preventDefault={handleLogin}>
                        <div class="form-group">
                            <label class="form-label" for="email">Email</label>
                            <input
                                class="form-input"
                                type="email"
                                id="email"
                                bind:value={email}
                                placeholder="Enter your email"
                                required
                            />
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="password">Password</label>
                            <input
                                class="form-input"
                                type="password"
                                id="password"
                                bind:value={password}
                                placeholder="Enter your password"
                                required
                            />
                        </div>
                        <div class="form-group">
                            <button class="btn btn-primary" type="submit">Login</button>
                        </div>
                    </form>
                </div>
                <div class="card-footer">
                    <p class="text-center">
                        Don't have an account? <a href="/register">Register here</a>.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .container {
        margin-top: 2rem;
    }
    .card {
        margin-top: 2rem;
        box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.1);
    }
    .card-header {
        background-color: #f8f9fa;
        border-bottom: 1px solid #e1e1e1;
    }
    .card-footer {
        background-color: #f8f9fa;
        border-top: 1px solid #e1e1e1;
    }
</style>