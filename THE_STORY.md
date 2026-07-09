# The Story of the Sofa Theorem
### How a proof of an integral Hodge conjecture was built, brick by brick, over a long campaign

*This document is the human story behind the mathematics. The proof stands on its own; but the path to it — and the discipline that produced it — is itself the evidence that this is serious work, not a lucky guess.*

---

## The problem, in one image

Degtyarev and Shimada conjectured (2017) that a certain integral Hodge statement holds for the Fermat fourfolds. Translated to the arithmetic that this project attacks, the question became: does a single cubic polynomial, $P(q)=15q^3-45q^2+55q-24$, give the dimension $A(q)$ of a truncated coordinate ring — **for every level $q=3^v$ of an infinite tower, all at once?**

Measuring $A(q)$ at one level is easy. Proving it for the *whole infinite tower* is the wall. The campaign's private name for the obstacle was "the cat," and closing the conjecture was "getting the cat into the water." For months, the cat walked the edge of the roof and laughed.

## The discipline: how the work was actually done

This was not a single flash of insight. It was a governed campaign with rules — a constitution — built to make an amateur's intuition survive contact with rigorous mathematics. A few numbers convey the scale:

- **~398 dead ends**, each buried in a "graveyard" with the byte-exact datum that killed it. (A project that invents its results has no graveyard; this one has almost four hundred entries.) Torsion-by-local-decomposition, freeness of the annihilator, matching-adapted frames, a dozen renamings of the same wall — all tried, all killed, all recorded.
- **249 versions** of the running findings master — an append-only log, never overwritten, so that no idea and no failure was ever lost.
- **A five-model logical review** and a **four-way computational verification**, described in the dossier.

The governing principle, stated many ways, was always the same: *measured is not proved.* A value confirmed at $v=1,2$ is an egg, not a law of the tower. The entire fight was to show that every egg is the same egg at another scale — that level $v+1$ is an exact $\times 3$ copy of level $v$ — and this is exactly what the mathematics finally delivered.

## The turning points

**The bala sin marcas (Frobenius).** In characteristic 3, $(a+b)^3=a^3+b^3$ — the cross term carries a factor 3 and vanishes. Raising to the power $q=3^v$ is *linear*: the bullet passes through the sum and leaves no mark. This is why the tower is tractable at all; almost everything downstream rests on it.

**The Recognition Theorem.** Below the threshold $q$, the syzygy census of the middle window does not depend on $v$. The tower disappears from an entire zone of the problem — a single finite computation seals infinitely many levels.

**The Ledger.** A cubic identity showed that *all* of the possible discrepancy $A(q)-P(q)$, across the entire infinite tower, is concentrated in four boundary degrees. The infinite problem collapsed to a finite one — four numbers.

**The collar, and the needle.** Those four numbers required a fixed rank certificate. Finding its generator was, in the campaign's image, searching a haystack for a needle — until the lesson landed: *you don't search, you distill.* A symmetrizer applied to the raw data produced the generator directly. The wall, up close, was made of Koszul relations with tiny cofactors.

## What is claimed, and what is not

The mathematics is complete within the campaign's terms: every link is a pencil argument valid for all $v$, or a finite certificate on a fixed object, gated byte-exact. The computational layer has been reproduced four independent ways, including in Macaulay2, the community-standard system.

**And yet:** this is a *candidate*, not a confirmed record. No human expert in integral Hodge theory has yet examined the pencil logic at the depth a journal referee would. Five AI models found no break; that is encouraging, not conclusive — they share a lineage, and a human's independent eye is exactly the check we have not had. We say this plainly, because a result offered with its honest status intact is the only kind worth offering.

The cat may be in the water. The only way to be sure is for an expert to reach in and feel that it is wet.

---

*Rafael Amichis Luengo — Madrid — tretoef@gmail.com — github.com/tretoef-estrella*
