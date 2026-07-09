# How to verify this proof yourself

Every load-bearing number is a finite computation over $\mathbb{F}_3$. You do not need to trust the authors — you can reproduce each certificate, ideally by a method different from ours. Three levels, from fastest to most convincing.

## Level 1 — run the Macaulay2 scripts (minutes, no installation)
Macaulay2 is the community-standard computer algebra system. Go to the **Macaulay2 web interface** (search "Macaulay2 web" — a browser console hosted on the Melbourne Research Cloud), and for each script in `engines/macaulay2/`, upload it and run `load "SOFA_M2_census_sigma.m2"` (etc.). Expected output:

- `SOFA_M2_census_sigma.m2` → `HF_M = 1, 11, 52, 171, 456, 1032`; `σ(e=4,5,6) = 25, 70, 145`.
- `SOFA_M2_collar_ranks.m2` → `dim D_f = 10, 55, 145, 280`.
- `SOFA_M2_annihilator.m2` → `HF_N₃ = 0,3,18,66,183,426,876,…`; `HF_M′ = 0,7,42,154,427,994,…`; `ann_c = 0,0,0,0,0,0,15,45,90,150,225,315,420`.

This is the check a referee applies first, and it uses M2's own 30-year-tested machinery, fully independent of our code.

## Level 2 — run the authors' engines
In `engines/authors/`:
- Python (needs numpy): `python3 collar_ranks_engine_v1_P0_Bisel.py` and `python3 m_kernel_elimination_v4_FIXED_P0_Bisel.py`.
- C++ (portable, standard headers): `g++ -O2 -std=c++17 -o p2b p2b_annihilator_engine_v1_P0_Bisel.cpp && ./p2b`.

Each engine gates itself against the sealed anchors before printing; a gate failure aborts with a diagnostic.

## Level 3 — reconstruct from scratch (the strongest check)
The specifications in `engines/independent/` describe each module mathematically, with no code. Re-implement them in your own language or CAS. If your numbers match ours by a *different method*, the mathematics does not depend on any one implementation. A separate agent did exactly this (see the reconstruction logs), reproducing the census by direct edge linear algebra and the annihilator by a direct slot-scalar method — both matching byte-exact.

## The sealed anchors
Everything is gated against two directly-measured values: `A(3) = 141` and `A(9) = 7761`, with full degreewise footprints. If any engine disagrees with these, it is wrong by construction.

## If you find a discrepancy
Please report it, with the byte-exact numbers, to **tretoef@gmail.com**. A number that differs from ours is the most valuable thing you can send.
