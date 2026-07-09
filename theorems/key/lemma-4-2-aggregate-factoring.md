# LEMMA 4.2, FORMALIZED
## The aggregate factoring as a coordinate-by-coordinate identity of linear maps

*A standalone component of **The Sofa Theorem** — a proof of Degtyarev–Shimada Conjecture 1.2 for the 3^v Fermat tower. Rafael Amichis Luengo (Madrid, tretoef@gmail.com) and Claude (Anthropic). Repository: github.com/tretoef-estrella/sofa-theorem.*

---

**The Sofa Theorem — formal development of Lemma 4.2 (the collar's aggregate factoring) · 9 July 2026**
**Purpose: replace the prose of the announcement's Lemma 4.2 with explicit formulas, so that the multi-heavy concern is settled by inspection. Nothing here changes the statement; it changes the level of detail.**

---

### 0. Data and conventions
`q = 3^v ≥ 9`, `f ∈ {0,1,2,3}`. λ = (λ₀..λ₅) ∈ (S_{q+f})⁶ with coefficients `λ_i = Σ_m c_{i,m} s^m` (m an exponent vector, |m| = q+f). Sheets `J = {P₁,P₂,P₃}` with ordered pairs `P_k = (a_k, b_k)`, `a_k < b_k`; sheet coordinates `u_k` via `s_{a_k} ↦ u_k`, `s_{b_k} ↦ −u_k`.

**Restriction formula (monomial-wise, exact):** for any exponent vector m,
> `s^m |_J = (−1)^{Σ_k m_{b_k}} · ∏_k u_k^{m_{a_k} + m_{b_k}}`.  (R)

**Extraction:** `δ_{k,l}^{(J)} :=` the coefficient of `u_l^q` in `Δ_k = (λ_{a_k} − λ_{b_k})|_J`, i.e. the sum of all terms of `Δ_k` with `u_l`-exponent ≥ q, divided by `u_l^q`. (Well-defined: by deg = q+f < 2q at most one coordinate can carry exponent ≥ q per monomial.)

### 1. Which monomials contribute, and through what functional
Fix J, fix l, and let `p = P_l = {a,b}` (a<b). By (R), a monomial `s^m` of `λ_i` contributes to the `u_l^q`-part of `λ_i|_J` **iff its p-pair-weight `w_p(m) := m_a + m_b ≥ q`.** Write such an m as `(m_a, m_b, γ)` with `γ` = the restriction of m to the four variables outside p, and `w := m_a + m_b = q + t`. Since `|m| = q+f`:
> **`t = f − |γ|` is DETERMINED by γ.**  (T)
By (R), the contribution of `s^m` to the `u_l^q`-part of `λ_i|_J` is
> `(−1)^{m_b} · (−1)^{ε(γ,J)} · u_l^{t} · μ(γ,J)`,
where `μ(γ,J) = ∏_{k≠l} u_k^{γ_{a_k}+γ_{b_k}}` and `ε(γ,J) = Σ_{x ∈ supp γ, x = some b_k} γ_x` — both depending only on (γ, J), not on the split (m_a, m_b).

**Hence the split-dependence enters ONLY through `(−1)^{m_b}`.** Define the alternating aggregates (linear functionals on the coefficients of λ_i):
> **`c̃_i(p, γ) := Σ_{β ≥ 0} (−1)^β · c_{i, (w−β, β, γ)}`**, with `w = q + f − |γ|`.  (AGG)
Then, coordinate-by-coordinate:
> **`[u_l^q-part of λ_i|_J] = Σ_γ (−1)^{ε(γ,J)} · c̃_i(p,γ) · u_l^{f−|γ|} · μ(γ,J)`.**  (★)

### 2. The factoring, as an identity of maps
Let `W_f := ⊕_{(i,p,γ)} F₃` (i ∈ 6 slots, p ∈ 15 pairs, γ a monomial of degree ≤ f on the 4 complement variables) — the FREE aggregate space, q-free. Define:
- `agg: (S_{q+f})⁶ → W_f`, `λ ↦ ( c̃_i(p,γ) )_{(i,p,γ)}` — a tuple of linear functionals (AGG);
- `A_f: W_f → ⊕_{J, k≠l} F₃[u]_f` by `A_f(e_{(i,p,γ)}) = Σ_{J ∋ p} Σ_{k≠l(J,p)} ε_i^{(J,k)} (−1)^{ε(γ,J)} u_{l}^{f−|γ|} μ(γ,J)` in coordinate (J,k,l), where `l = l(J,p)` is p's position in J and `ε_i^{(J,k)} = +1` if `i = a_k`, `−1` if `i = b_k`, `0` otherwise.
Both maps have **fixed, q-free coefficients** (±1 and monomial placements determined by (γ, J, i) alone).

> **Proposition (factoring).** `Φ_collar = A_f ∘ agg` as linear maps on `(S_{q+f})⁶`. Consequently `Im(Φ_collar) ⊆ Im(A_f)`; combined with T-block (iii) (antisymmetry, forced for syzygies), `Im(Φ_collar|_{Syz}) ⊆ D_f := Im(A_f) ∩ {antisym}`.
*Proof.* Evaluate both sides on λ at each coordinate (J,k,l): the left side is `δ_{k,l}^{(J)} = [u_l^q-part of (λ_{a_k} − λ_{b_k})|_J]`; by (★) applied to `i = a_k` (sign +1) and `i = b_k` (sign −1), this equals the (J,k,l)-coordinate of `A_f(agg(λ))`. The two sides agree on every λ and every coordinate. ∎

### 3. Three remarks that settle the standing objections
**Remark 1 (multi-heavy monomials — the objection, dissolved).** A monomial may satisfy `w_p(m) ≥ q` for several pairs p (e.g. one exponent ≥ q−f). This creates NO ambiguity: `agg` is a tuple of functionals — the SAME coefficient `c_{i,m}` simply enters the aggregates of every pair for which m is heavy, each time with the sign dictated by (AGG). No disjoint decomposition of λ is used anywhere; the factoring identity is verified coefficient-wise in the proof above. (A sign inconsistency would require the same coefficient to enter one coordinate of the output through two different functionals with contradictory signs — impossible, since each output coordinate (J,k,l) reads only the p = P_l aggregates, once.)
**Remark 2 (why the bound needs nothing more).** The ceiling uses ONLY `dim Im(Φ|_Syz) ≤ dim D_f` — a superset bound. No injectivity, surjectivity, or exactness of `agg` or `A_f` is claimed or needed. `dim D_f = 10, 55, 145, 280` is a fixed rank certificate, verified four independent ways (including Macaulay2).
**Remark 3 (the kernel identification uses radicality, NOT Recognition out of range).** `ker(Φ_collar|_{Syz})`: for a syzygy, T-block (i) kills the reduced parts and `δ = 0` kills the large parts, so `Δ_k = 0` identically on every sheet, for all k, J. Then `λ_a − λ_b` vanishes on all three sheets through each edge p, i.e. on `V(p)`; since `I(p)` is RADICAL (mod ε₁, ε₃ = −(c+d)(c+e)(d+e) splits into three distinct linear forms in char 3), `λ_a − λ_b ∈ I(V(p)) = I(p)`, i.e. λ ∈ M. The Recognition Theorem (proved for e < q) is never invoked at e ≥ q. Conversely M ⊆ ker trivially. Hence `ker = π(M)`, of dimension `HF(R)_{q+f} + σ_{q+f}` by the certified census law (valid ∀e). ∎

---
*Part of the Sofa Theorem repository: github.com/tretoef-estrella · tretoef@gmail.com*
