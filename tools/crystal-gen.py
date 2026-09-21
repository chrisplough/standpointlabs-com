import math, random, sys
phi=(1+5**0.5)/2
V=[(sx,sy,sz) for sx in (1,-1) for sy in (1,-1) for sz in (1,-1)]
for a in (1,-1):
  for b in (1,-1):
    V+= [(0,a/phi,b*phi),(a/phi,b*phi,0),(a*phi,0,b/phi)]
N=[]
for a in (1,-1):
  for b in (1,-1):
    N+=[(0,a*phi,b),(a*phi,b,0),(a,0,b*phi)]
dot=lambda u,v: sum(x*y for x,y in zip(u,v))
def norm(v): l=math.sqrt(dot(v,v)); return tuple(x/l for x in v)
faces=[]
for n in N:
    n=norm(n); ds=sorted(range(20), key=lambda i:-dot(V[i],n))[:5]
    c=tuple(sum(V[i][k] for i in ds)/5 for k in range(3))
    u=norm(tuple(V[ds[0]][k]-c[k] for k in range(3)))
    w=norm((n[1]*u[2]-n[2]*u[1], n[2]*u[0]-n[0]*u[2], n[0]*u[1]-n[1]*u[0]))
    def ang(i):
        d=tuple(V[i][k]-c[k] for k in range(3)); return math.atan2(dot(d,w),dot(d,u))
    faces.append((n, sorted(ds,key=ang)))
def rot(v,ax,ay,az=0):
    x,y,z=v
    y,z = y*math.cos(ax)-z*math.sin(ax), y*math.sin(ax)+z*math.cos(ax)
    x,z = x*math.cos(ay)+z*math.sin(ay), -x*math.sin(ay)+z*math.cos(ay)
    x,y = x*math.cos(az)-y*math.sin(az), x*math.sin(az)+y*math.cos(az)
    return (x,y,z)
def build(AX,AY,AZ,cx,cy,s,seed,nfl=80,lit_rank=0,fleck=True):
    P=[ (lambda r:(cx+r[0]*s, cy-r[1]*s, r[2]))(rot(v,AX,AY,AZ)) for v in V]
    fs=[]
    for fi,(n,idx) in enumerate(faces):
        depth=rot(n,AX,AY,AZ)[2]
        fs.append((depth,fi," ".join("%.1f,%.1f"%(P[i][0],P[i][1]) for i in idx)))
    fs.sort()
    lit=sorted(fs,key=lambda t:-t[0])[lit_rank][1]
    parts=[]
    if fleck:
        random.seed(seed)
        for _ in range(nfl):
            while True:
                v=tuple(random.uniform(-1.3,1.3) for _ in range(3))
                if all(dot(v,norm(n))<=1.20 for n in N): break
            r=rot(v,AX,AY,AZ); x,y=cx+r[0]*s, cy-r[1]*s; a=random.uniform(0,180); L=random.uniform(0.04,0.08)*s
            parts.append('<line class="fk" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" transform="rotate(%.0f %.1f %.1f)"/>'%(x-L,y,x+L,y,a,x,y))
    for depth,fi,pts in fs:
        k="back" if depth<0 else "front"
        if fi==lit: k+=" lit"
        parts.append('<polygon class="face %s" points="%s"/>'%(k,pts))
    litpts=[P[i] for i in faces[lit][1]]
    return "".join(parts), (sum(p[0] for p in litpts)/5, sum(p[1] for p in litpts)/5)
if __name__=="__main__":
    AX,AY,AZ,rank=[float(x) for x in sys.argv[1:4]]+[int(sys.argv[4])]
    main,(cx,cy)=build(AX,AY,AZ,300,272,150,7,80,rank)
    mini,_=build(AX+0.4,AY-0.5,0.3,700,150,64,11,40,0)
    svg=f'''<svg class="crystal" viewBox="0 0 860 540" role="img" aria-label="A faceted solid; one face is highlighted as a standpoint, and that face opens into a faceted solid of its own">
<g class="s1">{main}</g>
<g class="s3"><line class="lift" x1="{cx:.0f}" y1="{cy:.0f}" x2="700" y2="150"/>{mini}<text class="lbl" x="700" y="268" text-anchor="middle">one face, seen whole</text></g>
<text class="lbl lit-lbl" x="{cx:.0f}" y="{cy+5:.0f}" text-anchor="middle">a standpoint</text>
</svg>'''
    open("crystal.svg","w").write(svg); print("ok",round(cx),round(cy))
