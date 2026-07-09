# NOTE (v4 fix): the Hilbert-series splitter returns HF(S^6/in M) (the QUOTIENT).
# The kernel M is read as HF_M = 6*HF_S - quotient. v3 compared the quotient
# directly and printed a spurious FAIL with fingerprint HF=[5,25,74,165,300,480]
# = 6*HF_S - control. This is the corrected certificate engine.
# =============================================================================
# P2'-a FINAL: kernel via EXTENDED MODULE + ELIMINATION ORDER (Bologna, take 4)
# W = <(g_j, e_j)> in S^45 (+) S^141 ; elimination order: y-block >> z-block.
# Zero-y elements of the complete GB -> their z-parts = GB of Syz(columns);
# first-6 z-coordinates -> generators of M = ker(Phi).
# GATES: (A) generators satisfy the validated edge conditions (spot degrees<=4)
#        (B) HF_M(0..5) from in(M) == 1,11,52,171,456,1032
#        (C) law check for e=4..100 (>> series width) == 15e^2-90e+145
# NO pair-skipping criteria anywhere (Ley 43).
# =============================================================================
import heapq, sys
from math import comb
NV=6
def mdeg(m): return sum(m)
def mono_mul(a,b): return tuple(x+y for x,y in zip(a,b))
def mono_div(a,b): return all(x>=y for x,y in zip(a,b))
def mono_sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mono_lcm(a,b): return tuple(max(x,y) for x,y in zip(a,b))
def scale(f,c):
    c%=3
    return {} if c==0 else {k:(v*c)%3 for k,v in f.items()}
def shift(f,mono):
    return {(p,mono_mul(m,mono)):c for (p,m),c in f.items()}
def add(f,g):
    r=dict(f)
    for k,c in g.items():
        n=(r.get(k,0)+c)%3
        if n: r[k]=n
        elif k in r: del r[k]
    return r
NY=45
def tkey(t):
    p,m=t
    blk=1 if p<NY else 0            # y-block strictly larger
    return (blk, mdeg(m), tuple(m), -p)
def lead(f): return max(f,key=tkey)

def matchings(el):
    if not el: yield []; return
    a=el[0]
    for j in el[1:]:
        rest=[x for x in el[1:] if x!=j]
        for m in matchings(rest): yield [(a,j)]+m
M15=list(matchings(list(range(6))))
SLOTS=[]
for Ji,J in enumerate(M15):
    for pr in J: SLOTS.append((Ji,tuple(sorted(pr))))
ZERO=tuple([0]*NV)
def um(i):
    m=[0]*NV; m[i]=1; return tuple(m)
cols=[]
for i in range(NV):
    e={}
    for sidx,(Ji,(a,b)) in enumerate(SLOTS):
        v=(1 if i==a else 0)-(1 if i==b else 0)
        if v%3: e[(sidx,ZERO)]=v%3
    cols.append(e)
for sidx,(Ji,pr) in enumerate(SLOTS):
    for (a,b) in M15[Ji]:
        cols.append({(sidx,um(a)):1,(sidx,um(b)):1})
NC=len(cols); assert NC==141
# extended generators: (g_j, e_j): z-block positions 45..185
GENS=[]
for j in range(NC):
    g=dict(cols[j]); g[(NY+j,ZERO)]=1
    GENS.append(g)

basis=[]; Lds=[]; bypos={}
def nf(f):
    f=dict(f); rem={}
    while f:
        t=lead(f); p,m=t
        red=-1
        for (bm,i) in bypos.get(p,()):
            if mono_div(m,bm): red=i; break
        if red<0: rem[t]=f.pop(t)
        else:
            g=basis[red]; gl=Lds[red]; c=f[t]; gc=g[gl]; inv=1 if gc==1 else 2
            f=add(f,scale(shift(g,mono_sub(m,gl[1])),(-c*inv)%3))
    return rem
H=[]
def install(r):
    basis.append(r); L=lead(r); Lds.append(L)
    bypos.setdefault(L[0],[]).append((L[1],len(basis)-1))
    k=len(basis)-1
    for i in range(k):
        if Lds[i][0]==L[0]:
            heapq.heappush(H,(mdeg(mono_lcm(Lds[i][1],L[1])),i,k))
for g in GENS:
    r=nf(g)
    if r: install(r)
proc=0; CAP=400000
while H and proc<CAP:
    d,i,j=heapq.heappop(H); proc+=1
    mi,mj=Lds[i][1],Lds[j][1]
    L=mono_lcm(mi,mj); gi,gj=basis[i],basis[j]; ci=gi[Lds[i]]; cj=gj[Lds[j]]
    S=add(scale(shift(gi,mono_sub(L,mi)),cj),scale(shift(gj,mono_sub(L,mj)),(-ci)%3))
    r=nf(S)
    if r: install(r)
if H: sys.exit(f"INCOMPLETE after {proc} pairs")
print(f"EXTENDED GB complete: basis={len(basis)}, pairs={proc}")
# zero-y elements -> M generators
Mgens=[]
for g in basis:
    if all(p>=NY for (p,m) in g):
        lam={}
        for (p,m),c in g.items():
            if NY<=p<NY+6:
                lam[(p-NY,m)]=(lam.get((p-NY,m),0)+c)%3
        lam={k:c for k,c in lam.items() if c}
        if lam: Mgens.append(lam)
print(f"zero-y GB elements -> M-generators: {len(Mgens)}; degrees: {sorted(set(mdeg(lead(g)[1]) for g in Mgens))}")

# ---- GATE A: each low-degree generator satisfies the sheet conditions Phi(lam)=0 on V(E)
def restrict_ok(lam):
    # check (lam_a-lam_b)|_{L_J}=0 for all sheets J and pairs (a,b) in J
    for J in M15:
        sub={}
        for k,(a,b) in enumerate(J):
            va=[0,0,0]; va[k]=1; sub[a]=tuple(va)
            vb=[0,0,0]; vb[k]=-1%3; sub[b]=tuple(vb)
        for (a,b) in J:
            diff={}
            for (p,m),c in lam.items():
                if p==a: diff[m]=(diff.get(m,0)+c)%3
                if p==b: diff[m]=(diff.get(m,0)-c)%3
            # restrict diff to sheet
            out={}
            for m,c in diff.items():
                if not c%3: continue
                pcur={(0,0,0):c%3}
                for i in range(6):
                    for _ in range(m[i]):
                        np_={}
                        for e2,cc in pcur.items():
                            for k2 in range(3):
                                if sub[i][k2]:
                                    ee=list(e2); ee[k2]+=1; ee=tuple(ee)
                                    np_[ee]=(np_.get(ee,0)+cc*sub[i][k2])%3
                        pcur={e2:cc for e2,cc in np_.items() if cc}
                        if not pcur: break
                    if not pcur: break
                for e2,cc in pcur.items(): out[e2]=(out.get(e2,0)+cc)%3
            if any(v%3 for v in out.values()): return False
    return True
low=[g for g in Mgens if mdeg(lead(g)[1])<=4]
gateA=all(restrict_ok(g) for g in low)
print(f"GATE A (edge conditions on {len(low)} gens of deg<=4): {'PASS' if gateA else 'FAIL'}")
if not gateA: sys.exit("GATE A FAILED")

# ---- STAGE B: GB of M in S^6 (POT, all pairs) ----
def tkeyB(t):
    p,m=t
    return (-p, mdeg(m), tuple(m))
def leadB(f): return max(f,key=tkeyB)
basisB=[]; LdsB=[]; byposB={}
def nfB(f):
    f=dict(f); rem={}
    while f:
        t=leadB(f); p,m=t
        red=-1
        for (bm,i) in byposB.get(p,()):
            if mono_div(m,bm): red=i; break
        if red<0: rem[t]=f.pop(t)
        else:
            g=basisB[red]; gl=LdsB[red]; c=f[t]; gc=g[gl]; inv=1 if gc==1 else 2
            f=add(f,scale(shift(g,mono_sub(m,gl[1])),(-c*inv)%3))
    return rem
HB=[]
def installB(r):
    basisB.append(r); L=leadB(r); LdsB.append(L)
    byposB.setdefault(L[0],[]).append((L[1],len(basisB)-1))
    k=len(basisB)-1
    for i in range(k):
        if LdsB[i][0]==L[0]:
            heapq.heappush(HB,(mdeg(mono_lcm(LdsB[i][1],L[1])),i,k))
for g in Mgens:
    r=nfB(g)
    if r: installB(r)
proc=0
while HB and proc<CAP:
    d,i,j=heapq.heappop(HB); proc+=1
    mi,mj=LdsB[i][1],LdsB[j][1]
    L=mono_lcm(mi,mj); gi,gj=basisB[i],basisB[j]; ci=gi[LdsB[i]]; cj=gj[LdsB[j]]
    S=add(scale(shift(gi,mono_sub(L,mi)),cj),scale(shift(gj,mono_sub(L,mj)),(-ci)%3))
    r=nfB(S)
    if r: installB(r)
if HB: sys.exit("STAGE B incomplete")
print(f"STAGE B GB of M complete: basis={len(basisB)}, pairs={proc}, max lead deg={max(mdeg(m) for (p,m) in LdsB)}")

# ---- Hilbert series of in(M); micro-test the splitter first ----
def HS_num(gs):
    gs=sorted(set(gs),key=mdeg); mini=[]
    for g in gs:
        if not any(mono_div(g,h) for h in mini): mini.append(g)
    gs=mini
    if not gs: return [1]
    if len(gs)==1:
        n=[0]*(mdeg(gs[0])+1); n[0]=1; n[-1]-=1; return n
    m=gs[-1]; J=gs[:-1]
    colon=[tuple(max(x-y,0) for x,y in zip(g,m)) for g in J]
    A=HS_num(J); B=HS_num(colon)
    out=[0]*max(len(A),len(B)+mdeg(m))
    for i,c in enumerate(A): out[i]+=c
    for i,c in enumerate(B): out[i+mdeg(m)]-=c
    while out and out[-1]==0: out.pop()
    return out
assert HS_num([(2,0,0,0,0,0)])==[1,0,-1], "HS microtest 1 fail"
assert HS_num([(1,0,0,0,0,0),(0,1,0,0,0,0)])==[1,-2,1], "HS microtest 2 fail"
NUM=[0]
for p in range(6):
    n=HS_num([m for (pp,m) in LdsB if pp==p])
    if len(n)>len(NUM): NUM=NUM+[0]*(len(n)-len(NUM))
    for i,c in enumerate(n): NUM[i]+=c
def HF_M(e): return 6*comb(e+5,5) - sum(NUM[i]*comb(e-i+5,5) for i in range(len(NUM)) if e-i>=0)  # KERNEL-side read: 6*HF_S - HF(S^6/inM)
control=[1,11,52,171,456,1032]
got=[HF_M(e) for e in range(6)]
print("GATE B: HF_M(0..5) =",got," control =",control," ->","PASS" if got==control else "FAIL")
if got!=control: sys.exit("GATE B FAILED - NO CERTIFICATE")
def dimE(e):
    h=[1,2,3,3,3,2,1]
    return comb(e+5,5)-sum(h[j]*comb(e-j+2,2) for j in range(7) if e-j>=0)
def sigma(e): return HF_M(e)-comb(e+5,5)-5*dimE(e)
print("sigma_e CERTIFIED, e=0..12:", [sigma(e) for e in range(13)])
bad=[e for e in range(4,101) if sigma(e)!=15*e*e-90*e+145]
print(f"GATE C: law 15e^2-90e+145 for e=4..100 (series width {len(NUM)}):","ALL MATCH — PROVEN FOR ALL e" if not bad else f"MISMATCH {bad[:6]}")
if not bad:
    print("\n"+"="*74)
    print("  P2'-a CLOSED: sigma_e = 15e^2 - 90e + 145 FOR ALL e >= 4  —  CERTIFIED")
    print("  (three gates passed: edge-conditions, control dims, full-series law)")
    print("="*74)
