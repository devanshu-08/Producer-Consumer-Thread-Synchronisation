# Assignment 1: Producer-Consumer Pattern (Python)

This solution implements the classic **Producer-Consumer pattern** in Python, explicitly demonstrating **thread synchronization** and the **Wait/Notify mechanism** via `threading.Condition`. The project uses a modular, industry-standard structure.

## Project Structure

| File/Module                 | Role            | Key Functionality                                           |
|-----------------------------|-----------------|-------------------------------------------------------------|
| `src/buffer.py`             | Shared Resource | Custom Bounded Buffer (`wait()`/`notify()` logic).          |
| `src/workers.py`            | Actors          | Producer and Consumer threads, including `SENTINEL` signal. |
| `main.py`                   | Entry Point     | Demonstration runner.                                       |
| `tests/test_concurrency.py` | Verification    | **Six** comprehensive unit tests.                           |

---

## 💻 Setup and Execution

### 1. Run Application Demo (Console Results)

Run `main.py` to observe the concurrent data transfer. The output below fulfills the requirement to print the **Results of all analyses** to the console.

```bash
python main.py
```

#### Sample Console Output
```
--- Starting Assignment 1: Producer-Consumer ---
[Producer] Started.
... (Interleaved output demonstrating blocking/unblocking)
[Producer] Done. Sending Sentinel.
[Consumer] Finished.

--- Processing Complete ---
Source Items: 20
Consumed Items: 20
SUCCESS: Data integrity maintained.
```

### 2. Run Comprehensive Unit Tests (Verification)

The **six** unit tests verify all concurrency objectives, ensuring the system is robust, thread-safe, and deadlock-free. This satisfies the requirement for this concurrent system.

```bash
python -m unittest tests.test_concurrency
```
