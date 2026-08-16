# SPACE ↔ GUARDIAN — Authority and Reporting Architecture v1.0

## Purpose

Define the separation between Space and Guardian, their authorities, reporting paths, and limits.

## Core principle

Space and Guardian are separate system roles. Guardian is not a hidden submodule of Space and Space is not the controller of Guardian.

## Roles

### SPACE
Primary cognitive/system execution domain.

Responsibilities:
- operate capabilities and organs;
- interpret validated information;
- plan and execute authorized work;
- maintain Space-derived knowledge;
- request resources and tools;
- propose structural changes;
- receive Guardian health/security reports.

Limits:
- cannot silently disable Guardian;
- cannot promote unverified observations to trusted system facts;
- cannot access isolated User Memory without permission;
- cannot alter Guardian audit records;
- cannot grant itself new authority.

### GUARDIAN
Independent oversight and system-integrity domain.

Responsibilities:
- observe organ health and dependency state;
- verify provenance and integrity;
- enforce authority boundaries;
- detect anomalies and unsafe state transitions;
- monitor redundancy and dependency failures;
- maintain audit trail;
- issue health/state reports to Space;
- quarantine or pause a capability when a predefined safety condition is met;
- request human confirmation for high-impact actions.

Limits:
- does not become the source of ordinary domain knowledge;
- does not rewrite Space memory to hide failures;
- cannot silently alter user data;
- cannot expand its own authority;
- emergency intervention must be logged with reason, scope and evidence.

## Reporting model

Organs report operational telemetry to Guardian.
Guardian produces a normalized system-health graph and reports to Space.

`ORGANS → TELEMETRY → GUARDIAN → HEALTH/INTEGRITY REPORT → SPACE`

Space may also send requests/intent to Guardian:

`SPACE → REQUEST/POLICY CHECK → GUARDIAN → ALLOW / DENY / DEFER / QUARANTINE`

Guardian does not become the data transport layer for ordinary application data. This preserves separation between control/management and data planes.

## Authority classes

- A0: observe
- A1: report
- A2: recommend
- A3: block/quarantine predefined unsafe operation
- A4: modify system state within explicitly delegated scope
- A5: irreversible/high-impact action — human approval required unless a separately approved emergency policy exists

Default authority for Guardian: A0–A3.
Default authority for Space: domain execution only within granted capabilities.
No component may self-promote its authority class.

## Dependency graph

Guardian maintains a graph of:
- organs;
- suborgans;
- tools;
- dependencies;
- backups;
- communication paths;
- required permissions;
- health state;
- failure propagation;
- recovery options.

For every dependency candidate, test:

1. Is the dependency real?
2. Is it required for startup?
3. Is it required for normal operation?
4. Can the organ operate degraded without it?
5. Is there a fallback?
6. What information/state is lost if it is removed?
7. Can the dependency be moved or duplicated safely?
8. Does moving it create a new single point of failure?

Never remove a seemingly duplicated component solely because its function appears similar.

## Health states

Use more than binary status:

`HEALTHY → DEGRADED → AT_RISK → UNAVAILABLE → UNKNOWN`

Health propagation must follow dependency semantics. A failed optional capability must not automatically mark the whole Space unavailable.

## Independence test

Guardian must remain able to report a Space failure even when the affected Space component is unavailable.

Space must remain able to preserve already-valid state when Guardian is temporarily unavailable, except for operations that explicitly require Guardian authorization.

This follows the established control-plane/data-plane principle that existing data-plane work should not unnecessarily depend on a functioning control plane.

## Audit requirements

Every Guardian intervention records:
- timestamp;
- actor/component;
- authority class;
- target node/edge/organ;
- requested action;
- decision;
- evidence/provenance;
- resulting state;
- rollback/recovery path.

## Initial architecture status

🟢 separation of roles defined
🟢 reporting direction defined
🟢 authority classes defined
🟢 dependency/redundancy rules defined
🟡 runtime Guardian not yet implemented
🟡 automated authority enforcement not yet implemented
🟡 failure-injection benchmark pending
