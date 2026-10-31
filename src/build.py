import bpy,bmesh,math,os,sys,glob
from mathutils import Vector,Matrix
HQ=os.path.dirname(os.path.abspath(bpy.context.space_data.text.filepath)) if False else sys.argv[sys.argv.index('--')+1]
ARGS=sys.argv[sys.argv.index('--')+2:]
F='/Users/havi.tv/Downloads/Furniture Pack OBJ/';C='/Users/havi.tv/Downloads/CGT_Free_Pack/'
FT=.3048;S=60.5;OX=1163;OY=217;H=9*FT
X=lambda p:(p-OX)/S*FT
Y=lambda p:-(p-OY)/S*FT
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene;col=sc.collection
sc.unit_settings.system='METRIC'

# ---------- materials ----------
MAT={};TILE={}
def teximg(path,cs):
    im=bpy.data.images.load(path,check_existing=True);im.colorspace_settings.name=cs;return im
def pbr(name,tex=None,tile=1.0,tint=None,rough=None,nor=1.0,metal=0.0,color=None,sheen=0.0,diffpath=None,alpha=None,emit=None,emitS=1.0,trans=0.0,norfile=None,uvs=None):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;b=n['Principled BSDF'];TILE[name]=tile
    b.inputs['Metallic'].default_value=metal
    if color is not None:b.inputs['Base Color'].default_value=(*color,1)
    if rough is not None:b.inputs['Roughness'].default_value=rough
    if sheen:b.inputs['Sheen Weight'].default_value=sheen
    if trans:b.inputs['Transmission Weight'].default_value=trans
    d=f'{HQ}/tex/{tex}' if tex else None
    dp=diffpath or (d and f'{d}/diff.jpg')
    if dp:
        t=n.new('ShaderNodeTexImage');t.image=teximg(dp,'sRGB')
        if tint:
            mx=n.new('ShaderNodeMixRGB');mx.blend_type='MULTIPLY';mx.inputs[0].default_value=1;mx.inputs[2].default_value=(*tint,1);l.new(t.outputs[0],mx.inputs[1]);l.new(mx.outputs[0],b.inputs['Base Color'])
        else:l.new(t.outputs[0],b.inputs['Base Color'])
        if alpha:l.new(t.outputs[1],b.inputs['Alpha']);m.blend_method='CLIP'
    if d and os.path.exists(f'{d}/rough.jpg') and rough is None:
        t=n.new('ShaderNodeTexImage');t.image=teximg(f'{d}/rough.jpg','Non-Color');l.new(t.outputs[0],b.inputs['Roughness'])
    if d and os.path.exists(f'{d}/nor.jpg') and nor>0:
        t=n.new('ShaderNodeTexImage');t.image=teximg(f'{d}/nor.jpg','Non-Color');nm=n.new('ShaderNodeNormalMap');nm.inputs[0].default_value=nor;l.new(t.outputs[0],nm.inputs[1]);l.new(nm.outputs[0],b.inputs['Normal'])
    if norfile:
        t=n.new('ShaderNodeTexImage');t.image=teximg(f'{HQ}/tex/{norfile}/nor.jpg','Non-Color');nm=n.new('ShaderNodeNormalMap');nm.inputs[0].default_value=.8;tc=n.new('ShaderNodeTexCoord');mp=n.new('ShaderNodeMapping');mp.inputs['Scale'].default_value=(uvs,uvs,1);l.new(tc.outputs['UV'],mp.inputs[0]);l.new(mp.outputs[0],t.inputs[0]);l.new(t.outputs[0],nm.inputs[1]);l.new(nm.outputs[0],b.inputs['Normal'])
    if emit:b.inputs['Emission Color'].default_value=(*emit,1);b.inputs['Emission Strength'].default_value=emitS
    MAT[name]=m;return m
pbr('wall',color=(.78,.74,.66),rough=.88)
pbr('ceil',color=(.86,.84,.79),rough=.9)
pbr('skirting',color=(.72,.67,.57),rough=.5)
pbr('teak','teak_veneer',tile=1.2,nor=.4)
pbr('walnut','walnut_veneer',tile=1.2,nor=.4)
pbr('oak','oak_veneer_01',tile=1.2,nor=.4)
pbr('fwarm','marble_01',tile=2.4,tint=(.96,.92,.85),rough=.1,nor=.1)
pbr('fgrey','marble_01',tile=2.4,tint=(.60,.59,.57),rough=.12,nor=.1)
pbr('fwood','herringbone_parquet',tile=1.8,nor=.6)
pbr('fstone','marble_01',tile=1.2,tint=(.8,.78,.74),rough=.2,nor=.1)
pbr('fkota',color=(.34,.34,.31),rough=.62)
pbr('linen','rough_linen',tile=.5,tint=(.95,.9,.8),nor=.8,sheen=.4)
pbr('boucle',color=(.78,.71,.58),rough=.95,sheen=.5,norfile='rough_linen',uvs=9)
pbr('velvetRust',color=(.42,.11,.035),rough=.7,sheen=1.0,norfile='rough_linen',uvs=7)
pbr('jacquard','quatrefoil_jacquard_fabric',tile=.3,tint=(.95,.8,.55),nor=.6)
pbr('terra','rough_linen',tile=.5,tint=(.64,.26,.13),nor=.8,sheen=.3)
pbr('jute',diffpath=f'{HQ}/art/jute.jpg',tile=.55,rough=.95)
pbr('mural',diffpath=f'{HQ}/art/mural.jpg',rough=.9,tile=1)
pbr('birds',diffpath=f'{HQ}/art/birds.jpg',rough=.8)
pbr('cane',diffpath=f'{HQ}/art/cane.png',alpha=True,rough=.6)
pbr('brass',color=(.78,.58,.28),metal=1,rough=.28)
pbr('blackstone',color=(.02,.02,.018),rough=.2)
pbr('steel',color=(.75,.75,.73),metal=1,rough=.3)
pbr('bronze',color=(.05,.035,.025),metal=.7,rough=.38)
pbr('glass',color=(.9,.95,.93),rough=.02,trans=1.0)
pbr('sheer',color=(.97,.94,.87),rough=.9,trans=.55)
pbr('rustcurt','rough_linen',tile=.5,tint=(.6,.25,.12),nor=.6)
pbr('led',color=(1,1,1),emit=(1,.78,.52),emitS=3)
pbr('leaf',color=(.10,.23,.07),rough=.42)
pbr('leafD',color=(.05,.16,.05),rough=.38)
pbr('pot',color=(.30,.12,.06),rough=.55)
pbr('potDark',color=(.09,.075,.06),rough=.45)
pbr('soil',color=(.03,.02,.012),rough=1)
pbr('screen',color=(.01,.01,.012),rough=.15)

# ---------- shell builder ----------
class Mesher:
    def __init__(s):s.d={}
    def box(s,mat,x1,y1,z1,x2,y2,z2):
        x1,x2=sorted((x1,x2));y1,y2=sorted((y1,y2));z1,z2=sorted((z1,z2))
        v=[(x1,y1,z1),(x2,y1,z1),(x2,y2,z1),(x1,y2,z1),(x1,y1,z2),(x2,y1,z2),(x2,y2,z2),(x1,y2,z2)]
        s.add(mat,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
    def add(s,mat,v,f):
        a=s.d.setdefault(mat,([],[]));o=len(a[0]);a[0].extend(v);a[1].extend([tuple(i+o for i in q) for q in f])
    def build(s,name,lm=True):
        out=[]
        for mat,(v,f) in s.d.items():
            me=bpy.data.meshes.new(f'{name}_{mat}');me.from_pydata(v,[],f);me.update()
            uv=me.uv_layers.new(name='uv');t=TILE.get(mat,1.0)
            for p in me.polygons:
                nr=p.normal
                for li in p.loop_indices:
                    c=me.vertices[me.loops[li].vertex_index].co
                    if abs(nr.z)>.7:u=(c.x/t,c.y/t)
                    elif abs(nr.x)>.7:u=(c.y/t,c.z/t)
                    else:u=(c.x/t,c.z/t)
                    uv.data[li].uv=u
            me.materials.append(MAT[mat]);ob=bpy.data.objects.new(me.name,me);col.objects.link(ob);ob['shell']=1;out.append(ob)
        return out
M=Mesher();GLASS=Mesher();colliders=[]
def pb(mat,r,z1,z2,G=None):(G or M).box(mat,X(r[0]),Y(r[1]),z1,X(r[2]),Y(r[3]),z2)
def W(a,b,c,d):
    pb('wall',(a,b,c,d),0,H);colliders.append((a,b,c,d,'wall'))
    # skirting wraps every wall box; hidden sides are harmless
    e=.012;M.box('skirting',X(a)-e,Y(b)+e,0,X(c)+e,Y(d)-e,.1)
def thresh(r):pb('walnut',r,-.01,.004)
def header(r,h=7.5*FT):pb('wall',r,h,H)
def casing(r,h=7.5*FT):
    vert=(r[2]-r[0])<(r[3]-r[1]);t=.07;e=.012
    if vert:
        for a,bb in((Y(r[1]),Y(r[1])-t),(Y(r[3])+t,Y(r[3]))):M.box('teak',X(r[0])-e,a,0,X(r[2])+e,bb,h)
        M.box('teak',X(r[0])-e,Y(r[1]),h-t,X(r[2])+e,Y(r[3]),h)
    else:
        for a,bb in((X(r[0]),X(r[0])+t),(X(r[2])-t,X(r[2]))):M.box('teak',a,Y(r[1])+e,0,bb,Y(r[3])-e,h)
        M.box('teak',X(r[0]),Y(r[1])+e,h-t,X(r[2]),Y(r[3])-e,h)
def door(r,end,dir):
    thresh(r);header(r);casing(r)
    vert=(r[2]-r[0])<(r[3]-r[1]);w=(vert and (r[3]-r[1]) or (r[2]-r[0]))/S*FT-.1
    if vert:
        z=(Y(r[3])+.05) if end else (Y(r[1])-.05);x=(X(r[0])+X(r[2]))/2
        M.box('teak',x,z-.022,0,x+dir*w,z+.022,2.2);M.box('walnut',x+dir*w*.12,z-.03,.25,x+dir*w*.88,z+.03,1.05);M.box('walnut',x+dir*w*.12,z-.03,1.2,x+dir*w*.88,z+.03,2.0);M.box('brass',x+dir*(w-.09),z-.05,.98,x+dir*(w-.05),z+.05,1.12)
        colliders.append((min(x,x+dir*w)/FT*S+OX,-(z+.022)/FT*S+OY,max(x,x+dir*w)/FT*S+OX,-(z-.022)/FT*S+OY,'door'))
    else:
        x=(X(r[2])-.05) if end else (X(r[0])+.05);y=(Y(r[1])+Y(r[3]))/2
        # plan dir +1 means the leaf swings toward larger plan y, which is smaller Blender y
        M.box('teak',x-.022,y,0,x+.022,y-dir*w,2.2);M.box('walnut',x-.03,y-dir*w*.12,.25,x+.03,y-dir*w*.88,1.05);M.box('walnut',x-.03,y-dir*w*.12,1.2,x+.03,y-dir*w*.88,2.0);M.box('brass',x-.05,y-dir*(w-.09),.98,x+.05,y-dir*(w-.05),1.12)
        a,b=sorted((y,y-dir*w));colliders.append(((x-.022)/FT*S+OX,-b/FT*S+OY,(x+.022)/FT*S+OX,-a/FT*S+OY,'door'))
def opening(r):thresh(r);header(r,8*FT)
CURT=[]
def win(r,sill=1.5,head=8.2,inn=None,mat='sheer',cov=.24):
    pb('wall',r,0,sill*FT);pb('wall',r,head*FT,H);colliders.append((*r,'window'))
    vert=(r[2]-r[0])<(r[3]-r[1]);n=max(1,round((r[3]-r[1] if vert else r[2]-r[0])/S/3.2));e=.03
    mx=(r[0]+r[2])/2;my=(r[1]+r[3])/2;s=sill*FT;h=head*FT
    if vert:
        GLASS.box('glass',X(mx)-.003,Y(r[1]),s,X(mx)+.003,Y(r[3]),h)
        for i in range(n+1):
            yy=Y(r[1])+(Y(r[3])-Y(r[1]))*i/n;M.box('bronze',X(mx)-e,yy-e,s,X(mx)+e,yy+e,h)
        M.box('bronze',X(mx)-e,Y(r[1]),s,X(mx)+e,Y(r[3]),s+.05);M.box('bronze',X(mx)-e,Y(r[1]),h-.05,X(mx)+e,Y(r[3]),h)
    else:
        GLASS.box('glass',X(r[0]),Y(my)-.003,s,X(r[2]),Y(my)+.003,h)
        for i in range(n+1):
            xx=X(r[0])+(X(r[2])-X(r[0]))*i/n;M.box('bronze',xx-e,Y(my)-e,s,xx+e,Y(my)+e,h)
        M.box('bronze',X(r[0]),Y(my)-e,s,X(r[2]),Y(my)+e,s+.05);M.box('bronze',X(r[0]),Y(my)-e,h-.05,X(r[2]),Y(my)+e,h)
    if inn:CURT.append((r,inn,mat,cov))
def slider(r,inn=None,mat='sheer'):
    thresh(r);pb('wall',r,8.2*FT,H);vert=(r[2]-r[0])<(r[3]-r[1]);e=.03;h=8.2*FT
    L=(r[3]-r[1] if vert else r[2]-r[0])/S;n=max(2,round(L/3.6));mx=(r[0]+r[2])/2;my=(r[1]+r[3])/2
    # the half nearer the start of the opening stays clear so doorways remain walkable
    if vert:
        a=Y(r[1]);c=Y(r[3]);m=(a+c)/2;GLASS.box('glass',X(mx)-.003,m,0,X(mx)+.003,c,h)
        for i in range(n//2+1):
            yy=m+(c-m)*i/(n//2);M.box('bronze',X(mx)-e,yy-e,0,X(mx)+e,yy+e,h)
        M.box('bronze',X(mx)-e,m,0,X(mx)+e,c,.06);colliders.append((r[0],my,r[2],r[3],'glass'))
    else:
        a=X(r[0]);c=X(r[2]);m=(a+c)/2;GLASS.box('glass',m,Y(my)-.003,0,c,Y(my)+.003,h)
        for i in range(n//2+1):
            xx=m+(c-m)*i/(n//2);M.box('bronze',xx-e,Y(my)-e,0,xx+e,Y(my)+e,h)
        M.box('bronze',m,Y(my)-e,0,c,Y(my)+e,.06);colliders.append((mx,r[1],r[2],r[3],'glass'))
    if inn:CURT.append((r,inn,mat,.1))
def rail(a,b,c,d):
    colliders.append((min(a,c)-3,min(b,d)-3,max(a,c)+3,max(b,d)+3,'rail'));t=.004
    GLASS.box('glass',X(a)-t,Y(b)+t,0,X(c)+t,Y(d)-t,1.05);M.box('brass',X(a)-.018,Y(b)+.018,1.05,X(c)+.018,Y(d)-.018,1.08)

ROOMS=[
 ('Foyer',(4369,1953,5127,2372),'fwarm',"~12'6\" x 6'11\""),('Drawing Room',(3426,2418,4914,3566),'fwarm',"24'10\" x 18'11\""),
 ('Living Room',(2318,2417,3381,3561),'fgrey',"18'0\" x 18'11\""),('Dining',(2318,1586,3380,2417),'fgrey',"18'0\" x 13'9\""),
 ('Kitchen',(2318,800,3381,1586),'fgrey',"18'0\" x 13'0\""),('Wash',(2318,252,3381,755),'fstone',"17'7\" x 8'4\""),
 ('Utility',(3381,372,4066,755),'fstone',"~11'4\" x 6'4\""),('Passage',(2060,1587,2318,2373),'fgrey',"~4'3\" x 13'"),
 ('Theater Room',(1163,1587,2040,2373),'fwood',"14'6\" x 13'"),("Son's Bedroom",(1163,262,2273,1123),'fwood',"18'4\" x 12'"),
 ("Son's Dressing",(1628,1144,2273,1552),'fwood',"~10'9\" x 6'9\""),("Son's Bath",(1163,1144,1607,1552),'fstone',"~7'4\" x 6'9\""),
 ('Master Room',(1163,2836,2273,3698),'fwood',"18'4\" x 12'"),("Master's Dressing",(1628,2408,2273,2815),'fwood',"~10'9\" x 6'9\""),
 ("Master's Bath",(1163,2408,1607,2815),'fstone',"~7'4\" x 6'9\""),("Daughter's Room",(3402,1182,4429,1908),'fwood',"17' x 12'"),
 ("Daughter's Bath",(3523,800,4066,1162),'fstone',"~9' x 6'"),('Guest Room',(4934,2418,5662,3328),'fwood',"12' x 15'"),
 ('Guest Bath',(5151,1953,5481,2396),'fstone',"~5'5\" x 7'4\""),('Temple',(3400,1953,3742,2372),'fwarm',"~6' x 6'11\""),
 ('Balcony',(3426,3612,4914,4112),'fkota',"~24'7\" x 8'3\""),("Son's Balcony",(800,532,1143,957),'fkota',"~5'8\" x 7'"),
 ("Master's Balcony",(1849,3608,2273,3850),'fkota',"~7' x 4'6\""),('Vestibule',(4475,1364,5261,1908),'fkota',"~13' x 9'"),
]
for n,r,f,s in ROOMS:pb(f,r,-.02,0)
for r in [(3402,2372,5000,3612),(1118,217,2318,3743),(2273,252,3402,3607),(3402,755,4113,3612),(3426,3566,4959,4112),(4113,1182,4475,2418),(4475,1953,5708,3375),(800,532,1143,957),(1849,3608,2273,3850),(4475,1319,5300,1953)]:
    _i=globals().get('_i',0)+1;globals()['_i']=_i;pb('ceil',r,H+_i*.0015,H+.25+_i*.0015);pb('ceil',r,-.3-_i*.0015,-.025-_i*.0015)
pb('ceil',(3381,217,4113,800),-.3,-.025)
# walls exactly as the plan drawing
W(1118,217,1849,262);W(1118,262,1163,532);slider((1143,532,1163,957),inn=(1,0));W(1118,957,1163,1274);win((1118,1274,1163,1422),4.2,7.2);W(1118,1422,1163,1587)
W(1813,262,1849,397);win((1849,352,2273,397),1.5,8.2,inn=(0,1));W(2273,217,2318,1587)
W(1163,1123,2060,1144);opening((2060,1123,2273,1144));W(1607,1144,1628,1279);door((1607,1279,1628,1428),0,-1);W(1607,1428,1628,1552)
W(1163,1552,2060,1587);door((2060,1552,2273,1587),1,-1)
win((1143,1587,1163,2373),.5,8.4,inn=(1,0),mat='rustcurt',cov=.28);W(2040,1786,2060,2373);door((2040,1587,2060,1786),0,-1);W(1118,1587,1143,1610);W(1118,2350,1143,2408)
W(1163,2373,2060,2408);door((2060,2373,2273,2408),1,1);W(1118,2408,1163,2538);win((1118,2538,1163,2683),4.2,7.2);W(1118,2683,1163,3003)
win((1143,3003,1163,3425),1.5,8.2,inn=(1,0));W(1118,3425,1163,3743);W(1118,3698,1849,3743);W(1813,3561,1849,3698);W(2273,2373,2318,3608)
W(1163,2815,2060,2836);opening((2060,2815,2273,2836));W(1607,2408,1628,2531);door((1607,2531,1628,2681),0,-1);W(1607,2681,1628,2815)
slider((1849,3561,2273,3608),inn=(0,-1))
W(2318,3561,2475,3607);win((2475,3561,3199,3607),.6,8.4,inn=(0,-1),cov=.2);W(3199,3561,3548,3612);slider((3548,3566,4792,3612),inn=(0,-1));W(4792,3566,4959,3612)
W(3381,3424,3426,3607);W(3380,2372,3426,2417);pb('wall',(2318,2372,3380,2417),8.2*FT,H)
W(3381,800,3402,1733);door((3381,1733,3402,1908),0,1);W(3380,1908,4667,1953);door((4674,1908,4904,1953),0,1);door((4674,1908,4904,1953),1,-1);W(4904,1908,5527,1953);W(4667,1908,4674,1953)
W(3742,1953,3789,2372);W(4324,1953,4369,2372);door((3380,1953,3400,2155),0,1);win((3380,2155,3400,2372),.3,8);W(3789,1953,4324,2372)
W(3380,2372,3936,2418);pb('steel',(3936,2384,4177,2406),0,7.8*FT);pb('wall',(3936,2372,4177,2418),7.8*FT,H);colliders.append((3936,2372,4177,2418,'lift'));W(4177,2372,4551,2418);opening((4551,2372,4909,2418));W(4909,2372,5151,2418)
door((4914,2418,4934,2595),0,1);W(4914,2595,4934,3375);W(5662,2418,5708,3375);W(4934,3328,5055,3375);win((5055,3328,5541,3375),1.5,8.2,inn=(0,-1));W(5541,3328,5662,3375)
W(5127,1953,5151,2396);win((5481,1953,5527,2074),4.2,7.2);W(5481,2074,5527,2372);W(5294,2396,5527,2418);door((5151,2396,5294,2418),0,-1);W(5527,2372,5708,2418)
W(3402,1162,3523,1182);door((3523,1162,3668,1182),0,-1);W(3668,1162,4113,1182);win((4113,1137,4429,1182),2,8,inn=(0,1));W(4429,1137,4475,1908)
W(4066,217,4113,1182);W(2318,755,2776,800);slider((2776,755,3169,800));W(3169,755,3703,800);win((3703,755,3824,800),5,7.2);W(3824,755,4066,800)
W(2318,217,2776,252);win((2776,217,3230,252),3,8,inn=(0,1));W(3230,217,3426,252);W(3381,252,3426,532);rail(3426,362,4066,362)
W(4475,1319,5261,1364);W(5261,1364,5300,1908)
rail(3426,4112,4914,4112);rail(3426,3612,3426,4112);rail(4914,3612,4914,4112);rail(800,532,1143,532);rail(800,957,1143,957);rail(800,532,800,957);rail(1849,3850,2273,3850);rail(1849,3608,1849,3850);rail(2273,3608,2273,3850)

# tray ceiling with a hidden warm cove in the big rooms
def tray(r,inset=.42,drop=.11):
    x1,y1,x2,y2=X(r[0]),Y(r[1]),X(r[2]),Y(r[3]);t=.03;z=H-drop
    for a,b,c,d in((x1,y1,x2,y1-inset),(x1,y2+inset,x2,y2),(x1,y1-inset,x1+inset,y2+inset),(x2-inset,y1-inset,x2,y2+inset)):M.box('ceil',a,b,z,c,d,H)
    e=.06
    for a,b,c,d in((x1+inset-e,y1-inset+e,x2-inset+e,y1-inset+e-.012),(x1+inset-e,y2+inset-e,x2-inset+e,y2+inset-e+.012),(x1+inset-e,y1-inset+e,x1+inset-e+.012,y2+inset-e),(x2-inset+e,y1-inset+e,x2-inset+e-.012,y2+inset-e)):M.box('led',a,b,z+.015,c,d,z+.03)
for r in [(3426,2418,4914,3566),(2318,2417,3381,3561),(2318,1586,3380,2372),(1163,2836,2273,3561),(1163,397,2273,1123),(3402,1182,4429,1908),(4934,2418,5662,3328),(1163,1587,2040,2373)]:tray(r)

# ---------- curtains: pleated meshes ----------
def pleats(x1,y1,x2,y2,mat,z1=.03,z2=H-.05):
    L=math.hypot(x2-x1,y2-y1);n=max(14,int(L/.035));v=[];f=[];dx,dy=(x2-x1)/L,(y2-y1)/L;nx,ny=-dy,dx
    for i in range(n+1):
        t=i/n;a=math.sin(t*L*math.tau/.15)*.032+math.sin(t*L*math.tau/.43)*.012
        px,py=x1+dx*t*L+nx*a,y1+dy*t*L+ny*a;v+=[(px,py,z1),(px,py,z2)]
    for i in range(n):f.append((i*2,i*2+2,i*2+3,i*2+1))
    M.add(mat,v,f)
for r,inn,mat,cov in CURT:
    vert=(r[2]-r[0])<(r[3]-r[1]);off=.12
    if vert:
        bx=(X(r[2]) if inn[0]>0 else X(r[0]))+inn[0]*off;a,c=Y(r[1]),Y(r[3]);L=(c-a)*cov
        pleats(bx,a+.2,bx,a+L,mat);pleats(bx,c-L,bx,c-.2,mat);M.box('brass',bx-.012,a+.25,H-.05,bx+.012,c-.25,H-.03)
    else:
        by=(Y(r[3]) if inn[1]>0 else Y(r[1]))-inn[1]*off;a,c=X(r[0]),X(r[2]);L=(c-a)*cov
        pleats(a-.2,by,a+L,by,mat);pleats(c-L,by,c+.2,by,mat);M.box('brass',a-.25,by-.012,H-.05,c+.25,by+.012,H-.03)

# ---------- furniture helpers ----------
TEX={os.path.basename(p).lower():p for p in glob.glob(C+'Textures/*')}
def deselect():
    for o in bpy.context.selected_objects:o.select_set(False)
def fp_mat(mat,folder,stem,res='1024px'):
    mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;b=n.get('Principled BSDF')
    if not b:return
    for nd in [x for x in n if x.type=='TEX_IMAGE']:n.remove(nd)
    def tx(k,cs):
        p=os.path.join(folder,f'{res} Textures',f'{stem}_{k}.png')
        if not os.path.exists(p):return None
        t=n.new('ShaderNodeTexImage');t.image=teximg(p,cs);return t
    t=tx('BaseColor','sRGB');t and l.new(t.outputs[0],b.inputs['Base Color'])
    t=tx('Roughness','Non-Color');t and l.new(t.outputs[0],b.inputs['Roughness'])
    t=tx('Metallic','Non-Color');t and l.new(t.outputs[0],b.inputs['Metallic'])
    t=tx('Normal','Non-Color')
    if t:
        m=n.new('ShaderNodeNormalMap');l.new(t.outputs[0],m.inputs[1]);l.new(m.outputs[0],b.inputs['Normal'])
def join(obs,name):
    ms=[o for o in obs if o.type=='MESH'];names=[o.name for o in obs]
    deselect()
    for o in ms:o.select_set(True)
    bpy.context.view_layer.objects.active=ms[0]
    if len(ms)>1:bpy.ops.object.join()
    ob=bpy.context.view_layer.objects.active
    for nm_ in names:
        if nm_!=ob.name and nm_ in bpy.data.objects:bpy.data.objects.remove(bpy.data.objects[nm_])
    ob.parent=None;ob.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);ob.name=name;return ob
def norm(ob,face=0):
    # move the pivot to the footprint centre at floor level, then turn the front to -Y
    if face:ob.data.transform(Matrix.Rotation(math.radians(face),4,'Z'))
    vs=[v.co for v in ob.data.vertices];mn=Vector(map(min,*vs)) if False else Vector((min(v.x for v in vs),min(v.y for v in vs),min(v.z for v in vs)));mx=Vector((max(v.x for v in vs),max(v.y for v in vs),max(v.z for v in vs)))
    ob.data.transform(Matrix.Translation(Vector((-(mn.x+mx.x)/2,-(mn.y+mx.y)/2,-mn.z))));ob.data.update();ob['dim']=list(mx-mn);return ob
MAST={}
def fp(key,path,face=0,sub=0,override=None,texdir=None):
    if key in MAST:return MAST[key]
    b=set(bpy.data.objects);bpy.ops.wm.obj_import(filepath=path);obs=[o for o in bpy.data.objects if o not in b]
    folder=texdir or os.path.dirname(path);stems=sorted({os.path.basename(p).rsplit('_BaseColor',1)[0] for p in glob.glob(os.path.join(folder,'1024px Textures','*_BaseColor.png'))})
    for o in obs:
        for s in getattr(o,'material_slots',[]):
            if s.material and stems:
                st=[t for t in stems if s.material.name.split('.')[0].lower() in t.lower()] or stems;fp_mat(s.material,folder,st[0])
    ob=join(obs,key);norm(ob,face)
    if override:
        ob.data.materials.clear();ob.data.materials.append(MAT[override])
    if sub:
        m=ob.modifiers.new('sub','SUBSURF');m.levels=m.render_levels=sub;m.subdivision_type='SIMPLE' if False else 'CATMULL_CLARK'
    ob.data.shade_smooth();ob.data.set_sharp_from_angle(angle=math.radians(40))
    ob.hide_render=True;ob.hide_set(True);MAST[key]=ob;return ob
def fbx(key,name,face=0,scale=1):
    if key in MAST:return MAST[key]
    b=set(bpy.data.objects);bpy.ops.import_scene.fbx(filepath=C+'FBX/'+name);obs=[o for o in bpy.data.objects if o not in b]
    for o in obs:
        for s in getattr(o,'material_slots',[]):
            if s.material and s.material.use_nodes:
                for n in s.material.node_tree.nodes:
                    if n.type=='TEX_IMAGE' and n.image:
                        bn=os.path.basename(n.image.filepath.replace('\\','/')).lower()
                        if bn in TEX:n.image.filepath=TEX[bn];n.image.reload()
    ob=join(obs,key);norm(ob,face)
    ob.data.shade_smooth();ob.data.set_sharp_from_angle(angle=math.radians(40))
    ob.hide_render=True;ob.hide_set(True);MAST[key]=ob;return ob
ITEMS=[]
def place(master,r,rot=0,name=None,h=None,uniform=False,free=False,label=True):
    d=Vector(master['dim']);sw=abs(rot)%180==90;w=(r[2]-r[0])/S*FT;dd=(r[3]-r[1])/S*FT;tw,td=(dd,w) if sw else (w,dd)
    sx,sy=tw/d.x,td/d.y
    if uniform:sx=sy=min(sx,sy)
    sz=(h/d.z) if h else (sx+sy)/2
    ob=master.copy();col.objects.link(ob);ob.hide_render=False;ob.hide_set(False);ob.scale=(sx,sy,sz);ob.rotation_euler=(0,0,math.radians(rot));ob.location=((X(r[0])+X(r[2]))/2,(Y(r[1])+Y(r[3]))/2,0);ob['furn']=1
    if not free:colliders.append((*r,name or master.name))
    ITEMS.append(dict(name=name or master.name,r=list(r),free=free,label=label,dims=[round(d.x*sx/FT,2),round(d.y*sy/FT,2)]));return ob
def soft(mat,w,d,h,loc,rot=0,crown=.2,name='cush',cuts=2,bev=.3):
    bm=bmesh.new();bmesh.ops.create_cube(bm,size=1);
    me=bpy.data.meshes.new(name);bm.to_mesh(me);bm.free();ob=bpy.data.objects.new(name,me);col.objects.link(ob)
    ob.scale=(w/2,d/2,h/2);ob.location=loc;ob.rotation_euler=(0,0,math.radians(rot))
    ob.scale=(1,1,1);me.transform(Matrix.Diagonal((w,d,h,1)));bv=ob.modifiers.new('s','BEVEL');bv.width=min(.05,h*.42);bv.segments=4
    me.materials.append(MAT[mat]);
    for p in me.polygons:p.use_smooth=True
    ob['furn']=1;return ob
def pillow(mat,w,th,loc,rx=-1.15,rz=0):
    bm=bmesh.new();g=bmesh.ops.create_grid(bm,x_segments=12,y_segments=12,size=w/2)
    for v in bm.verts:
        a,b=max(-1,min(1,v.co.x/(w/2))),max(-1,min(1,v.co.y/(w/2)));v.co.z=max(0,1-a*a)**.55*max(0,1-b*b)**.55*th*.5;e=(1-.13*(1-a*a)*abs(b)**4);ee=(1-.13*(1-b*b)*abs(a)**4);v.co.x*=ee;v.co.y*=e
    bot=bmesh.ops.duplicate(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces))
    for v in [g for g in bot['geom'] if isinstance(g,bmesh.types.BMVert)]:v.co.z=-v.co.z
    bmesh.ops.reverse_faces(bm,faces=[g for g in bot['geom'] if isinstance(g,bmesh.types.BMFace)]);bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=.0005);uv=bm.loops.layers.uv.new('uv')
    for f in bm.faces:
        for l in f.loops:l[uv].uv=(l.vert.co.x/.35,l.vert.co.y/.35)
    me=bpy.data.meshes.new('pillow');bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('pillow',me);col.objects.link(ob);ob.location=loc;ob.rotation_euler=(rx,0,rz);me.materials.append(MAT[mat])
    for p in me.polygons:p.use_smooth=True
    ob['furn']=1;return ob
def uv_scale_cube(ob,t):
    me=ob.data;uv=me.uv_layers.get('uv') or me.uv_layers.new(name='uv')
def flat(mat,r,z1,z2):
    d=Mesher();d.box(mat,X(r[0]),Y(r[1]),z1,X(r[2]),Y(r[3]),z2);obs=d.build('flat');[o.__setitem__('furn',1) for o in obs];return obs[0]
def rug(mat,r,th=.018):
    flat(mat,r,0,th);ITEMS.append(dict(name='Rug',r=list(r),free=True,label=True,dims=[round((r[2]-r[0])/S,2),round((r[3]-r[1])/S,2)]))
# plants from your set, with leaves, pot, soil and stand given separate materials
PL={}
def load_plants():
    if PL:return
    b=set(bpy.data.objects);bpy.ops.wm.obj_import(filepath='/Users/havi.tv/Downloads/Plants_Set.obj',forward_axis='NEGATIVE_Z',up_axis='Y',use_split_groups=True)
    for o in [o for o in bpy.data.objects if o not in b]:PL[o.name.split('.')[0].lower()]=o;o.hide_render=True;o.hide_set(True)
    for k,o in PL.items():
        o.data.materials.clear()
        m='leaf' if k.startswith('plant') else 'soil' if k.startswith('soil') else 'brass' if k.startswith('leg') else 'pot'
        o.data.materials.append(MAT[m])
        for p in o.data.polygons:p.use_smooth=True
def plant(n,r,h=None,name='Plant',ratio=.5,leaf='leaf',potmat='pot',free=False,seed=0,leafonly=False):
    load_plants();nn=f'{n:02d}';parts=[PL[f'plant_{nn}'],PL.get(f'pot_{nn}'),PL.get(f'soil_{nn}'),PL.get(f'legs_{nn}') or PL.get(f'leg_{nn}')]
    parts=[p for p in parts if p];pot=PL[f'pot_{nn}']
    cx=sum((pot.matrix_world@Vector(c)).x for c in pot.bound_box)/8;cy=sum((pot.matrix_world@Vector(c)).y for c in pot.bound_box)/8
    zmin=min((p.matrix_world@Vector(c)).z for p in parts for c in p.bound_box);zmax=max((p.matrix_world@Vector(c)).z for p in parts for c in p.bound_box)
    k=(h/(zmax-zmin)) if h else .001
    gx,gy=(X(r[0])+X(r[2]))/2,(Y(r[1])+Y(r[3]))/2
    for p in (parts[:1] if leafonly else parts):
        o=p.copy();col.objects.link(o);o.hide_render=False;o.hide_set(False);o.scale=(k,k,k);o.location=(gx-cx*k,gy-cy*k,-zmin*k);o['furn']=1
        if leafonly:o['gobo']=1;o['furn']=0
        if p.name.lower().startswith('plant'):
            o.data=p.data.copy();o.data.materials.clear();o.data.materials.append(MAT[leaf])
            if len(o.data.polygons)>30000:
                d=o.modifiers.new('d','DECIMATE');d.ratio=30000/len(o.data.polygons)
        if p.name.lower().startswith('pot'):
            o.data=p.data.copy();o.data.materials.clear();o.data.materials.append(MAT[potmat])
    if not free:colliders.append((*r,name))
    ITEMS.append(dict(name=name,r=list(r),free=free,label=True,dims=[round((r[2]-r[0])/S,2),round((r[3]-r[1])/S,2)]))
def glb(name,path,loc,size,rot=0):
    b=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=path);obs=[o for o in bpy.data.objects if o not in b];ob=join(obs,name);norm(ob);d=Vector(ob['dim']);k=size/d.z
    ob.scale=(k,k,k);ob.location=loc;ob.rotation_euler=(0,0,rot);ob['furn']=1;return ob
def lathe(mat,prof,loc,seg=48,name='lathe'):
    bm=bmesh.new();rings=[]
    for r,z in prof:
        rg=[bm.verts.new((math.cos(i/seg*math.tau)*r,math.sin(i/seg*math.tau)*r,z)) for i in range(seg)];rings.append(rg)
    uv=bm.loops.layers.uv.new('uv')
    for a in range(len(rings)-1):
        for i in range(seg):
            j=(i+1)%seg;f=bm.faces.new((rings[a][i],rings[a][j],rings[a+1][j],rings[a+1][i]))
            for l,(u,v) in zip(f.loops,((i,a),(i+1,a),(i+1,a+1),(i,a+1))):l[uv].uv=(u/seg*14,v/max(1,len(rings)-1)*3)
    me=bpy.data.meshes.new(name);bm.to_mesh(me);bm.free();ob=bpy.data.objects.new(name,me);col.objects.link(ob);ob.location=loc;me.materials.append(MAT[mat])
    for p in me.polygons:p.use_smooth=True
    ob['furn']=1;return ob
def slab_table(r,thick=.075,height=.34):
    w=(r[2]-r[0])/S*FT;d=(r[3]-r[1])/S*FT;cx,cy=(X(r[0])+X(r[2]))/2,(Y(r[1])+Y(r[3]))/2
    pts=[]
    for i in range(72):
        a=i/72*math.tau;k=1+.09*math.sin(a*3+1)+.045*math.sin(a*7+.4);pts.append((math.cos(a)*w/2*k,math.sin(a)*d/2*k))
    bm=bmesh.new();top=[bm.verts.new((x,y,height+thick)) for x,y in pts];bot=[bm.verts.new((x*.965,y*.965,height)) for x,y in pts];f=bm.faces.new(top);uv=bm.loops.layers.uv.new('uv')
    bm.faces.new(list(reversed(bot)))
    n=len(pts)
    for i in range(n):bm.faces.new((bot[i],bot[(i+1)%n],top[(i+1)%n],top[i]))
    for f in bm.faces:
        for l in f.loops:l[uv].uv=(l.vert.co.x/1.1,l.vert.co.y/1.1+l.vert.co.z)
    me=bpy.data.meshes.new('slab');bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('slab',me);col.objects.link(ob);ob.location=(cx,cy,0);me.materials.append(MAT['walnut']);ob['furn']=1
    for p in me.polygons:p.use_smooth=len(p.vertices)==4
    b=ob.modifiers.new('b','BEVEL');b.width=.012;b.segments=3;b.limit_method='ANGLE'
    lathe('walnut',[(0,0),(w*.25,0),(w*.25,.02),(w*.21,.1),(w*.2,height-.01),(w*.24,height),(0,height)],(cx,cy,0),name='slabbase');colliders.append((*r,'Slab coffee table'));ITEMS.append(dict(name='Slab coffee table',r=list(r),free=False,label=True,dims=[round(w/FT,2),round(d/FT,2)]))

# ---------- rooms: Drawing, semi-partition, Living, Dining ----------
sofa=fp('sofa',F+'sofas/sofa/sofa.obj')
def swap_base(ob,path):
    for s_ in ob.data.materials:
        s_.use_nodes=True
        for n_ in s_.node_tree.nodes:
            if n_.type=='TEX_IMAGE' and 'BaseColor' in (n_.image.name if n_.image else ''):n_.image=teximg(path,'sRGB')
swap_base(sofa,f'{HQ}/art/sofa_cream.jpg')
chair4=fp('chair4',F+'chairs/chair4/chair4.obj',face=-90)
chair3=fp('chair3',F+'chairs/chair3/chair3.obj',face=-90)
tray=fbx('tray','CGT_coffee_table_002.fbx')
lamp=fbx('lamp38','CGT_Table_Lamp_38_001.fbx')
# DRAWING
RED=[3425,3355,4486,3524]
place(sofa,(4691,2741,4860,3302),-90,'Sofa',h=.82);place(sofa,(3490,2765,3659,3326),90,'Sofa',h=.82);place(sofa,(3925,3356,4486,3524),180,'Sofa',h=.82)
place(chair4,(3670,3330,3820,3480),135,'Lounge chair',uniform=True);place(chair4,(4530,3330,4680,3480),-135,'Lounge chair',uniform=True)
rug('jute',(3919,2886,4408,3233));slab_table((3985,2955,4265,3135))
glb('vase','%s/ph/brass_vase_01/brass_vase_01.gltf'%HQ,((X(3985)+X(4265))/2,(Y(2955)+Y(3135))/2,.415),.34)
def cushions(side,cx,cy,w,rot):
    # three cushions along a sofa back; side is the unit vector from back toward the seat
    sx,sy=side;perp=(-sy,sx)
    for k,mt,s in((-.32,'velvetRust',.5),(0,'jacquard',.46),(.32,'velvetRust',.5)):
        pillow(mt,s,.15,(cx+perp[0]*k*w+sx*.0,cy+perp[1]*k*w+sy*.0,.62),rx=-1.12,rz=rot)
cushions((-1,0),X(4691)+.34,(Y(2741)+Y(3302))/2,2.6,math.radians(-90));cushions((1,0),X(3659)-.34,(Y(2765)+Y(3326))/2,2.6,math.radians(90));cushions((0,1),(X(3925)+X(4486))/2,Y(3524)+.34,2.6,math.radians(180))
place(fbx('side','CGT_side_table_039.fbx'),(3432,3377,3552,3497),0,'Side table',uniform=True);place(fbx('side2','CGT_side_table_042.fbx'),(4722,3377,4842,3497),0,'Side table',uniform=True)
plant(2,(4790,2605,4905,2725),h=2.25,name='Tall plant',potmat='potDark')
# mural in an arched cream plaster surround on the Guest Room wall
wx=X(4914)-.012;zb=0;z1=H-.12;ya,yb=Y(2620),Y(3350)
mm=Mesher();TILE['mural']=1;
me=bpy.data.meshes.new('mural');me.from_pydata([(wx,ya,zb),(wx,yb,zb),(wx,yb,z1),(wx,ya,z1)],[],[(0,1,2,3)]);uv=me.uv_layers.new(name='uv')
for li,u in zip(range(4),((0,0),(1,0),(1,1),(0,1))):uv.data[li].uv=u
me.materials.append(MAT['mural']);o=bpy.data.objects.new('mural',me);col.objects.link(o);o['shell']=1
for a,b,c,d in((wx-.03,ya+.05,wx+.003,ya),(wx-.03,yb,wx+.003,yb-.05)):M.box('skirting',a,b,0,c,d,z1)
M.box('skirting',wx-.03,ya+.05,z1-.05,wx+.003,yb-.05,z1)
# rattan pendant over the rug (photo 1)
cx,cy=(X(3919)+X(4408))/2,(Y(2886)+Y(3233))/2
p=[(0.02,.0)]+[(.27*math.sin(t/14*math.pi*.62)**.75+.02,-t/14*.42) for t in range(1,15)]
sh=lathe('cane',p,(cx,cy,H-.55),seg=64,name='pendant');lathe('led',[(.05,.04),(.05,-.04)],(cx,cy,H-.8),seg=16,name='bulb');lathe('brass',[(.004,.55),(.004,0)],(cx,cy,H-.55),seg=8,name='cord')
# oval cane and bird screen as the plan's semi-partition
def oval(xp,zc,y0,w,h,matp):
    n=48;pts=[]
    for i in range(n):
        a=i/n*math.tau;sx=(w/2);s_=(h/2-w/2)
        c,si=math.cos(a),math.sin(a);zz=si*sx+(s_ if si>0 else -s_);pts.append((y0+c*sx,zc+zz))
    bm=bmesh.new();t=.04;bw=.022;ring=[]
    # frame: an outer and inner ring extruded in x
    for (px,pz) in pts:
        d=Vector((px-y0,0,pz-zc));e=(math.hypot(px-y0,pz-zc));ring.append((px,pz))
    uv=bm.loops.layers.uv.new('uv')
    outerF=[];
    A=[bm.verts.new((xp-bw,p[0],p[1])) for p in ring];B=[bm.verts.new((xp+bw,p[0],p[1])) for p in ring]
    def inset(p):
        dy,dz=p[0]-y0,p[1]-zc;k=max(.001,math.hypot(dy,dz));return (p[0]-dy/k*t,p[1]-dz/k*t)
    I=[inset(p) for p in ring];C=[bm.verts.new((xp-bw,p[0],p[1])) for p in I];D=[bm.verts.new((xp+bw,p[0],p[1])) for p in I]
    for i in range(n):
        j=(i+1)%n
        bm.faces.new((A[i],A[j],B[j],B[i]));bm.faces.new((C[j],C[i],D[i],D[j]));bm.faces.new((A[j],A[i],C[i],C[j]));bm.faces.new((B[i],B[j],D[j],D[i]))
    for f in bm.faces:
        for l in f.loops:l[uv].uv=(l.vert.co.y*2,l.vert.co.z*2)
    me=bpy.data.meshes.new('ovalframe');bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('ovalframe',me);col.objects.link(ob);me.materials.append(MAT['walnut']);ob['furn']=1
    for p in me.polygons:p.use_smooth=True
    bm=bmesh.new();vs=[bm.verts.new((xp,p[0],p[1])) for p in I];f=bm.faces.new(vs);uv=bm.loops.layers.uv.new('uv')
    for l in f.loops:
        y,z=l.vert.co.y,l.vert.co.z
        l[uv].uv=(((y-y0)/w+.5),((z-zc)/h+.5)) if matp=='birds' else ((y-y0)/.3,(z-zc)/.3)
    me=bpy.data.meshes.new('ovalp');bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('ovalp',me);col.objects.link(ob);me.materials.append(MAT[matp]);ob['furn']=1
yt,yb2=Y(2809),Y(3424);N=5;q=(yt-yb2)/N;xp=X(3403.5)
for i in range(N):
    y0=yt-q*(i+.5);off=.17 if i%2 else 0;tH=1.22 if i%2 else 1.08
    top=H-.1-off;gap=.02;bH=top-tH-gap-.06
    oval(xp,top-tH/2,y0,q-.06,tH,'birds' if i%2 else 'cane');oval(xp,.06+bH/2,y0,q-.06,bH,'cane' if i%2 else 'birds')
    M.box('walnut',xp-.012,y0-.012,top,xp+.012,y0+.012,H);M.box('walnut',xp-.03,y0-.08,0,xp+.03,y0+.08,.06)
M.box('walnut',xp-.02,yt,H-.05,xp+.02,yb2,H);colliders.append((3392,2809,3414,3424,'Semi-partition'));ITEMS.append(dict(name='Semi-partition',r=[3392,2809,3414,3424],free=False,label=True,dims=[.3,10.17]))
# LIVING
place(sofa,(3196,2774,3366,3334),-90,'Sofa',h=.82);place(sofa,(2523,3344,3083,3514),180,'Sofa',h=.82)
cushions((-1,0),X(3196)+.34,(Y(2774)+Y(3334))/2,2.6,math.radians(-90));cushions((0,1),(X(2523)+X(3083))/2,Y(3514)+.34,2.6,math.radians(180))
place(chair4,(2661,2624,2846,2774),0,'Armchair',uniform=True);place(chair4,(2888,2624,3073,2774),0,'Armchair',uniform=True)
rug('terra',(2576,2892,3063,3237));place(tray,(2700,2985,2880,3155),0,'Brass tray table',uniform=True)
place(fbx('side3','CGT_side_table_018.fbx'),(3115,3369,3236,3489),0,'Side table',uniform=True)
plant(5,(2330,2430,2450,2550),h=2.0,name='Planter',potmat='potDark')
# cane TV unit and screen on the wall shared with the Master Room
d=Mesher();x1,x2=X(2318),X(2403);y1,y2=Y(2818),Y(3303)
d.box('oak',x1,y1,.1,x2,y2,.58);d.box('walnut',x1+.01,y1-.01,.04,x2-.01,y2+.01,.1);d.box('oak',x1,y1,.58,x2+.01,y2,.61)
for o in d.build('tvunit'):o['furn']=1
nd=4;step=(y1-y2)/nd
for i in range(nd):
    a,b=y1-i*step-.02,y1-(i+1)*step+.02;f=Mesher();TILE['cane']=.22;f.box('cane',x2+.004,a,.15,x2+.006,b,.54);[o.__setitem__('furn',1) for o in f.build('tvcane')]
sc_=Mesher();sc_.box('blackstone',x1+.02,Y(2895),.86,x1+.05,Y(3225),1.76);[o.__setitem__('furn',1) for o in sc_.build('tv')];colliders.append((2318,2818,2403,3303,'TV unit'));ITEMS.append(dict(name='Cane TV unit',r=[2318,2818,2403,3303],free=False,label=True,dims=[1.4,8.02]))
# DINING
dining=fp('table6',F+'tables/table6/Table6.obj')
place(dining,(2689,1902,2992,2205),0,'Dining table',h=.76)
for x,y,rot in[(2750,1858,0),(2931,1858,0),(2750,2249,180),(2931,2249,180),(2645,1963,-90),(2645,2144,-90),(3036,1963,90),(3036,2144,90)]:
    place(chair3,(x-38,y-38,x+38,y+38),rot,'Dining chair',free=True,uniform=False,h=.98,label=(x==2750 and y==1858))
colliders.append((2600,1820,3080,2290,'Dining set'))
glb('vase2','%s/ph/brass_vase_02/brass_vase_02.gltf'%HQ,((X(2689)+X(2992))/2,(Y(1902)+Y(2205))/2,.79),.3)
plant(6,(3250,1600,3370,1720),h=1.9,name='Plant',potmat='potDark')

BEDFACE=-90
exec(open(f'{HQ}/rooms2.py').read())
# ---------- finish ----------
for o in M.build('shell'):o['shell']=1
for o in GLASS.build('glass'):o['glass']=1;o['shell']=0

# ---------- world ----------
w=bpy.data.worlds.new('w');w.use_nodes=True;n=w.node_tree.nodes;l=w.node_tree.links;t=n.new('ShaderNodeTexEnvironment');t.image=bpy.data.images.load(f'{HQ}/hdri/kloofendal_48d_partly_cloudy_puresky.hdr');mp=n.new('ShaderNodeMapping');tc=n.new('ShaderNodeTexCoord');l.new(tc.outputs['Generated'],mp.inputs[0]);l.new(mp.outputs[0],t.inputs[0]);l.new(t.outputs[0],n['Background'].inputs[0]);n['Background'].inputs[1].default_value=1.0;sc.world=w
s=bpy.data.lights.new('sun','SUN');s.energy=11;s.angle=math.radians(1.0);s.color=(1,.9,.76);so=bpy.data.objects.new('sun',s);col.objects.link(so)
d=Vector((-.5,-.72,.52)).normalized();so.rotation_euler=d.to_track_quat('Z','Y').to_euler()
for n_,r,f,s_ in ROOMS:
    if n_ in("Balcony","Son's Balcony","Master's Balcony","Utility"):continue
    w_=(r[2]-r[0])/S*FT;d_=(r[3]-r[1])/S*FT;L=bpy.data.lights.new('fill_'+n_,'AREA');L.shape='RECTANGLE';L.size=max(.3,w_*.7);L.size_y=max(.3,d_*.7);L.energy=w_*d_*1.5;L.color=(1,.94,.86);L.cycles.max_bounces=4;Lo=bpy.data.objects.new(L.name,L);col.objects.link(Lo);Lo.location=((X(r[0])+X(r[2]))/2,(Y(r[1])+Y(r[3]))/2,H-.16);Lo.visible_camera=False;Lo.visible_glossy=False;Lo.visible_transmission=False;Lo['fill']=1
# foliage outside the balcony casts dappled sun, matching photo 1
load_plants()
for gx,gy,hh,n_ in[(3560,4240,5.4,9),(3980,4290,6.2,10),(4420,4250,5.6,9),(4820,4300,6.0,10),(2650,3760,5.5,9),(3050,3790,6,10)]:
    plant(n_,(gx-40,gy-40,gx+40,gy+40),h=hh,name='OutsideTree',free=True,leaf='leafD',potmat='soil',leafonly=True);ITEMS.pop()

import json
json.dump(dict(colliders=colliders,items=ITEMS,rooms=[dict(n=n_,r=r,f=f,size=s_) for n_,r,f,s_ in ROOMS]),open(f'{HQ}/layout.json','w'))

# ---------- render settings ----------
sc.render.engine='CYCLES';sc.cycles.device='GPU';p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='METAL';p.get_devices()
for dv in p.devices:dv.use=True
sc.cycles.use_denoising=True;sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - High Contrast'
sc.view_settings.exposure=.75
def shot(name,px,py,yaw,lens=20,z=1.676,samples=128,res=(1600,1000),pitch=0):
    c=bpy.data.cameras.new(name);c.lens=lens;c.sensor_width=36;ob=bpy.data.objects.new(name,c);col.objects.link(ob);ob.location=(X(px),Y(py),z)
    # yaw 0 looks up the page, 90 looks page-left, matching the walkthrough
    ob.rotation_euler=(math.pi/2+pitch,0,math.radians(yaw));sc.camera=ob;sc.cycles.samples=samples;sc.render.resolution_x,sc.render.resolution_y=res;sc.render.filepath=f'{HQ}/renders/{name}.png';bpy.ops.render.render(write_still=True)
if 'blend' in ARGS:bpy.ops.wm.save_as_mainfile(filepath=f'{HQ}/scene.blend')
if 'plan' in ARGS:
    for o in col.objects:
        if o.type=='MESH' and o.data.materials and o.data.materials[0].name in('ceil','led') or o.get('gobo'):o.hide_render=True
    sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='STUDIO';sc.display.shading.color_type='TEXTURE';sc.display.shading.show_cavity=True;sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0
    c=bpy.data.cameras.new('plan');c.type='ORTHO';c.ortho_scale=26;c.clip_end=500;ob=bpy.data.objects.new('plan',c);col.objects.link(ob);ob.location=(X(3250),Y(2150),40);sc.camera=ob;sc.render.resolution_x,sc.render.resolution_y=2400,2000;sc.render.filepath=f'{HQ}/renders/plan.png';bpy.ops.render.render(write_still=True)
if 'views' in ARGS:
    for nm,a in(('master',(2000,3500,30)),('son',(2150,950,50)),('daughter',(3700,1300,-143)),('guest',(5100,2650,-120)),('sbath',(1570,1500,40)),('balcony',(4680,3980,74)),('foyer',(4800,2130,80)),('utility',(3500,480,-150))):
        shot(nm,*a,samples=48,res=(1100,700))
if 'test' in ARGS:
    shot('drawing',3760,2560,-112,samples=int(ARGS[ARGS.index('test')+1]) if len(ARGS)>ARGS.index('test')+1 else 96)
    shot('living',3160,2520,124,samples=96)
    shot('screen',4300,2700,108,samples=96)
print('BUILD OK',len(colliders),'colliders',len(ITEMS),'items')
if 'bake' in ARGS:exec(open(f'{HQ}/bake.py').read())
