#!/usr/bin/env python3
"""Experimental Guardian control plane.

Guardian is a coordinator, not an authority that silently mutates the
organism. It observes health, plans bounded CL checks, requests repair work,
and records an auditable decision. Actual repair remains explicit and
reversible until separately proven.
"""
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List
import time


class State(str, Enum):
    READY = "READY"
    DEGRADED = "DEGRADED"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    VERIFY = "VERIFY"


@dataclass
class OrganStatus:
    organ: str
    state: State
    reason: str = ""


@dataclass
class CLTask:
    organ: str
    graph: str
    direction: str
    budget_ms: float = 5000.0


class Guardian:
    def __init__(self):
        self.organs: Dict[str, OrganStatus] = {}
        self.trace: List[dict] = []

    def observe(self, organ: str, state: State, reason: str = ""):
        status = OrganStatus(organ, state, reason)
        self.organs[organ] = status
        self.trace.append({"event": "observe", "ts": time.time(), **asdict(status)})

    def plan_cl(self, organ: str, graph: str, bidirectional: bool = True):
        directions = ["forward", "reverse"] if bidirectional else ["forward"]
        tasks = [CLTask(organ, graph, d) for d in directions]
        self.trace.append({"event": "plan_cl", "organ": organ, "graph": graph,
                           "directions": directions})
        return tasks

    def classify(self):
        states = [x.state for x in self.organs.values()]
        if any(s == State.REPAIR_REQUIRED for s in states):
            return State.REPAIR_REQUIRED
        if any(s == State.DEGRADED for s in states):
            return State.DEGRADED
        return State.READY

    def wake_gate(self):
        state = self.classify()
        self.trace.append({"event": "wake_gate", "state": state.value, "ts": time.time()})
        return state


if __name__ == "__main__":
    g = Guardian()
    g.observe("GRAPH", State.READY)
    g.observe("MEMORY", State.READY)
    print(g.wake_gate().value)
    for task in g.plan_cl("GRAPH", "CL-SCALING-001", bidirectional=True):
        print(task)
