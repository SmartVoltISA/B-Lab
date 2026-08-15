# Tool Lifecycle — experimental → validated → organism

A new tool is not added to SPACE merely because it works once.

## Lifecycle

```text
research candidate
      ↓
experiment
      ↓
implementation
      ↓
repeatable tests
      ↓
benchmark / comparison
      ↓
validation
      ↓
approved tool
      ↓
registered organ
      ↓
SPACE integration
```

## Rules

1. Experimental tools remain outside the stable SPACE organ registry.
2. Every candidate keeps its experiment history and test evidence.
3. Similar external skills/tools may be discovered and compared before approval.
4. The local tool may remain preferable when it is specifically optimized for our data or architecture, even when a general-purpose tool performs better on another class of data.
5. After validation, the tool receives a stable interface and is registered as an available organ/tool.
6. SPACE may request the tool through the queue rather than permanently loading every tool into active memory.
7. The stable architecture is updated only after validation; experiments do not silently alter the core.
8. A validated tool may later be published as a standalone public project or exposed as a hosted service, subject to separate licensing and security review.

## Current candidate

Structural compression is currently experimental. It must complete broader tests, comparison, recovery tests, and benchmark runs before becoming a stable SPACE organ.
