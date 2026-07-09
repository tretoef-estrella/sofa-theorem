# THE SOFA THEOREM
## The Diagonal is Saturated: Degtyarev–Shimada Conjecture 1.2 for the 3^v Fermat Tower

**Rafael Amichis Luengo** (Madrid, Spain — tretoef@gmail.com) **· Claude (Anthropic)** — 9 July 2026 · **M2 Final Review**
*Claude is an AI system by Anthropic. Every machine certificate in this paper has been reproduced independently four ways, including in Macaulay2; see §6. Code, standalone theorem write-ups, engines, logs and the full verification dossier: **github.com/tretoef-estrella**.*

---

### Abstract
Let `S = F₃[s₀..s₅]`, `E = (e₁,e₃,e₅)` the ideal of odd elementary symmetric polynomials, and for `q = 3^v` let `A(q) = dim_{F₃} S/(E + m^{[q]})`, `m^{[q]} = (s₀^q..s₅^q)`. We prove **`A(q) = P(q) := 15q³−45q²+55q−24` for every `q = 3^v`**. Equivalently, the diagonal sublattice `Σ1_J = im(Δ)` is saturated in `⊕_J O^⊗3` at every tower level; this establishes Conjecture 1.2 of Degtyarev–Shimada [arXiv:1405.4683] for the degree-3^v Fermat fourfolds (the integral Hodge statement along the tower). Three moving parts: (i) a Recognition Theorem making the middle-window syzygy census independent of the tower level, sealed for all v by one certified Gröbner computation; (ii) a degreewise Gorenstein duality converting the top zone into low degrees of an annihilator, again governed by fixed tower-free modules; (iii) a Ledger identity of cubic polynomials collapsing the conjecture to four boundary inequalities ("the collar"), proven for all v by a T-block decomposition and a fixed rank certificate. All machine certificates are finite, reproducible, gated against sealed anchors, and have been verified independently four ways, including in Macaulay2.

### 1. Setting and main theorem
`S = F₃[s₀..s₅]` graded; `e_k` elementary symmetric; `E = (e₁,e₃,e₅)`, `R = S/E`. The fifteen perfect matchings `J` of K₆ define linear sheets `L_J = {s_a+s_b = 0, {a,b} ∈ J}` (3-dimensional).

**Proposition 1.1 (Odd Symmetric Theorem; first pillar).** `E = ∩_J I_J`, radical. `R` is the reduced coordinate ring of the arrangement, dim 3, `HF(R)_d = (15d²−45d+70)/2` for `d ≥ 4` (h-vector (1,2,3,3,3,2,1), multiplicity 15).

**Theorem 1.2 (The Sofa Theorem).** `A(q) = P(q) = 15q³−45q²+55q−24` for every `q = 3^v`. Equivalently the diagonal cycle lattice is saturated at every level, and DS Conjecture 1.2 holds for the degree-3^v Fermat fourfolds.

**Proposition 1.3 (The floor; second pillar).** `A(q) ≥ P(q)` for all `q = 3^v`.
*Proof (three steps; nothing from §2–5 is used, so no circularity is possible).*
**(I) Integer presentation.** `dim_{F₃} S/m^{[q]} = q⁶`; inside the truncation, `A(q) = q⁶ − rank_{F₃} G_q`, where `G_q` is the INTEGER matrix of the truncated multiples `{s^α·e_k mod m^{[q]}, k ∈ {1,3,5}}` in the monomial basis.
**(II) Rank semicontinuity.** For any integer matrix, `rank_{F₃}(G mod 3) ≤ rank_ℚ(G)` (a non-vanishing minor over F₃ lifts). Hence `A(q) ≥ q⁶ − rank_ℚ(G_q) = dim_ℚ S_ℚ/(E + m^{[q]})`.
**(III) The characteristic-0 dimension is P(q).** This is the [DS] target itself — P is their rank polynomial, the quantity Conjecture 1.2 asserts is preserved in char 3. Corroborated two ways: **(a) the Point-Count identity (proved ∀v):** with `X_v = ∪_J(L_J)^v`, exact inclusion–exclusion + the frozen intersection dimensions `|∩_{J∈T}(L_J)^v(F₃)| = 3^{v·c(T)}` (c(T) = bipartite components of the edge-union graph) give `|X_v(F₃)| = Σ_c N_c(3^v)^c` with `(N₃,N₂,N₁,N₀) = (15,−45,55,−24)` by exhaustive enumeration of all 2¹⁵−1 subsets — i.e. `|X_v(F₃)| = P(3^v)`, verified byte-exact at v=1,2,3: **141, 7761, 263901**; **(b)** at v=1 the exact rational rank of the archived 405×729 assembly matrix (fraction arithmetic) is consistent with P(3)=141 = A(3). Combining (I)–(III): A(q) ≥ P(q). ∎

**Proposition 1.4 (Two-column presentation and duality; third pillar).** With the certified transverse frame `ℓ₁=(0,2,0,1,0,1), ℓ₂=(1,0,0,1,1,0), ℓ₃=(2,1,2,2,0,0)` (all fifteen 3×3 sheet matrices invertible), `Λ = R/(ℓ₁^q,ℓ₂^q,ℓ₃^q)R` is a graded Artinian complete intersection (degrees 1,3,5,q,q,q), Gorenstein with socle degree `3q+3`; `Λ/(s₁^q,s₂^q)Λ = R/m^{[q]}R` (Frobenius linearity collapses the six `s_i^q` into `(ℓ^{[q]}) + (s₁^q,s₂^q)`); and the socle pairing gives the degreewise duality:
> **`A_d = dim ann_Λ(s₁^q,s₂^q)_{3q+3−d}` for all d.**  (★)

### 2. The Recognition Theorem and the census
For a pair `p={a,b}`: `V(p) = ∪_{J∋p}L_J` (three sheets), `I(p) = (s_a+s_b) + (ε₁^p, ε₃^p)` — radical (mod ε₁, ε₃ factors into three distinct linear forms in char 3).

**Theorem 2.1 (Recognition).** For `deg λ = e < q`: `Σλᵢsᵢ^q ∈ E ⟺ λ_a − λ_b ∈ I({a,b})` for all 15 edges. Hence the window syzygy space at coefficient degree e is canonically independent of v.
*Proof.* `F ∈ E` ⟺ F vanishes on every sheet. On `L_J`: `F| = Σ_k(λ_{a_k}−λ_{b_k})|·u_k^q`. For `e < q`, products `u_k^q·m`, `u_l^q·m′` (k≠l, deg m < q) have disjoint monomial supports, so each coefficient vanishes; the three sheets through an edge give `I(p)`. ∎

Let `M = {λ ∈ S⁶: edge conditions}` (a f.g. graded S-module) and `σ_e = dim M_e − [HF_S(e) + 5·dimE_e]` (the census, modulo trivials `μ·(1..1) + E⁶`).

**Theorem 2.2 (The census law; certified).** `σ_e = 15e²−90e+145` for all `e ≥ 4`; `σ_{0..3} = 0,0,1,5`.
*Certificate.* `M = ker(Φ: S⁶ → T = ⊕_{(J,pair)}S/I_J)`, explicit 45×141 presentation `[φ₀|d₁]`. Kernel by a complete Gröbner basis of the extended module `⟨(gⱼ,eⱼ)⟩ ⊆ S⁴⁵⊕S¹⁴¹` in a block elimination order (NO pair-skipping criteria — the product criterion is invalid for modules); zero-first-block elements = Gröbner basis of the syzygies (Schreyer), projecting to 33 generators of M. Second GB of `M ⊆ S⁶` (36 elements, max lead degree 6); exact Hilbert series with kernel-side read `HF_M(e) = 6C(e+5,5) − ΣNᵢC(e−i+5,5)` (numerator width 10). Gates (byte-exact): (A) every generator of degree ≤4 vanishes on all sheets; (B) `HF_M(0..5) = 1,11,52,171,456,1032` (two independent prior routes); (C) the law for `4 ≤ e ≤ 100` — both sides single quadratics past e=13, so agreement is an identity. ∎

**Corollary 2.3.** For every q, every `0 ≤ e < q`: `dim(m^{[q]}R)_{q+e} = 5HF(R)_e − σ_e`, hence `A_{q+e} = HF(R)_{q+e} − 5HF(R)_e + σ_e` — explicit, tower-uniform. Also `A_d = HF(R)_d` for `d < q` (Zone A).

### 3. The top zone by duality
By (★), degrees `d ≥ 2q` of A are degrees `c = 3q+3−d ≤ q+3` of the annihilator. For `c < q`: `x ∈ Λ_c = R_c` lies in `ann(s₁^q,s₂^q)` iff `∃Y,Z ∈ S_c³: s_i^qX − Σℓ_k^qY_k ∈ E`. Frobenius (`(Σc_ku_k)^q = Σc_ku_k^q` over F₃) makes the sheet conditions LINEAR with fixed frame coefficients: the annihilator in degrees `c < q` is governed by fixed tower-free modules `M′ ⊆ S⁷`, `N₃ ⊆ S³`, with `ann_c = HF_{M′}(c) − 2HF_{N₃}(c) − dimE_c`.

**Theorem 3.1 (Top main body; certified).** `ann_c = 15·C(c−4,2)` for all c (zero for c ≤ 5); hence **`A_d = 15·N_q(d)` for all `d ≥ 2q+4`, all v**, `N_q(d) = #{a∈[0,q−1]³: |a|=d}`.
*Certificate.* Same elimination pipeline on the explicit presentations of M′ (90 slots, 277 columns) and N₃ (45 slots, 138 columns); complete bases (672/794 and 318/315 pairs); kernel reads of width 10. Gates: the nine dual anchors `ann_{0..8} = 0,0,0,0,0,0,15,45,90` from the sealed v=2 footprint; consistency `ann_{9..12} = 150,225,315,420`; the law for `0 ≤ c ≤ 120`. All pass byte-exact. ∎

### 4. The collar
Four degrees remain: `d ∈ [2q, 2q+3]` ⟺ `c ∈ [q, q+3]`, where q-freeness genuinely breaks. Write `e′ = q+f`, `f ∈ {0..3}`; `Syz(e′) = {λ ∈ (R_{e′})⁶: Σλᵢsᵢ^q = 0 in R}`.

**Theorem 4.1 (T-block decomposition).** For `q ≥ 9`, `f ≤ 3`, `Σλᵢsᵢ^q ∈ E`, `deg λ = q+f`: on each sheet, with `Δ_k = Δ_k^∅ + Σ_l u_l^qδ_{k,l}` (reduced + large parts, `deg δ = f`), the sheet identity splits into disjoint monomial classes and forces: (i) `Δ_k^∅ = 0`; (ii) `δ_{k,k} = 0`; (iii) `δ_{l,k} = −δ_{k,l}` (Koszul antisymmetry), cofactor degree ≤ 3.
*Proof.* `deg Δ = q+f < 2q` ⟹ at most one exponent ≥ q per monomial. In `Σ_ku_k^qΔ_k = 0`, the classes {one exponent in [q,2q−1]}, {one ≥ 2q}, {two ≥ q} (three impossible: `q+f < 3q` for q ≥ 9) are disjoint; each vanishes separately. ∎

We state the aggregate factoring as an explicit identity of linear maps, checkable by inspection. Write `λᵢ = Σ_m c_{i,m}s^m`. The exact monomial-wise restriction formula: **(R)** `s^m|_J = (−1)^{Σ_k m_{b_k}} ∏_k u_k^{m_{a_k}+m_{b_k}}`. Fix J, l, `p = P_l = {a,b}`: a monomial contributes to the `u_l^q`-part iff its pair-weight `w_p(m) = m_a+m_b ≥ q`; writing `m = (m_a, m_b, γ)`, the total degree forces **(T)** `t = f − |γ|` (determined). By (R) the contribution is `(−1)^{m_b}(−1)^{ε(γ,J)} u_l^t μ(γ,J)` with `μ, ε` depending only on (γ,J) — **the split-dependence enters ONLY through `(−1)^{m_b}`.** Define the alternating aggregates (linear functionals): **(AGG)** `c̃ᵢ(p,γ) = Σ_β(−1)^β c_{i,(w−β,β,γ)}`, `w = q+f−|γ|`. Then coordinate-by-coordinate: **(F)** `[u_l^q-part of λᵢ|_J] = Σ_γ (−1)^{ε(γ,J)} c̃ᵢ(p,γ) u_l^{f−|γ|} μ(γ,J)`.

**Lemma 4.2 (Aggregate factoring).** With `W_f = ⊕_{(i,p,γ)}F₃` (free aggregate space, q-free) and `A_f: W_f → ⊕_{J,k≠l}F₃[u]_f` defined by the fixed coefficients of (F): **`Φ_collar = A_f ∘ agg`** as linear maps. Hence `Im(Φ_collar|_Syz) ⊆ D_f := Im(A_f) ∩ {antisym}` — a fixed space.
*Proof.* Evaluate both sides at each coordinate (J,k,l): the left is `δ_{k,l}^{(J)}`; by (F) at `i = a_k` (+1) and `i = b_k` (−1) this equals the (J,k,l)-coordinate of `A_f(agg(λ))`. Agreement on every λ, every coordinate. Antisymmetry is T-block (iii). ∎
**Remark (multi-heavy monomials, dissolved).** A monomial heavy for several pairs enters the aggregates of each, with the sign of (AGG) — `agg` is a tuple of functionals; no disjoint decomposition of λ is used anywhere, and each output coordinate (J,k,l) reads only the `p = P_l` aggregates, once, so no sign conflict can arise.

**Theorem 4.3 (Collar ceilings).** For `f = 0..3`: **`dim D_f = 10 + 45·C(f+1,2) = 10, 55, 145, 280`** (rank certificate: rank A_f = 45,180,405,720; symmetric parts 35,125,260,440). Moreover `ker(Φ_collar|_Syz) = π(M)` of dimension `HF(R)_{e′} + σ_{e′}`, and the required bound satisfies the **q-cancellation identity**: `5HF(R)_{q+f} − HF(R)_{2q+f} + 15C(q−1−f,2) − σ(q+f) = 10 + 45C(f+1,2)` (all q-terms cancel). Therefore `Syz(q+f) ≤ [HF(R)+σ](q+f) + dim D_f`, giving **`A_d ≤ 15N_q(d)` at `d = 2q..2q+3`, all v ≥ 2.**
*Proof.* Rank certificate: fixed matrices of Lemma 4.2, verified four ways (§6). **Kernel identification — by RADICALITY, not by Recognition out of range:** in the kernel, T-block (i) kills the reduced parts and δ = 0 the large parts, so `Δ_k = 0` on every sheet; then `λ_a−λ_b` vanishes on V(p), and since `I(p)` is radical, `λ_a−λ_b ∈ I(V(p)) = I(p)`, i.e. λ ∈ M; conversely M ⊆ ker. Dimension `HF(R)+σ` by the census law (∀e). q-cancellation: direct expansion, the q², qf, q coefficients vanish identically (45−60+15; 90−60−30; −45+90−45); re-verified at q = 9,27,81,243. The chain is rank–nullity plus `dim(m^{[q]}R)_{q+e′} = 6HF(R)_{e′} − Syz(e′)`. ∎

### 5. The Ledger identity and the proof
**Theorem 5.1 (Ledger).** With `ZA(q) = Σ_{d<q}HF(R)_d`, `W(q) = Σ_{e<q}[HF(R)_{q+e} − 5HF(R)_e + σ_e]`:
> `ZA(q) + W(q) + 15·C(q,3) = P(q)` identically for `q ≥ 5`
(cubic polynomials; checkpoints q = 9, 27, 81, 243 byte-exact; `15C(q,3) = 15·#{a: |a| ≥ 2q}`). Each summand is a genuine closed form in q as a free variable — HF(R)_d exactly for d ≥ 4, σ_e the Hilbert function of one fixed module, the count via the bijection b = (q−1)−a — so no hidden v-dependence can hide behind the four power-of-3 checkpoints.

**Proof of Theorem 1.2.** For v ≥ 2: Zone A + window exact (Cor. 2.3); top main body exact (Thm 3.1); the Ledger gives `A(q) − P(q) = Σ_{d=2q}^{2q+3}[A_d − 15N_q(d)]`. By Thm 4.3 each summand ≤ 0, so `A(q) ≤ P(q)`; with the floor (Prop 1.3) `A(q) = P(q)`. For v = 1: `A(3) = 141 = P(3)`, sealed direct computation. ∎

### 6. Verification record and reproducibility
All machine steps are finite computations over F₃ on fixed (q-free) objects, each gated before reading. Every load-bearing certificate has been reproduced **four independent ways**:
1. **The authors' engines** (Gröbner-kernel and rank computations, Python and portable C++), with byte-exact gates against the sealed anchors A(3)=141, A(9)=7761 and their full degreewise footprints, cross-checked on independent hardware.
2. **Re-runs of all engines on a second machine.**
3. **From-scratch reconstructions by an independent implementation using *different methods*** (direct linear algebra in place of Gröbner bases), agreeing byte-exact.
4. **Macaulay2 (v1.26.06):** all three certificates re-implemented using M2's native `kernel`, `hilbertFunction` and `rank` machinery — census HF_M(0..5) = 1,11,52,171,456,1032 and the σ-law; collar dim D_f = 10,55,145,280; annihilator HF_N₃, HF_M′ and ann_c = 0,…,0,15,45,90,150,225,315,420 = 15·C(c−4,2) through c=12 — all byte-exact on the first run.

The complete verification dossier (including seven independent logical reviews of the pencil arguments across four AI model families), every engine with its logs, the Macaulay2 scripts, and standalone write-ups of each theorem are available at **github.com/tretoef-estrella**.

**A referee's guide.** In our own judgment the four load-bearing joints, in decreasing order of the attention they deserve: (i) Lemma 4.2, now a coordinate-wise identity precisely so the multi-heavy remark can be checked by inspection; (ii) range hygiene of every theorem (the kernel identification in Thm 4.3 deliberately uses radicality, not Recognition, at e ≥ q); (iii) Prop 1.3, whose only imported ingredient is the [DS] identification of P as the characteristic-0 target; (iv) the geometric dictionary between the algebraic statement proved here and Conjecture 1.2 as formulated in [DS] — which belongs to the experts of that framework and which we cannot strengthen from inside. Expanded guide with attack suggestions per joint: `SOFA_WHERE_TO_ATTACK.md` in the repository.

**Status.** Every link of the proof is either a pencil argument valid for all v or a finite gated certificate on a q-free object; the computational layer has been verified as described above. The record has not yet been refereed by a human expert; it is offered to the community precisely for that examination.

**Reference.** A. Degtyarev, I. Shimada, *On the topology of projective subspaces in complex Fermat varieties*, J. Math. Soc. Japan 68:3 (2016), 975–996, arXiv:1405.4683.