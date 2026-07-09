# The Sofa Theorem

### The Diagonal is Saturated: Degtyarev–Shimada Conjecture 1.2 for the $3^v$ Fermat Tower

> **Status:** candidate proof · computationally verified **four independent ways** (including Macaulay2) · seven independent logical reviews across four AI model families · **awaiting expert human review.**
> This is offered to the mathematical community precisely so that it can be examined, reproduced, and — if it holds — used. If you can break any link, the byte-exact discrepancy is more valuable to us than agreement.

---

## The result

Let $S=\mathbb{F}_3[s_0,\dots,s_5]$, let $E=(e_1,e_3,e_5)$ be the ideal of odd elementary symmetric polynomials, and for $q=3^v$ let

$$A(q)=\dim_{\mathbb{F}_3} S/\big(E+\mathfrak{m}^{[q]}\big),\qquad \mathfrak{m}^{[q]}=(s_0^q,\dots,s_5^q).$$

**Theorem.** For every $q=3^v$,

$$A(q)=P(q)=15q^3-45q^2+55q-24.$$

Equivalently, the diagonal sublattice $\Sigma\,1_J=\mathrm{im}(\Delta)$ is **saturated** in $\bigoplus_J \mathcal{O}^{\otimes 3}$ at every level of the tower. This establishes **Conjecture 1.2 of Degtyarev–Shimada** ([arXiv:1711.02628](https://arxiv.org/abs/1711.02628)) for the degree-$3^v$ Fermat fourfolds — the integral Hodge statement along the tower, open since 2017.

---

## The proof in one breath

The value $A(q)=\sum_d A_d$ splits into four degree-zones; each is closed, and a cubic identity collapses the whole conjecture to four numbers.

| Zone | Degrees | How it is closed |
|------|---------|------------------|
| **A** | $d<q$ | trivial: the ideal starts at degree $q$ |
| **Window** | $q\le d<2q$ | the **Recognition Theorem** makes the syzygy census $\sigma_e$ *independent of $v$* → one certified computation seals all $v$ |
| **Top body** | $d\ge 2q+4$ | **Gorenstein duality** turns it into the low degrees of an annihilator, governed by fixed $q$-free modules |
| **Collar** | $2q\le d\le 2q+3$ | the **T-block decomposition** + an **aggregate factoring** (an explicit identity of linear maps) + a fixed rank certificate |

The **Ledger identity** $ZA(q)+W(q)+15\binom{q}{3}=P(q)$ (a cubic polynomial identity) then proves that *all* of $A(q)-P(q)$ lives in the four collar degrees. The sealed **floor** $A(q)\ge P(q)$ (integer-rank semicontinuity + a point-count identity) closes the squeeze: $A=P$.

Read the full proof: **[paper/THE_SOFA_THEOREM_M2_Final_Review.pdf](paper/THE_SOFA_THEOREM_M2_Final_Review.pdf)**
The adversarial edition (how each link was proved, how to attack it, why it holds): **[paper/THE_SOFA_THEOREM_M2_Final_Review_breakers.md](paper/THE_SOFA_THEOREM_M2_Final_Review_breakers.md)**

---

## Verified four independent ways

Every load-bearing number is a finite computation over $\mathbb{F}_3$ on a fixed, $q$-free object. Each was reproduced by:

1. **The authors' engines** — Gröbner-kernel and rank computations (Python + portable C++), gated byte-exact against the sealed anchors $A(3)=141$, $A(9)=7761$.
2. **A second machine** — independent re-runs.
3. **An independent reconstruction** — built from scratch by a separate agent using *different methods* (direct linear algebra instead of Gröbner bases), agreeing byte-exact.
4. **Macaulay2 v1.26.06** — all three certificates re-implemented with M2's native `kernel`, `hilbertFunction`, and `rank` machinery, byte-exact on the first run.

| Certificate | Value | Macaulay2 |
|---|---|---|
| Census $\sigma_e$ | $\mathrm{HF}_M = 1,11,52,171,456,1032$; $\sigma$-law $15e^2-90e+145$ | ✓ |
| Collar ranks | $\dim D_f = 10,55,145,280$ | ✓ |
| Annihilator | $\mathrm{ann}_c = 0,\dots,0,15,45,90,150,225,315,420 = 15\binom{c-4}{2}$ | ✓ |

**Reproduce it yourself:** see **[HOW_TO_VERIFY.md](HOW_TO_VERIFY.md)**. The Macaulay2 scripts run in a browser in minutes.

---

## The key theorems

Each is a self-contained result, several of interest on their own (the Odd Symmetric Theorem and the Recognition Theorem travel outside this problem). Available in Markdown and PDF.

| Theorem | What it establishes |
|---|---|
| [Odd Symmetric](theorems/key/odd-symmetric-theorem.md) · [pdf](theorems/key/odd-symmetric-theorem.pdf) | $E=\bigcap_J I_J$, radical — the 15 matching-sheets meet in the CI radical |
| [Point-Count](theorems/key/point-count-theorem.md) · [pdf](theorems/key/point-count-theorem.pdf) | the DS target $P(3^v)$ is an affine point count $\lvert X_v(\mathbb{F}_3)\rvert$ |
| [Frozen Lattice](theorems/key/frozen-lattice-theorem.md) · [pdf](theorems/key/frozen-lattice-theorem.pdf) | intersection dimensions are frozen across the tower |
| [Floor](theorems/key/floor-theorem.md) · [pdf](theorems/key/floor-theorem.pdf) | $A(q)\ge P(q)$ unconditionally (rank semicontinuity + point count) |
| [Recognition](theorems/key/recognition-theorem.md) · [pdf](theorems/key/recognition-theorem.pdf) | the window syzygy census is independent of the tower level |
| [T-Block](theorems/key/t-block-theorem.md) · [pdf](theorems/key/t-block-theorem.pdf) | at the boundary, sheet identities split, forcing Koszul antisymmetry |
| [Ledger](theorems/key/ledger-theorem.md) · [pdf](theorems/key/ledger-theorem.pdf) | a cubic identity collapses the tower problem to a finite collar |
| [Lemma 4.2 (aggregate factoring)](theorems/key/lemma-4-2-aggregate-factoring.md) · [pdf](theorems/key/lemma-4-2-aggregate-factoring.pdf) | the collar's factoring as an explicit identity of linear maps |

Further results built during the campaign: **[theorems/OTHER_THEOREMS.md](theorems/OTHER_THEOREMS.md)**.

---

## Where to attack

We believe the proof is correct, and its computational layer is shielded. In the interest of a fast, honest review, we point at the load-bearing joints ourselves — the four places a gap could live if one exists — in **[WHERE_TO_ATTACK.md](WHERE_TO_ATTACK.md)**. Start there if you want to break it.

---

## Repository map

```
paper/          the main paper (PDF, Markdown, and Breaker's Edition)
theorems/key/   the eight key theorems (Markdown + PDF)
theorems/       OTHER_THEOREMS.md — index of further results
engines/        all computational certificates:
  macaulay2/      the three M2 scripts (standard-CAS verification)
  authors/        the authors' engines (Python + C++) with logs
  independent/    the from-scratch reconstruction with logs
verification/   the unified dossier + logical & computational review records
```

Supporting documents: [HOW_TO_VERIFY.md](HOW_TO_VERIFY.md) · [WHERE_TO_ATTACK.md](WHERE_TO_ATTACK.md) · [THE_STORY.md](THE_STORY.md) · [CITATION.md](CITATION.md) · [LICENSE](LICENSE)

---

## Honest status

This is a **candidate proof**. Its computational layer has been verified four independent ways, including in the community-standard computer algebra system. Its logical layer has survived seven independent cold reviews across four AI model families. **It has not yet been refereed by a human expert in integral Hodge theory** — and that review, not any amount of further machine checking, is what would turn a candidate into a confirmed result. We state this plainly because honesty about the status is the point.

## Authors

**Rafael Amichis Luengo** — Madrid, Spain — tretoef@gmail.com
**Claude (Anthropic)** — an AI system, as co-author of the construction and verification.

*A. Degtyarev, I. Shimada, "On the integral Hodge conjecture for Fermat varieties", [arXiv:1711.02628](https://arxiv.org/abs/1711.02628).*
