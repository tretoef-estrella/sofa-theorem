# WHERE TO ATTACK THIS PROOF — a transparency note for referees
## The four places a gap could live, stated by the authors themselves

**Purpose.** We believe this proof is correct, and its computational layer has been verified four independent ways (including Macaulay2). But no proof should be trusted on its authors' word, and the honest service we can render a referee is to point at the load-bearing joints ourselves. Below are the four places where, in our own judgment, a gap could live if one exists — with what we have done about each, and what only an expert reader can do. If you want to break this proof, start here.

### 1. Lemma 4.2 (aggregate factoring) — the joint with the most prose
**The risk:** the extraction map's factoring through the fixed aggregate space must be well-defined for *every* syzygy, including monomials that are heavy for several pairs simultaneously.
**What we did:** rewrote the lemma as a coordinate-by-coordinate identity of linear maps (`LEMMA_4_2_FORMAL.md` in this repository): the factoring `Φ_collar = A_f ∘ agg` holds because `agg` is a tuple of linear functionals — it never requires a disjoint decomposition of λ, so multi-heavy monomials simply feed several functionals with fixed signs. Two independent logical reviewers pressed exactly this point (sign cocycles; multi-heavy) and found no inconsistency; the rank of the fixed space D_f is verified four ways.
**What remains for a referee:** read the formal write-up and confirm the extraction identity; it is now formula, not prose.

### 2. Theorems used at the edge of their proven range
**The risk (the classic failure mode of long proofs):** the Recognition Theorem is proven for coefficient degree e < q; the collar works at e = q+f ≥ q.
**What we did:** the collar never invokes Recognition out of range. The kernel identification `ker(Φ_collar|Syz) = π(M)` uses only: (a) the T-block theorem (pure exponent arithmetic at q ≥ 9), and (b) RADICALITY of the edge ideals — if all sheet-differences vanish identically on the three sheets through an edge, then λ_a − λ_b ∈ I(V(p)) = I(p) because I(p) is radical (proven: mod ε₁, ε₃ splits into three distinct linear forms in char 3). No Recognition needed at e ≥ q. This is now stated explicitly in `LEMMA_4_2_FORMAL.md`, Remark 3.
**What remains for a referee:** check every other theorem's quantifiers the same way. We list each theorem's proven range in its standalone file.

### 3. Proposition 1.3 (the floor A ≥ P) — the pillar proved elsewhere
**The risk:** the paper states the floor in one line; its proof lived in project files, not in the paper.
**What we did:** full standalone write-up now in this repository (`THE_FLOOR_THEOREM_standalone.md`): the floor is the semicontinuity of integer-matrix rank under reduction mod 3, plus the sealed Point-Count identity `P(3^v) = |X_v(F₃)|` (verified byte-exact at v = 1, 2, 3: 141, 7761, 263901, engine and data files archived). The one imported identification — that P is the characteristic-0 dimension — is the Degtyarev–Shimada framework itself (arXiv:1711.02628), i.e., the definition of their target, not something we assert.
**What remains for a referee:** confirm the char-0 identification against [DS] and re-run the point-count engine (seconds).

### 4. The geometric translation (algebra ⟷ DS Conjecture 1.2)
**The risk:** this paper proves the algebraic statement `A(q) = P(q)` and asserts its equivalence with the saturation / integral-Hodge statement of [DS].
**What we did:** this translation is the [DS] framework's own dictionary; we use it as stated there. We are algebraists by construction of this project; the geometric dictionary is precisely the part that belongs to the experts who wrote it.
**What remains for a referee:** an expert in the [DS] setting should confirm that the algebraic target we hit is exactly their Conjecture 1.2 target for the 3^v tower. **This is the one link we cannot strengthen further from inside, and we say so plainly.**

*If you break any of these four — or anything else — the byte-exact discrepancy is more valuable to us than agreement. tretoef@gmail.com.*
