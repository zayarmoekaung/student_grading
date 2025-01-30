<script lang="ts">
    import { course } from "$lib/stores/course";
    import { clearCourse } from "$lib/stores/course";
    import { startLoading } from "$lib/stores/loading";
    import { addError, addMessage } from "$lib/stores/notification";
    import { createCourse } from "$lib/services/api";
    import { get } from "svelte/store";

    // Function to handle saving the course
    async function handleSave() {
        const newCourse = get(course); 
        const loading = startLoading();
        try {
            if (newCourse) {
                const res = await createCourse(newCourse); 
                const data = res.data;
                if (data && data.success) {
                    addMessage('Course Created'); 
                    clearCourse(); 
                }
            }
        } catch (error) {
            console.log(error);
            addError('Course Create Failed'); 
        } finally {
            loading.stop_loading(); 
        }
    }
</script>

<div class="modal active" id="modal-id">
    <a href="#close" class="modal-overlay" aria-label="Close" on:click={clearCourse}></a>
    <div class="modal-container">
        <div class="modal-header">
            <a href="#close" class="btn btn-clear float-right" aria-label="Close"></a>
            <div class="modal-title h5">New Course</div>
        </div>
        <div class="modal-body">
            {#if $course}
            <div class="content">
                <!-- Instructor Input -->
                <div class="form-group">
                    <label class="form-label" for="instructor">Instructor</label>
                    <input
                        class="form-input"
                        type="text"
                        id="instructor"
                        bind:value={$course.instructor}
                        placeholder="Enter Instructor Name"
                    />
                </div>

                <!-- Course Name Input -->
                <div class="form-group">
                    <label class="form-label" for="name">Course Name</label>
                    <input
                        class="form-input"
                        type="text"
                        id="name"
                        bind:value={$course.name}
                        placeholder="Enter Course Name"
                    />
                </div>

                <!-- Semester Input -->
                <div class="form-group">
                    <label class="form-label" for="semester">Semester</label>
                    <input
                        class="form-input"
                        type="text"
                        id="semester"
                        bind:value={$course.semester}
                        placeholder="Enter Semester"
                    />
                </div>
            </div>
            {/if}
        </div>
        <div class="modal-footer">
            <button class="btn btn-primary" on:click={handleSave}>Save</button>
            <button class="btn btn-primary" on:click={clearCourse}>Cancel</button>
        </div>
    </div>
</div>

<style>
    .modal {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .modal-container {
        max-width: 600px;
        width: 100%;
    }

    .modal-title {
        margin-bottom: 1rem;
    }

    .form-group {
        margin-bottom: 1rem;
    }

    .form-label {
        display: block;
        margin-bottom: 0.5rem;
    }

    .form-input {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    .btn {
        margin-right: 0.5rem;
    }
</style>