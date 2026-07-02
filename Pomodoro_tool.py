"""
Pomodoro Timer Tools for a LangGraph Agent.
Exposes the pomodoro timer as a set of LangChain/LangGraph tools:

    - start_pomodoro_timer
    - get_pomodoro_status
    - pause_pomodoro_timer
    - resume_pomodoro_timer
    - stop_pomodoro_timer

The timer runs on a background daemon thread, so calling a tool never
blocks the agent - every call returns immediately, and the LLM can
call get_pomodoro_status later to check progress.
"""

import threading
import time
from datetime import datetime
from typing import Optional

from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Shared timer state (module-level so every tool call sees the same timer)
_lock = threading.Lock()
_stop_event = threading.Event()
_pause_event = threading.Event()
_thread: Optional[threading.Thread] = None

_state = {
    "phase": "idle",  # idle | work | break | done | stopped
    "iteration": 0,
    "iterations": 0,
    "remaining": 0,
    "work_minutes": 0,
    "break_minutes": 0,
    "log": [],  # recent events, most recent last
}


def _log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    entry = f"[{ts}] {msg}"
    _state["log"].append(entry)
    _state["log"] = _state["log"][-20:]
    print(entry)


def _sleep_with_control(seconds: int) -> bool:
    """Sleep second-by-second so pause/stop take effect quickly. Returns False if stopped."""
    _state["remaining"] = seconds
    while _state["remaining"] > 0:
        if _stop_event.is_set():
            return False
        if _pause_event.is_set():
            time.sleep(0.2)
            continue
        time.sleep(1)
        _state["remaining"] -= 1
    return True


def _timer_loop(work_minutes: float, break_minutes: float, iterations: int) -> None:
    work_seconds = int(work_minutes * 60)
    break_seconds = int(break_minutes * 60)

    for i in range(1, iterations + 1):
        _state["iteration"] = i

        _state["phase"] = "work"
        _log(f"Session {i}/{iterations}: WORK started ({work_minutes:g} min). Focus!")
        if not _sleep_with_control(work_seconds):
            _state["phase"] = "stopped"
            _log("Timer stopped.")
            return
        _log(f"Session {i}/{iterations}: WORK done. Take a break!")

        if i == iterations:
            break  # no break after the final session

        _state["phase"] = "break"
        _log(f"BREAK started ({break_minutes:g} min). Relax!")
        if not _sleep_with_control(break_seconds):
            _state["phase"] = "stopped"
            _log("Timer stopped.")
            return
        _log("BREAK done. Back to work!")

    _state["phase"] = "done"
    _log("All pomodoro sessions complete. Nice work today!")


@tool
def start_pomodoro_timer(work_minutes: float = 25, break_minutes: float = 5, iterations: int = 4) -> str:
    """Start a pomodoro timer that runs in the background.

    Args:
        work_minutes: Length of each focus session in minutes. Default 25.
        break_minutes: Length of each break in minutes. Default 5.
        iterations: How many work sessions to run. Default 4.

    Returns:
        Confirmation that the timer started. The timer runs in the
        background; call get_pomodoro_status to check progress later.
    """
    global _thread

    with _lock:
        if _thread and _thread.is_alive():
            return "A pomodoro timer is already running. Call stop_pomodoro_timer first."

        _stop_event.clear()
        _pause_event.clear()
        _state.update({
            "phase": "work",
            "iteration": 0,
            "iterations": iterations,
            "remaining": 0,
            "work_minutes": work_minutes,
            "break_minutes": break_minutes,
            "log": [],
        })

        _thread = threading.Thread(
            target=_timer_loop, args=(work_minutes, break_minutes, iterations), daemon=True
        )
        _thread.start()

    return (f"Started pomodoro timer: {iterations} session(s) of {work_minutes:g} min work "
            f"and {break_minutes:g} min break each.")


@tool
def get_pomodoro_status() -> str:
    """Get the current status of the pomodoro timer.

    Returns the phase (work/break/idle/done/stopped), which iteration it's
    on, and how much time is left in the current phase.
    """
    phase = _state["phase"]
    if phase == "idle":
        return "No pomodoro timer has been started yet."
    if phase in ("done", "stopped"):
        return f"Pomodoro timer is {phase}."

    flag = "PAUSED" if _pause_event.is_set() else "RUNNING"
    mins, secs = divmod(_state["remaining"], 60)
    return (f"[{flag}] Iteration {_state['iteration']}/{_state['iterations']} "
            f"- {phase.upper()} - {mins:02d}:{secs:02d} remaining")


@tool
def pause_pomodoro_timer() -> str:
    """Pause the currently running pomodoro timer."""
    if _state["phase"] in ("idle", "done", "stopped"):
        return "There is no active timer to pause."
    if _pause_event.is_set():
        return "Timer is already paused."
    _pause_event.set()
    _log("Timer paused.")
    return "Timer paused."


@tool
def resume_pomodoro_timer() -> str:
    """Resume a paused pomodoro timer."""
    if not _pause_event.is_set():
        return "Timer is not currently paused."
    _pause_event.clear()
    _log("Timer resumed.")
    return "Timer resumed."


@tool
def stop_pomodoro_timer() -> str:
    """Stop the pomodoro timer entirely (cannot be resumed; start a new one instead)."""
    if _state["phase"] in ("idle", "done", "stopped"):
        return "There is no active timer to stop."
    _stop_event.set()
    return "Stopping the pomodoro timer."


