// countOpen(tasks) -> how many tasks are not done.
function countOpen(tasks) {
  const open = tasks.filter((task) => !task.done && !task.deleted); // new list of the not-done tasks
  return open.length;
}

module.exports = { countOpen };
