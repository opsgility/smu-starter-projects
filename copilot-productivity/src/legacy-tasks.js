// ForgeBoard Legacy Task Module - Uses callbacks (needs modernization to async/await)
const fs = require('fs');

function loadTasks(filename, callback) {
  fs.readFile(filename, 'utf8', function(err, data) {
    if (err) { callback(err, null); return; }
    try {
      var tasks = JSON.parse(data);
      callback(null, tasks);
    } catch(e) {
      callback(e, null);
    }
  });
}

function saveTasks(filename, tasks, callback) {
  var data = JSON.stringify(tasks, null, 2);
  fs.writeFile(filename, data, 'utf8', function(err) {
    if (err) { callback(err); return; }
    callback(null);
  });
}

function filterTasks(tasks, status, callback) {
  setTimeout(function() {
    var filtered = tasks.filter(function(t) { return t.status === status; });
    callback(null, filtered);
  }, 100);
}

function sortTasks(tasks, field, callback) {
  setTimeout(function() {
    var sorted = tasks.slice().sort(function(a, b) {
      if (a[field] < b[field]) return -1;
      if (a[field] > b[field]) return 1;
      return 0;
    });
    callback(null, sorted);
  }, 50);
}

module.exports = { loadTasks, saveTasks, filterTasks, sortTasks };
