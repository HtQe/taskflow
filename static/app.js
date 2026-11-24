// Talks to server.py through the /api/tasks endpoints.
let currentStatus = "all";

const list = document.getElementById("task-list");
const errorBox = document.getElementById("error");

async function api(method, url, body) {
  const response = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error);
  return data;
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = !message;
}

async function loadTasks() {
  const tasks = await api("GET", `/api/tasks?status=${currentStatus}`);
  list.innerHTML = "";
  for (const task of tasks) list.appendChild(renderTask(task));
  document.getElementById("empty").hidden = tasks.length > 0;

  const all = await api("GET", "/api/tasks?status=open");
  document.getElementById("counter").textContent = `${all.length} open`;
}

function renderTask(task) {
  const li = document.createElement("li");
  if (task.done) li.classList.add("done");

  const title = document.createElement("span");
  title.className = "title";
  title.textContent = task.title; // textContent: safe against HTML injection

  const badge = document.createElement("span");
  badge.className = `badge ${task.priority}`;
  badge.textContent = task.priority;

  li.append(title, badge);

  if (!task.done) {
    const done = document.createElement("button");
    done.textContent = "✓ Done";
    done.onclick = () => run(api("POST", `/api/tasks/${task.id}/complete`));
    li.append(done);
  }
  const del = document.createElement("button");
  del.textContent = "Delete";
  del.className = "delete";
  del.onclick = () => run(api("DELETE", `/api/tasks/${task.id}`));
  li.append(del);
  return li;
}

// Run an action, show any error, then refresh the list.
async function run(promise) {
  try {
    await promise;
    showError("");
  } catch (error) {
    showError(error.message);
  }
  await loadTasks();
}

document.getElementById("add-form").onsubmit = async (event) => {
  event.preventDefault();
  const titleInput = document.getElementById("title");
  await run(api("POST", "/api/tasks", {
    title: titleInput.value,
    priority: document.getElementById("priority").value,
  }));
  if (errorBox.hidden) titleInput.value = "";
};

for (const button of document.querySelectorAll(".filters button")) {
  button.onclick = () => {
    document.querySelector(".filters .active").classList.remove("active");
    button.classList.add("active");
    currentStatus = button.dataset.status;
    loadTasks();
  };
}

loadTasks();
