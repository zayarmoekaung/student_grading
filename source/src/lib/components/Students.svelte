<script lang="ts">
    import { onMount } from "svelte";
    import { get } from "svelte/store";
    import { currentcourse, clearCurrentCourse } from "$lib/stores/course";
    import {
        fetchStudents,
        addStudent,
        enrollStudent,
    } from "$lib/services/api";

    import { Student } from "$lib/types/students.type";
    import { startLoading } from "$lib/stores/loading";
    import { addError, addMessage } from "$lib/stores/notification";

    let students: Array<Student> = [];
    let pagination = {
        page: 1,
        per_page: 10,
        pages: 1,
        count: 0,
    };
    const course = get(currentcourse);

    let newStudent = {
        name: "",
        email: "",
        studentID: "",
    };
    let isAddStudentModalOpen = false;

    async function fetchStudent(page: number = 1, per_page: number = 10) {
        if (course) {
            const loading = startLoading();
            try {
                const res = await fetchStudents(page, per_page, course.id);
                const data = res.data;
                if (data) {
                    students = data.students;
                    pagination = data.pagination;
                }
            } catch (error) {
                addError("Fetch Students Failed");
            } finally {
                loading.stop_loading();
            }
        }
    }

    function handlePageChange(page: number) {
        fetchStudent(page, pagination.per_page);
    }

    function openAddStudentModal() {
        isAddStudentModalOpen = true;
    }

    function closeAddStudentModal() {
        isAddStudentModalOpen = false;
    }

    async function handleAddStudent() {
        const loading = startLoading();
        try {
            const res = await addStudent(newStudent);
            const data = res.data;
            if (data.success) {
                const student = data.data as Student;
                if (student && course) {
                    const student_id = student.studentID;
                    const course_id = course.courseID;
                    const enroll = await enrollStudent({
                        student_id,
                        course_id,
                    });
                }
                addMessage("Student Added Successfully");
                closeAddStudentModal();
                fetchStudent();
            } else {
                addError("Failed to Add Student");
            }
        } catch (error) {
            addError("Failed to Add Student");
        } finally {
            loading.stop_loading();
        }
    }

    onMount(() => {
        fetchStudent();
    });

    function close() {
        clearCurrentCourse();
    }
</script>

<div class="modal active">
    <a
        href="#close"
        class="modal-overlay"
        aria-label="Close"
        on:click={clearCurrentCourse}
    ></a>
    <div class="modal-container">
        <div class="modal-header">
            <h2>Students</h2>
            <button class="close-btn" on:click={clearCurrentCourse}
                >&times;</button
            >
        </div>
        <div class="modal-body">
            <button class="add-btn" on:click={openAddStudentModal}
                >Add Student</button
            >
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Student ID</th>
                    </tr>
                </thead>
                <tbody>
                    {#each students as student}
                        <tr>
                            <td>{student.id}</td>
                            <td>{student.name}</td>
                            <td>{student.email}</td>
                            <td>{student.studentID}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
            <div class="pagination">
                {#if pagination.pages > 1}
                    {#each Array(pagination.pages) as _, i}
                        <button on:click={() => handlePageChange(i + 1)}
                            >{i + 1}</button
                        >
                    {/each}
                {/if}
            </div>
        </div>
    </div>
</div>

<!-- Add Student Modal -->
{#if isAddStudentModalOpen}
    <div class="modal active">
        <a
            href="#close"
            class="modal-overlay"
            aria-label="Close"
            on:click={closeAddStudentModal}
        ></a>
        <div class="modal-container">
            <div class="modal-header">
                <h2>Add New Student</h2>
                <button class="close-btn" on:click={closeAddStudentModal}
                    >&times;</button
                >
            </div>
            <div class="modal-body">
                <form on:submit|preventDefault={handleAddStudent}>
                    <div>
                        <label for="name">Name:</label>
                        <input
                            type="text"
                            id="name"
                            bind:value={newStudent.name}
                            required
                        />
                    </div>
                    <div>
                        <label for="email">Email:</label>
                        <input
                            type="email"
                            id="email"
                            bind:value={newStudent.email}
                            required
                        />
                    </div>
                    <button type="submit">Add Student</button>
                </form>
            </div>
        </div>
    </div>
{/if}

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

    .close-btn {
        background: none;
        border: none;
        font-size: 20px;
        cursor: pointer;
    }

    .add-btn {
        float: right;
        margin-bottom: 10px;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th,
    td {
        border: 1px solid #ddd;
        padding: 8px;
    }

    .pagination button {
        margin: 5px;
    }

    form div {
        margin-bottom: 10px;
    }

    form input {
        width: 100%;
        padding: 8px;
    }

    form button {
        margin-top: 10px;
    }
</style>
