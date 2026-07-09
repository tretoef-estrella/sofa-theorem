# THE SOFA THEOREM — M2 FINAL REVIEW · BREAKER'S EDITION
## The full proof, plus — for every link — how it was proved, how to attack it, and why it holds

**This edition is for cold reviewers. It contains the complete Final Review proof, and after each load-bearing link, an adversarial annotation: HOW PROVED / HOW TO ATTACK / WHY IT HOLDS. The mathematics is identical to the paper; only the annotations are added. Break any link and the byte-exact discrepancy is worth more to us than agreement. — R. Amichis Luengo (tretoef@gmail.com), github.com/tretoef-estrella**

---

## THE COMPUTATIONAL SHIELD (read first — it removes an entire class of attack)
Every load-bearing number in this proof is a finite computation over F₃ on a fixed, q-free object. Each has been reproduced **four independent ways**, so "the number is wrong" is essentially off the table; what remains to attack is the LOGIC that connects the numbers.
- **σ census** = 1,11,52,171,456,1032; σ-law 15e²−90e+145 — authors (Gröbner), 2nd machine, R.E.1 (direct edge linear algebra, NO Gröbner), **Macaulay2 v1.26.06** (native kernel+hilbertFunction).
- **collar ranks** dim D_f = 10,55,145,280 — authors, 2nd machine, R.E.1 (own code), **Macaulay2** (native rank over ZZ/3).
- **annihilator** ann_c = 0,…,0,15,45,90,150,225,315,420 = 15·C(c−4,2) — authors (extended-module Gröbner), 2nd machine, R.E.1 (direct slot-scalar LA), **Macaulay2** (native kernel).
All three agreed byte-exact on the first Macaulay2 run. **Attack surface remaining: the pencil logic below, not the certificates.**

---

### Abstract
Let `S = F₃[s₀..s₅]`, `E = (e₁,e₃,e₅)` the ideal of odd elementary symmetric polynomials, and for `q = 3^v` let `A(q) = dim_{F₃} S/(E + m^{[q]})`, `m^{[q]} = (s₀^q..s₅^q)`. We prove **`A(q) = P(q) := 15q³−45q²+55q−24` for every `q = 3^v`**. Equivalently, the diagonal sublattice `Σ1_J = im(Δ)` is saturated in `⊕_J O^⊗3` at every tower level; this establishes Conjecture 1.2 of Degtyarev–Shimada [arXiv:1711.02628] for the degree-3^v Fermat fourfolds (the integral Hodge statement along the tower). Three moving parts: (i) a Recognition Theorem making the middle-window syzygy census independent of the tower level, sealed for all v by one certified Gröbner computation; (ii) a degreewise Gorenstein duality converting the top zone into low degrees of an annihilator, again governed by fixed tower-free modules; (iii) a Ledger identity of cubic polynomials collapsing the conjecture to four boundary inequalities ("the collar"), proven for all v by a T-block decomposition and a fixed rank certificate. All machine certificates are finite, reproducible, gated against sealed anchors, and have been verified independently four ways, including in Macaulay2.

### 1. Setting and main theorem
`S = F₃[s₀..s₅]` graded; `e_k` elementary symmetric; `E = (e₁,e₃,e₅)`, `R = S/E`. The fifteen perfect matchings `J` of K₆ define linear sheets `L_J = {s_a+s_b = 0, {a,b} ∈ J}` (3-dimensional).

**Proposition 1.1 (Odd Symmetric Theorem; first pillar).** `E = ∩_J I_J`, radical. `R` is the reduced coordinate ring of the arrangement, dim 3, `HF(R)_d = (15d²−45d+70)/2` for `d ≥ 4` (h-vector (1,2,3,3,3,2,1), multiplicity 15).

**Theorem 1.2 (The Sofa Theorem).** `A(q) = P(q) = 15q³−45q²+55q−24` for every `q = 3^v`. Equivalently the diagonal cycle lattice is saturated at every level, and DS Conjecture 1.2 holds for the degree-3^v Fermat fourfolds.

**Proposition 1.3 (The floor; second pillar).** `A(q) ≥ P(q)` for all `q = 3^v`.
*Proof (three steps; nothing from §2–5 is used, so no circularity is possible).*
**(I) Integer presentation.** `dim_{F₃} S/m^{[q]} = q⁶`; inside the truncation, `A(q) = q⁶ − rank_{F₃} G_q`, where `G_q` is the INTEGER matrix of the truncated multiples `{s^α·e_k mod m^{[q]}, k ∈ {1,3,5}}` in the monomial basis.
**(II) Rank semicontinuity.** For any integer matrix, `rank_{F₃}(G mod 3) ≤ rank_ℚ(G)` (a non-vanishing minor over F₃ lifts). Hence `A(q) ≥ q⁶ − rank_ℚ(G_q) = dim_ℚ S_ℚ/(E + m^{[q]})`.
**(III) The characteristic-0 dimension is P(q).** This is the [DS] target itself — P is their rank polynomial, the quantity Conjecture 1.2 asserts is preserved in char 3. Corroborated two ways: **(a) the Point-Count identity (proved ∀v):** with `X_v = ∪_J(L_J)^v`, exact inclusion–exclusion + the frozen intersection dimensions `|∩_{J∈T}(L_J)^v(F₃)| = 3^{v·c(T)}` (c(T) = bipartite components of the edge-union graph) give `|X_v(F₃)| = Σ_c N_c(3^v)^c` with `(N₃,N₂,N₁,N₀) = (15,−45,55,−24)` by exhaustive enumeration of all 2¹⁵−1 subsets — i.e. `|X_v(F₃)| = P(3^v)`, verified byte-exact at v=1,2,3: **141, 7761, 263901**; **(b)** at v=1 the exact rational rank of the archived 405×729 assembly matrix (fraction arithmetic) is consistent with P(3)=141 = A(3). Combining (I)–(III): A(q) ≥ P(q). ∎

> **BREAKER — Proposition 1.3 (the floor).**
> HOW PROVED: integer matrix G_q (definitional) → rank can only drop mod 3 (minor lift) → char-0 dim is the [DS] target, corroborated by the Point-Count identity (3 byte-exact checkpoints 141/7761/263901) and the v=1 rational rank.
> HOW TO ATTACK: (a) is `A(q) = q⁶ − rank G_q` exactly right, including the truncation bookkeeping? (b) is the char-0 quotient truly P(q), or only at the sampled v? — attack via the [DS] definition of the target. (c) re-run the point-count engine (seconds) and check 141/7761/263901.
> WHY IT HOLDS: (I) and (II) are one-line each and field-general; (III) imports only the *definition* of the [DS] target, not a step. No §2–5 machinery is used — no circularity is even possible.



**Proposition 1.4 (Two-column presentation and duality; third pillar).** With the certified transverse frame `ℓ₁=(0,2,0,1,0,1), ℓ₂=(1,0,0,1,1,0), ℓ₃=(2,1,2,2,0,0)` (all fifteen 3×3 sheet matrices invertible), `Λ = R/(ℓ₁^q,ℓ₂^q,ℓ₃^q)R` is a graded Artinian complete intersection (degrees 1,3,5,q,q,q), Gorenstein with socle degree `3q+3`; `Λ/(s₁^q,s₂^q)Λ = R/m^{[q]}R` (Frobenius linearity collapses the six `s_i^q` into `(ℓ^{[q]}) + (s₁^q,s₂^q)`); and the socle pairing gives the degreewise duality:
> **`A_d = dim ann_Λ(s₁^q,s₂^q)_{3q+3−d}` for all d.**  (★)

### 2. The Recognition Theorem and the census
For a pair `p={a,b}`: `V(p) = ∪_{J∋p}L_J` (three sheets), `I(p) = (s_a+s_b) + (ε₁^p, ε₃^p)` — radical (mod ε₁, ε₃ factors into three distinct linear forms in char 3).

**Theorem 2.1 (Recognition).** For `deg λ = e < q`: `Σλᵢsᵢ^q ∈ E ⟺ λ_a − λ_b ∈ I({a,b})` for all 15 edges. Hence the window syzygy space at coefficient degree e is canonically independent of v.
*Proof.* `F ∈ E` ⟺ F vanishes on every sheet. On `L_J`: `F| = Σ_k(λ_{a_k}−λ_{b_k})|·u_k^q`. For `e < q`, products `u_k^q·m`, `u_l^q·m′` (k≠l, deg m < q) have disjoint monomial supports, so each coefficient vanishes; the three sheets through an edge give `I(p)`. ∎

> **BREAKER — Theorem 2.1 (Recognition).**
> HOW PROVED: F ∈ E ⟺ vanishes on every sheet; for e < q the products u_k^q·m have DISJOINT monomial supports (two exponents ≥ q would need degree ≥ 2q), so coefficients vanish per sheet; the three sheets through an edge give I(p).
> HOW TO ATTACK: the sharpness of `e < q` — at e = q the disjointness fails (this is exactly why the collar exists; the collar does NOT use Recognition, see Thm 4.3). Check the radicality of I(p): mod ε₁, ε₃ = −(c+d)(c+e)(d+e) in char 3 — verify this factorization by expansion.
> WHY IT HOLDS: pure exponent arithmetic below the threshold; the char-3 factorization of ε₃ is a two-line computation.



Let `M = {λ ∈ S⁶: edge conditions}` (a f.g. graded S-module) and `σ_e = dim M_e − [HF_S(e) + 5·dimE_e]` (the census, modulo trivials `μ·(1..1) + E⁶`).

**Theorem 2.2 (The census law; certified).** `σ_e = 15e²−90e+145` for all `e ≥ 4`; `σ_{0..3} = 0,0,1,5`.
*Certificate.* `M = ker(Φ: S⁶ → T = ⊕_{(J,pair)}S/I_J)`, explicit 45×141 presentation `[φ₀|d₁]`. Kernel by a complete Gröbner basis of the extended module `⟨(gⱼ,eⱼ)⟩ ⊆ S⁴⁵⊕S¹⁴¹` in a block elimination order (NO pair-skipping criteria — the product criterion is invalid for modules); zero-first-block elements = Gröbner basis of the syzygies (Schreyer), projecting to 33 generators of M. Second GB of `M ⊆ S⁶` (36 elements, max lead degree 6); exact Hilbert series with kernel-side read `HF_M(e) = 6C(e+5,5) − ΣNᵢC(e−i+5,5)` (numerator width 10). Gates (byte-exact): (A) every generator of degree ≤4 vanishes on all sheets; (B) `HF_M(0..5) = 1,11,52,171,456,1032` (two independent prior routes); (C) the law for `4 ≤ e ≤ 100` — both sides single quadratics past e=13, so agreement is an identity. ∎

**Corollary 2.3.** For every q, every `0 ≤ e < q`: `dim(m^{[q]}R)_{q+e} = 5HF(R)_e − σ_e`, hence `A_{q+e} = HF(R)_{q+e} − 5HF(R)_e + σ_e` — explicit, tower-uniform. Also `A_d = HF(R)_d` for `d < q` (Zone A).

### 3. The top zone by duality
By (★), degrees `d ≥ 2q` of A are degrees `c = 3q+3−d ≤ q+3` of the annihilator. For `c < q`: `x ∈ Λ_c = R_c` lies in `ann(s₁^q,s₂^q)` iff `∃Y,Z ∈ S_c³: s_i^qX − Σℓ_k^qY_k ∈ E`. Frobenius (`(Σc_ku_k)^q = Σc_ku_k^q` over F₃) makes the sheet conditions LINEAR with fixed frame coefficients: the annihilator in degrees `c < q` is governed by fixed tower-free modules `M′ ⊆ S⁷`, `N₃ ⊆ S³`, with `ann_c = HF_{M′}(c) − 2HF_{N₃}(c) − dimE_c`.

**Theorem 3.1 (Top main body; certified).** `ann_c = 15·C(c−4,2)` for all c (zero for c ≤ 5); hence **`A_d = 15·N_q(d)` for all `d ≥ 2q+4`, all v**, `N_q(d) = #{a∈[0,q−1]³: |a|=d}`.
*Certificate.* Same elimination pipeline on the explicit presentations of M′ (90 slots, 277 columns) and N₃ (45 slots, 138 columns); complete bases (672/794 and 318/315 pairs); kernel reads of width 10. Gates: the nine dual anchors `ann_{0..8} = 0,0,0,0,0,0,15,45,90` from the sealed v=2 footprint; consistency `ann_{9..12} = 150,225,315,420`; the law for `0 ≤ c ≤ 120`. All pass byte-exact. ∎

> **BREAKER — Theorem 3.1 (top main body, CERTIFIED via duality).**
> HOW PROVED: by the socle pairing A_d = ann_{3q+3−d}; Frobenius makes the frame coefficients pass through the q-th power unchanged ⟹ fixed q-free modules M′⊆S⁷, N₃⊆S³; ann_c = HF_M′ − 2HF_N₃ − dimE.
> HOW TO ATTACK: verify the socle degree 3q+3 = Σ(deg_i − 1). Recompute ann at c = 6,7,8 by brute LA at v=2 (must give 15,45,90 = footprint). Check M′ ∈ S⁷ (ONE shared X: HF_M′(1)=7, NOT two/S⁸ — a rebuilder's trap). Re-run in Macaulay2 (done — matches).
> WHY IT HOLDS: nine gates are values of the SEALED v=2 footprint reached by a completely different route (duality); q-freeness is forced by Frobenius, not assumed; Macaulay2 confirms HF_N₃, HF_M′ and ann.



### 4. The collar
Four degrees remain: `d ∈ [2q, 2q+3]` ⟺ `c ∈ [q, q+3]`, where q-freeness genuinely breaks. Write `e′ = q+f`, `f ∈ {0..3}`; `Syz(e′) = {λ ∈ (R_{e′})⁶: Σλᵢsᵢ^q = 0 in R}`.

**Theorem 4.1 (T-block decomposition).** For `q ≥ 9`, `f ≤ 3`, `Σλᵢsᵢ^q ∈ E`, `deg λ = q+f`: on each sheet, with `Δ_k = Δ_k^∅ + Σ_l u_l^qδ_{k,l}` (reduced + large parts, `deg δ = f`), the sheet identity splits into disjoint monomial classes and forces: (i) `Δ_k^∅ = 0`; (ii) `δ_{k,k} = 0`; (iii) `δ_{l,k} = −δ_{k,l}` (Koszul antisymmetry), cofactor degree ≤ 3.
*Proof.* `deg Δ = q+f < 2q` ⟹ at most one exponent ≥ q per monomial. In `Σ_ku_k^qΔ_k = 0`, the classes {one exponent in [q,2q−1]}, {one ≥ 2q}, {two ≥ q} (three impossible: `q+f < 3q` for q ≥ 9) are disjoint; each vanishes separately. ∎

We state the aggregate factoring as an explicit identity of linear maps, checkable by inspection. Write `λᵢ = Σ_m c_{i,m}s^m`. The exact monomial-wise restriction formula: **(R)** `s^m|_J = (−1)^{Σ_k m_{b_k}} ∏_k u_k^{m_{a_k}+m_{b_k}}`. Fix J, l, `p = P_l = {a,b}`: a monomial contributes to the `u_l^q`-part iff its pair-weight `w_p(m) = m_a+m_b ≥ q`; writing `m = (m_a, m_b, γ)`, the total degree forces **(T)** `t = f − |γ|` (determined). By (R) the contribution is `(−1)^{m_b}(−1)^{ε(γ,J)} u_l^t μ(γ,J)` with `μ, ε` depending only on (γ,J) — **the split-dependence enters ONLY through `(−1)^{m_b}`.** Define the alternating aggregates (linear functionals): **(AGG)** `c̃ᵢ(p,γ) = Σ_β(−1)^β c_{i,(w−β,β,γ)}`, `w = q+f−|γ|`. Then coordinate-by-coordinate: **(★)** `[u_l^q-part of λᵢ|_J] = Σ_γ (−1)^{ε(γ,J)} c̃ᵢ(p,γ) u_l^{f−|γ|} μ(γ,J)`.

**Lemma 4.2 (Aggregate factoring).** With `W_f = ⊕_{(i,p,γ)}F₃` (free aggregate space, q-free) and `A_f: W_f → ⊕_{J,k≠l}F₃[u]_f` defined by the fixed coefficients of (★): **`Φ_collar = A_f ∘ agg`** as linear maps. Hence `Im(Φ_collar|_Syz) ⊆ D_f := Im(A_f) ∩ {antisym}` — a fixed space.
*Proof.* Evaluate both sides at each coordinate (J,k,l): the left is `δ_{k,l}^{(J)}`; by (★) at `i = a_k` (+1) and `i = b_k` (−1) this equals the (J,k,l)-coordinate of `A_f(agg(λ))`. Agreement on every λ, every coordinate. Antisymmetry is T-block (iii). ∎
**Remark (multi-heavy monomials, dissolved).** A monomial heavy for several pairs enters the aggregates of each, with the sign of (AGG) — `agg` is a tuple of functionals; no disjoint decomposition of λ is used anywhere, and each output coordinate (J,k,l) reads only the `p = P_l` aggregates, once, so no sign conflict can arise.

> **BREAKER — Lemma 4.2 (aggregate factoring) — THE thinnest joint, now formalized.**
> HOW PROVED: as an explicit identity of linear maps `Φ_collar = A_f ∘ agg`, verified coordinate-by-coordinate via the restriction formula (R), the degree determination (T), and the alternating aggregates (AGG)→(★). No disjoint decomposition of λ is ever used.
> HOW TO ATTACK: THIS is where two independent reviewers pushed hardest. The multi-heavy objection: a monomial heavy for several pairs. Try to build a sign cocycle — a cycle p₁→p₂→p₃→p₁ whose signs multiply to −1. Try to make Im(Φ) EXCEED D_f (the rank certificate 10,55,145,280 would then break — but it's verified four ways including Macaulay2). Check that each output coordinate (J,k,l) reads only the p=P_l aggregates, once.
> WHY IT HOLDS: `agg` is a TUPLE OF FUNCTIONALS — a shared coefficient feeds several coordinates with fixed signs; no new direction is created, and the factoring is a coordinate-wise identity (Remark, dissolved). The bound needs only dim Im ≤ dim D_f (a superset bound — no injectivity, no surjectivity, no exactness).



**Theorem 4.3 (Collar ceilings).** For `f = 0..3`: **`dim D_f = 10 + 45·C(f+1,2) = 10, 55, 145, 280`** (rank certificate: rank A_f = 45,180,405,720; symmetric parts 35,125,260,440). Moreover `ker(Φ_collar|_Syz) = π(M)` of dimension `HF(R)_{e′} + σ_{e′}`, and the required bound satisfies the **q-cancellation identity**: `5HF(R)_{q+f} − HF(R)_{2q+f} + 15C(q−1−f,2) − σ(q+f) = 10 + 45C(f+1,2)` (all q-terms cancel). Therefore `Syz(q+f) ≤ [HF(R)+σ](q+f) + dim D_f`, giving **`A_d ≤ 15N_q(d)` at `d = 2q..2q+3`, all v ≥ 2.**
*Proof.* Rank certificate: fixed matrices of Lemma 4.2, verified four ways (§6). **Kernel identification — by RADICALITY, not by Recognition out of range:** in the kernel, T-block (i) kills the reduced parts and δ = 0 the large parts, so `Δ_k = 0` on every sheet; then `λ_a−λ_b` vanishes on V(p), and since `I(p)` is radical, `λ_a−λ_b ∈ I(V(p)) = I(p)`, i.e. λ ∈ M; conversely M ⊆ ker. Dimension `HF(R)+σ` by the census law (∀e). q-cancellation: direct expansion, the q², qf, q coefficients vanish identically (45−60+15; 90−60−30; −45+90−45); re-verified at q = 9,27,81,243. The chain is rank–nullity plus `dim(m^{[q]}R)_{q+e′} = 6HF(R)_{e′} − Syz(e′)`. ∎

> **BREAKER — Theorem 4.3 (collar ceilings).**
> HOW PROVED: fixed rank certificate (dim D_f, four ways) + kernel identification BY RADICALITY (not Recognition at e≥q!) + q-cancellation identity (all q-terms vanish) + rank–nullity.
> HOW TO ATTACK: the range-hygiene trap — confirm the kernel identification uses I(p) radical, NOT Recognition out of its e<q range (it does: T-block ⟹ Δ_k=0 on sheets ⟹ λ_a−λ_b ∈ I(V(p)) = I(p)). Redo the q-cancellation by hand (10 lines): 45−60+15=0, 90−60−30=0, −45+90−45=0. Check tightness at v=2: bound = measured Syz(9..12)=1000,1360,1810,2350 (any slack would show as strict inequality).
> WHY IT HOLDS: only exponent arithmetic + a superset factoring + one fixed rank + polynomial algebra; the squeeze is tight at v=2 on all four f, leaving no slack for a hidden error.



### 5. The Ledger identity and the proof
**Theorem 5.1 (Ledger).** With `ZA(q) = Σ_{d<q}HF(R)_d`, `W(q) = Σ_{e<q}[HF(R)_{q+e} − 5HF(R)_e + σ_e]`:
> `ZA(q) + W(q) + 15·C(q,3) = P(q)` identically for `q ≥ 5`
(cubic polynomials; checkpoints q = 9, 27, 81, 243 byte-exact; `15C(q,3) = 15·#{a: |a| ≥ 2q}`). Each summand is a genuine closed form in q as a free variable — HF(R)_d exactly for d ≥ 4, σ_e the Hilbert function of one fixed module, the count via the bijection b = (q−1)−a — so no hidden v-dependence can hide behind the four power-of-3 checkpoints.

**Proof of Theorem 1.2.** For v ≥ 2: Zone A + window exact (Cor. 2.3); top main body exact (Thm 3.1); the Ledger gives `A(q) − P(q) = Σ_{d=2q}^{2q+3}[A_d − 15N_q(d)]`. By Thm 4.3 each summand ≤ 0, so `A(q) ≤ P(q)`; with the floor (Prop 1.3) `A(q) = P(q)`. For v = 1: `A(3) = 141 = P(3)`, sealed direct computation. ∎

> **BREAKER — Theorem 5.1 (Ledger) & the assembly.**
> HOW PROVED: ZA+W+15C(q,3)=P(q), a cubic identity (4 checkpoints); each summand a genuine closed form in q (no hidden v-dependence). Assembly: exact zones + Ledger ⟹ A−P = Σ_collar(A_d−target); ceilings ⟹ A≤P; floor ⟹ A≥P ⟹ A=P.
> HOW TO ATTACK: the sharpest logical attack found (by Opus 4.8): the 4 checkpoints are all powers of 3, so an impostor P(q)+g(v)·[vanishing v=2..5] would pass — CLOSED because each summand is a genuine polynomial in q free (no v hidden). Check the zone partition is a disjoint exact cover (d<q; q≤d<2q; 2q≤d≤2q+3; d≥2q+4). Check no circularity: floor (Prop 1.3) is independent of §2–5.
> WHY IT HOLDS: four points determine a cubic once each side is genuinely polynomial in free q; the partition is disjoint by construction; the floor is older than and disjoint from the ceiling machinery.



### 6. Verification record and reproducibility
All machine steps are finite computations over F₃ on fixed (q-free) objects, each gated before reading. Every load-bearing certificate has been reproduced **four independent ways**:
1. **The authors' engines** (Gröbner-kernel and rank computations, Python and portable C++), with byte-exact gates against the sealed anchors A(3)=141, A(9)=7761 and their full degreewise footprints, cross-checked on independent hardware.
2. **Re-runs of all engines on a second machine.**
3. **From-scratch reconstructions by an independent implementation using *different methods*** (direct linear algebra in place of Gröbner bases), agreeing byte-exact.
4. **Macaulay2 (v1.26.06):** all three certificates re-implemented using M2's native `kernel`, `hilbertFunction` and `rank` machinery — census HF_M(0..5) = 1,11,52,171,456,1032 and the σ-law; collar dim D_f = 10,55,145,280; annihilator HF_N₃, HF_M′ and ann_c = 0,…,0,15,45,90,150,225,315,420 = 15·C(c−4,2) through c=12 — all byte-exact on the first run.

The complete verification dossier (including seven independent logical reviews of the pencil arguments across four AI model families), every engine with its logs, the Macaulay2 scripts, and standalone write-ups of each theorem are available at **github.com/tretoef-estrella**.

**A referee's guide.** In our own judgment the four load-bearing joints, in decreasing order of the attention they deserve: (i) Lemma 4.2, now a coordinate-wise identity precisely so the multi-heavy remark can be checked by inspection; (ii) range hygiene of every theorem (the kernel identification in Thm 4.3 deliberately uses radicality, not Recognition, at e ≥ q); (iii) Prop 1.3, whose only imported ingredient is the [DS] identification of P as the characteristic-0 target; (iv) the geometric dictionary between the algebraic statement proved here and Conjecture 1.2 as formulated in [DS] — which belongs to the experts of that framework and which we cannot strengthen from inside. Expanded guide with attack suggestions per joint: `SOFA_WHERE_TO_ATTACK.md` in the repository.

**Status.** Every link of the proof is either a pencil argument valid for all v or a finite gated certificate on a q-free object; the computational layer has been verified as described above. The record has not yet been refereed by a human expert; it is offered to the community precisely for that examination.

**Reference.** A. Degtyarev, I. Shimada, *On the integral Hodge conjecture for Fermat varieties*, arXiv:1711.02628.
