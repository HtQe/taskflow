"""Web server: serves the frontend and a small JSON API.

Uses only the standard library. Run:  python server.py
then open http://localhost:8000
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from manager import TaskManager, TaskNotFoundError
from storage import Storage

HOST = "localhost"
PORT = 8000
STATIC_DIR = Path(__file__).parent / "static"
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
}

manager = TaskManager(Storage())


class Handler(BaseHTTPRequestHandler):
    """Routes:
    GET    /api/tasks?status=all|open|done   list tasks
    POST   /api/tasks                        add  {title, priority}
    POST   /api/tasks/<id>/complete          mark done
    DELETE /api/tasks/<id>                   delete
    anything else -> a file from static/
    """

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message, status=400):
        self.send_json({"error": message}, status)

    def task_id_from_path(self):
        """'/api/tasks/3/complete' -> 3, or None if it is not a number."""
        parts = self.path.split("?")[0].strip("/").split("/")
        try:
            return int(parts[2])
        except (IndexError, ValueError):
            return None

    def do_GET(self):
        path, _, query = self.path.partition("?")
        if path == "/api/tasks":
            params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
            try:
                tasks = manager.list(params.get("status", "all"))
            except ValueError as error:
                return self.send_error_json(str(error))
            return self.send_json([task.to_dict() for task in tasks])
        self.serve_static(path)

    def do_POST(self):
        path = self.path.split("?")[0]
        if path == "/api/tasks":
            length = int(self.headers.get("Content-Length", 0))
            try:
                data = json.loads(self.rfile.read(length) or b"{}")
                task = manager.add(
                    str(data.get("title", "")),
                    str(data.get("priority", "medium")),
                )
            except (json.JSONDecodeError, ValueError) as error:
                return self.send_error_json(str(error))
            return self.send_json(task.to_dict(), 201)
        if path.startswith("/api/tasks/") and path.endswith("/complete"):
            return self.change_task(manager.complete)
        self.send_error_json("Not found", 404)

    def do_DELETE(self):
        if self.path.startswith("/api/tasks/"):
            return self.change_task(manager.delete)
        self.send_error_json("Not found", 404)

    def change_task(self, action):
        task_id = self.task_id_from_path()
        if task_id is None:
            return self.send_error_json("Id must be a number")
        try:
            task = action(task_id)
        except TaskNotFoundError as error:
            return self.send_error_json(str(error), 404)
        self.send_json(task.to_dict())

    def serve_static(self, path):
        if path == "/":
            path = "/index.html"
        file = (STATIC_DIR / path.lstrip("/")).resolve()
        # Block paths like /../manager.py that leave the static folder
        if STATIC_DIR.resolve() not in file.parents or not file.is_file():
            return self.send_error_json("Not found", 404)
        body = file.read_bytes()
        self.send_response(200)
        self.send_header(
            "Content-Type", CONTENT_TYPES.get(file.suffix, "text/plain")
        )
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"TaskFlow running on http://{HOST}:{PORT}  (Ctrl+C to stop)")
    HTTPServer((HOST, PORT), Handler).serve_forever()
