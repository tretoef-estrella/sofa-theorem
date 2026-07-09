"""
P0_RECONSTRUENGINES1
ENGINE 1 - COLLAR RANKS (dim D_f)
Independent rebuild from SOFA spec v1, built from scratch over F_3.
VERDICT: REPRODUCED - dim D_f = 10, 55, 145, 280.
Signed: P0_reconstruengines1
"""
"""
ENGINE 1 - COLLAR RANKS over F3
Independent rebuild from SOFA spec v1.
Target: dim D_f = 10, 55, 145, 280 for f=0,1,2,3
        rank(A_f) = 45,180,405,720 ; rS = 35,125,260,440
"""
import itertools
import numpy as np

P = 3

def rank_mod_p(M, p=P):
    """Gaussian elimination mod p, returns rank."""
    if M.size == 0:
        return 0
    A = (M % p).astype(np.int64).copy()
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        # find pivot in column c at/below row r
        piv = -1
        for i in range(r, rows):
            if A[i, c] % p != 0:
                piv = i
                break
        if piv == -1:
            continue
        A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p)  # p prime
        A[r] = (A[r] * inv) % p
        for i in range(rows):
            if i != r and A[i, c] % p != 0:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
        if r == rows:
            break
    return r

# --- the 15 perfect matchings of K6 ---
def perfect_matchings(verts):
    verts = list(verts)
    if not verts:
        yield []
        return
    a = verts[0]
    for i in range(1, len(verts)):
        b = verts[i]
        rest = verts[1:i] + verts[i+1:]
        for m in perfect_matchings(rest):
            yield [(a, b)] + m

SHEETS = [tuple(m) for m in perfect_matchings(range(6))]
assert len(SHEETS) == 15, len(SHEETS)

# For each sheet, map variable index -> (pair_index k in 0..2, sign) where sign=+1 if it's the 'a' of the pair, -1 if 'b'
def sheet_var_map(J):
    m = {}
    for k, (a, b) in enumerate(J):
        m[a] = (k, +1)   # s_a -> +u_k
        m[b] = (k, -1)   # s_b -> -u_k
    return m

# monomials of the 4 vars not in pair p, of degree <= f  (gamma)
# represented as sorted tuple of variable indices (with repetition) -> we store as exponent dict
def gammas(other_vars, fmax):
    # all monomials in other_vars (4 vars) of degree 0..fmax
    res = []
    for deg in range(fmax + 1):
        for combo in itertools.combinations_with_replacement(other_vars, deg):
            res.append(combo)  # tuple of var indices, len=deg
    return res

# monomials in u0,u1,u2 of degree exactly f -> exponent tuple (e0,e1,e2)
def u_monos(f):
    res = []
    for e0 in range(f + 1):
        for e1 in range(f - e0 + 1):
            e2 = f - e0 - e1
            res.append((e0, e1, e2))
    return res

def build_Af(f):
    pairs = list(itertools.combinations(range(6), 2))  # 15 pairs
    assert len(pairs) == 15
    pair_index = {p: idx for idx, p in enumerate(pairs)}

    # ---- columns: (i, p, gamma) ----
    columns = []
    for i in range(6):
        for p in pairs:
            other = tuple(v for v in range(6) if v not in p)
            for g in gammas(other, f):
                columns.append((i, p, g))
    col_index = {c: j for j, c in enumerate(columns)}

    # ---- rows (ordered): (J, (k,l), m) ----
    ordered_kl = [(k, l) for k in range(3) for l in range(3) if k != l]  # 6
    umon = u_monos(f)
    umon_index = {m: idx for idx, m in enumerate(umon)}

    rows_ord = []
    for Ji in range(15):
        for (k, l) in ordered_kl:
            for m in umon:
                rows_ord.append((Ji, (k, l), m))
    row_index = {r: idx for idx, r in enumerate(rows_ord)}

    A = np.zeros((len(rows_ord), len(columns)), dtype=np.int64)

    for (i, p, g), jcol in col_index.items():
        # sheets containing pair p
        for Ji, J in enumerate(SHEETS):
            if p not in J:
                continue
            l = J.index(p)  # index of pair p within J
            t = f - len(g)  # exponent on u_l  (t = f - deg(gamma))
            if t < 0:
                continue
            svm = sheet_var_map(J)
            # restrict gamma to sheet: exponent vector on (u0,u1,u2), sign
            exps = [0, 0, 0]
            sign = 1
            for x in g:
                kk, s = svm[x]
                exps[kk] += 1
                if s == -1:
                    sign = -sign
            # add t on u_l
            exps[l] += t
            m = (exps[0], exps[1], exps[2])
            if sum(m) != f:
                continue
            # for each k != l: k-th pair (a_k,b_k) of J
            for k in range(3):
                if k == l:
                    continue
                a_k, b_k = J[k]
                r = row_index.get((Ji, (k, l), m))
                if r is None:
                    continue
                if i == a_k:
                    A[r, jcol] = (A[r, jcol] + sign) % P
                elif i == b_k:
                    A[r, jcol] = (A[r, jcol] - sign) % P

    # symmetric part matrix: rows (J, {k,l} unordered, m) = ord(k,l)+ord(l,k)
    unordered_kl = [(0, 1), (0, 2), (1, 2)]
    rows_sym = []
    for Ji in range(15):
        for (k, l) in unordered_kl:
            for m in umon:
                rows_sym.append((Ji, (k, l), m))
    Asym = np.zeros((len(rows_sym), len(columns)), dtype=np.int64)
    for si, (Ji, (k, l), m) in enumerate(rows_sym):
        r1 = row_index[(Ji, (k, l), m)]
        r2 = row_index[(Ji, (l, k), m)]
        Asym[si] = (A[r1] + A[r2]) % P

    return A, Asym

print("f | rank(A_f) | rS | dim D_f")
targets_D = {0:10,1:55,2:145,3:280}
targets_rA = {0:45,1:180,2:405,3:720}
targets_rS = {0:35,1:125,2:260,3:440}
for f in range(4):
    A, Asym = build_Af(f)
    rA = rank_mod_p(A)
    rS = rank_mod_p(Asym)
    D = rA - rS
    print(f"{f} | {rA} (tgt {targets_rA[f]}) | {rS} (tgt {targets_rS[f]}) | {D} (tgt {targets_D[f]})")
