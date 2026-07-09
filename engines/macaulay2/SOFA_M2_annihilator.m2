-- ============================================================================
-- THE SOFA THEOREM -- ANNIHILATOR CERTIFICATE in Macaulay2  (the third engine)
-- Independent verification of  ann_c = HF_M'(c) - 2*HF_N3(c) - dimE(c)
--                                    = 15*binomial(c-4,2)
-- TARGETS:
--   HF_N3(0..8) = 0,3,18,66,183,426,876,1641,2856
--   HF_M'(0..8) = 0,7,42,154,427,994,2059,3874,6754
--   ann(0..8)   = 0,0,0,0,0,0,15,45,90   then 150,225,315,420 at c=9..12
--
-- Uses Macaulay2's native kernel + hilbertFunction (independent of all
-- Python/C++ engines). HOW TO RUN:  load "SOFA_M2_annihilator.m2"
-- NOTE: M' has 90 slots; the kernel computation may take a few minutes. Patience.
-- ============================================================================

R = ZZ/3[s_0..s_5];

-- the 15 perfect matchings of K6 (same code as the collar script, validated)
matchings = method();
matchings List := (elts) -> (
    if #elts == 0 then return {{}};
    a := elts#0;
    rest := drop(elts,1);
    flatten for i from 0 to #rest-1 list (
        b := rest#i;
        others := drop(rest,{i,i});
        apply(matchings others, m -> prepend({a,b}, m))
    )
);
SHEETS = matchings splice{0..5};
assert(#SHEETS == 15);

FRAME = {{0,2,0,1,0,1},{1,0,0,1,1,0},{2,1,2,2,0,0}};

-- sheet ideal I_J = (s_a+s_b : pairs of J);  gamma_{m,k} = frame coeff on pair k
sheetIdeal = (J) -> ideal apply(J, p -> s_(p#0) + s_(p#1));
gam = (J,m,k) -> ( p := J#k; FRAME#m#(p#0) - FRAME#m#(p#1) );

-- ======================= MODULE N3 (gate this first) ========================
-- N3 = ker( R^3 -> \oplus_{(J,k)} R/I_J ),  column m has scalar gamma_{m,k}
-- at slot (J,k).
slotsN3 = flatten for Ji from 0 to 14 list for k from 0 to 2 list (Ji,k);
TN3 = directSum apply(slotsN3, sl -> R^1/sheetIdeal(SHEETS#(sl#0)));
matN3 = matrix table(#slotsN3, 3, (r,m) -> (
    sl := slotsN3#r;
    (gam(SHEETS#(sl#0), m, sl#1))*1_R
));
phiN3 = map(TN3, R^3, matN3);
N3 = kernel phiN3;
print "-- HF_N3(c) for c=0..8  (target 0,3,18,66,183,426,876,1641,2856) --";
for c from 0 to 8 do (
    print("  HF_N3(" | toString c | ") = " | toString hilbertFunction(c, N3))
);

-- ======================= MODULE M' (the shared-X module) ====================
-- M' = ker( R^7 -> \oplus_{(J,blk,k)} R/I_J ),  columns = (X, Y0,Y1,Y2, Z0,Z1,Z2):
--   X (column 0): at slot (J,blk,k): if k == k* (the pair of J containing
--     s_idx, idx = blk, i.e. s_1 for block 1 / s_2 for block 2) then eps
--     (+1 if s_idx is the 'a' of that pair, -1 if the 'b'), else 0.
--     ONE shared X serving both blocks -- this is what ties s_1 and s_2.
--   Y_m (columns 1..3): -gamma_{m,k} at slots of block 1 only.
--   Z_m (columns 4..6): -gamma_{m,k} at slots of block 2 only.
slotsM = flatten flatten for Ji from 0 to 14 list
             for blk from 1 to 2 list
                 for k from 0 to 2 list (Ji,blk,k);
TM = directSum apply(slotsM, sl -> R^1/sheetIdeal(SHEETS#(sl#0)));
matM = matrix table(#slotsM, 7, (r,j) -> (
    sl := slotsM#r;
    J := SHEETS#(sl#0);  blk := sl#1;  k := sl#2;
    if j == 0 then (
        idx := blk;                                   -- s_1 or s_2
        kstar := position(J, p -> member(idx,p));
        if k != kstar then 0_R
        else if (J#kstar)#0 == idx then 1_R else -1_R
    ) else (
        m := (j-1)%3;
        b := (j-1)//3 + 1;                            -- 1 for Y-block, 2 for Z-block
        if b != blk then 0_R else (-(gam(J,m,k)))*1_R
    )
));
phiM = map(TM, R^7, matM);
print "-- computing kernel of the 90-slot map (may take a few minutes)... --";
Mp = kernel phiM;
print "-- HF_M'(c) for c=0..8  (target 0,7,42,154,427,994,2059,3874,6754) --";
for c from 0 to 8 do (
    print("  HF_M'(" | toString c | ") = " | toString hilbertFunction(c, Mp))
);

-- ======================= THE ANNIHILATOR ====================================
elemSym = (varlist, k) -> sum(subsets(varlist, k), p -> product p);
E = ideal(elemSym(gens R,1), elemSym(gens R,3), elemSym(gens R,5));
print "-- ann_c = HF_M' - 2*HF_N3 - dimE  (target 0,0,0,0,0,0,15,45,90 ; then 150,225,315,420) --";
for c from 0 to 12 do (
    hfM := hilbertFunction(c, Mp);
    hfN := hilbertFunction(c, N3);
    dE  := hilbertFunction(c, module E);
    a   := hfM - 2*hfN - dE;
    law := if c >= 6 then 15*binomial(c-4,2) else 0;
    print("  c=" | toString c | ": ann = " | toString a | "   (law 15*C(c-4,2) = " | toString law | ")")
);
print "-- DONE. If ann = 0,...,0,15,45,90,150,225,315,420 the third certificate";
print "-- is verified in Macaulay2 and ALL THREE engines hold in the standard CAS. --";
