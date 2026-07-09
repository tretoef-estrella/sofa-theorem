"""
P0_RECONSTRUENGINES1
ENGINE 2 - THE CENSUS (sigma_e), direct window-syzygy linear algebra over F_3 (no Groebner).
Independent rebuild from SOFA spec v1, built from scratch.
VERDICT: REPRODUCED - sigma_e = 1, 5, 25, 70; quadratic 15e^2-90e+145 fits e=4,5.
Signed: P0_reconstruengines1
"""
"""
ENGINE 2 - THE CENSUS sigma_e  (direct linear-algebra route, no Groebner)
Independent rebuild from SOFA spec v1.
Target: sigma_2,3,4,5 = 1,5,25,70 ; quadratic 15e^2-90e+145 for e>=4.

Window syzygy at degree e: tuple lambda=(l0..l5) of homogeneous deg-e forms
such that for EVERY edge {a,b} of K6:  l_a - l_b in I({a,b}),
where I({a,b}) = (s_a+s_b, eps1, eps3) with eps1,eps3 the 1st,3rd elem sym
polynomials of the OTHER four variables.

sigma_e = dim{window syzygies} - trivial( HF_S(e) + 5*dim E_e ).
"""
import itertools
import numpy as np

P = 3
NV = 6
VARS = list(range(NV))

# ---------- monomial machinery over 6 vars ----------
def monomials(deg, nv=NV):
    """all monomials of given degree as exponent tuples length nv."""
    if nv == 1:
        yield (deg,)
        return
    for e0 in range(deg + 1):
        for rest in monomials(deg - e0, nv - 1):
            yield (e0,) + rest

def mono_index(deg):
    ms = list(monomials(deg))
    return ms, {m: i for i, m in enumerate(ms)}

def mult(m, expo):
    return tuple(a + b for a, b in zip(m, expo))

# elementary symmetric of a subset of variable-indices
def elem_sym(subset, k):
    """returns dict monomial(exp tuple len6)->coeff for e_k of variables in subset."""
    res = {}
    for combo in itertools.combinations(sorted(subset), k):
        e = [0]*NV
        for v in combo:
            e[v] += 1
        res[tuple(e)] = res.get(tuple(e), 0) + 1
    return res

def linform_pair(a, b):
    """s_a + s_b as dict deg-1 mono->coeff."""
    ea = [0]*NV; ea[a] = 1
    eb = [0]*NV; eb[b] = 1
    return {tuple(ea): 1, tuple(eb): 1}

def poly_mul_mono(poly, mono):
    return {mult(m, mono): c for m, c in poly.items()}

def poly_add(dst, poly, coeff=1):
    for m, c in poly.items():
        dst[m] = (dst.get(m, 0) + coeff*c) % P

# generators of I({a,b}) : s_a+s_b (deg1), eps1(deg1), eps3(deg3) over the other 4 vars
def ideal_gens(a, b):
    others = [v for v in VARS if v not in (a, b)]
    g1 = linform_pair(a, b)                 # deg 1
    eps1 = elem_sym(others, 1)              # deg 1
    eps3 = elem_sym(others, 3)              # deg 3
    return [(1, g1), (1, eps1), (3, eps3)]  # (deg, poly)

def ideal_basis_in_degree(a, b, e):
    """spanning set of I({a,b}) in degree e as list of vectors over monomials(e)."""
    ms_e, idx_e = mono_index(e)
    vecs = []
    for gdeg, gpoly in ideal_gens(a, b):
        if gdeg > e:
            continue
        # multiply gpoly by every monomial of degree e-gdeg
        for mm in monomials(e - gdeg):
            v = np.zeros(len(ms_e), dtype=np.int64)
            pm = poly_mul_mono(gpoly, mm)
            for mono, c in pm.items():
                v[idx_e[mono]] = (v[idx_e[mono]] + c) % P
            vecs.append(v)
    if not vecs:
        return np.zeros((0, len(ms_e)), dtype=np.int64), ms_e, idx_e
    return np.array(vecs, dtype=np.int64) % P, ms_e, idx_e

# ---------- rref / rank / nullspace mod p ----------
def rref_mod_p(M, p=P):
    A = (M % p).astype(np.int64).copy()
    rows, cols = A.shape
    pivots = []
    r = 0
    for c in range(cols):
        piv = -1
        for i in range(r, rows):
            if A[i, c] % p != 0:
                piv = i; break
        if piv == -1:
            continue
        A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), p-2, p)
        A[r] = (A[r]*inv) % p
        for i in range(rows):
            if i != r and A[i, c] % p != 0:
                A[i] = (A[i] - A[i, c]*A[r]) % p
        pivots.append(c)
        r += 1
        if r == rows: break
    return A[:r], pivots

def rank_mod_p(M, p=P):
    _, piv = rref_mod_p(M, p)
    return len(piv)

def nullspace_dim(M, ncols, p=P):
    """dimension of right-nullspace of M (M has ncols columns)."""
    if M.shape[0] == 0:
        return ncols
    return ncols - rank_mod_p(M, p)

# ---------- membership constraints ----------
# We want, for form x (vector over monomials(e)), x in I({a,b})_e.
# Equivalent: x is in the row-span of ideal_basis. Encode as: for a fixed complement
# projection, the coordinates of x outside the ideal must vanish.
# Cleanest: build a linear map "reduce mod I_e" = projection onto complement, then
# constraints = (complement coords of x) = 0. We realize complement coords via rref.

def complement_projector(a, b, e):
    """Return matrix C (k x N) s.t. x in I_e  <=>  C @ x == 0, where N=#monomials(e).
       k = codim of I_e. Built from rref of ideal basis (pivot cols -> free of I;
       we need constraints that x lies in span). Use: x in rowspan(B) iff
       appending x to B doesn't increase rank. Equivalent linear constraints:
       let B have rref R with pivot set Ppiv. Any vector in rowspan is determined
       by pivot coords; the non-pivot coords are linear combos. Construct constraint
       matrix from the left-nullspace of B^T? Simpler: constraints = rows of a matrix
       whose kernel is exactly rowspan(B). That's the (right) nullspace basis of B
       arranged as constraints: C such that C x =0 iff x in rowspan(B) is NOT direct.
       Instead: x in rowspan(B) iff x is orthogonal (mod p) to left-nullspace of B^T,
       i.e. to the row-space's orthogonal complement = nullspace of B (as constraints).
       Over a field: rowspan(B) = { x : y·x=0 for all y in (rowspan B)^perp }.
       (rowspan B)^perp = nullspace of B (vectors y with B y =0)? No: nullspace of B
       is {v: Bv=0} = orthogonal complement of rowspan(B). Its basis vectors y give
       constraints y·x = 0 which hold for x in rowspan(B). And they characterize it.
    """
    B, ms_e, idx_e = ideal_basis_in_degree(a, b, e)
    N = len(ms_e)
    if B.shape[0] == 0:
        # I_e = 0 -> membership means x=0 -> constraints = identity
        return np.eye(N, dtype=np.int64), ms_e, idx_e
    # nullspace of B (right nullspace): vectors v with B v = 0
    R, piv = rref_mod_p(B)
    pivset = set(piv)
    free = [c for c in range(N) if c not in pivset]
    basis = []
    for fcol in free:
        v = np.zeros(N, dtype=np.int64)
        v[fcol] = 1
        for ri, pc in enumerate(piv):
            v[pc] = (-R[ri, fcol]) % P
        basis.append(v)
    if not basis:
        C = np.zeros((0, N), dtype=np.int64)
    else:
        C = np.array(basis, dtype=np.int64) % P
    return C, ms_e, idx_e

# ---------- E = (e1,e3,e5) needed for dim E_e ----------
def E_ideal_basis(e):
    ms_e, idx_e = mono_index(e)
    vecs = []
    for gk in (1, 3, 5):
        if gk > e:
            continue
        g = elem_sym(VARS, gk)  # e_k of all 6 vars
        for mm in monomials(e - gk):
            v = np.zeros(len(ms_e), dtype=np.int64)
            pm = poly_mul_mono(g, mm)
            for mono, c in pm.items():
                v[idx_e[mono]] = (v[idx_e[mono]] + c) % P
            vecs.append(v)
    if not vecs:
        return 0
    B = np.array(vecs, dtype=np.int64) % P
    return rank_mod_p(B)

def HF_S(e):
    return len(list(monomials(e)))

# ---------- assemble window-syzygy system ----------
EDGES = list(itertools.combinations(range(6), 2))  # 15 edges

def sigma(e):
    ms_e, idx_e = mono_index(e)
    N = len(ms_e)               # dim of one deg-e form
    total_unknowns = 6 * N      # lambda_0..lambda_5 coefficients
    # For each edge {a,b}: constraint  C_ab @ (lambda_a - lambda_b) = 0
    # Build big constraint matrix over the 6N unknowns.
    rows = []
    for (a, b) in EDGES:
        C, _, _ = complement_projector(a, b, e)  # (k x N)
        if C.shape[0] == 0:
            continue
        k = C.shape[0]
        block = np.zeros((k, total_unknowns), dtype=np.int64)
        block[:, a*N:(a+1)*N] = C % P
        block[:, b*N:(b+1)*N] = (-C) % P
        rows.append(block)
    if rows:
        Big = np.vstack(rows) % P
        sol_dim = nullspace_dim(Big, total_unknowns)
    else:
        sol_dim = total_unknowns
    dimE = E_ideal_basis(e)
    trivial = HF_S(e) + 5 * dimE
    return sol_dim - trivial, sol_dim, trivial, dimE

print("e | sigma_e | (soldim, trivial, dimE_e)")
targets = {2:1, 3:5, 4:25, 5:70}
got = {}
for e in range(2, 6):
    s, sd, tr, de = sigma(e)
    got[e] = s
    tgt = targets[e]
    print(f"{e} | {s} (tgt {tgt}) | sol={sd} triv={tr} dimE={de}")

# check quadratic 15e^2-90e+145 at e=4,5
def quad(e): return 15*e*e - 90*e + 145
print("quadratic 15e^2-90e+145: e=4 ->", quad(4), " e=5 ->", quad(5))
