# Stack and Queue Simulators

A pair of Flask web applications for demonstrating stack (LIFO) and queue (FIFO) data structures. Each simulator stores its state in the visitor's Flask session and provides a visual interface for adding, removing, peeking at, and clearing values.

## Author

Princess Jhoana B. Macatantan
BSIT WMT 4-2

## Requirements

- Python 3.10 or later
- Flask 3.1 or later

Install the dependencies from the repository root:

```powershell
python -m pip install -r requirements.txt
```

## Run the Stack Simulator

From the repository root:

```powershell
python app.py
```

Open <http://127.0.0.1:5000>.

## Run the Queue Simulator

In a second terminal, from the repository root:

```powershell
Set-Location queue-simulator
python app.py
```

Open <http://127.0.0.1:5001>.

## Operations

### Stack

- **Push** adds a value to the top.
- **Pop** removes the top value and adds it to the removed-items area.
- **Peek** highlights the top value without removing it.
- **Clear** empties the stack and removed-items area.

### Queue

- **Enqueue** adds a value to the rear.
- **Dequeue** removes the front value and adds it to the removed-items area.
- **Peek** highlights the front value without removing it.
- **Clear** empties the queue and removed-items area.

Queue values are displayed from front to rear. Both simulators reject blank values and values longer than 24 characters, and show a message when Peek or Pop/Dequeue is used on an empty structure.
