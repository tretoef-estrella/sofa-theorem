// ============================================================================
// P2'-b MAIN BODY ENGINE (Bisel) - dual annihilator certification, q-free.
// ann_c = HF_{M'}(c) - 2*HF_{N3}(c) - dimE(c);  TARGET ann_c = 15*C(c-4,2).
// Pipeline: extended-module elimination kernel (validated in P2'-a), no pair
// skipping, kernel-side Hilbert read. Gates: v=2 dual anchors at c=0..8.
// Portable headers only (Ley 38). Single thread. Deterministic.
// ============================================================================
#include <cstdio>
#include <cstdint>
#include <vector>
#include <map>
#include <queue>
#include <algorithm>
#include <array>
#include <set>
#include <cstdlib>
using namespace std;

typedef array<uint8_t,6> Mono;
static inline int mdeg(const Mono&m){int s=0;for(int i=0;i<6;i++)s+=m[i];return s;}
static inline Mono mmul(const Mono&a,const Mono&b){Mono r;for(int i=0;i<6;i++)r[i]=a[i]+b[i];return r;}
static inline bool mdiv(const Mono&a,const Mono&b){for(int i=0;i<6;i++)if(a[i]<b[i])return false;return true;}
static inline Mono msub(const Mono&a,const Mono&b){Mono r;for(int i=0;i<6;i++)r[i]=a[i]-b[i];return r;}
static inline Mono mlcm(const Mono&a,const Mono&b){Mono r;for(int i=0;i<6;i++)r[i]=max(a[i],b[i]);return r;}

struct Term{int pos;Mono m;};
// order params (set per pipeline stage)
static int G_NY=0;           // elimination: y-block positions < G_NY are LARGER
static bool G_elim=false;    // true: extended stage (block first); false: POT stage
static inline bool termLess(const Term&A,const Term&B){ // strict: A < B  (max = lead)
    if(G_elim){
        int ba=(A.pos<G_NY)?1:0, bb=(B.pos<G_NY)?1:0;
        if(ba!=bb)return ba<bb;
        int da=mdeg(A.m), db=mdeg(B.m);
        if(da!=db)return da<db;
        for(int i=0;i<6;i++)if(A.m[i]!=B.m[i])return A.m[i]<B.m[i];
        return A.pos>B.pos;
    }else{
        if(A.pos!=B.pos)return A.pos>B.pos;      // smaller pos = larger term
        int da=mdeg(A.m), db=mdeg(B.m);
        if(da!=db)return da<db;
        for(int i=0;i<6;i++)if(A.m[i]!=B.m[i])return A.m[i]<B.m[i];
        return false;
    }
}
struct TermCmpDesc{bool operator()(const Term&A,const Term&B)const{return termLess(B,A);}}; // map: begin()=lead
typedef map<Term,int,TermCmpDesc> Poly;   // coef in {1,2}

static void addInto(Poly&f,const Poly&g,int c,const Mono&sh){ // f += c * x^sh * g
    c%=3; if(c<0)c+=3; if(!c)return;
    for(auto&kv:g){
        Term t{kv.first.pos, mmul(kv.first.m,sh)};
        auto it=f.find(t);
        int v=((it==f.end())?0:it->second)+c*kv.second;
        v%=3;
        if(it==f.end()){ if(v) f.emplace(t,v);}
        else{ if(v) it->second=v; else f.erase(it);}
    }
}
struct GB{
    vector<Poly> basis; vector<Term> leads;
    vector<vector<pair<Mono,int>>> bypos; // per position: (leadmono, idx)
    priority_queue<tuple<int,int,int>,vector<tuple<int,int,int>>,greater<>> H;
    void init(int npos){bypos.assign(npos,{});}
    Poly NF(Poly f){
        Poly rem;
        while(!f.empty()){
            auto lt=f.begin(); Term t=lt->first; int c=lt->second;
            int red=-1;
            for(auto&pr:bypos[t.pos]) if(mdiv(t.m,pr.first)){red=pr.second;break;}
            if(red<0){ rem.emplace(t,c); f.erase(lt); }
            else{
                const Poly&g=basis[red]; Term gl=leads[red];
                int gc=g.begin()->second; int inv=(gc==1)?1:2;
                int co=(3-(c*inv)%3)%3;
                addInto(f,g,co,msub(t.m,gl.m));
            }
        }
        return rem;
    }
    void install(Poly r){
        basis.push_back(move(r));
        int k=(int)basis.size()-1;
        Term L=basis[k].begin()->first; leads.push_back(L);
        for(int i=0;i<k;i++) if(leads[i].pos==L.pos)
            H.emplace(mdeg(mlcm(leads[i].m,L.m)),i,k);
        bypos[L.pos].push_back({L.m,k});
    }
    bool complete(long cap){
        long proc=0;
        while(!H.empty()&&proc<cap){
            auto[d,i,j]=H.top();H.pop();proc++;
            Mono L=mlcm(leads[i].m,leads[j].m);
            int ci=basis[i].begin()->second, cj=basis[j].begin()->second;
            Poly S;
            addInto(S,basis[i],cj,msub(L,leads[i].m));
            addInto(S,basis[j],(3-ci)%3,msub(L,leads[j].m));
            Poly r=NF(move(S));
            if(!r.empty()) install(move(r));
        }
        printf("    pairs=%ld basis=%zu %s\n",proc,basis.size(),H.empty()?"COMPLETE":"CAP-HIT");
        return H.empty();
    }
};
// combinatorics
static long long C2(long long n){return n<2?0:n*(n-1)/2;}
static long long C5(long long n){ if(n<5)return 0; long long r=1; for(int i=0;i<5;i++)r=r*(n-i)/(i+1); return r;} // C(n,5)
static long long CB(long long n,int k){ if(n<k||n<0)return 0; long long r=1; for(int i=0;i<k;i++)r=r*(n-i)/(i+1); return r;}
static long long HFS(long long e){return CB(e+5,5);}
static long long dimE(long long e){
    static const int h[7]={1,2,3,3,3,2,1};
    long long s=0; for(int j=0;j<7;j++) if(e-j>=0) s+=h[j]*CB(e-j+2,2);
    return HFS(e)-s;
}
// matchings of K6
static vector<vector<pair<int,int>>> M15;
static void gen_match(vector<int> el, vector<pair<int,int>> cur){
    if(el.empty()){M15.push_back(cur);return;}
    int a=el[0];
    for(size_t t=1;t<el.size();t++){
        int j=el[t]; vector<int> rest;
        for(size_t s=1;s<el.size();s++) if(el[s]!=j) rest.push_back(el[s]);
        auto c2=cur; c2.push_back({a,j});
        gen_match(rest,c2);
    }
}
static const int FRAME[3][6]={{0,2,0,1,0,1},{1,0,0,1,1,0},{2,1,2,2,0,0}};
// per sheet: sorted pairs; restriction coeff of linear form c: gamma_k = c[a]-c[b]
struct Sheet{ array<pair<int,int>,3> prs; };
static vector<Sheet> SHEETS;
static array<int,3> restrict_coef(const Sheet&sh,const int*c){
    array<int,3> g;
    for(int k=0;k<3;k++){ int a=sh.prs[k].first,b=sh.prs[k].second; g[k]=((c[a]-c[b])%3+3)%3; }
    return g;
}
// generic kernel pipeline: returns Hilbert numerator (kernel read done by caller)
struct PipeOut{ vector<long long> NUMq; int nvars; };
static vector<long long> HS_num(vector<Mono> gs){
    sort(gs.begin(),gs.end(),[](const Mono&a,const Mono&b){return mdeg(a)<mdeg(b);});
    vector<Mono> mini;
    for(auto&g:gs){bool red=false;for(auto&h:mini)if(mdiv(g,h)){red=true;break;} if(!red)mini.push_back(g);}
    gs=mini;
    if(gs.empty())return {1};
    if(gs.size()==1){vector<long long> n(mdeg(gs[0])+1,0);n[0]=1;n[mdeg(gs[0])]-=1;return n;}
    Mono m=gs.back(); vector<Mono> J(gs.begin(),gs.end()-1), colon;
    for(auto&g:J){Mono r;for(int i=0;i<6;i++)r[i]=(uint8_t)max(0,(int)g[i]-(int)m[i]);colon.push_back(r);}
    auto A=HS_num(J), B=HS_num(colon);
    vector<long long> out(max(A.size(),B.size()+mdeg(m)),0);
    for(size_t i=0;i<A.size();i++)out[i]+=A[i];
    for(size_t i=0;i<B.size();i++)out[i+mdeg(m)]-=B[i];
    while(!out.empty()&&out.back()==0)out.pop_back();
    return out;
}
static PipeOut pipeline(int nvars,int nslots,const vector<Poly>&cols,const char*label){
    printf("  [%s] cols=%zu slots=%d\n",label,cols.size(),nslots);
    // extended stage
    G_NY=nslots; G_elim=true;
    int NC=(int)cols.size();
    GB E1; E1.init(nslots+NC);
    for(int j=0;j<NC;j++){
        Poly g=cols[j];
        Mono z{}; g.emplace(Term{nslots+j,z},1);
        Poly r=E1.NF(move(g));
        if(!r.empty())E1.install(move(r));
    }
    if(!E1.complete(3000000)){printf("ABORT ext\n");exit(1);}
    // kernel gens: zero-y elements, project z-coords 0..nvars-1; graded split
    vector<Poly> K;
    for(auto&g:E1.basis){
        bool zeroy=true;
        for(auto&kv:g) if(kv.first.pos<nslots){zeroy=false;break;}
        if(!zeroy)continue;
        map<int,Poly> byd;
        for(auto&kv:g){
            int p=kv.first.pos-nslots;
            if(p>=0&&p<nvars) byd[mdeg(kv.first.m)].emplace(Term{p,kv.first.m},kv.second);
        }
        for(auto&pr:byd) if(!pr.second.empty()) K.push_back(pr.second);
    }
    printf("    kernel gens (graded pieces)=%zu\n",K.size());
    // stage B: GB of kernel in S^nvars (POT)
    G_elim=false;
    GB B2; B2.init(nvars);
    // NOTE: Poly maps carry comparator state via G_elim at use time; rebuild terms into fresh maps
    for(auto&g:K){
        Poly h;
        for(auto&kv:g)h.emplace(kv.first,kv.second);
        Poly r=B2.NF(move(h));
        if(!r.empty())B2.install(move(r));
    }
    if(!B2.complete(3000000)){printf("ABORT B\n");exit(1);}
    int maxld=0;
    vector<long long> NUM(1,0);
    for(int p=0;p<nvars;p++){
        vector<Mono> gs;
        for(auto&L:B2.leads) if(L.pos==p){gs.push_back(L.m); maxld=max(maxld,mdeg(L.m));}
        auto n=HS_num(gs);
        if(n.size()>NUM.size())NUM.resize(n.size(),0);
        for(size_t i=0;i<n.size();i++)NUM[i]+=n[i];
    }
    printf("    max lead deg=%d, series width=%zu\n",maxld,NUM.size());
    return {NUM,nvars};
}
static long long HFker(const PipeOut&P,long long e){
    long long v=P.nvars*HFS(e);
    for(size_t i=0;i<P.NUMq.size();i++) if(e>=(long long)i) v-=P.NUMq[i]*HFS(e-(long long)i);
    return v;
}
int main(){
    setvbuf(stdout,NULL,_IONBF,0);
    gen_match({0,1,2,3,4,5},{});
    for(auto&J:M15){Sheet s;for(int k=0;k<3;k++){int a=J[k].first,b=J[k].second;if(a>b)swap(a,b);s.prs[k]={a,b};}SHEETS.push_back(s);}
    printf("sheets=%zu (expect 15)\n",SHEETS.size());
    Mono Z{}; 
    auto um=[&](int i){Mono m{};m[i]=1;return m;};
    // ---------------- N3: slots (J,k): sum_m gamma_{m,k} Y_m|_J = 0 ----------------
    {
        vector<Poly> cols;
        int nsl=45;
        // variable columns Y_m
        for(int m=0;m<3;m++){
            Poly e;
            for(int Ji=0;Ji<15;Ji++){
                auto g=restrict_coef(SHEETS[Ji],FRAME[m]);
                for(int k=0;k<3;k++){int v=g[k]%3; if(v)e.emplace(Term{Ji*3+k,Z},v);}
            }
            cols.push_back(e);
        }
        // relation columns: I_J generators per slot
        for(int Ji=0;Ji<15;Ji++)for(int k=0;k<3;k++){
            int s=Ji*3+k;
            for(int kk=0;kk<3;kk++){
                auto[a,b]=SHEETS[Ji].prs[kk];
                Poly e; e.emplace(Term{s,um(a)},1); e.emplace(Term{s,um(b)},1);
                cols.push_back(e);
            }
        }
        G_NY=nsl;G_elim=true;
        static PipeOut P_N3=pipeline(3,nsl,cols,"N3 frame-syzygies");
        // ---------------- M': slots (J, blk in{1,2}, k) ----------------
        vector<Poly> cols2;
        int nsl2=90;
        auto slot=[&](int Ji,int blk,int k){return Ji*6+(blk-1)*3+k;};
        auto s_rest=[&](int Ji,int idx,int&eps,int&kk){
            for(int k=0;k<3;k++){auto[a,b]=SHEETS[Ji].prs[k];
                if(idx==a){eps=1;kk=k;return;} if(idx==b){eps=2;kk=k;return;}}
            eps=0;kk=-1;
        };
        // X column: eps*[k==k_idx] at (J,blk,k), idx = 1 for blk1, 2 for blk2
        {
            Poly e;
            for(int Ji=0;Ji<15;Ji++)for(int blk=1;blk<=2;blk++){
                int eps,kk; s_rest(Ji,blk==1?1:2,eps,kk);
                if(eps)e.emplace(Term{slot(Ji,blk,kk),Z},eps);
            }
            cols2.push_back(e);
        }
        // Y_m columns (blk1), Z_m columns (blk2): value -(gamma_{m,k})
        for(int blk=1;blk<=2;blk++)for(int m=0;m<3;m++){
            Poly e;
            for(int Ji=0;Ji<15;Ji++){
                auto g=restrict_coef(SHEETS[Ji],FRAME[m]);
                for(int k=0;k<3;k++){int v=(3-g[k]%3)%3; if(v)e.emplace(Term{slot(Ji,blk,k),Z},v);}
            }
            cols2.push_back(e);
        }
        // relation columns per slot
        for(int Ji=0;Ji<15;Ji++)for(int blk=1;blk<=2;blk++)for(int k=0;k<3;k++){
            int s=slot(Ji,blk,k);
            for(int kk=0;kk<3;kk++){
                auto[a,b]=SHEETS[Ji].prs[kk];
                Poly e; e.emplace(Term{s,um(a)},1); e.emplace(Term{s,um(b)},1);
                cols2.push_back(e);
            }
        }
        static PipeOut P_M7=pipeline(7,nsl2,cols2,"M' dual annihilator");
        // ---------------- ann and gates ----------------
        auto ann=[&](long long c){return HFker(P_M7,c)-2*HFker(P_N3,c)-dimE(c);};
        long long A9tail[9]={0,0,0,0,0,0,15,45,90};
        bool gate=true;
        printf("\nGATE (v=2 dual anchors, c=0..8):\n  computed:");
        for(int c=0;c<9;c++){long long a=ann(c);printf(" %lld",a);if(a!=A9tail[c])gate=false;}
        printf("\n  control :");
        for(int c=0;c<9;c++)printf(" %lld",A9tail[c]);
        printf("  -> %s\n",gate?"PASS":"FAIL");
        if(!gate){printf("NO CERTIFICATE\n");return 1;}
        printf("consistency c=9..12 (v=2 collar values, law):");
        for(int c=9;c<=12;c++)printf(" %lld(vs %lld)",ann(c),15*C2(c-4));
        printf("\n");
        bool law=true; long long bad=-1;
        for(long long c=0;c<=120;c++){ long long t=(c>=6)?15*C2(c-4):0; if(ann(c)!=t){law=false;bad=c;break;} }
        printf("LAW ann_c = 15*C(c-4,2), c=0..120 (series widths %zu/%zu): %s\n",
               P_M7.NUMq.size(),P_N3.NUMq.size(), law?"ALL MATCH":"MISMATCH");
        if(!law){printf("first mismatch at c=%lld: ann=%lld target=%lld\n",bad,ann(bad),(bad>=6)?15*C2(bad-4):0);return 1;}
        printf("\n==========================================================================\n");
        printf("  P2'-b MAIN BODY CERTIFIED (q-free): ann_c = 15*C(c-4,2) FOR ALL c\n");
        printf("  => A_d = 15*N_q(d) for all d >= 2q+4, FOR ALL v (Gorenstein duality)\n");
        printf("  remaining: the finite collar c in [q,q+3]  (d in [2q,2q+3])\n");
        printf("==========================================================================\n");
    }
    return 0;
}
