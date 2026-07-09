-- ============================================================================
-- THE SOFA THEOREM -- COLLAR RANKS CERTIFICATE in Macaulay2
-- Independent verification of  dim D_f = 10, 55, 145, 280  (f = 0,1,2,3)
-- D_f = Im(A_f) \cap Antisym,  dim D_f = rank(A_f) - rank(symmetric part).
--
-- Uses Macaulay2's own exact rank over ZZ/3. Independent of the Python code.
--
-- HOW TO RUN:   M2 SOFA_M2_collar_ranks.m2
-- TARGET:       dim D_f = 10,55,145,280 ; rank A_f = 45,180,405,720 ;
--               rank(sym) = 35,125,260,440
-- ============================================================================

kk = ZZ/3;

-- the 15 perfect matchings of K6
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
PAIRS = subsets(splice{0..5},2);

-- monomials of degree d in nv variables, as exponent lists
monos = method();
monos(ZZ,ZZ) := (d,nv) -> (
    if nv==1 then return {{d}};
    flatten for i from 0 to d list apply(monos(d-i,nv-1), r -> prepend(i,r))
);

-- build A_f and its symmetric part, return (rank A_f, rank sym)
buildAf = (f) -> (
    umon := monos(f,3);
    nm := #umon;
    umonIndex := hashTable apply(#umon, i -> (umon#i, i));
    ordkl := flatten for k from 0 to 2 list for l from 0 to 2 list (if k=!=l then (k,l) else continue);
    rowsPerSheet := 6*nm;
    ridx := (Ji,k,l,m) -> Ji*rowsPerSheet + (position(ordkl, x -> x===(k,l)))*nm + umonIndex#m;
    -- columns (i, pair p, gamma monomial deg<=f on the 4 complement vars)
    cols := flatten flatten for i from 0 to 5 list for p in PAIRS list (
        compl := select(splice{0..5}, v -> not member(v,p));
        flatten for dg from 0 to f list apply(monos(dg,4), g4 -> (i,p,dg,g4,compl))
    );
    NR := 15*rowsPerSheet;
    A := mutableMatrix(kk, NR, #cols);
    for cj from 0 to #cols-1 do (
        (i,p,dg,g4,compl) := cols#cj;
        t := f - dg;
        for Ji from 0 to 14 do (
            J := SHEETS#Ji;
            if not member(p,J) then continue;
            l := position(J, x -> x===p);
            expo := new MutableList from {0,0,0};
            sgn := 1;
            ok := true;
            for idx from 0 to 3 do (
                gx := g4#idx;
                if gx==0 then continue;
                x := compl#idx;
                found := false;
                for kk2 from 0 to 2 do (
                    pr := J#kk2;
                    if x==pr#0 then (expo#kk2 = expo#kk2 + gx; found=true; break);
                    if x==pr#1 then (expo#kk2 = expo#kk2 + gx; sgn = sgn*(-1)^gx; found=true; break);
                );
                if not found then ok=false;
            );
            if not ok then continue;
            expo#l = expo#l + t;
            m := toList expo;
            if sum m != f then continue;
            for k from 0 to 2 do (
                if k==l then continue;
                ak := (J#k)#0; bk := (J#k)#1;
                if i==ak then A_(ridx(Ji,k,l,m),cj) = A_(ridx(Ji,k,l,m),cj) + sgn_kk
                else if i==bk then A_(ridx(Ji,k,l,m),cj) = A_(ridx(Ji,k,l,m),cj) - sgn_kk;
            );
        );
    );
    Am := matrix A;
    rA := rank Am;
    -- symmetric part: rows (J, {k,l} unordered, m) = ord(k,l)+ord(l,k)
    unord := {(0,1),(0,2),(1,2)};
    Sym := mutableMatrix(kk, 15*3*nm, #cols);
    rr := 0;
    for Ji from 0 to 14 do for kl in unord do for mi from 0 to nm-1 do (
        (k,l) := kl;
        r1 := ridx(Ji,k,l,umon#mi);
        r2 := ridx(Ji,l,k,umon#mi);
        for cj from 0 to #cols-1 do Sym_(rr,cj) = Am_(r1,cj) + Am_(r2,cj);
        rr = rr+1;
    );
    rS := rank matrix Sym;
    (rA, rS, rA-rS)
);

print "-- f | rank(A_f) | rank(sym) | dim D_f  (target 45/35/10, 180/125/55, 405/260/145, 720/440/280) --";
for f from 0 to 3 do (
    (rA,rS,dD) := buildAf(f);
    print("  f=" | toString f | ": " | toString rA | " | " | toString rS | " | " | toString dD)
);
print "-- DONE. Target dim D_f = 10,55,145,280. --";
