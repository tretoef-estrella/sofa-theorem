# THE FROZEN-LATTICE THEOREM
### Intersection dimensions in the matching-subspace arrangement are frozen across the tower

*A standalone component of **The Sofa Theorem** — a proof of Degtyarev–Shimada Conjecture 1.2 for the 3^v Fermat tower. Rafael Amichis Luengo (Madrid, tretoef@gmail.com) and Claude (Anthropic). Repository: github.com/tretoef-estrella/sofa-theorem.*

---

## Setup

Over F₃, index six coordinates by {0,…,5}. K₆ has 15 perfect matchings J₁,…,J₁₅. For a matching J, let L_J = { y ∈ 𝔸⁶ : y_a + y_b = 0, (a,b) ∈ J }, a 3-dimensional diagonal subspace. For a nonempty set T of matchings, let E(T) = ⋃_{J∈T} J and let **c(T)** = number of bipartite connected components of the graph (6 vertices, edges E(T)) = 6 − rank_{F₃}{ ℓ_e = s_a + s_b : e ∈ E(T) }.

At tower level v, the arrangement is { (L_J)^v ⊆ 𝔸^{6v} }, and the intersection over T is (⋂_{J∈T} L_J)^v.

---

## Theorem (Frozen Lattice)

**For every nonempty T ⊆ {1,…,15} and every v ≥ 1:**
> **dim_{F₃} (⋂_{J∈T} (L_J)^v) = v · c(T),  hence  |(⋂_{J∈T} (L_J)^v)(F₃)| = 3^{v·c(T)}.**

The intersection dimension per level is **c(T), independent of v** ("frozen"); the tower merely multiplies it by v. In particular the numbers 3^{c(T)} that feed the inclusion–exclusion of the arrangement are **char-independent and v-independent** — they are set counts of a fixed finite arrangement, carrying no torsion.

---

## Proof

The intersection ⋂_{J∈T} L_J is the solution space in 𝔸⁶ of the linear system { ℓ_e = 0 : e ∈ E(T) }. Its dimension is 6 − rank_{F₃}{ℓ_e : e ∈ E(T)}. Each ℓ_e = s_a + s_b is the (signed) incidence vector of edge e; the rank of a set of such vectors over any field equals |V| − (number of bipartite components of the edge graph) — the standard rank of a graph's incidence matrix, where a component contributes (its vertex count − 1) to the rank if it contains an odd cycle, and (vertex count − 1) with one extra relation, i.e. bipartite components each drop the rank by one relative to a spanning forest. Concretely rank = 6 − c(T) with c(T) the bipartite-component count, giving dim(⋂ L_J) = c(T).

For the product, (⋂_{J∈T} L_J)^v = ⋂_{J∈T} (L_J)^v (products commute with these coordinate-wise intersections), and dim of a v-fold product is v times the factor dimension, so dim = v·c(T) and the point count is 3^{v·c(T)}. Nothing in the argument uses the field beyond char ≠ 2 issues absorbed into the bipartite-component count; the value c(T) is a graph invariant of the fixed arrangement, identical at every tower level. ∎

---

## Verification (byte-exact, direct enumeration at v=1)

| T (sample) | \|⋂ L_J(F₃)\| | 3^{c(T)} | c(T) |
|---|---|---|---|
| singleton {J} (all 15) | 27 | 27 | 3 |
| pair, bipartite-merging | 3 | 3 | 1 |
| pair, disjoint-merging | 9 | 9 | 2 |
| triple (K₃,₃ type) | 3 | 3 | 1 |

All tested T satisfy |⋂_{J∈T} L_J| = 3^{c(T)} byte-exact.

---

## Significance

This theorem is the structural backbone that makes the Point-Count Theorem possible: because every intersection dimension is frozen at c(T) per level, the inclusion–exclusion of the arrangement is a **fixed finite combinatorial datum**, blind to the tower and to the field. It confines all the arithmetic difficulty of the Sofa problem out of the *lattice of intersections* (which is frozen and torsion-free) and into the single question of how the truncated coordinate ring sits against this frozen lattice — i.e. it is the theorem that lets one say "the torsion does not live in the intersections, only in how the subspaces sum."

---
*Part of the Sofa Theorem repository: github.com/tretoef-estrella · tretoef@gmail.com*
