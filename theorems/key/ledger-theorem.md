# THE LEDGER THEOREM
## A tower problem collapses to a finite collar: an exact cubic identity in q

*A standalone component of **The Sofa Theorem** — a proof of Degtyarev–Shimada Conjecture 1.2 for the 3^v Fermat tower. Rafael Amichis Luengo (Madrid, tretoef@gmail.com) and Claude (Anthropic). Repository: github.com/tretoef-estrella/sofa-theorem.*

---

### Overview
A Frobenius-tower problem asks for a quantity `A(q)` at every level `q = 3^v` of an infinite tower. The naive fear is that one must understand `A(q)` degree by degree, forever. The Ledger Theorem says the opposite: once three of the four degree-zones of `A(q)` are known *exactly* and tower-uniformly, an exact identity of cubic polynomials in `q` proves that **the entire discrepancy `A(q) − P(q)` is concentrated in four boundary degrees** — "the collar". The infinite tower is thereby reduced to a fixed, finite inequality. It is the lever that turns an infinite conjecture into a bounded computation.

### 1. Setup
`S = F₃[s₀..s₅]`, `E = (e₁,e₃,e₅)`, `R = S/E` (reduced, dim 3, `HF(R)_d = (15d²−45d+70)/2` for `d ≥ 4`). For `q = 3^v`, `A(q) = dim R/m^{[q]}R = Σ_d A_d`, and `P(q) = 15q³−45q²+55q−24`. Write `N_q(d) = #{a ∈ [0,q−1]³ : |a| = d}`.

Define the two accumulator polynomials:
- `ZA(q) = Σ_{d<q} HF(R)_d` (Zone A total),
- `W(q) = Σ_{e=0}^{q−1} [HF(R)_{q+e} − 5·HF(R)_e + σ_e]` (window total), where `σ_e = 15e²−90e+145` for `e ≥ 4` and `σ_{0..3} = 0,0,1,5` (the certified census law).

### 2. The theorem
> **Theorem (Ledger).** As polynomials in `q`,
> `ZA(q) + W(q) + 15·C(q,3) = P(q)` identically for all `q ≥ 5`.
> Both sides are cubic in `q`; equality at the four checkpoints `q = 9, 27, 81, 243` therefore forces the identity.

### 3. Proof
Each summand is a genuine polynomial in `q` with `q` a *free variable* — not merely a function agreeing on the sequence `3^v`. This is the crux (and the point a careful referee must check):
- **`HF(R)_d`** is the exact quadratic `(15d²−45d+70)/2` for `d ≥ 4`, with no dependence on `v` (Odd Symmetric pillar; a closed form, not an induction).
- **`σ_e`** is the exact Hilbert function of one *fixed* graded module (the Recognition syzygy module), certified `= 15e²−90e+145` for `e ≥ 4` — again `v`-free.
- **`15·C(q,3)`** counts the top-zone monomials: `#{a ∈ [0,q−1]³ : |a| ≥ 2q} = #{b ∈ Z_{≥0}³ : |b| ≤ q−3} = C(q,3)` via the bijection `b = (q−1)−a` (no coordinate cap is active since `|a| ≥ 2q ⟹ each a_i ≥ q − (sum of the other two) ≥ ...`, equivalently `b_i ≤ q−1` automatically). A pure identity in `q`.

Hence `ZA(q)`, `W(q)` are finite sums of genuine polynomials in `q` (the exceptional low-degree corrections `σ_{0..3}` and the `d<4` values of `HF(R)` contribute only *constants*, absorbed once `q ≥ 5`), so both sides of the claimed identity are cubic polynomials in the free variable `q`. Two cubics agreeing at four distinct points are equal. The four checkpoints `q = 9,27,81,243` are verified byte-exact. ∎

**Remark (the impostor test — why four points of the form `3^v` suffice here).** A function `P(q) + g(v)·h(q)` with `h` vanishing at `v = 2,3,4,5` would pass all four checkpoints yet fail at `v = 6`. This does *not* threaten the theorem precisely because each summand is proven `v`-free (a closed form in `q`), so no such hidden `g(v)` term exists. The checkpoints confirm an identity already guaranteed polynomial; they do not, by themselves, carry the argument.

### 4. The consequence (the collapse)
Suppose the non-collar zones are exact: `A_d = HF(R)_d` for `d < q` (Zone A); `A_{q+e} = HF(R)_{q+e} − 5HF(R)_e + σ_e` for `0 ≤ e < q` (window); `A_d = 15·N_q(d)` for `d ≥ 2q+4` (top main body). Summing and subtracting the Ledger identity:
> **`A(q) − P(q) = Σ_{d=2q}^{2q+3} [A_d − 15·N_q(d)]` for all `v ≥ 2`.**
Every term outside the collar cancels against `P(q)` exactly. The infinite-tower discrepancy lives entirely in four degrees.

### 5. Scope
The theorem is an identity of polynomials plus a telescoping; it assumes the *exactness* (not mere bounds) of the three non-collar zones, each established independently (Zone A trivially; the window by the certified census; the top main body by Gorenstein duality). It is independent of how the collar itself is bounded.

---
*Part of the Sofa Theorem repository: github.com/tretoef-estrella · tretoef@gmail.com*
