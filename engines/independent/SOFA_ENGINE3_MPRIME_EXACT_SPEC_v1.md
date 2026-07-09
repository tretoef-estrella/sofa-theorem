# SOFA — ENGINE 3 (M′) EXACT SPECIFICATION · for the independent rebuilder
## The precise definition of M′ that Engine 1/2's spec was missing — no ambiguity this time

**Context:** you rebuilt Engine 1 and Engine 2 from scratch and claved them (10,55,145,280 and 1,5,25,70). Correct and appreciated — and you were RIGHT that the M′ spec was vague. Here is the exact definition, at the level of every slot, sign, and column. Your interpretation "X-carrier = u_b per block" was the wrong guess; the truth is below. Rebuild M′ from THIS and check `ann_c`.

---

## The object
`ann_c = HF_{M′}(c) − 2·HF_{N₃}(c) − dim E_c`, target `ann_c = 15·C(c−4,2)` (anchors `ann_{6,7,8} = 15,45,90`). You already have N₃ and dim E_c solid; only M′ was ambiguous.

## Slots (the codomain index)
M′ is the KERNEL of a map whose codomain has **90 slots**, indexed `(J, blk, k)`:
- `J` = one of the 15 sheets,
- `blk ∈ {1, 2}` = which of the two annihilator conditions (block 1 tests `s₁^q`, block 2 tests `s₂^q`),
- `k ∈ {0,1,2}` = which pair of sheet `J`.
So slot index = `J*6 + (blk−1)*3 + k`, total `15*6 = 90`.

## Columns (the domain — 7 variable-columns + relation-columns)
The domain is `S⁷`: seven variable-columns `(X, Y₁,Y₂,Y₃, Z₁,Z₂,Z₃)`, PLUS the per-slot relation columns that impose "modulo I_J".

**The single X-column** (this is the piece you had to guess — here is the truth):
For each sheet `J` and each block `blk`: X restricts to the sheet the variable `s₁` if `blk==1`, or `s₂` if `blk==2`. Concretely — let `idx = 1` for block 1, `idx = 2` for block 2. Find how `s_idx` restricts on sheet `J`: `s_idx` belongs to some pair `k*` of `J`, as either the `a`-element (sign `eps = +1`) or the `b`-element (sign `eps = +2 ≡ −1 mod 3`). Then the X-column has entry `eps` at slot `(J, blk, k*)`, and zero at the other two `k` of that (J,blk). 
*(In words: X carries `s₁^q` into block 1 and `s₂^q` into block 2 — the two generators of the ideal `(s₁^q,s₂^q)` whose annihilator we want. That is why there are exactly two blocks and one X: `s_i^q·X` for i=1,2.)*

**The six Y/Z-columns** (three per block, carrying the frame — these you had roughly right):
For `blk = 1`, columns `Y₁,Y₂,Y₃`; for `blk = 2`, columns `Z₁,Z₂,Z₃`. Column `m` (m=0,1,2) of block `blk` has, at slot `(J, blk, k)`, the entry `−(γ_{m}|_J)_k` where `γ_m|_J` is the restriction of the frame form `ℓ_{m+1}` to sheet `J` (a 3-vector in the sheet coordinates; `(·)_k` is its k-th component). Sign is `−` (i.e. `(3 − value) mod 3`). Block 1 uses Y, block 2 uses Z, but BOTH use the SAME three frame forms `ℓ₁,ℓ₂,ℓ₃` — the blocks are NOT different frames; they differ only in which `s_i` the X-column feeds.
*(In words: the relation being encoded is `s_i^q·X = Σ_m ℓ_m^q·Y_m` on each sheet, i.e. `s_i^q X − Σ ℓ_m^q Y_m ∈ E`. Block 1 for i=1 with Y, block 2 for i=2 with Z. Frobenius makes the q-th powers linear, so the sheet restriction is what you see — q-free.)*

**The relation columns** (impose "modulo I_J", per slot): for each slot `(J, blk, k)` and each of the 3 pairs `(a,b)` of `J`, a column with entries `+1` at `s_a` and `+1` at `s_b` in that slot (this is the generator `s_a+s_b` of the sheet ideal I_J acting in that slot). That's `90 slots × 3 = 270` relation columns, plus the 7 variable columns = 277 columns total.

## The map, in one sentence
A tuple `(X,Y,Z) ∈ S⁷` is in M′ iff on every sheet J and every block: `s_idx^q·X − Σ_m ℓ_m^q·(Y or Z)_m ≡ 0` modulo I_J, degreewise — encoded as the columns above. Compute M′ = kernel via extended-module elimination (or degree-by-degree kernel), read `HF_{M′}`, combine `ann_c = HF_{M′}(c) − 2·HF_{N₃}(c) − dim E_c`.

## Gate
`ann_{0..8} = 0,0,0,0,0,0,15,45,90`; `ann_{9..12} = 150,225,315,420`; law `15·C(c−4,2)`. Report your `ann_c`. If it still differs, the discrepancy is real and I want the exact numbers.
