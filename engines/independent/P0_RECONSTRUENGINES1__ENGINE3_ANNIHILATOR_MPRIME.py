"""
P0_RECONSTRUENGINES1
ENGINE 3 (M') - faithful rebuild of Bisel's SLOT-SCALAR syzygy semantics.

CORRECT structure (read from Bisel cpp lines 216-276):
  - Codomain is SCALAR slots: N3 has 45 = 15 sheets x 3 pair-slots k;
    M' has 90 = 15 x 2 blocks x 3 pair-slots k.
  - A "column" is a MODULE GENERATOR: a polynomial-vector over the slots.
    * variable columns Y_m / X carry the frame/s_idx as SCALAR entries per slot
      (gamma_{m,k} = (l_m|_J)_k ; for X, single-slot eps).
    * relation columns: per slot s, generators s_a + s_b of I_J living IN that slot
      (entries (s, x_a) and (s, x_b) with coeff 1). These impose "modulo I_J".
  - The module map Phi: S^{ncols} -> S^{nslots} sends gen j to column_j.
    M = ker(Phi) = SYZYGY module. HF over the FIRST (variable) columns only.

We compute HF of the syzygy module degree-by-degree with pure F3 linear algebra:
  In degree d, unknowns = coeff of a deg-d form on EACH column (ncols * |S_d|).
  Map sends the tuple to sum_j column_j * f_j evaluated in each slot; the slot
  values live in S (degree d+1 for linear columns, d+1 for relation columns).
  A syzygy = tuple with total slot-value 0 (exactly, in S, NOT restricted).
  Then HF_M(d) = dim{ syzygies } projected onto the variable columns
              = nullity(map) - (syzygies supported only on relation cols).
Equivalently and cleanly (what Bisel's extended kernel computes):
  HF_M(d) = nullity over variable columns of the map
              variable-tuple  |-->  (slot values)  mod (image of relation columns).
  "mod image of relation columns" per slot = "modulo I_J in that slot"
  = restrict that slot's value to sheet J and require 0.

That restriction is the SAME as before -- BUT the slot values are now SCALAR-carried
(gamma_{m,k}), so the map is different and smaller. Let's build it faithfully.

Signed: P0_reconstruengines1
"""
import itertools
import numpy as np
from math import comb

P=3; NV=6
def monomials(deg,nv=NV):
    if nv==1: yield (deg,); return
    for e0 in range(deg+1):
        for rest in monomials(deg-e0,nv-1): yield (e0,)+rest
def mono_idx(deg):
    ms=list(monomials(deg)); return ms,{m:i for i,m in enumerate(ms)}
def mult(m,e): return tuple(a+b for a,b in zip(m,e))

def perfect_matchings(v):
    v=list(v)
    if not v: yield []; return
    a=v[0]
    for i in range(1,len(v)):
        b=v[i]; rest=v[1:i]+v[i+1:]
        for m in perfect_matchings(rest): yield [(a,b)]+m
SHEETS=[tuple(tuple(sorted(p)) for p in m) for m in perfect_matchings(range(6))]

FRAME=[[0,2,0,1,0,1],[1,0,0,1,1,0],[2,1,2,2,0,0]]
def restrict_coef(J,c):
    g=[0,0,0]
    for k,(a,b) in enumerate(J):
        g[k]=((c[a]-c[b])%3+3)%3
    return g

def rank_mod_p(M,p=P):
    if M.size==0: return 0
    A=(M%p).astype(np.int32).copy(); rows,cols=A.shape; r=0
    for c in range(cols):
        # find pivot at/below r in col c
        colslice=A[r:,c]
        nz=np.nonzero(colslice)[0]
        if nz.size==0: continue
        piv=r+int(nz[0])
        if piv!=r:
            tmp=A[r].copy(); A[r]=A[piv]; A[piv]=tmp
        inv=pow(int(A[r,c]),p-2,p)
        if inv!=1: A[r]=(A[r]*inv)%p
        # eliminate all other rows with nonzero in col c (vectorized)
        col=A[:,c].copy()
        col[r]=0
        mask=col!=0
        if mask.any():
            factors=col[mask][:,None]
            A[mask]=(A[mask]-factors*A[r][None,:])%p
        r+=1
        if r==rows: break
    return r
def nullity(M,ncols):
    if M.shape[0]==0: return ncols
    return ncols - rank_mod_p(M)

# monomials times a variable: x_i * mono
def var_mul(mono,i):
    m=list(mono); m[i]+=1; return tuple(m)

"""
Slot-scalar syzygy, degree d.  Columns:
  VARIABLE columns (ncomp of them): each has, per slot s, a SCALAR coeff c_{col,s}.
     A deg-d form f_col contributes, in slot s, the poly  c_{col,s} * f_col
     (degree d).  [scalar * form]
  RELATION columns: for slot s=(...), pair (a,b) of its sheet, a column that in slot
     s carries the linear form (x_a + x_b).  A deg-d form g contributes in slot s the
     poly (x_a+x_b)*g  (degree d+1).

Total slot value in slot s (a polynomial):
     sum_col c_{col,s} * f_col      [these are degree d]
   + sum_{relation cols at s} (x_a+x_b) * g_rel   [degree d+1]
A SYZYGY: total slot value == 0 in S, for every slot.

Problem: variable contributions are degree d, relation contributions degree d+1.
They can only cancel within the same graded piece. So actually the map target per
slot is graded; equate each degree separately. Variable part (deg d) must cancel
among variable columns alone (scalars can't change degree). Relation part (deg d+1)
cancels among relation columns alone. => the two decouple, giving:
   HF_M(d) = nullity(scalar variable-map in degree d)  [target: slot-space (deg d)]
             where the RELATION columns only matter to say the scalar map is taken
             MODULO I_J per slot in the appropriate degree.
The clean reading Bisel uses: variable slot-value (deg d) must lie in I_J per slot
(so it's killable by relation columns). "lies in I_J in slot (J,k)" = restrict the
slot-value form to sheet J and require 0.

So: unknowns = ncomp * |S_d|. For each slot s=(J,blk,k): value = sum_col c_{col,s}*f_col
(a deg-d form). Restrict to sheet J -> require 0 (all 3-var monomials of degree d).
This is a proper, SMALL linear system. Build it.
"""
def sheet_var_map(J):
    d={}
    for k,(a,b) in enumerate(J):
        d[a]=(k,+1); d[b]=(k,-1)
    return d
def restrict_mono(mono6,J):
    svm=sheet_var_map(J); exps=[0,0,0]; sign=1
    for v in range(NV):
        p=mono6[v]
        if p==0: continue
        k,s=svm[v]; exps[k]+=p
        if s==-1 and p%2==1: sign=-sign
    return (exps[0],exps[1],exps[2]), sign%P

def mono3(d):
    res=[]
    for e0 in range(d+1):
        for e1 in range(d-e0+1):
            res.append((e0,e1,d-e0-e1))
    return res

# ---- dim E ----
def elem_sym_all(k):
    d={}
    for combo in itertools.combinations(range(NV),k):
        e=[0]*NV
        for v in combo: e[v]+=1
        d[tuple(e)]=1
    return d
def poly_mul_mono(poly,mono): return {mult(m,mono):c for m,c in poly.items()}
def HF_R(d):
    msd,idx=mono_idx(d); N=len(msd); vecs=[]
    for gk in (1,3,5):
        if gk>d: continue
        g=elem_sym_all(gk)
        for mm in monomials(d-gk):
            v=np.zeros(N,dtype=np.int64)
            for mono,c in poly_mul_mono(g,mm).items():
                v[idx[mono]]=(v[idx[mono]]+c)%P
            vecs.append(v)
    if not vecs: return N
    return N-rank_mod_p(np.array(vecs,dtype=np.int64)%P)
def dimE(d):
    msd,_=mono_idx(d); return len(msd)-HF_R(d)

# ---- N3: variable columns = 3 (Y1,Y2,Y3), scalar coeff gamma_{m,k} per slot (J,k) ----
def build_N3(d):
    ms_d,idx_d=mono_idx(d); L=len(ms_d); ncomp=3; Ncol=ncomp*L
    # slot list (J,k). value in slot = sum_m gamma_{m,k}(J) * f_{Y_m}
    # restrict value to sheet J -> equations over mono3(d)
    gam=[[restrict_coef(J,FRAME[m]) for m in range(3)] for J in SHEETS]
    # restriction of each S_d monomial per sheet
    rc=[{mono6:restrict_mono(mono6,J) for mono6 in ms_d} for J in SHEETS]
    row_index={}
    for Ji in range(15):
        for k in range(3):
            for mm in mono3(d): row_index[(Ji,k,mm)]=len(row_index)
    A=np.zeros((len(row_index),Ncol),dtype=np.int64)
    for mono6,jj in idx_d.items():
        for Ji in range(15):
            b3,bs=rc[Ji][mono6]  # restricted monomial (deg d) + sign
            for m in range(3):
                col=m*L+jj
                for k in range(3):
                    g=gam[Ji][m][k]%3
                    if not g: continue
                    r=row_index.get((Ji,k,b3))
                    if r is None: continue
                    A[r,col]=(A[r,col]+bs*g)%P
    return nullity(A,Ncol)
def HF_N3(d):
    if d<0: return 0
    return build_N3(d)

# ---- M': variable columns = 7 (X, Y1..3 blk1, Z1..3 blk2), slots (J,blk,k) ----
def s_single_slot(J,idx):
    for k,(a,b) in enumerate(J):
        if idx==a: return k,1
        if idx==b: return k,2
    return None,0
def build_Mprime(d):
    ms_d,idx_d=mono_idx(d); L=len(ms_d); ncomp=7; Ncol=ncomp*L
    Xoff=0; Yoff=[1*L,2*L,3*L]; Zoff=[4*L,5*L,6*L]
    gam=[[restrict_coef(J,FRAME[m]) for m in range(3)] for J in SHEETS]
    Xdata=[[s_single_slot(J,1), s_single_slot(J,2)] for J in SHEETS]
    rc=[{mono6:restrict_mono(mono6,J) for mono6 in ms_d} for J in SHEETS]
    row_index={}
    for Ji in range(15):
        for blk in (1,2):
            for k in range(3):
                for mm in mono3(d): row_index[(Ji,blk,k,mm)]=len(row_index)
    A=np.zeros((len(row_index),Ncol),dtype=np.int64)
    for mono6,jj in idx_d.items():
        for Ji in range(15):
            b3,bs=rc[Ji][mono6]
            for blk,W_off in ((1,Yoff),(2,Zoff)):
                # X: single slot k*, scalar eps
                kstar,eps=Xdata[Ji][blk-1]
                if eps:
                    r=row_index.get((Ji,blk,kstar,b3))
                    if r is not None:
                        A[r,Xoff+jj]=(A[r,Xoff+jj]+bs*eps)%P
                # Y/Z: -(gamma_{m,k}) scalar at slot (J,blk,k)
                for m in range(3):
                    col=W_off[m]+jj
                    for k in range(3):
                        g=gam[Ji][m][k]%3
                        if not g: continue
                        r=row_index.get((Ji,blk,k,b3))
                        if r is None: continue
                        A[r,col]=(A[r,col]-bs*g)%P
    return nullity(A,Ncol)
def HF_Mprime(d):
    if d<0: return 0
    return build_Mprime(d)

import sys
CMIN=int(sys.argv[1]) if len(sys.argv)>1 else 0
CMAX=int(sys.argv[2]) if len(sys.argv)>2 else 8
tgtHM=[0,7,42,154,427,994,2059,3874,6754]
tgtHN=[0,3,18,66,183,426,876,1641,2856]
print("ENGINE 3 (M') — slot-scalar syzygy rebuild")
print("c | HF_M' | HF_N3 | dimE | ann_c | target")
allpass=True
for c in range(CMIN,CMAX+1):
    hm=HF_Mprime(c); hn=HF_N3(c); de=dimE(c)
    a=hm-2*hn-de
    t=15*comb(c-4,2) if c>=6 else 0
    ok=(a==t); allpass&=ok
    flag=""
    if c<=8:
        flag=f"  [HM {hm} vs {tgtHM[c]} {'ok' if hm==tgtHM[c] else 'X'} | HN {hn} vs {tgtHN[c]} {'ok' if hn==tgtHN[c] else 'X'}]"
    print(f"{c} | {hm} | {hn} | {de} | {a} | (tgt {t}) {'PASS' if ok else 'FAIL'}{flag}")
print("VERDICT:", "REPRODUCED" if allpass else "DISCREPANCY")
