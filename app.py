from __future__ import annotations

import os

from flask import Flask, flash, redirect, render_template, request, session, url_for


class Stack:
	def __init__(self, items: list[str] | None = None) -> None:
		self.items = items if items is not None else []

	def push(self, value: str) -> None:
		self.items.append(value)

	def pop(self) -> str | None:
		return self.items.pop() if self.items else None

	def peek(self) -> str | None:
		return self.items[-1] if self.items else None

	def clear(self) -> None:
		self.items.clear()


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "stack-queue-simulator-dev-key")
app.config["SESSION_COOKIE_NAME"] = "stack_simulator_session"


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
	stack = Stack(session.get("items", []))
	removed = session.get("removed", [])
	action = request.form.get("action", "")
	session.pop("highlighted", None)

	if action == "push":
		value = request.form.get("value", "").strip()
		if not value:
			flash("Enter a value before pushing it onto the stack.", "error")
		elif len(value) > 24:
			flash("Stack values must be 24 characters or fewer.", "error")
		else:
			stack.push(value)
			flash(f"Pushed {value} onto the stack.", "success")
	elif action == "pop":
		value = stack.pop()
		if value is None:
			flash("The stack is empty. Nothing to pop.", "error")
		else:
			removed.append(value)
			flash(f"Popped {value} from the stack.", "success")
	elif action == "peek":
		value = stack.peek()
		if value is None:
			flash("The stack is empty. Nothing to peek at.", "error")
		else:
			session["highlighted"] = value
			flash(f"Top of stack: {value}.", "info")
	elif action == "clear":
		stack.clear()
		removed.clear()
		flash("Stack and removed items cleared.", "info")
	else:
		flash("Choose a valid stack operation.", "error")

	session["items"] = stack.items
	session["removed"] = removed
	return redirect(url_for("index"))


if __name__ == "__main__":
	app.run(debug=True)
