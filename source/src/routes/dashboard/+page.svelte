<script lang="ts">
    import { onMount } from "svelte";
    import { startLoading } from "$lib/stores/loading";
    import { addError } from "$lib/stores/notification";
    import { Course } from "$lib/types/course.type";
    import { fetchCourses } from "$lib/services/api";
    import NewCourse from "$lib/components/NewCourse.svelte";
    import { course, makeCourse, setCurrentCourse, currentcourse } from "$lib/stores/course";
    import Students from "$lib/components/Students.svelte";
    // State for courses and pagination
    let courses: Array<Course> = [];
    let pagination = {
        page: 1,
        per_page: 10,
        pages: 1,
        count: 0,
    };
    let semesterFilter = "";

    async function fetchCourse(
        page: number = 1,
        per_page: number = 10,
        semester: string = "",
    ) {
       const loading = startLoading()
       try {
        const res = await fetchCourses(page, per_page, semester);
        const data = res.data
        if (data) {
            courses = data.courses;
            pagination = data.pagination;
        }
       } catch (error) {
            addError('Fetch Courses Failed')
       }finally{
        loading.stop_loading()
       }
    }

    function handlePageChange(page: number) {
        fetchCourse(page, pagination.per_page, semesterFilter);
    }

    function handleSemesterFilter() {
        fetchCourse(1, pagination.per_page, semesterFilter);
    }
    function handleAddCourse() {
        makeCourse()
    }
    function handleRegisterStudent( course: Course) {
        setCurrentCourse(course)
    }
   
    onMount(() => {
        fetchCourse();
    });
</script>
{#if $course}
    <NewCourse/>
{/if}
{#if $currentcourse}
    <Students/>
{/if}
<div class="container">
    <h1>Courses</h1>

    <div class="container col-12 flex-row">
        <!-- Search Box -->
    <div class="search-box">
        <input
            type="text"
            bind:value={semesterFilter}
            placeholder="Filter by semester"
        />
        <button on:click={handleSemesterFilter}>Search</button>
    </div>
    <button on:click={handleAddCourse}>Add Course</button>
    </div>

    <!-- Table -->
    <table>
        <thead>
            <tr>
                <th>Course ID</th>
                <th>Name</th>
                <th>Instructor</th>
                <th>Semester</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {#each courses as course}
                <tr>
                    <td>{course.courseID}</td>
                    <td>{course.name}</td>
                    <td>{course.instructor}</td>
                    <td>{course.semester}</td>
                    <td>
                        <button
                            on:click={() =>
                                handleRegisterStudent(course)}
                        >
                            Register Student
                        </button>
                        <button
                            on:click={() =>
                                console.log("Upload Grading:", course.id)}
                        >
                            Upload Grading
                        </button>
                        <button
                            on:click={() =>
                                console.log("View Grading:", course.id)}
                        >
                            View Grading
                        </button>
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>

    <!-- Pagination -->
    <div class="pagination">
        <button
            on:click={() => handlePageChange(pagination.page - 1)}
            disabled={pagination.page === 1}
        >
            Previous
        </button>
        <span>Page {pagination.page} of {pagination.pages}</span>
        <button
            on:click={() => handlePageChange(pagination.page + 1)}
            disabled={pagination.page === pagination.pages}
        >
            Next
        </button>
    </div>
</div>

<style>
    .container {
        padding: 1rem;
    }
    .flex-row{
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    .search-box {
        margin-bottom: 1rem;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
    }

    th,
    td {
        padding: 0.75rem;
        border: 1px solid #ddd;
        text-align: left;
    }

    th {
        background-color: #f8f9fa;
    }

    button {
        margin-right: 0.5rem;
        padding: 0.5rem 1rem;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }

    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
    }
</style>
