<script lang="ts">
  import { add, formatISO, parseISO, sub } from 'date-fns';
  import { onMount } from 'svelte';

  import type { TaskItem } from './types';

  let currentDate: Date = new Date();
  let dateString: string;
  let tasks: Array<TaskItem> = [];

  async function changeDate(dateString: string, func: Function) {
    const dateObject = parseISO(dateString);
    currentDate = func(dateObject, { days: 1 });
    await updateDateAndFetch(currentDate);
  }

  async function pickDate(event: Event): Promise<void> {
    await updateDateAndFetch(parseISO((event.target as HTMLInputElement).value));
  }

  async function updateDateAndFetch(date: Date): Promise<void> {
    dateString = formatISO(date, { representation: 'date' });

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
        <input disabled type=checkbox>
        {task.description}
      </li>
    {/each}
  </ul>
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
