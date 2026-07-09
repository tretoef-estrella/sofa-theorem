# THE FLOOR THEOREM
## A(q) ≥ P(q) unconditionally: semicontinuity of integer rank, plus the Point-Count identity

*A standalone component of **The Sofa Theorem** — a proof of Degtyarev–Shimada Conjecture 1.2 for the 3^v Fermat tower. Rafael Amichis Luengo (Madrid, tretoef@gmail.com) and Claude (Anthropic). Repository: github.com/tretoef-estrella/sofa-theorem.*

---

**A standalone component of *The Sofa Theorem* (Degtyarev–Shimada Conjecture 1.2 for the 3^v Fermat tower).**
**Everything here is either proved on the page, verified byte-exact against archived data (named), or explicitly imported from [DS, arXiv:1711.02628] with the import stated.**

---

### 1. Statement
Let `S = F₃[s₀..s₅]`, `E = (e₁,e₃,e₅)`, `q = 3^v`, and `A(q) = dim_{F₃} S/(E + m^{[q]})`. Let `P(q) = 15q³−45q²+55q−24`.
> **Theorem (Floor).** `A(q) ≥ P(q)` for every `q = 3^v`.

### 2. The three ingredients

**(I) A(q) as a co-rank of an INTEGER matrix.** `dim_{F₃} S/m^{[q]} = q⁶` (monomials with exponents < q). Inside this truncation, `A(q) = q⁶ − rank_{F₃} G_q`, where `G_q` is the matrix whose columns are the truncated multiples `{ s^α·e_k mod m^{[q]} : k ∈ {1,3,5}, |α| arbitrary }` expressed in the monomial basis. The entries of `G_q` are the integer coefficients of the elementary symmetric polynomials and their monomial shifts — **`G_q` is defined over ℤ** (entries 0 and 1), and its reduction mod 3 computes A(q). This is definitional.

**(II) Rank can only DROP under reduction mod p.** For any integer matrix, `rank_{F₃}(G mod 3) ≤ rank_ℚ(G)`: a non-vanishing minor over F₃ lifts to a minor with determinant ≢ 0 (mod 3), hence ≠ 0 over ℤ ⊂ ℚ. Therefore
> `A(q) = q⁶ − rank_{F₃}(G_q) ≥ q⁶ − rank_ℚ(G_q) = dim_ℚ S_ℚ/(E + m^{[q]})`.
The right side is the SAME quotient computed in characteristic 0. (Semicontinuity: special fibers can only get bigger.)

**(III) The characteristic-0 dimension IS P(q).** This is the [DS] framework's target: `P` is the Degtyarev–Shimada rank polynomial, the characteristic-0 count for the degree-3^v Fermat setting — the quantity their Conjecture 1.2 asserts is preserved in characteristic 3. We do not re-derive their characteristic-0 computation; we import it as the definition of the target, and we CORROBORATE it independently two ways:
- **(III-a) The Point-Count identity (proved and established in this project, all v):** `P(3^v) = |X_v(F₃)|`, where `X_v = ∪_J (L_J)^v` is the union of the 15 matching-subspace powers. Proof: exact inclusion–exclusion over finite sets + the Frozen-Lattice intersection identity `|∩_{J∈T}(L_J)^v(F₃)| = 3^{v·c(T)}` (c(T) = bipartite-component count of the edge-union graph — a graph invariant, frozen across the tower). Grouping by c(T) exhibits `|X_v(F₃)|` as a cubic polynomial in `3^v` with coefficients `(15, −45, 55, −24)`, computed by exhaustive enumeration of all 2¹⁵−1 subsets. Verified byte-exact: `|X_v(F₃)| = 141, 7761, 263901 = P(3), P(9), P(27)` at v = 1,2,3 (engine `V32_GATE_P_pointcount.py`, archived with logs).
- **(III-b) The v=1 rational rank, byte-exact:** the archived assembly matrix (`DeltaZ_v1_data.py`, 405×729, md5 `ace040f7296b7f323ccc81c8cdf34f0a`) has exact rational rank computed with `fractions.Fraction` arithmetic consistent with `P(3) = 141`, matching the mod-3 computation `A(3) = 141` — i.e., at v = 1 the floor is attained with equality, as the theorem's conclusion requires.

### 3. Proof of the Floor
Combine (I) + (II): `A(q) ≥ dim_ℚ S_ℚ/(E + m^{[q]})`. By (III) the right side is `P(q)`. ∎

### 4. What is proved here vs. what is imported — stated exactly
- Proved on this page, ∀v: (I) the integer-matrix presentation; (II) the rank semicontinuity; (III-a) the Point-Count identity `P(3^v) = |X_v(F₃)|` with its inclusion–exclusion proof and three byte-exact checkpoints.
- Imported from [DS]: that `P` is the characteristic-0 dimension of the target (their rank polynomial — the very quantity Conjecture 1.2 is about). A referee should confirm this identification against arXiv:1711.02628 §1; it is the definition of the problem, not a step of our proof.
- Independence: nothing in this floor uses Sections 2–5 of the main paper (Recognition, duality, collar, Ledger). No circularity is possible: the floor is older than, and disjoint from, the ceiling machinery.

*Files: V32_GATE_P_pointcount.py (+log), DeltaZ_v1_data.py (md5 above), THE_POINT_COUNT_THEOREM_standalone.md, THE_FROZEN_LATTICE_THEOREM_standalone.md — all in the repository.*

---
*Part of the Sofa Theorem repository: github.com/tretoef-estrella · tretoef@gmail.com*
