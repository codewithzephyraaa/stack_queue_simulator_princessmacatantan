from __future__ import annotations

import os

from flask import Flask, flash, redirect, render_template, request, session, url_for


class Queue:
    def __init__(self, items: list[str] | None = None) -> None:
        self.items = items if items is not None else []

    def enqueue(self, value: str) -> None:
        self.items.append(value)

    def dequeue(self) -> str | None:
        return self.items.pop(0) if self.items else None

    def peek(self) -> str | None:
        return self.items[0] if self.items else None

    def clear(self) -> None:
        self.items.clear()


APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(APP_DIRECTORY, "templates"),
    static_folder=os.path.join(APP_DIRECTORY, "static"),
)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "stack-queue-simulator-dev-key")
app.config["SESSION_COOKIE_NAME"] = "queue_simulator_session"


@app.get("/")
def index():
    return render_template(
        "index.html",
        items=session.get("items", []),
        removed=session.get("removed", []),
        highlighted=session.get("highlighted"),
    )


@app.post("/operate")
def operate():
    queue = Queue(session.get("items", []))
    removed = session.get("removed", [])
    action = request.form.get("action", "")
    session.pop("highlighted", None)

    if action == "enqueue":
        value = request.form.get("value", "").strip()
        if not value:
            flash("Enter a value before enqueueing it.", "error")
        elif len(value) > 24:
            flash("Queue values must be 24 characters or fewer.", "error")
        else:
            queue.enqueue(value)
            flash(f"Enqueued {value} at the rear of the queue.", "success")
    elif action == "dequeue":
        value = queue.dequeue()
        if value is None:
            flash("The queue is empty. Nothing to dequeue.", "error")
        else:
            removed.append(value)
            flash(f"Dequeued {value} from the front of the queue.", "success")
    elif action == "peek":
        value = queue.peek()
        if value is None:
            flash("The queue is empty. Nothing to peek at.", "error")
        else:
            session["highlighted"] = value
            flash(f"Front of queue: {value}.", "info")
    elif action == "clear":
        queue.clear()
        removed.clear()
        flash("Queue and removed items cleared.", "info")
    else:
        flash("Choose a valid queue operation.", "error")

    session["items"] = queue.items
    session["removed"] = removed
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
