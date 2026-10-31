import {createCanvas} from 'canvas';import fs from 'fs';
let seed=11;const rnd=(a=1,b)=>{seed=(seed*16807)%2147483647;const v=seed/2147483647;return b===undefined?v*a:a+v*(b-a)};
const out=process.argv[2];
// 13.2 x 7.9 ft panel; 1 ft = 310 px. Heights are in ft above the floor.
const PX=310,W=Math.round(13.2*PX),TOP=8.3,Hp=Math.round(TOP*PX);
const c=createCanvas(W,Hp),g=c.getContext('2d');const yy=ft=>Hp-ft*PX;
g.fillStyle='#a8603f';g.fillRect(0,0,W,Hp);
for(let i=0;i<90000;i++){g.fillStyle=['#96532f','#b56d4b','#a15a3b','#8f4f30'][i%4];g.globalAlpha=rnd(.025,.07);const s=rnd(1,16);g.fillRect(rnd(W),rnd(Hp),s,s*rnd(.4,2))}g.globalAlpha=1;
// tone-on-tone scalloped arch
g.fillStyle='#b26b49';const ax=W/2,ah=yy(7.25),ab=yy(4.3),aw=2.15*PX;g.beginPath();g.moveTo(ax-aw,ab);g.lineTo(ax-aw,ah+aw*.72);for(let i=0;i<=10;i++){const a=Math.PI-i/10*Math.PI;g.arc(ax+Math.cos(a)*aw*.84,ah+aw*.72-Math.sin(a)*aw*.72,aw*.2,0,7)}g.lineTo(ax+aw,ab);g.closePath();g.fill();
function palm(x,base,h,s){g.strokeStyle='#8c4a2b';g.lineWidth=11*s;g.lineCap='round';g.beginPath();g.moveTo(x,base);g.quadraticCurveTo(x+8,base-h*.5,x,base-h);g.stroke();
  for(let i=0;i<19;i++){const a=-Math.PI*(i/18);g.save();g.translate(x,base-h);g.rotate(a);const L=rnd(.95,1.2)*150*s;g.strokeStyle='#8c4a2b';g.lineWidth=2.4;g.beginPath();g.moveTo(0,0);g.quadraticCurveTo(L*.5,-10*s,L,4*s);g.stroke();g.lineWidth=1.5;for(let k=12;k<L;k+=6.5){const f=Math.sin(k/L*Math.PI)*22*s;g.beginPath();g.moveTo(k,-.2*k*.05);g.lineTo(k+f*.6,-f);g.moveTo(k,0);g.lineTo(k+f*.6,f);g.stroke()}g.restore()}}
const bandY=yy(4.2);[[.15,2.55,1.3],[.3,2.0,1],[.7,2.0,1],[.85,2.55,1.3],[.42,1.5,.75],[.58,1.5,.75]].forEach(([p,h,s])=>palm(W*p,bandY,h*PX,s));
function cow(x,base,hPx,flip){const s=hPx/118;g.save();g.translate(x,base-hPx);g.scale(flip?-s:s,s);g.translate(0,0);const body='#f5efe2',shade='#d9cfbd';
  g.fillStyle=body;g.beginPath();g.moveTo(-98,34);g.bezierCurveTo(-112,10,-60,4,-20,8);g.bezierCurveTo(30,12,50,4,74,14);g.bezierCurveTo(90,22,92,52,78,70);g.bezierCurveTo(40,80,-50,84,-92,70);g.bezierCurveTo(-104,60,-102,44,-98,34);g.fill();
  [[-86,64,14],[-58,66,14],[46,66,14],[72,62,14]].forEach(([lx,ly,lw],i)=>{g.fillStyle=i%2?shade:body;g.beginPath();g.moveTo(lx,ly);g.lineTo(lx+lw,ly);g.lineTo(lx+lw-3,ly+40);g.lineTo(lx+lw-1,ly+50);g.lineTo(lx,ly+50);g.lineTo(lx+2,ly+40);g.closePath();g.fill();g.fillStyle='#3d2a1e';g.fillRect(lx,ly+46,lw,5)});
  g.fillStyle=body;g.beginPath();g.moveTo(60,12);g.bezierCurveTo(70,-8,88,-12,100,-14);g.bezierCurveTo(108,-20,114,-25,118,-26);g.bezierCurveTo(134,-30,146,-20,150,-4);g.bezierCurveTo(152,8,146,16,134,16);g.bezierCurveTo(118,20,96,40,86,52);g.closePath();g.fill();
  g.strokeStyle=body;g.lineWidth=5;g.beginPath();g.moveTo(128,-27);g.quadraticCurveTo(122,-40,132,-42);g.moveTo(140,-24);g.quadraticCurveTo(146,-36,154,-34);g.stroke();
  g.fillStyle=shade;g.beginPath();g.ellipse(112,-20,12,6,-.5,0,7);g.fill();g.fillStyle='#2a1c14';g.beginPath();g.arc(132,-10,3,0,7);g.fill();
  g.strokeStyle=body;g.lineWidth=4;g.beginPath();g.moveTo(-100,26);g.quadraticCurveTo(-120,44,-112,76);g.stroke();
  g.fillStyle='#d48a2f';for(let i=0;i<34;i++){const px=rnd(-90,70),py=rnd(14,70);g.beginPath();g.arc(px,py,3.4,0,7);g.fill()}
  g.strokeStyle='#5a4638';g.lineWidth=3.5;g.beginPath();g.moveTo(92,6);g.quadraticCurveTo(84,28,74,44);g.stroke();g.strokeStyle='#c49a4b';g.lineWidth=2;for(let i=0;i<6;i++){g.beginPath();g.arc(92-i*3,8+i*6,3.4,0,7);g.stroke()}
  g.restore()}
const cw=W*.2/2.3;[[.15,.88*cw,0],[.34,1.12*cw,0],[.66,1.12*cw,1],[.85,.88*cw,1]].forEach(([p,h,f])=>cow(W*p,bandY-1,h,f));
// patterned band at 4.2 ft
g.fillStyle='#ecd9bd';g.fillRect(0,bandY,W,5);g.fillRect(0,bandY+56,W,5);g.fillStyle='#8c4a2b';g.fillRect(0,bandY+5,W,51);g.fillStyle='#ecd9bd';for(let x=12;x<W;x+=44){g.save();g.translate(x,bandY+30);g.rotate(Math.PI/4);g.fillRect(-9,-9,18,18);g.restore();g.beginPath();g.arc(x+22,bandY+30,3.5,0,7);g.fill();g.fillRect(x+6,bandY+11,20,2.5);g.fillRect(x+6,bandY+47,20,2.5)}
// lotus row 2.7 to 4.2 ft
function lotus(x,base,h,s){g.strokeStyle='#6c9a6f';g.lineWidth=5;g.beginPath();g.moveTo(x,base);g.quadraticCurveTo(x-22,base-h*.5,x,base-h);g.stroke();const y=base-h;
  for(const[n,r,c]of[[9,50,'#f6f0e2'],[7,34,'#f1dfc7'],[5,20,'#eecfb0']]){for(let i=0;i<n;i++){const a=-Math.PI*.95+i/(n-1)*Math.PI*.9;g.save();g.translate(x,y);g.rotate(a+Math.PI/2);g.fillStyle=c;g.beginPath();g.moveTo(0,0);g.quadraticCurveTo(-r*.42*s,-r*.55*s,0,-r*1.15*s);g.quadraticCurveTo(r*.42*s,-r*.55*s,0,0);g.fill();g.strokeStyle='rgba(150,100,70,.3)';g.lineWidth=1;g.stroke();g.restore()}}
  g.fillStyle='#e5a93c';g.beginPath();g.ellipse(x,y-4,14*s,7*s,0,0,7);g.fill()}
const LB=yy(2.72),LH=yy(4.05);for(let i=0;i<7;i++){const x=W*(.1+i*.133);lotus(x,LB,(LB-LH)*.82,1.15);
 g.fillStyle='#7ba07a';g.strokeStyle='#567a58';g.lineWidth=2;const lx=x+W*.066;g.beginPath();g.ellipse(lx,LB-46,56,17,rnd(-.12,.12),0,7);g.fill();g.stroke();g.strokeStyle='#6c9a6f';g.lineWidth=4;g.beginPath();g.moveTo(lx,LB);g.lineTo(lx,LB-38);g.stroke()}
// blossom branches at top
function branch(x,y,a,len,w,d=0){if(d>8||len<9)return;const nx=x+Math.cos(a)*len,ny=y+Math.sin(a)*len;g.strokeStyle='#4f2e1d';g.lineWidth=w;g.lineCap='round';g.beginPath();g.moveTo(x,y);g.quadraticCurveTo((x+nx)/2+rnd(-9,9),(y+ny)/2+rnd(-9,9),nx,ny);g.stroke();
  if(d>3)for(let i=0;i<2;i++){const bx=nx+rnd(-14,14),by=ny+rnd(-14,14);g.fillStyle=rnd()>.2?'#f7f1e4':'#efd9ae';for(let k=0;k<5;k++){const t=k/5*6.28;g.beginPath();g.ellipse(bx+Math.cos(t)*4.6,by+Math.sin(t)*4.6,4,3,t,0,7);g.fill()}g.fillStyle='#d9a23a';g.beginPath();g.arc(bx,by,1.8,0,7);g.fill()}
  branch(nx,ny,a+rnd(.2,.7),len*rnd(.66,.85),w*.7,d+1);branch(nx,ny,a-rnd(.2,.7),len*rnd(.66,.85),w*.7,d+1)}
[[.02,.25],[.26,.55],[.74,2.6],[.98,2.9]].forEach(([p,a])=>branch(W*p,4,a,86,8));
fs.writeFileSync(out+'/mural.jpg',c.toBuffer('image/jpeg',{quality:.93}));

// jute weave colour + normal-ish height
{const s=2048,k=createCanvas(s,s),q=k.getContext('2d');q.fillStyle='#b8935f';q.fillRect(0,0,s,s);const cell=20;for(let y=0;y<s;y+=cell)for(let x=0;x<s;x+=cell){const odd=((x+y)/cell)%2;const base=['#a98551','#c3a071','#b8935f','#ceb086','#9d7a47'][Math.floor(rnd(5))];const gr=odd?q.createLinearGradient(x,y,x,y+cell):q.createLinearGradient(x,y,x+cell,y);gr.addColorStop(0,'#6f5430');gr.addColorStop(.25,base);gr.addColorStop(.75,base);gr.addColorStop(1,'#6f5430');q.fillStyle=gr;q.fillRect(x,y,cell,cell);q.strokeStyle='rgba(70,50,25,.35)';q.lineWidth=1;for(let i=0;i<3;i++){q.beginPath();if(odd){const px=x+rnd(cell);q.moveTo(px,y);q.lineTo(px+rnd(-2,2),y+cell)}else{const py=y+rnd(cell);q.moveTo(x,py);q.lineTo(x+cell,py+rnd(-2,2))}q.stroke()}}fs.writeFileSync(out+'/jute.jpg',k.toBuffer('image/jpeg',{quality:.9}))}

// cane panel with real holes (alpha) for screens and shutters
{const s=1024,k=createCanvas(s,s),q=k.getContext('2d');q.clearRect(0,0,s,s);q.strokeStyle='#c9a26c';q.lineCap='round';const n=16,st=s/n;for(let i=-n;i<=2*n;i++){q.lineWidth=7;q.beginPath();q.moveTo(i*st,0);q.lineTo(i*st,s);q.stroke();q.beginPath();q.moveTo(0,i*st);q.lineTo(s,i*st);q.stroke();q.strokeStyle='#b58d57';q.lineWidth=6;q.beginPath();q.moveTo(i*st,0);q.lineTo(i*st+s,s);q.stroke();q.beginPath();q.moveTo(i*st+s,0);q.lineTo(i*st,s);q.stroke();q.strokeStyle='#c9a26c'}fs.writeFileSync(out+'/cane.png',k.toBuffer('image/png'))}

// painted bird panel for the oval screen (photo 5)
{const pw=600,ph=1500,k=createCanvas(pw,ph),q=k.getContext('2d');q.fillStyle='#ece3cf';q.fillRect(0,0,pw,ph);for(let i=0;i<9000;i++){q.fillStyle=i%2?'#e3d8c0':'#f3ecdc';q.globalAlpha=.25;q.fillRect(rnd(pw),rnd(ph),2,2)}q.globalAlpha=1;
 const br=(x,y,a,len,w,d=0)=>{if(d>8||len<9)return;const nx=x+Math.cos(a)*len,ny=y+Math.sin(a)*len;q.strokeStyle='#5d3f27';q.lineWidth=w;q.lineCap='round';q.beginPath();q.moveTo(x,y);q.quadraticCurveTo((x+nx)/2+rnd(-14,14),(y+ny)/2+rnd(-14,14),nx,ny);q.stroke();if(d>3)for(let i=0;i<5;i++){q.fillStyle=['#8fae86','#c8cf9e','#e6c4c0','#d7b65a','#6f9674'][Math.floor(rnd(5))];q.beginPath();q.ellipse(nx+rnd(-20,20),ny+rnd(-20,20),rnd(5,11),rnd(2.5,5),rnd(3),0,7);q.fill()}br(nx,ny,a+rnd(.2,.65),len*rnd(.68,.86),w*.7,d+1);br(nx,ny,a-rnd(.2,.65),len*rnd(.68,.86),w*.7,d+1)};
 br(pw*.2,ph,-1.25,190,20);br(pw*.8,ph*.42,-2.4,130,12);
 const bird=(x,y,s,c,c2)=>{q.save();q.translate(x,y);q.scale(s,s);q.fillStyle=c;q.beginPath();q.ellipse(0,0,40,20,-.4,0,7);q.fill();q.fillStyle=c2;q.beginPath();q.ellipse(-8,-1,26,10,-.55,0,7);q.fill();q.fillStyle=c;q.beginPath();q.moveTo(-28,14);q.lineTo(-140,76);q.lineTo(-100,80);q.lineTo(-22,24);q.fill();q.beginPath();q.arc(34,-20,14,0,7);q.fill();q.fillStyle='#d9a23a';q.beginPath();q.moveTo(46,-22);q.lineTo(64,-18);q.lineTo(46,-14);q.fill();q.fillStyle='#111';q.beginPath();q.arc(38,-23,2.5,0,7);q.fill();q.restore()};
 bird(pw*.62,ph*.2,1.5,'#26425e','#7f9cb5');bird(pw*.38,ph*.5,1.25,'#b58c2e','#e3c777');bird(pw*.66,ph*.76,1.35,'#2a2a2a','#bdb6a6');fs.writeFileSync(out+'/birds.jpg',k.toBuffer('image/jpeg',{quality:.92}))}
console.log('art done');
