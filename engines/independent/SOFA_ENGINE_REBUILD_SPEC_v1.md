# SOFA — ENGINE REBUILD SPECIFICATION · v1
## For an independent Claude: build these engines FROM SCRATCH and check the numbers

**Your mission:** you are an independent verifier. Below are three finite computations over the field F₃ (integers mod 3). **Do NOT ask for or copy the original author's code.** Implement each from this mathematical specification using your own logic, run it, and report whether you get the target numbers. If you get different numbers, THOSE are the real ones — report them exactly. A single mismatch means the theorem it supports is in doubt. Be adversarial: your job is to catch an error, not to confirm.

**Environment:** Python 3 with numpy is fine for all three (Engine 3 is heavier but still runs). Everything is over F₃. Work exactly (no floating point for the algebra).

---

## SHARED SETUP (used by all three engines)

- Base ring `S = F₃[s₀,s₁,s₂,s₃,s₄,s₅]`, standard grading.
- **The 15 sheets:** the perfect matchings of the complete graph K₆ on vertices {0,1,2,3,4,5}. Each matching `J` is a set of 3 disjoint pairs, e.g. `{(0,1),(2,3),(4,5)}`. There are 15 of them. On sheet `J`, each pair `(a,b)` imposes `s_b = −s_a`; the sheet is a 3-dimensional coordinate space with coordinates `u₁,u₂,u₃` (one per pair), where a variable restricts as `s_a ↦ u_k`, `s_b ↦ −u_k` for the k-th pair.
- **Rank over F₃:** implement Gaussian elimination mod 3 (pivot, normalize, eliminate). You will need `rank(matrix)` repeatedly.
- **Elementary symmetric polynomials:** `e_k` = sum of all products of k distinct variables among the six.
- **HF(R)_d** (Hilbert function of `R = S/(e₁,e₃,e₅)`): equals `(15d²−45d+70)/2` for `d ≥ 4`; for `d = 0,1,2,3` it is `1, 5, 15, 34`. (h-vector (1,2,3,3,3,2,1) convolved with 1/(1−t)³.)

---

## ENGINE 1 — COLLAR RANKS (fastest; do this first)
**Target:** `dim D_f = 10, 55, 145, 280` for `f = 0, 1, 2, 3`.

**What D_f is.** Build an explicit linear map `A_f` over F₃ and intersect its image with an antisymmetry condition; `dim D_f = rank(A_f) − rank(symmetric-part-of-A_f)`.

**Domain of A_f (columns):** tuples `(i, p, γ)` where `i ∈ {0..5}` is a variable slot, `p = {a,b}` is one of the 15 pairs, and `γ` is a monomial of degree `≤ f` in the 4 variables NOT in `p`. (Enumerate all such tuples; that's the column set.)

**Codomain of A_f (rows):** tuples `(J, (k,l), m)` where `J` is one of the 15 sheets, `(k,l)` is an ORDERED pair of distinct indices in {0,1,2} (6 of them: (0,1),(0,2),(1,0),(1,2),(2,0),(2,1)), and `m` is a monomial of degree exactly `f` in the sheet coordinates `u₁,u₂,u₃`.

**The map A_f** (column `(i,p,γ)` → rows): for each sheet `J` that CONTAINS pair `p`:
  - let `l` = the index (0,1,2) of pair `p` within `J`;
  - set `t = f − deg(γ)`; this is the exponent that goes on `u_l`;
  - restrict `γ` to the sheet: each variable `x` in `γ` belongs to some pair `k'` of `J` as either the `a` (restricts to `+u_{k'}`) or the `b` (restricts to `−u_{k'}`); accumulate the exponents into an exponent vector on `(u₀,u₁,u₂)` and a sign `(−1)^(number of b-substitutions, counted with multiplicity)`;
  - add `t` to the `u_l` exponent; the resulting monomial `m` must have total degree `f` (else skip);
  - for each `k ≠ l` in {0,1,2}: let `(a_k,b_k)` be the k-th pair of `J`; if `i == a_k` add `(+sign)` to entry `(J,(k,l),m)`; if `i == b_k` add `(−sign)`.
  (All arithmetic mod 3.)

**The symmetric part** (to intersect image with antisymmetric subspace): build a second matrix whose rows are indexed by `(J, {k,l} unordered, m)` (3 unordered pairs × sheets × monomials), each row = `A_f[(J,(k,l),m)] + A_f[(J,(l,k),m)]` (the sum of the two ordered rows). Call its rank `rS`.

**Answer:** `dim D_f = rank(A_f) − rS`. Compute for f = 0,1,2,3.
**Report:** the four numbers. Target 10, 55, 145, 280 (= 10 + 45·C(f+1,2)). Also report rank(A_f) (should be 45,180,405,720) and rS (should be 35,125,260,440).

---

## ENGINE 2 — THE CENSUS σ_e (medium)
**Target:** `σ_e = 15e²−90e+145` for `e ≥ 4`; `σ_{0,1,2,3} = 0,0,1,5`. Equivalently, via the module M below, `HF_M(0..5) = 1, 11, 52, 171, 456, 1032`.

**Cleanest independent route (recommended — avoids Gröbner entirely):** compute `σ_e` DIRECTLY from the Recognition conditions, which is a finite linear-algebra problem.
- A "window syzygy" at degree `e` is a tuple `λ = (λ₀,…,λ₅)` of homogeneous degree-`e` forms such that for EVERY one of the 15 edges `{a,b}` of K₆: `λ_a − λ_b ∈ I({a,b})`, where `I({a,b}) = (s_a+s_b, ε₁, ε₃)` and `ε₁,ε₃` are the 1st and 3rd elementary symmetric polynomials of the OTHER four variables.
- Set up the linear system over F₃ whose unknowns are the coefficients of the six degree-`e` forms `λ_i`, and whose equations impose all 15 memberships (a membership `x ∈ I` is: `x` reduces to 0 modulo a basis of `I` in degree `e`; encode as linear constraints via the complement of `I_e`).
- `dim{solutions} = ` total; subtract the trivial solutions `λ_i = μ + (element of E)_i` (dimension `HF_S(e) + 5·dim E_e`). The remainder is `σ_e`.
- Compute for `e = 2,3,4,5` and check against `1, 5, 25, 70`.

**Report:** σ₂, σ₃, σ₄, σ₅ (target 1, 5, 25, 70) and whether the quadratic `15e²−90e+145` fits e = 4,5.
(If you instead reproduce the author's Gröbner kernel route: the kernel-side Hilbert read is `HF_M = 6·HF_S − HF(S⁶/in M)`, and you must use NO pair-skipping criteria — the coprime/product criterion is invalid for module Gröbner bases. But the direct linear-algebra route above is a stronger independent check.)

---

## ENGINE 3 — THE ANNIHILATOR MAIN BODY (heaviest)
**Target:** `ann_c = 15·C(c−4,2)` for all c (zero for c ≤ 5); the nine anchors `ann_{0..8} = 0,0,0,0,0,0,15,45,90`.

**What ann_c is.** With the certified transverse frame `ℓ₁=(0,2,0,1,0,1), ℓ₂=(1,0,0,1,1,0), ℓ₃=(2,1,2,2,0,0)` (coefficients of s₀..s₅), and Λ = R/(ℓ₁^q,ℓ₂^q,ℓ₃^q)R, the top zone of A is dual to `ann_Λ(s₁^q,s₂^q)` in low degrees. Because Frobenius is linear over F₃ (`(Σc_i s_i)^q = Σc_i s_i^q`), the annihilator conditions in degrees `c < q` become q-FREE: they are governed by two fixed modules
  `M′ ⊆ S⁷` and `N₃ ⊆ S³`, with `ann_c = HF_{M′}(c) − 2·HF_{N₃}(c) − dim E_c`.
- `N₃` = kernel of the map sending `(Y₁,Y₂,Y₃) ∈ S³` to `Σ_m (ℓ_m restricted)·Y_m` on each sheet (45 slot-conditions). It captures the frame's own syzygies.
- `M′` = kernel of the analogous 7-column map (one X-column carrying the `s_i` restriction, plus two blocks of three Y/Z-columns carrying the frame), 90 slot-conditions.
- Build each as a kernel over F₃ degree by degree (or via a Gröbner/elimination kernel), read Hilbert functions, combine.

**Report:** ann_c for c = 6,7,8 (target 15, 45, 90) and whether `15·C(c−4,2)` fits up to c = 12 (150,225,315,420).

---

## VERDICT FORMAT
For each engine you rebuild: `ENGINE k: REPRODUCED (numbers match)` or `ENGINE k: DISCREPANCY — I get [your numbers], target was [target]`. If you cannot build one (too heavy, ambiguous spec), say `ENGINE k: NOT ATTEMPTED — [reason]`. Do not confirm what you did not run. The most valuable thing you can do is find a number that differs.
