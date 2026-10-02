# Loop, Memory and Self-Reference — Working Principle

This document records a mechanism established by EXP-0019.

## Minimal chain

loop + persistent relational state + feedback/read-back → history-dependent behavior

## Important distinction

LOOP ≠ MEMORY
MEMORY ≠ SELF-REFERENCE

A loop supplies repeated access to a location/state.

Persistent state stores information about prior activity.

Self-reference in this laboratory is operational: the system's own previous activity changes state that is later read to determine its own action.

## Architectural use

B-Lab uses this mechanism as a minimal causal test for larger architectures such as SPACE.

A larger system claiming memory or self-reference should be reducible to measurable questions:

- Can the same visible state produce different futures?
- Is the difference caused by stored internal state?
- Was that state changed by the system's own previous activity?
- Does removing persistence remove the effect?
- Does removing the return/read-back path remove the tested effect?

## Boundary

This principle does not establish consciousness, subjective experience, free will, intelligence, or a universal theory of memory.

See EXPERIMENTS/EXP-0019_SELF_REFERENCE.md for the controlled experiment and parameter results.
