# ---------- remaining rooms, run inside build.py ----------
circle=lambda x,y,R:[x-R*S/FT*FT,y-R*S,x+R*S,y+R*S]
import json as _j
A=f'{HQ}/art'
pbr('plaster','clay_plaster',tile=1.4,tint=(.75,.68,.6),nor=1.0,rough=.95)
pbr('disc',color=(.5,.2,.1),rough=.8)
pbr('arch',diffpath=f'{A}/arch.jpg',rough=.9)
pbr('persian',diffpath=f'{A}/persian.jpg',rough=1,tile=1)
pbr('kilimrug',diffpath=f'{A}/kilimrug.jpg',rough=1)
pbr('kilimfab',diffpath=f'{A}/kilimfab.jpg',rough=1,tile=.6)
pbr('ombre',diffpath=f'{A}/ombre.jpg',rough=1)
pbr('macrame',diffpath=f'{A}/macrame.jpg',rough=1)
pbr('frameart',diffpath=f'{A}/frame.jpg',rough=.7)
pbr('jali',diffpath=f'{A}/jali.jpg',rough=.55,tile=1.3)
pbr('cer',color=(.86,.85,.82),rough=.12)
pbr('chrome',color=(.82,.82,.8),metal=1,rough=.14)
pbr('mirror',color=(.92,.93,.92),metal=1,rough=.03)
pbr('towel',color=(.72,.68,.6),rough=1)
pbr('vanity',color=(.2,.11,.06),rough=.45)
pbr('vtop',color=(.8,.78,.73),rough=.15)
pbr('whiteapp',color=(.78,.78,.76),rough=.28)
pbr('blacksteel',color=(.03,.03,.03),metal=.8,rough=.3)
pbr('wstone','marble_01',tile=1.3,rough=.15,nor=.1)
pbr('sage',color=(.25,.32,.2),rough=.95,sheen=.3)
pbr('mustard',color=(.55,.34,.07),rough=.9,sheen=.3)
pbr('choc',color=(.09,.05,.03),rough=.8,sheen=.2)
pbr('blue',color=(.05,.09,.16),rough=.95,sheen=.4)
pbr('cord',color=(.72,.62,.45),rough=1)
pbr('pomA',color=(.5,.16,.06),rough=1);pbr('pomB',color=(.3,.08,.05),rough=1);pbr('pomC',color=(.78,.7,.56),rough=1)
pbr('cream',color=(.78,.72,.6),rough=.95,sheen=.4)
for a_,b_,c_ in[('Son','bed1','bed1')]:pass
FM=F+'sofas/armchair/2048px Textures/littleSofa_Material_BaseColor.png'
sofaT=fp('sofaT',F+'sofas/sofa/sofa.obj');swap_base(sofaT,f'{A}/sofa_terra.jpg')
recl=fp('recl',F+'sofas/armchair/armchair.obj');swap_base(recl,f'{A}/arm_choc.jpg')
bedM=fp('bed',F+'beds/bed2/bed1.obj',face=BEDFACE,texdir=F+'beds/bed1')
side2=fp('side2b',F+'dressers and cabinets/bedside table 2/bedsideTable2.obj',face=-90)
side1=fp('side1b',F+'dressers and cabinets/bedside table 1/bedsideTable1.obj',face=-90)
dresser=fp('dresser',F+'dressers and cabinets/dresser/dresser.obj',face=-90)
ward1=fp('ward1',F+'wardrobes/wardrobe1/wardrobe1.obj',face=-90)
ward2=fp('ward2',F+'wardrobes/wardrobe2/wardrobe2.obj',face=-90)
tbl3=fp('tbl3',F+'tables/table3/Table3.obj',face=-90)
chairS=fp('chairS',F+'chairs/chair4/chair4.obj',face=-90);swap_base(chairS,f'{A}/chair_sage.jpg')
cab1=fp('cab1',F+'Kitchen/Cabinet1/Cabinet1.obj',face=-90);cab2=fp('cab2',F+'Kitchen/Cabinet2/Cabinet2.obj',face=-90)
cabSink=fp('cabSink',F+'Kitchen/Cabinet with sink/CabinetWithSink.obj',face=-90);cabStove=fp('cabStove',F+'Kitchen/Cabinet with stove/CabinetWithStove.obj',face=-90);cabOven=fp('cabOven',F+'Kitchen/Cabinet with stove and oven/CabinetWithStoveAndOven.obj',face=-90)
cup=fp('cup',F+'Kitchen/Cupboard/Cupboard.obj',face=-90)
lamp2=fbx('lampW','CGT_Wall-Light_38_001.fbx')
def real(m,px,py,rot=0,z=0,name=None,collide=True,free=False,k=1.0,label=False):
    d=Vector(m['dim']);ob=m.copy();col.objects.link(ob);ob.hide_render=False;ob.hide_set(False);ob.scale=(k,k,k);ob.rotation_euler=(0,0,math.radians(rot));ob.location=(X(px),Y(py),z);ob['furn']=1
    sw=abs(rot)%180==90;w=(d.y if sw else d.x)*k;dd=(d.x if sw else d.y)*k;rx,ry=w/2/FT*S,dd/2/FT*S;r=[px-rx,py-ry,px+rx,py+ry]
    if collide:colliders.append((*r,name or m.name))
    if name:ITEMS.append(dict(name=name,r=r,free=not collide,label=label,dims=[round(w/FT,2),round(dd/FT,2)]))
    return ob
# 1.obj bathroom library
LIB={};LJ=_j.load(open(f'{HQ}/lib.json'))
def libload():
    if LIB:return
    b_=set(bpy.data.objects);bpy.ops.wm.obj_import(filepath='/Users/havi.tv/Downloads/1.obj',forward_axis='Y',up_axis='Z')
    for o in [o for o in bpy.data.objects if o not in b_]:
        LIB[o.name]=o;o.hide_render=True;o.hide_set(True)
def libm(key,ids,rule):
    if key in MAST:return MAST[key]
    libload();obs=[]
    for i in ids:
        for n in LJ[i]['names']:
            o=LIB.get(n)
            if not o:continue
            c=o.copy();c.data=o.data.copy();col.objects.link(c);c.hide_render=False;c.hide_set(False);obs.append(c)
    ranked=sorted(obs,key=lambda o:o.dimensions.x*o.dimensions.y*o.dimensions.z+o.dimensions.x*o.dimensions.z,reverse=True)
    for i,c in enumerate(ranked):
        mt_=rule(i,c);bm=bmesh.new();bm.from_mesh(c.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(c.data);bm.free()
        c.data.materials.clear();c.data.materials.append(MAT[mt_])
    for c in obs:bpy.context.view_layer.objects.active=c
    ob=join(obs,key);ob.data.transform(Matrix.Scale(.001,4));ob.data.update()
    if len(ob.data.polygons)>45000:
        m=ob.modifiers.new('d','DECIMATE');m.ratio=45000/len(ob.data.polygons);deselect();ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=m.name)
    norm(ob);ob.data.shade_smooth();ob.data.set_sharp_from_angle(angle=math.radians(35));ob.hide_render=True;ob.hide_set(True);MAST[key]=ob;return ob
rWC=lambda i,c:'cer' if i==0 else 'chrome'
rTowel=lambda i,c:'towel' if i==0 else 'chrome'
rWash=lambda i,c:'chrome' if max(c.dimensions)<45 else 'whiteapp'
rVan=lambda i,c:'vanity' if i==0 else ('vtop' if c.dimensions.z<70 and c.dimensions.x>400 else ('cer' if c.dimensions.x>200 else 'chrome'))
rMir=lambda i,c:'mirror' if i==0 else 'chrome'
wc=libm('wc',[130,131],rWC);vanity=libm('vanity',[72,74,75],rVan);mirrorM=libm('mirrorL',[57],rMir);towelR=libm('towelR',[102],rTowel);showerH=libm('showerH',[2],lambda i,c:'chrome');washer=libm('washer',[132],rWash);washer2=libm('washer2',[133],rWash);basket=libm('basket',[137],lambda i,c:'towel')

def book_shelf(r,rot=-90):
    w=(r[3]-r[1])/S*FT;d=(r[2]-r[0])/S*FT;x2=X(r[2]);y1=Y(r[1]);y2=Y(r[3]);m=Mesher()
    for i in range(6):
        z=.05+i*.46;m.box('walnut',x2-d,y1,z,x2,y2,z+.03)
    m.box('walnut',x2-.02,y1,0,x2,y2,2.45);m.box('walnut',x2-d,y1,0,x2,y1-.03,2.45);m.box('walnut',x2-d,y2+.03,0,x2,y2,2.45)
    C_=['rustcurt','sage','blue','mustard','cream','terra','choc'];j=0
    for sh in range(1,5):
        yy=y1-.05
        while yy-.05>y2:
            th=rnd_(.025,.06);hh=rnd_(.24,.36);m.box(C_[j%7],x2-d*.8,yy,.08+sh*.46,x2-.04,yy-th,.08+sh*.46+hh);yy-=th+.003;j+=1
            if j%11==0:yy-=rnd_(.06,.14)
    for o in m.build('shelf'):o['furn']=1
    colliders.append((*r,'Book shelf'));ITEMS.append(dict(name='Book shelf',r=list(r),free=False,label=True,dims=[round(d/FT,2),round(w/FT,2)]))
import random as _r;_r.seed(5);rnd_=lambda a,b:_r.uniform(a,b)
def poufM(r,top,side):
    R_=(r[2]-r[0])/2/S*FT;cx,cy=(X(r[0])+X(r[2]))/2,(Y(r[1])+Y(r[3]))/2
    lathe(side,[(R_*.82,0),(R_*.98,.03),(R_,.2),(R_,.31)],(cx,cy,0),name='pouf')
    lathe(top,[(R_,.31),(R_*1.02,.36),(R_*.95,.42),(R_*.5,.44),(0,.445)],(cx,cy,0),name='pouftop');colliders.append((*r,'Pouf'));ITEMS.append(dict(name='Pouf',r=list(r),free=False,label=True,dims=[round(2*R_/FT,2),round(2*R_/FT,2)]))
def wall_img(mat,x1,y1,x2,y2,z1,z2,nrm_flip=False):
    v=[(x1,y1,z1),(x2,y2,z1),(x2,y2,z2),(x1,y1,z2)];f=[(0,1,2,3)] if not nrm_flip else [(3,2,1,0)]
    me=bpy.data.meshes.new('img');me.from_pydata(v,[],f);uv=me.uv_layers.new(name='uv');us=((0,0),(1,0),(1,1),(0,1)) if not nrm_flip else ((0,1),(1,1),(1,0),(0,0))
    for li,u in zip(range(4),us):uv.data[li].uv=u
    me.materials.append(MAT[mat]);o=bpy.data.objects.new('img',me);col.objects.link(o);o['furn']=1;return o
def arch_panel(cx,y,w,h,z0,mat='arch'):
    # arched panel on a wall that faces -Y (toward the room), with a walnut rim
    n=32;R_=w/2;pts=[(cx-R_,z0),(cx+R_,z0)]+[(cx+math.cos(i/n*math.pi)*R_,z0+h-R_+math.sin(i/n*math.pi)*R_) for i in range(n+1)]
    bm=bmesh.new();vs=[bm.verts.new((p[0],y-.006,p[1])) for p in pts];f=bm.faces.new(vs);uv=bm.loops.layers.uv.new('uv')
    for l in f.loops:l[uv].uv=((l.vert.co.x-(cx-R_))/w,(l.vert.co.z-z0)/h)
    me=bpy.data.meshes.new('arch');bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('arch',me);col.objects.link(ob);me.materials.append(MAT[mat]);ob['furn']=1
    bm=bmesh.new();t=.035;uv=bm.loops.layers.uv.new('uv');a=[];c=[]
    for p in pts:
        dx=p[0]-cx;dz=p[1]-(z0+h-R_) if p[1]>z0+h-R_ else 0;k=max(.001,math.hypot(dx,dz));c.append((p[0]+dx/k*t,p[1]+dz/k*t if dz else p[1]))
    L=len(pts);o1=[bm.verts.new((p[0],y-.03,p[1])) for p in pts];o2=[bm.verts.new((p[0],y-.03,p[1])) for p in c];b2=[bm.verts.new((p[0],y,p[1])) for p in c]
    for i in range(1,L):
        j=(i+1)%L
        if i==L-1:j=0
        bm.faces.new((o1[i],o2[i],o2[j],o1[j]));bm.faces.new((o2[i],b2[i],b2[j],o2[j]))
    for f in bm.faces:
        for l in f.loops:l[uv].uv=(l.vert.co.x*1.5,l.vert.co.z*1.5)
    me=bpy.data.meshes.new('archrim');bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('archrim',me);col.objects.link(ob);me.materials.append(MAT['walnut']);ob['furn']=1
def mac_headboard(x1,x2,y,z1,z2):
    # real cord: a walnut frame, hanging strands, a wave of pom clusters and a lower fringe (photo 6)
    m=Mesher();m.box('walnut',x1,y,z1,x2,y+.04,z1+.05);m.box('walnut',x1,y,z2-.05,x2,y+.04,z2);m.box('walnut',x1,y,z1,x1+.05,y+.04,z2);m.box('walnut',x2-.05,y,z1,x2,y+.04,z2);m.box('cream',x1+.05,y+.002,z1+.05,x2-.05,y+.012,z2-.05)
    n=int((x2-x1)/.011);verts=[];faces=[]
    for i in range(n):
        x=x1+.06+(x2-x1-.12)*i/n;b_=z1+.06+_r.uniform(0,.02);t_=z2-.06;o=len(verts);dy=y+.02+_r.uniform(0,.012);verts+=[(x,dy,b_),(x+.005,dy,b_),(x+.005,dy,t_),(x,dy,t_)];faces.append((o,o+1,o+2,o+3))
    m.add('cord',verts,faces)
    for o in m.build('machead'):o['furn']=1
    g=[]
    for i in range(60):
        t=i/59;x=x1+.12+(x2-x1-.24)*t;z=(z1+z2)/2+math.sin(t*math.tau*1.5)*(z2-z1)*.14+_r.uniform(-.03,.03);ob=None
        mt=('pomA','pomB','pomC')[i%3];bpy_m=bpy.data.meshes.new('pom');bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=2,radius=_r.uniform(.025,.042));bm.to_mesh(bpy_m);bm.free();o=bpy.data.objects.new('pom',bpy_m);col.objects.link(o);o.location=(x,y+.05,z);bpy_m.materials.append(MAT[mt]);bpy_m.shade_smooth();o['furn']=1
def macr_chair(r):
    # photo 6: walnut disc base, cream seat and a curved ombre shag back
    R_=(r[2]-r[0])/2/S*FT;cx,cy=(X(r[0])+X(r[2]))/2,(Y(r[1])+Y(r[3]))/2
    lathe('walnut',[(0,.03),(R_*.98,.03),(R_,.0),(R_*.9,.0)],(cx,cy,0),name='base');lathe('cream',[(R_*.72,.38),(R_*.78,.44),(R_*.6,.48),(0,.49)],(cx,cy,0),name='seat');lathe('cream',[(R_*.7,.03),(R_*.72,.38)],(cx,cy,0),name='seatb')
    n=30;bm=bmesh.new();uv=bm.loops.layers.uv.new('uv');rows=[]
    for z,rr in((.03,R_*.95),(.76,R_*.98)):
        rows.append([bm.verts.new((cx+math.sin(a)*rr,cy+math.cos(a)*rr,z)) for a in [(-1.6+3.2*i/n) for i in range(n+1)]])
    for i in range(n):
        f=bm.faces.new((rows[0][i],rows[0][i+1],rows[1][i+1],rows[1][i]))
        for l,u in zip(f.loops,((i/n*5,0),((i+1)/n*5,0),((i+1)/n*5,1),(i/n*5,1))):l[uv].uv=u
    me=bpy.data.meshes.new('shag');bm.to_mesh(me);bm.free();o=bpy.data.objects.new('shag',me);col.objects.link(o);me.materials.append(MAT['ombre']);me.shade_smooth();o['furn']=1
    d=Mesher();d.box('walnut',cx-R_,cy+R_*.05,.03,cx-R_+.05,cy+R_*.05-.05,.78);d.box('walnut',cx+R_-.05,cy+R_*.05,.03,cx+R_,cy+R_*.05-.05,.78)
    for o in d.build('chairp'):o['furn']=1
    colliders.append((*r,'Macrame chair'));ITEMS.append(dict(name='Macrame chair',r=list(r),free=False,label=True,dims=[round(2*R_/FT,2),round(2*R_/FT,2)]))

# THEATER
M.box('plaster',X(1163),Y(1587),0,X(2040),Y(1587)-.012,H);M.box('plaster',X(1163),Y(2373)+.012,0,X(2040),Y(2373),H)
for r_ in range(6):
    for c_ in range(9):
        bm=bmesh.new();bmesh.ops.create_uvsphere(bm,u_segments=18,v_segments=12,radius=1);me=bpy.data.meshes.new('disc');bm.to_mesh(me);bm.free();o=bpy.data.objects.new('disc',me);col.objects.link(o);me.materials.append(MAT['disc']);me.shade_smooth();o.scale=(_r.uniform(.07,.11),.028,_r.uniform(.09,.125));o.location=(X(1250)+c_*.38+_r.uniform(-.03,.03),Y(1587)-.04,.8+r_*.29+_r.uniform(-.03,.03));o.rotation_euler=(_r.uniform(-.2,.2),_r.uniform(0,3),_r.uniform(-.25,.25));o['furn']=1
place(sofaT,(1468,1776,1638,2356),90,'Terracotta sofa',h=.82)
cushions((1,0),X(1638)-.34,(Y(1776)+Y(2356))/2,2.6,math.radians(90))
for i,y in enumerate((1876,2071,2261)):place(recl,(1173,y-90,1418,y+90),90,'Recliner',h=.95,label=i==0)
d=Mesher();d.box('oak',X(1660),Y(1816),.06,X(1815),Y(2316),.09);
for o in d.build('otb'):o['furn']=1
soft('terra',(X(1815)-X(1660)),(Y(1816)-Y(2316)),.26,((X(1660)+X(1815))/2,(Y(1816)+Y(2316))/2,.22));colliders.append((1660,1816,1815,2316,'Ottoman'));ITEMS.append(dict(name='Ottoman',r=[1660,1816,1815,2316],free=False,label=True,dims=[2.56,8.26]))
place(tbl3,(1956,1798,2040,2281),-90,'TV unit',h=.55)
d=Mesher();d.box('blackstone',X(2040)-.05,Y(1860),.72,X(2040)-.02,Y(2220),1.68)
for o in d.build('ttv'):o['furn']=1
real(lamp2,1250,1600,0,z=1.5,name=None,collide=False)
# MASTER
arch_panel((X(1428)+X(1805))/2,Y(2836)-.012,1.75,2.3,.28)
place(bedM,(1428,2838,1805,3243),0,'Bed',h=.95,label=True)
for x,mt in((-.5,'mustard'),(.5,'rustcurt')):pillow(mt,.5,.14,((X(1428)+X(1805))/2+x*.7,Y(2838)-.48,.7),rx=-1.1)
place(side2,(1300,2836,1428,2940),0,'Bedside table');place(side2,(1805,2836,1933,2940),0,'Bedside table')
real(lamp,1364,2885,0,z=.62,collide=False);real(lamp,1869,2885,0,z=.62,collide=False)
rug('persian',(1280,3090,1960,3530))
place(chairS,(2062,3352,2245,3534),-135,'Spindle armchair',uniform=True)
place(tray,(1986,3285,2096,3395),0,'Round table',uniform=True)
for i in range(3):place(ward2,(1166+i*216,3563,1166+(i+1)*216-4,3698),180,'Wardrobe',h=2.5,label=i==0)
plant(13,(1175,3270,1290,3385),h=1.35,name='Plant',potmat='pot')
# SON
d=Mesher();d.box('kilimfab',X(1303)-.0,Y(262)-.012,.9,X(1710),Y(262)-.03,1.75)
for o in d.build('kh'):o['furn']=1
place(bedM,(1303,262,1710,670),0,'Bed',h=.95,label=True)
for x,mt in((-.5,'sage'),(.5,'rustcurt')):pillow(mt,.5,.14,((X(1303)+X(1710))/2+x*.7,Y(262)-.48,.7),rx=-1.1)
place(side1,(1190,262,1303,352),0,'Bedside table');place(side1,(1710,262,1813,352),0,'Bedside table');real(lamp,1246,307,0,z=.58,collide=False)
rug('kilimrug',(1370,720,1960,1000));book_shelf((2213,479,2273,729));poufM(circle(2020,860,.95),'kilimfab','kilimfab')
for i in range(3):place(ward1,(1166+i*216,1017,1166+(i+1)*216-4,1123),180,'Wardrobe',h=2.5,label=i==0)
place(ward1,(1631,1147,1757,1262),0,'Wardrobe',h=2.5);place(ward1,(1757,1147,1883,1262),0,'Wardrobe',h=2.5)
for i in range(3):place(ward1,(1638+i*140,1432,1638+(i+1)*140,1550),180,'Wardrobe',h=2.5)
poufM(circle(1963,1225,.7),'cream','macrame')
# MASTER dressing
place(ward2,(1640,2411,1779,2525),0,'Wardrobe',h=2.5);place(ward2,(1779,2411,1918,2525),0,'Wardrobe',h=2.5);place(ward2,(1918,2411,2058,2525),0,'Wardrobe',h=2.5)
place(ward2,(1631,2698,1757,2813),180,'Wardrobe',h=2.5);place(ward2,(1757,2698,1883,2813),180,'Wardrobe',h=2.5);poufM(circle(1963,2733,.7),'cream','macrame')
real(mirrorM,1964,1149,0,z=.6,collide=False,k=.9);real(mirrorM,1964,2811,180,z=.6,collide=False,k=.9)
# DAUGHTER
mac_headboard(X(3860),X(4297),Y(1908)+.005,.85,2.05)
place(bedM,(3890,1501,4267,1908),180,'Bed',h=.95,label=True)
for x,mt in((-.5,'pomA'),(.5,'cream')):pillow(mt,.5,.14,((X(3890)+X(4267))/2+x*.7,Y(1908)+.48,.7),rx=-1.1,rz=math.pi)
place(side1,(3770,1834,3890,1908),180,'Bedside table');place(side1,(4267,1834,4387,1908),180,'Bedside table');real(lamp,3830,1871,0,z=.58,collide=False)
for i in range(2):place(ward2,(3402,1182+i*212,3523,1182+(i+1)*212),90,'Wardrobe',h=2.5,label=i==0)
place(ward2,(3402,800,3523,1162),90,'Wardrobe',h=2.5)
place(side2,(3893,1182,3954,1232),0,'Dresser',h=.8);real(mirrorM,3814,1186,0,z=.6,collide=False,k=.85)
poufM(circle(3814,1251,.7),'cream','macrame');macr_chair((4280,1185,4415,1320));rug('jute',(3640,1270,4180,1490))
# GUEST
place(bedM,(5252,2740,5662,3119),-90,'Bed',h=.95,label=True)
place(side2,(5586,2640,5662,2740),-90,'Bedside table');place(side2,(5586,3119,5662,3219),-90,'Bedside table');real(lamp,5624,2690,0,z=.62,collide=False)
for i in range(3):place(ward2,(4934,2969+i*119.6,5055,2969+(i+1)*119.6),90,'Wardrobe',h=2.5,label=i==0)
place(ward2,(5308,2424,5484,2534),0,'Wardrobe',h=2.5);place(ward2,(5484,2424,5660,2534),0,'Wardrobe',h=2.5)
for i in range(2):oval(X(4934)+.03,1.5,Y(2780+i*110),.5,1.9,'birds' if i%2 else 'cane')
poufM(circle(5522,3218,.7),'cream','jute');rug('jute',(5060,2830,5340,3050))
# KITCHEN, WASH, UTILITY: your pack's cabinets, with a run of wall cupboards
for i,(mm_,nm) in enumerate(((cab1,'Cabinet'),(cabSink,'Sink cabinet'),(cab2,'Cabinet'),(cab1,'Cabinet'),(cab2,'Cabinet'))):
    y0=800+i*139.4;place(mm_,(2318,y0,2439,y0+139.4),90,nm,h=(1.1 if mm_ is cabSink else .9),label=i<2)
    place(cup,(2318,y0,2400,y0+139.4),90,'Wall cupboard',free=True,label=False);bpy.context.object if False else None
    col.objects[-1].location.z=1.5
for i,mm_ in enumerate((cab1,cabStove,cab2)):
    y0=982+i*121;place(mm_,(2595,y0,2763,y0+121),-90,'Island' if i==0 else 'Island hob',h=.9,label=i<2)
d=Mesher();d.box('steel',X(2640),Y(1120),2.25,X(2720),Y(1205),H);d.box('steel',X(2610),Y(1090),2.1,X(2750),Y(1235),2.25);d.box('steel',X(3260),Y(830),0,X(3381),Y(1040),2.0);d.box('blacksteel',X(3258),Y(832),1.25,X(3260),Y(1038),1.27);d.box('chrome',X(3253),Y(860),.9,X(3258),Y(870),1.2);d.box('wstone',X(2318),Y(800),.92,X(2320),Y(1497),1.5)
for o in d.build('kitx'):o['furn']=1
colliders.append((3260,830,3381,1040,'Fridge'));ITEMS.append(dict(name='Fridge',r=[3260,830,3381,1040],free=False,label=True,dims=[2.0,3.47]))
place(ward1,(3260,1040,3381,1165),-90,'Pantry',h=2.4);place(ward1,(3260,1165,3381,1290),-90,'Pantry',h=2.4)
for i,mm_ in enumerate((cab1,cab2,cabSink)):
    x0=2438+i*112.7;place(mm_,(x0,252,x0+112.7,372),0,'Wash cabinet',h=(1.1 if mm_ is cabSink else .9),label=i==0)
for i,mm_ in enumerate((cab1,cabStove,cab2)):
    y0=252+i*167.7;place(mm_,(2318,y0,2438,y0+167.7),90,'Wash cabinet',h=.9)
real(washer,3660,690,180,name='Washing machine',k=1.0,label=True);real(washer2,3850,690,180,name='Washing machine',k=1.0);real(basket,4010,700,180,name='Laundry basket',k=.9)
# PASSAGE
real(vanity,2108,1980,-90,z=.45,name='Basin counter',k=1.0,label=True);real(mirrorM,2066,1980,-90,z=1.08,collide=False,k=1.0)
# BATHS: toilet, vanity, mirror, shower and towels from 1.obj
def bathset(wcxy,wcrot,vanxy,vanrot,mirxy,showxy,showrot,towxy,towrot):
    real(wc,*wcxy,wcrot,z=.38,name='Wall-hung toilet',label=False);real(vanity,*vanxy,vanrot,z=.45,name='Vanity',k=.8,label=False);real(mirrorM,*mirxy,vanrot,z=1.05,collide=False,k=.75);real(showerH,*showxy,showrot,z=0,collide=False,k=1);real(towelR,*towxy,towrot,z=1.0,collide=False,k=.8)
bathset((1475,1190),0,(1490,1520),180,(1490,1545),(1200,1500),180,(1590,1300),-90);M.box('steel',X(1408)-.012,Y(1420),0,X(1408)+.012,Y(1420)-.05,2.3);GLASS.box('glass',X(1408)-.004,Y(1144),0,X(1408)+.004,Y(1420),2.3)
bathset((1475,2775),180,(1490,2440),0,(1490,2414),(1200,2455),0,(1590,2640),-90);M.box('steel',X(1408)-.012,Y(2540),0,X(1408)+.012,Y(2540)+.05,2.3);GLASS.box('glass',X(1408)-.004,Y(2540),0,X(1408)+.004,Y(2815),2.3)
bathset((3950,815),0,(3635,840),0,(3635,806),(4040,1100),180,(4055,990),-90);colliders.append((3960,1000,4066,1162,'Shower'))
bathset((5345,1985),0,(5205,2120),90,(5158,2120),(5450,2340),180,(5470,2170),-90)
# TEMPLE
m_=Mesher();x1,x2,y1,y2=X(3410),X(3722),Y(2257),Y(2372);m_.box('wstone',x1,y1,0,x2,y2,.72);m_.box('teak',x1,y2+.06,.72,x2,y2,2.45);m_.box('jali',x1+.1,y2+.07,.8,x2-.1,y2+.06,2.3);m_.box('teak',x1-.02,y1+.02,2.25,x2+.02,y2,2.45)
for xx in(x1,x2-.09):m_.box('teak',xx,y1,.72,xx+.09,y1-.09,2.25)
for o in m_.build('mandir'):o['furn']=1
cxm=(x1+x2)/2;lathe('brass',[(0,0),(.11,.0),(.13,.03),(.06,.08),(.1,.18),(.14,.27),(.1,.36),(.04,.4),(.07,.45),(0,.5)],(cxm,(y1+y2)/2,.72),name='kalash')
for xx in(-.5,.5):lathe('brass',[(0,.0),(.06,.0),(.075,.025),(.05,.04),(0,.03)],(cxm+xx,y1-.1,.72),name='diya')
for i in range(7):lathe('brass',[(0,.1),(.03,.08),(.055,.0),(.06,-.01),(0,-.01)],(x1+.15+i*(x2-x1-.3)/6,y1+.0,2.14),name='bell')
colliders.append((3410,2257,3722,2372,'Mandir'));ITEMS.append(dict(name='Mandir',r=[3410,2257,3722,2372],free=False,label=True,dims=[5.16,1.9]))
# FOYER
place(dresser,(4369,2054,4499,2271),90,'Console',h=.82);real(lamp,4434,2162,0,z=.82,collide=False)
wall_img('frameart',X(4369)+.01,Y(2240),X(4369)+.01,Y(2085),1.15,1.9,nrm_flip=False)
plant(14,(4380,1960,4470,2050),h=.9,name='Planter',potmat='brass');plant(15,(4380,2277,4470,2367),h=.9,name='Planter',potmat='brass')
for i in range(3):place(ward2,(4972,1953+i*139.7,5127,1953+(i+1)*139.7),-90,'Shoe cabinet',h=2.4,label=i==0)
# DINING art and carved screen, photo 3
d=Mesher();d.box('blackstone',X(2689),Y(1902),.765,X(2992),Y(2205),.79)
for o in d.build('dtop'):o['furn']=1
wall_img('frameart',X(3381)-.012,Y(1620),X(3381)-.012,Y(1720),1.0,2.0,nrm_flip=True) if False else None
# BALCONY jhula (photo 4), an addition: not on the plan
cx,cy=(X(3870)+X(4470))/2,(Y(3760)+Y(3900))/2;Wj=(X(4470)-X(3870));Dj=(Y(3760)-Y(3900));jm=Mesher();zs=.42
jm.box('teak',cx-Wj/2,cy-Dj/2,zs,cx+Wj/2,cy+Dj/2,zs+.05);jm.box('teak',cx-Wj/2+.05,cy+Dj/2-.03,zs+.5,cx+Wj/2-.05,cy+Dj/2,zs+.56)
for xx in(-1,0,1):jm.box('teak',cx+xx*(Wj/2-.05)-.025,cy+Dj/2-.03,zs,cx+xx*(Wj/2-.05)+.025,cy+Dj/2,zs+.56)
for sx in(-1,1):
    jm.box('teak',cx+sx*(Wj/2-.05)-.025,cy-Dj/2+.05,zs+.34,cx+sx*(Wj/2-.05)+.025,cy+Dj/2,zs+.39)
    for sy in(-1,1):
        jm.box('brass',cx+sx*(Wj/2-.05)-.008,cy+sy*(Dj/2-.05)-.008,zs,cx+sx*(Wj/2-.05)+.008,cy+sy*(Dj/2-.05)+.008,H)
TILE['cane']=.22
for o in jm.build('jhula'):o['furn']=1
cn=Mesher();cn.box('cane',cx-Wj/2+.06,cy+Dj/2-.015,zs+.05,cx+Wj/2-.06,cy+Dj/2-.018,zs+.5);[o.__setitem__('furn',1) for o in cn.build('jhcane')]
soft('cream',Wj-.14,Dj-.06,.11,(cx,cy,zs+.11));pillow('choc',.42,.14,(cx-.55,cy+.1,zs+.3),rx=-1.1);pillow('rustcurt',.42,.14,(cx+.55,cy+.1,zs+.3),rx=-1.1)
colliders.append((3870,3760,4470,3900,'Cane jhula'));ITEMS.append(dict(name='Cane jhula',r=[3870,3760,4470,3900],free=False,label=True,dims=[9.92,2.31]))
plant(1,(3450,3640,3570,3760),h=1.5,name='Planter');plant(4,(4770,3640,4890,3760),h=1.5,name='Planter');plant(7,(3450,3970,3570,4090),h=1.5,name='Planter');plant(9,(4770,3970,4890,4090),h=1.9,name='Planter')
plant(8,(2150,3620,2265,3735),h=1.0,name='Planter');plant(3,(820,560,930,670),h=1.0,name='Planter')
