# MEMORY BOUNDARIES v1.0

## Purpose

Separate Space-derived knowledge from user-owned personal memory while preserving graph structure, provenance, trust, permissions, and auditability.

## Core rule

`SPACE_MEMORY != USER_MEMORY`

They may be linked by explicit permission edges, but they are not one undifferentiated memory pool.

## Layers

### Space Memory

Contains system-owned architectural knowledge, verified experiments, reusable tools, models, benchmark results, and derived principles that are not personal user data.

### User Memory

Contains personal information, private files, personal relationships, preferences, conversations, and user-specific observations.

### Permission Graph

A separate control graph records whether a user has authorized a particular use of particular data for a stated purpose and scope. Authorization is revocable and must not silently broaden.

### Provenance / Trust

Every promoted memory item should retain source, owner/scope, timestamp, transformation history, confidence/trust, model/tool version, and verification status.

## Promotion rule

`observation -> validation -> permission check -> policy check -> promotion`

An ASR or vision observation is never automatically treated as a fact. User data is never automatically promoted into Space Memory.

## Security rule

Default state: user memory is private and isolated. External processing, training, analytics, or cross-user reuse requires an explicit policy decision and applicable legal basis/consent. Deletion must propagate to derived representations where required.

## Legal layer

The system must maintain jurisdiction-aware policy profiles rather than one global legal assumption. Initial research targets: Kazakhstan, EU/EEA, UK, US (state-specific where applicable), China, India, and other deployment jurisdictions. Legal profiles are implementation guidance, not legal advice, and must be reviewed against current law before production.

## External architecture comparison

Current research already contains related patterns: local-first memory with scoped authorization and audit logs; separate behavioral databases; encrypted portable memory; and trusted-enclave approaches. These validate the direction but do not replace our graph/provenance architecture.

## Status

🟢 Architectural principle fixed.
🟢 User/Space separation defined.
🟢 Permission boundary defined.
🟢 Provenance requirement defined.
🟡 Runtime isolation implementation pending.
🟡 Jurisdiction profiles pending legal review.
