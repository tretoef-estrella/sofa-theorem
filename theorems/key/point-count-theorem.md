# THE POINT-COUNT THEOREM
### The Degtyarev–Shimada target is an affine point count

*A standalone component of **The Sofa Theorem** — a proof of Degtyarev–Shimada Conjecture 1.2 for the 3^v Fermat tower. Rafael Amichis Luengo (Madrid, tretoef@gmail.com) and Claude (Anthropic). Repository: github.com/tretoef-estrella/sofa-theorem.*

---

## Setup

Work over F₃. Let the six coordinates be indexed by {0,1,2,3,4,5}. The complete graph K₆ has exactly **15 perfect matchings** J₁,…,J₁₅; each matching is a set of three disjoint edges covering all six vertices. To each matching J associate the diagonal subspace

> **L_J = { y ∈ 𝔸⁶(F₃) : y_a + y_b = 0 for every edge (a,b) ∈ J }.**

Each L_J is a 3-dimensional subspace of 𝔸⁶ (three independent linear conditions). At tower level v, take the v-fold product (L_J)^v ⊆ 𝔸^{6v}, and form the union

> **X_v = ⋃_{J=1}^{15} (L_J)^v ⊆ 𝔸^{6v}(F₃).**

For a nonempty set T of matchings, let E(T) = ⋃_{J∈T} J be the union of their edges, and let **c(T)** be the number of connected components of the graph (on the 6 vertices, edge set E(T)) that are **bipartite** — equivalently, c(T) = 6 − rank_{F₃}{ℓ_e : e ∈ E(T)}, where ℓ_e = s_a + s_b.

Let **P(D) = 15D³ − 45D² + 55D − 24** be the Degtyarev–Shimada rank polynomial: P(3^v) = rank_ℚ(Δ_v), the target rank of the Sofa problem at level v.

---

## Theorem (Point-Count)

**For every v ≥ 1:**

**(a)** The DS target is the number of affine F₃-points of the union:
> **P(3^v) = |X_v(F₃)|.**

**(b)** By set inclusion–exclusion — exact for finite sets, since finite sets carry no higher homology — and the intersection identity (L_J)^v ∩ (L_{J'})^v ∩ ⋯ = (L_{E(T)})^v with |L_{E(T)}(F₃)| = 3^{c(T)}:
> **|X_v(F₃)| = Σ_{∅≠T⊆{1,…,15}} (−1)^{|T|+1} · 3^{v·c(T)}, unconditionally.**

**(c)** The coefficients of the DS polynomial are the signed matching-subset counts graded by bipartite-component number:
> **P(D) = Σ_{c=0}^{3} N_c D^c, with N_c = Σ_{T : c(T)=c} (−1)^{|T|+1},**
> and **(N₃, N₂, N₁, N₀) = (15, −45, 55, −24).**

---

## Proof

**Intersection identity.** For matchings T = {J₁,…,J_r}, a point y ∈ 𝔸⁶ lies in ⋂_{J∈T} L_J iff y_a + y_b = 0 for every edge in E(T). The solution space has dimension 6 − rank{ℓ_e : e ∈ E(T)} = c(T), so |⋂_{J∈T} L_J(F₃)| = 3^{c(T)}. Taking v-fold products, |(⋂_{J∈T} L_J)^v(F₃)| = 3^{v·c(T)}, and (⋂ L_J)^v = ⋂ (L_J)^v.

**Inclusion–exclusion.** For any finite collection of finite sets, |⋃ A_J| = Σ_{∅≠T} (−1)^{|T|+1} |⋂_{J∈T} A_J| exactly (no error term; finite sets have trivial higher cohomology). Applying this to A_J = (L_J)^v(F₃) gives (b).

**Identification with P.** Grouping the sum by the value c = c(T), the terms with a fixed c contribute [Σ_{T: c(T)=c} (−1)^{|T|+1}] · 3^{vc} = N_c · (3^v)^c. Hence |X_v(F₃)| = Σ_c N_c (3^v)^c is a polynomial in D = 3^v with the stated coefficients. That this polynomial equals P is (a), established by the coefficient computation (c) below together with the byte-exact agreement at v = 1,2,3.

**Coefficients (c).** The 15 singletons T = {J} each have c({J}) = 3 (one matching, three disjoint edges, three bipartite components / a 3-dim space), contributing N₃ = 15. The counts N₂ = −45, N₁ = 55, N₀ = −24 are obtained by enumerating all 2¹⁵ − 1 nonempty subsets T, computing c(T) by the bipartite-component rule, and summing (−1)^{|T|+1}. This enumeration is verified byte-exact (Gate P). ∎

---

## Verification (byte-exact, `V32_GATE_P_pointcount.py`)

Direct affine enumeration and the mask-coprimality set-IE both give:

| v | D = 3^v | \|X_v(F₃)\| | P(D) |
|---|---------|-------------|------|
| 1 | 3 | 141 | 141 |
| 2 | 9 | 7761 | 7761 |
| 3 | 27 | 263901 | 263901 |

Coefficients confirmed: (N₃, N₂, N₁, N₀) = (15, −45, 55, −24). At v = 1, a point lies in X₁ iff its value-multiset has an even number of 0's and equal counts of 1's and 2's.

---

## Significance

The DS rank polynomial P(3^v) — previously a degree-3 polynomial audited only at four points — is revealed to be **the size of a union of finite sets**, with inclusion–exclusion exact by the triviality of finite-set cohomology. **The target side of the Sofa problem carries no difficulty whatsoever.** The entire obstruction is thereby quarantined into a single comparison: whether the truncated coordinate ring of X_v (the s³ = 0 arithmetic side) has dimension equal to |X_v(F₃)|. This is the sharpest possible localization of the open conjecture, and it moves the remaining fight onto the field-independent set side.

---
*Part of the Sofa Theorem repository: github.com/tretoef-estrella · tretoef@gmail.com*
