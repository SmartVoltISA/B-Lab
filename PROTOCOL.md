# B-Lab — Experimental Protocol

## Scientific loop

```text
hypothesis
→ define model
→ generate
→ observe
→ measure
→ compare
→ visualize
→ verify
→ archive
```

## Rules

1. Freeze the experiment definition before execution.
2. Record model version and parameters.
3. Separate generation from measurement.
4. Do not change code after a run to improve its result.
5. A failed hypothesis is retained as evidence.
6. A surprising result is not corrected to fit known mathematics.
7. Repeatability is required before promoting a result.
8. Formal comparison happens only after the experimental result is frozen.

## Phase 0 scope

Start with:

- single states `0` and `1`;
- static observations;
- deterministic transitions;
- repeated transitions;
- minimal cycles.

Memory, graph construction and mathematical comparison are introduced one layer at a time.

## Result record

Every experiment must record:

- experiment ID;
- date;
- code version / commit;
- model;
- parameters;
- input sequence or seed;
- observed result;
- expected result, if any;
- deviations;
- comparison result;
- visualization reference;
- conclusion;
- next experiment.
