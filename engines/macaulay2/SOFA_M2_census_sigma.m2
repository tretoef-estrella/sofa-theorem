-- ============================================================================
-- THE SOFA THEOREM -- CENSUS CERTIFICATE in Macaulay2
-- Independent verification of  sigma_e = 15 e^2 - 90 e + 145  (e >= 4)
-- via the Recognition module M, in the GEMEINDE-standard CAS (Macaulay2).
--
-- This is NOT a port of the authors' Gaussian-elimination code. It uses
-- Macaulay2's own kernel/Hilbert machinery, so agreement is a genuinely
-- independent check.
--
-- HOW TO RUN:   M2 SOFA_M2_census_sigma.m2
-- TARGET:       HF_M(0..5) = 1, 11, 52, 171, 456, 1032
--               sigma_e   = 0,0,1,5,25,70 (e=0..5); law 15e^2-90e+145 for e>=4
-- ============================================================================

R = ZZ/3[s_0..s_5];

-- The Recognition module M = { lambda in R^6 : lambda_a - lambda_b in I({a,b})
-- for every edge {a,b} of K6 }, where I({a,b}) = (s_a+s_b, eps1, eps3) with
-- eps1, eps3 the 1st and 3rd elementary symmetric polys of the OTHER four vars.

-- elementary symmetric polynomial e_k of a list of variables
elemSym = (vars, k) -> sum(subsets(vars, k), p -> product p);

-- the edge ideal I({a,b})
edgeIdeal = (a,b) -> (
    others := select(gens R, v -> v =!= s_a and v =!= s_b);
    ideal(s_a + s_b, elemSym(others,1), elemSym(others,3))
);

edges = subsets(splice{0..5}, 2);   -- the 15 edges of K6

-- Build M as the kernel of the map R^6 -> \oplus_{edges} R/I(edge)
-- sending (lambda_0..lambda_5) to ( lambda_a - lambda_b  mod I(a,b) )_{edges}.
-- We realize this degreewise via the presentation map.

-- Target module: direct sum over edges of R/I(edge)
targets = apply(edges, e -> (
    (a,b) := (e#0, e#1);
    R^1 / edgeIdeal(a,b)
));
T = directSum targets;

-- The map phi: R^6 -> T,  column i = contribution of lambda_i.
-- Row for edge {a,b}:  +1 in slot a, -1 in slot b (as elements of R/I).
phiMatrix = matrix table(#edges, 6, (r,i) -> (
    (a,b) := (edges#r#0, edges#r#1);
    if i == a then 1_R else if i == b then -1_R else 0_R
));
phi = map(T, R^6, phiMatrix);

M = kernel phi;

print "-- HF_M(e) for e = 0..8 (target: 1,11,52,171,456,1032,...) --";
for e from 0 to 8 do (
    print("  HF_M(" | toString e | ") = " | toString hilbertFunction(e, M))
);

-- sigma_e = HF_M(e) - ( HF_S(e) + 5 * dim E_e )
S = R;  E = ideal(elemSym(gens R,1), elemSym(gens R,3), elemSym(gens R,5));
print "-- sigma_e = HF_M(e) - HF_S(e) - 5*dimE(e)  (target 0,0,1,5,25,70) --";
for e from 0 to 6 do (
    hfM := hilbertFunction(e, M);
    hfS := hilbertFunction(e, S^1);
    dimE := hilbertFunction(e, module E);
    sig := hfM - hfS - 5*dimE;
    law := 15*e^2 - 90*e + 145;
    print("  e=" | toString e | ": sigma=" | toString sig |
          (if e>=4 then "  (law 15e^2-90e+145 = " | toString law | ")" else ""))
);
print "-- DONE. Compare against the Python/C++ engines and the paper. --";
