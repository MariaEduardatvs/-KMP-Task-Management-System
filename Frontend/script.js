console.log("Task management JavaScript loaded");

// =====================================================
// COMPLETE TASK
// =====================================================

async function completeTask(taskId) {
  try {
    const response = await fetch(`/tasks/${taskId}/complete`, {
      method: "PUT",
    });

    const data = await response.json();

    if (response.ok) {
      alert(data.message);
      location.reload();
    } else {
      alert(data.message);
    }
  } catch (error) {
    console.error("Error completing task:", error);
    alert("An error occurred while completing the task.");
  }
}

// =====================================================
// DELETE TASK
// =====================================================

async function deleteTask(taskId) {
  const confirmed = confirm("Are you sure you want to delete this task?");

  if (!confirmed) {
    return;
  }

  try {
    const response = await fetch(`/tasks/${taskId}`, {
      method: "DELETE",
    });

    const data = await response.json();

    if (response.ok) {
      alert(data.message);
      location.reload();
    } else {
      alert(data.message);
    }
  } catch (error) {
    console.error("Error deleting task:", error);
    alert("An error occurred while deleting the task.");
  }
}

// =====================================================
// SHOW / HIDE EDIT FORM
// =====================================================
function showEditForm(taskId) {
  const form = document.getElementById(`edit-form-${taskId}`);

  if (!form) {
    return;
  }
  form.classList.toggle("d-none");
}

// =====================================================
// EDIT TASK
// =====================================================

async function editTask(taskId) {
  const titleInput = document.getElementById(`edit-title-${taskId}`);
  const descriptionInput = document.getElementById(
    `edit-description-${taskId}`,
  );
  const dueDateInput = document.getElementById(`edit-due-date-${taskId}`);

  if (!titleInput || !descriptionInput || !dueDateInput) {
    alert("Could not find the edit form.");
    return;
  }

  const title = titleInput.value.trim();
  const description = descriptionInput.value.trim();
  const dueDate = dueDateInput.value;

  if (!title) {
    alert("Task title is required.");
    return;
  }

  if (!dueDate) {
    alert("Due date is required.");
    return;
  }

  try {
    const response = await fetch(`/tasks/${taskId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        title: title,
        description: description,
        due_date: dueDate,
        assigned_to: null,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      alert(data.message);
      location.reload();
    } else {
      alert(data.message);
    }
  } catch (error) {
    console.error("Error editing task:", error);
    alert("An error occurred while editing the task.");
  }
}

// =====================================================
// ADD SUBTASK
// =====================================================

async function addSubtask(taskId) {
  const input = document.getElementById(`subtask-title-${taskId}`);

  if (!input) {
    console.error(`Subtask input not found for task ${taskId}`);
    return;
  }

  const title = input.value.trim();

  if (!title) {
    alert("Please enter a sub-task title.");
    return;
  }

  try {
    const response = await fetch(`/tasks/${taskId}/subtasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: title,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      alert(data.message);
      input.value = "";
      loadSubtasks(taskId);
    } else {
      alert(data.message);
    }
  } catch (error) {
    console.error("Error adding subtask:", error);
    alert("An error occurred while adding the sub-task.");
  }
}

// =====================================================
// LOAD SUBTASKS
// =====================================================

async function loadSubtasks(taskId) {
  const container = document.getElementById(`subtasks-${taskId}`);

  if (!container) {
    console.error(`Subtask container not found for task ${taskId}`);
    return;
  }

  try {
    const response = await fetch(`/tasks/${taskId}/subtasks`);

    const data = await response.json();
    container.innerHTML = "";

    if (!data.subtasks || data.subtasks.length === 0) {
      container.innerHTML = "No sub-tasks yet.";
      return;
    }

    data.subtasks.forEach((subtask) => {
      const subtaskDiv = document.createElement("div");
      subtaskDiv.className =
        "d-flex justify-content-between align-items-center border rounded p-2 mb-2";

      const status = subtask.completed ? "Completed" : "Pending";
      subtaskDiv.innerHTML = `
                <div>
                    <span>
                        ${subtask.title}
                    </span>
                    <small class="text-muted ms-2">
                        ${status}
                    </small>
                </div>

                <div>
                    ${
                      subtask.completed
                        ? ""
                        : `
                                <button
                                    class="btn btn-success btn-sm complete-subtask-btn"
                                    data-subtask-id="${subtask.id}"
                                    data-task-id="${taskId}"
                                >
                                    Complete
                                </button>
                            `
                    }

                    <button
                        class="btn btn-danger btn-sm delete-subtask-btn"
                        data-subtask-id="${subtask.id}"
                        data-task-id="${taskId}"
                    >
                        Delete
                    </button>
                </div>

            `;

      container.appendChild(subtaskDiv);
    });

    // Complete subtask buttons
    container.querySelectorAll(".complete-subtask-btn").forEach((button) => {
      button.addEventListener("click", () => {
        const subtaskId = button.dataset.subtaskId;

        const taskId = button.dataset.taskId;

        completeSubtask(subtaskId, taskId);
      });
    });

    // Delete subtask buttons
    container.querySelectorAll(".delete-subtask-btn").forEach((button) => {
      button.addEventListener("click", () => {
        const subtaskId = button.dataset.subtaskId;
        const taskId = button.dataset.taskId;

        deleteSubtask(subtaskId, taskId);
      });
    });
  } catch (error) {
    console.error("Error loading subtasks:", error);

    container.innerHTML = "Could not load sub-tasks.";
  }
}

// =====================================================
// COMPLETE SUBTASK
// =====================================================

async function completeSubtask(subtaskId, taskId) {
  try {
    const response = await fetch(`/subtasks/${subtaskId}/complete`, {
      method: "PUT",
    });

    const data = await response.json();

    if (response.ok) {
      alert(data.message);
      loadSubtasks(taskId);
    } else {
      alert(data.message);
    }
  } catch (error) {
    console.error("Error completing subtask:", error);

    alert("An error occurred while completing the sub-task.");
  }
}

// =====================================================
// DELETE SUBTASK
// =====================================================

async function deleteSubtask(subtaskId, taskId) {
  const confirmed = confirm("Are you sure you want to delete this sub-task?");

  if (!confirmed) {
    return;
  }

  try {
    const response = await fetch(`/subtasks/${subtaskId}`, {
      method: "DELETE",
    });

    const data = await response.json();

    if (response.ok) {
      alert(data.message);
      loadSubtasks(taskId);
    } else {
      alert(data.message);
    }
  } catch (error) {
    console.error("Error deleting subtask:", error);

    alert("An error occurred while deleting the sub-task.");
  }
}

// =====================================================
// PAGE LOAD
// =====================================================

document.addEventListener("DOMContentLoaded", () => {
  // ---------------------------------------------
  // Load subtasks
  // ---------------------------------------------
  document.querySelectorAll("li[data-task-id]").forEach((taskElement) => {
    const taskId = taskElement.dataset.taskId;
    loadSubtasks(taskId);
  });
  // ---------------------------------------------
  // Add subtask buttons
  // ---------------------------------------------
  document.querySelectorAll(".add-subtask-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const taskId = button.dataset.taskId;
      addSubtask(taskId);
    });
  });

  // ---------------------------------------------
  // Complete task buttons
  // ---------------------------------------------
  document.querySelectorAll(".complete-task-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const taskId = button.dataset.taskId;
      completeTask(taskId);
    });
  });

  // ---------------------------------------------
  // Edit task buttons
  // ---------------------------------------------
  document.querySelectorAll(".edit-task-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const taskId = button.dataset.taskId;

      showEditForm(taskId);
    });
  });

  // ---------------------------------------------
  // Delete task buttons
  // ---------------------------------------------
  document.querySelectorAll(".delete-task-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const taskId = button.dataset.taskId;
      deleteTask(taskId);
    });
  });

  // ---------------------------------------------
  // Save edited task
  // ---------------------------------------------
  document.querySelectorAll(".save-task-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const taskId = button.dataset.taskId;
      editTask(taskId);
    });
  });

  // ---------------------------------------------
  // Cancel edit
  // ---------------------------------------------
  document.querySelectorAll(".cancel-edit-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const taskId = button.dataset.taskId;
      showEditForm(taskId);
    });
  });
});
