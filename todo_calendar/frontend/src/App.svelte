<script lang="ts">
  import { add, formatISO, parseISO, sub } from 'date-fns';
  import { onMount } from 'svelte';

  import type { TaskItem } from './types';

  let currentDate: Date = new Date();
  let dateString: string;
  let dialogEl: HTMLDialogElement;
  let tasks: Array<TaskItem> = [];

  async function changeDate(dateString: string, func: Function) {
    const dateObject = parseISO(dateString);
    currentDate = func(dateObject, { days: 1 });
    await updateDateAndFetch(currentDate);
  }

  function closeModal() {
    if (dialogEl) {
      dialogEl.close();
    }
  }

  async function createTask(inputData: SubmitEvent) {
    const target = inputData.target as HTMLFormElement;

    if (inputData?.target) {
      const formData = new FormData(target);
      const response = await fetch(target.action, {
        body: JSON.stringify(Object.fromEntries(formData)),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        method: 'POST',        
      });
      const createdTask: TaskItem = await response.json();

      if (createdTask && createdTask.tasksDate === dateString) {
        tasks = [...tasks, createdTask];
      }
    }
  }

  function dateToISO(date: Date) {
    return formatISO(date, { representation: 'date' });
  }

  function openModal() {
    if (dialogEl) {
      dialogEl.showModal();
    }
  }

  async function pickDate(event: Event): Promise<void> {
    await updateDateAndFetch(parseISO((event.target as HTMLInputElement).value));
  }

  async function updateDateAndFetch(date: Date): Promise<void> {
    dateString = dateToISO(date);

    const url = new URL('http://localhost:8000/tasks');
    url.searchParams.append('tasks_date', dateString);
    const response = await fetch(url, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    tasks = await response.json() || [];
  }

  onMount(async () => {
    await updateDateAndFetch(currentDate);
  })
</script>

<main>
  <h1>To Do Calendar</h1>
  <div class=nav-block>
    <button on:click={async () => await changeDate(dateString, sub)}>
      Prev
    </button>
    <input
      type=date
      value={dateString}
      on:change={async (e) => await pickDate(e)}
    >
    <button on:click={async () => await changeDate(dateString, add)}>
      Next
    </button>
  </div>
  <ul>
    {#each tasks as task}
      <li>
        <input checked={task.isCompleted} type=checkbox>
        {task.description}
      </li>
    {/each}
  </ul>
  <button on:click={openModal}>
    Create new task
  </button>
  <dialog bind:this={dialogEl}>
    <form
      action=http://localhost:8000/tasks
      method="dialog"
      on:submit={createTask}
    >
      <h2>New task</h2>
      <label for=tasksDate>
        Date
        <input name=tasksDate type=date value={dateToISO(new Date())}>
      </label>
      <label for=description>
        Description
        <input name=description type=text>
      </label>
      <input type=submit value=Add>
      <input type=button value=Cancel on:click={closeModal}>
    </form>
  </dialog>
</main>

<style>
.nav-block {
  display: grid;
  gap: 15px;
  grid-template-columns: 85px 1fr 85px;
  justify-content: center;
}

h1 {
  text-align: center;
}

main {
  width: 325px;
}

ul {
  list-style-type: none;
  padding: 0;
}

ul li input {
  margin-right: 5px;
}
</style>
