# Compression benchmark

The benchmark distinguishes three different questions:

1. **Semantic reduction:** can the model remove fields that are reconstructable?
2. **Physical serialization:** does the compact representation occupy fewer bytes than a naive transition/event representation?
3. **Codec effect:** after representation, does Zstd/LZ4/Brotli/XZ improve the result further?

This distinction is mandatory. A binary sequence stored as one byte per symbol and `initial + targets` stored the same way have equal physical size; that is a representation change, not physical compression.

The meaningful structural baseline is therefore a verbose transition representation such as `(source,target)` per event. The compact representation can omit `source` because it is reconstructable from `initial + previous target`.

All results must include exact byte counts and round-trip checks.
