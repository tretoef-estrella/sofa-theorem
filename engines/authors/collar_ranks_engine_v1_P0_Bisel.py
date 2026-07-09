# =============================================================================
# COLLAR RANKS ENGINE v1 — independent certificate of dim D_f = 10,55,145,280.
# D_f = Im(A_f) ∩ Antisym, the fixed q-free space bounding the collar image.
# Reproduces Theorem 4.3 of THE SOFA THEOREM. Pure F3 linear algebra.
# Portable: standard library + numpy only. Deterministic. Runs in seconds.
# GATE: the four ranks must equal 10 + 45*C(f+1,2) = 10, 55, 145, 280.
# =============================================================================
import numpy as np
from itertools import combinations
from math import comb

def matchings(el):
    if not el: yield []; return
    a=el[0]
    for j in el[1:]:
        rest=[x for x in el[1:] if x!=j]
        for m in matchings(rest): yield [(a,j)]+m
M15=[[tuple(sorted(p)) for p in J] for J in matchings(list(range(6)))]
PAIRS=[(a,b) for a in range(6) for b in range(6) if a<b]

def monos_k(d,nv):
    if nv==1: yield (d,); return
    for i in range(d+1):
        for r in monos_k(d-i,nv-1): yield (i,)+r

def rank3(M):
    if M.size==0: return 0
    M=M.astype(np.int16)%3; rows,cols=M.shape; r=0
    for c in range(cols):
        if r==rows: break
        nz=np.nonzero(M[r:,c])[0]
        if nz.size==0: continue
        p=r+int(nz[0])
        if p!=r: M[[r,p]]=M[[p,r]]
        if M[r,c]==2: M[r]=(M[r]*2)%3
        below=M[r+1:,c]; mask=below!=0
        if mask.any(): M[r+1:][mask]=(M[r+1:][mask]-np.outer(below[mask],M[r]))%3
        r+=1
    return r

# A_f : aggregate space (i, pair p, gamma on the 4 complement vars, deg<=f)
#       -> delta-ambient (sheet J, ordered (k,l), monomial of degree f in u1,u2,u3)
# then D_f = Im(A_f) ∩ Antisym; dim = rank(A_f) - rank(Sym∘A_f).
def compute_Df(f):
    monf=list(monos_k(f,3)); nm=len(monf); mi={m:i for i,m in enumerate(monf)}
    ords=[(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]
    rows_per_sheet=6*nm
    NR=15*rows_per_sheet
    def ridx(Ji,k,l,m): return Ji*rows_per_sheet+ords.index((k,l))*nm+mi[m]
    cols=[]
    for i in range(6):
        for p in PAIRS:
            compl=[x for x in range(6) if x not in p]
            for dg in range(f+1):
                for g4 in monos_k(dg,4):
                    gamma={compl[t]:g4[t] for t in range(4) if g4[t]}
                    cols.append((i,p,dg,dict(gamma)))
    A=np.zeros((NR,len(cols)),dtype=np.int16)
    for cj,(i,p,dg,gamma) in enumerate(cols):
        t=f-dg
        for Ji,J in enumerate(M15):
            if p not in J: continue
            l=J.index(p)
            expo={0:0,1:0,2:0}; sgn=1; ok=True
            for x,gx in gamma.items():
                found=False
                for kk,(a,b) in enumerate(J):
                    if x==a: expo[kk]+=gx; found=True; break
                    if x==b: expo[kk]+=gx; sgn*=(-1)**gx; found=True; break
                if not found: ok=False
            if not ok: continue
            expo[l]+=t
            m=(expo[0],expo[1],expo[2])
            if sum(m)!=f: continue
            for k in range(3):
                if k==l: continue
                a_k,b_k=J[k]
                for (slot,eps) in [(a_k,1),(b_k,-1)]:
                    if slot!=i: continue
                    A[ridx(Ji,k,l,m),cj]=(A[ridx(Ji,k,l,m),cj]+(eps*sgn))%3
    rkA=rank3(A.copy())
    # symmetric part: delta_{k,l}+delta_{l,k}
    Sym=np.zeros((15*3*nm,len(cols)),dtype=np.int16); r=0
    for Ji in range(15):
        for (k,l) in [(0,1),(0,2),(1,2)]:
            for m_i in range(nm):
                r1=Ji*6*nm+ords.index((k,l))*nm+m_i
                r2=Ji*6*nm+ords.index((l,k))*nm+m_i
                Sym[r]=(A[r1]+A[r2])%3; r+=1
    rkSym=rank3(Sym.copy())
    return rkA, rkSym, rkA-rkSym

print("COLLAR RANKS ENGINE v1 — independent certificate of Theorem 4.3")
print("="*66)
allok=True
for f in range(4):
    rkA,rkS,dD=compute_Df(f)
    tgt=10+45*comb(f+1,2)
    ok=(dD==tgt); allok&=ok
    print(f"f={f}: rank(A_f)={rkA:3d}  rank(sym)={rkS:3d}  dim D_f={dD:3d}  target {tgt:3d}  {'PASS' if ok else 'FAIL'}")
print("="*66)
print("VERDICT:", "ALL FOUR RANKS CERTIFIED — dim D_f = 10,55,145,280" if allok else "MISMATCH — CERTIFICATE FAILS")
