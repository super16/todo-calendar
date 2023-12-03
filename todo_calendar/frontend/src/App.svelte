<script lang="ts">
  import { add, formatISO, parseISO, sub } from 'date-fns'
  import { onMount } from 'svelte'

  import type { Duration } from 'date-fns'
  import type { TaskItem } from './types'

  let currentDate: Date = new Date()
  let dateString: string
  let dialogEl: HTMLDialogElement | null
  let formEl: HTMLFormElement | null
  let tasks: TaskItem[] = []

  async function changeDate (
    dateString: string,
    func: (date: Date, duration: Duration) => Date
  ): Promise<void> {
    const dateObject = parseISO(dateString)
    currentDate = func(dateObject, { days: 1 })
    await updateDateAndFetch(currentDate)
  }

  function closeModal (): void {
    if (dialogEl !== null) {
      dialogEl.close()
    }
  }

  async function createTask (inputData: SubmitEvent): Promise<void> {
    const target = inputData.target as HTMLFormElement | null

    if (target !== null) {
      const formData = new FormData(target)
      const response = await fetch(target.action, {
        body: JSON.stringify(Object.fromEntries(formData)),
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST'
      })
      const createdTask: TaskItem | null = await response.json()

      if (createdTask !== null && createdTask.tasksDate === dateString) {
        tasks = [...tasks, createdTask]
      }
    }
  }

  function dateToISO (date: Date): string {
    return formatISO(date, { representation: 'date' })
  }

  function openModal (): void {
    if (formEl !== null) {
      Array.from(formEl.elements).forEach((value: Element) => {
        const newValue = value as HTMLInputElement
        switch (newValue.name) {
          case 'tasksDate':
            newValue.value = dateToISO(currentDate)
            break
          case 'description':
            newValue.value = ''
            break
          default:
            break
        }
        value = newValue
      })
    }
    if (dialogEl !== null) {
      dialogEl.showModal()
    }
  }

  async function pickDate (event: Event): Promise<void> {
    await updateDateAndFetch(parseISO((event.target as HTMLInputElement).value))
  }

  async function updateDateAndFetch (date: Date): Promise<void> {
    dateString = dateToISO(date)

    const url = new URL('http://localhost:8000/tasks')
    url.searchParams.append('tasks_date', dateString)
    const response = await fetch(url, {
      method: 'GET',
      headers: { Accept: 'application/json' }
    })
    tasks = await response.json() as TaskItem[] ?? []
  }

  async function updateTaskStatus (event: Event, taskId: string): Promise<void> {
    const response = await fetch(
      new URL(`http://localhost:8000/tasks/${taskId}/complete`
      ), {
        body: JSON.stringify({
          isCompleted: (event.target as HTMLInputElement).checked
        }),
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'PATCH'
      })
    const updatedStatusTask: TaskItem | null = await response.json()
    if (updatedStatusTask !== null) {
      const taskToSwapIdx = tasks.findIndex((task) => {
        return task.uuid === updatedStatusTask.uuid
      })
      if (taskToSwapIdx > -1) {
        tasks[taskToSwapIdx] = updatedStatusTask
        tasks = [...tasks]
      }
    }
  }

  onMount(async () => {
    await updateDateAndFetch(currentDate)
  })
</script>

<main>
  <h1>To Do Calendar</h1>
  <div class=nav-block>
    <button on:click={async () => { await changeDate(dateString, sub) }}>
      Prev
    </button>
    <input
      type=date
      value={dateString}
      on:change={async (e) => { await pickDate(e) }}
    >
    <button on:click={async () => { await changeDate(dateString, add) }}>
      Next
    </button>
  </div>
  <ul>
    {#each tasks as task}
      <li>
        <input
          id={task.uuid}
          checked={task.isCompleted}
          type=checkbox
          on:change={async (e) => { await updateTaskStatus(e, task.uuid) }}
        >
        <label for={task.uuid}>
          {task.description}
        </label>
      </li>
    {/each}
  </ul>
  <button on:click={openModal}>
    Create new task
  </button>
  <dialog bind:this={dialogEl}>
    <h2>New task</h2>
    <form
      bind:this={formEl}
      action=http://localhost:8000/tasks
      method="dialog"
      on:submit={createTask}
    >
      <label for=tasksDate>
        Date
        <input
          id=tasksDate
          name=tasksDate
          type=date
          value={dateToISO(new Date())}
        >
      </label>
      <label for=description>
        Description
        <input
          id=description
          name=description
          type=text
        >
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
