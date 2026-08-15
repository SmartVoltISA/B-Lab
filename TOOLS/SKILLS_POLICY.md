# Skills vs Tools Policy

## Principle

B-Lab/SPACE may discover and compare external skills, libraries, algorithms, and tools, but an external capability is not automatically adopted into the core organism.

## Skill

A skill is an external capability available for evaluation. It may be inspected, benchmarked, wrapped, or rejected.

## Tool

A tool is a controlled, versioned capability that has been selected for a concrete task and integrated through a stable interface.

## Selection flow

`task → discover skills → identify comparable capabilities → benchmark → select → register tool → queue when needed`

## Rules

1. Do not replace a project-specific tool merely because a general-purpose tool exists.
2. Compare external alternatives when the task benefits from comparison.
3. Prefer the tool whose measured behavior best fits the actual workload.
4. Keep external dependencies at the tool boundary rather than inside the core model.
5. Record rejected alternatives and the reason for rejection when the comparison is consequential.
6. Tools must remain independently testable and removable.
7. The core remains responsible for representation, memory, relationships, provenance, and decision constraints; tools provide capabilities around it.

## Compression example

For binary structural memory, a general compressor such as Zstd may be useful as a secondary codec, but the project-specific structural compressor remains the canonical representation candidate because it exploits the semantics and reconstructability of the tested model.

External compressors can therefore be benchmarked as downstream codecs rather than treated as replacements for the structural memory model.
