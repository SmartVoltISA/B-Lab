# Compression Matrix — status board

Legend: 🟢 works/confirmed · 🟡 implemented but not yet measured as physical compression · 🔴 failed/not suitable · ⚪ not yet tested

| Test / property | B-Lab structural | Zstd | LZ4 | Brotli | XZ/LZMA2 |
|---|:---:|:---:|:---:|:---:|:---:|
| Binary 0/1 validation | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Exact round-trip | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Preserve `0→0` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Understand transition structure | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 |
| Reconstruct history from compact state | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 |
| Physical byte reduction | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 |
| Tiny-payload overhead handling | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 |
| Long repetitive binary history | ⚪ | 🟢 | 🟢 | 🟢 | 🟢 |
| Irregular/random binary history | ⚪ | 🟢 | 🟢 | 🟢 | 🟢 |
| Streaming | ⚪ | 🟢 | 🟢 | 🟢 | 🟢 |
| Project-specific semantic fit | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 |
| Independent implementation | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 |

## Current verdict

B-Lab structural compression is **not yet a proven physical compressor**. It is a proven compact representation for the tested contiguous binary history model. The key pending measurement is physical size after serialization, both alone and when passed through generic codecs.

## Required benchmark matrix

Run the same logical corpus through:

- RAW;
- B-Lab structural;
- RAW → Zstd/LZ4/Brotli/XZ;
- B-Lab structural → Zstd/LZ4/Brotli/XZ.

Record exact bytes, ratio, encode time, decode time, memory/CPU where available, and exact round-trip.

## External context

Published 2026 benchmarks show no universal winner: Zstd is a strong general-purpose balance, LZ4 favors speed, Brotli can favor ratio on structured text, and XZ/LZMA2 can favor archival ratio at higher cost. Compression can also increase size for small payloads because of overhead. These are external reference points, not measurements of B-Lab.

## Rule

No tool is promoted to a stable SPACE organ until the relevant cells are measured and the evidence is archived.
