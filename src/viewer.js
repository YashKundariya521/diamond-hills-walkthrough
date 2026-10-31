import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RGBELoader} from 'three/addons/loaders/RGBELoader.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';

const FT=.3048,S=60.5,OX=1163,OY=217,EYE=5.5*FT,RAD=.24,LSCALE=8,VSCALE=8;
const PX=p=>(p-OX)/S*FT,PZ=p=>(p-OY)/S*FT;
const $=id=>document.getElementById(id);
const b64=async id=>{const el=$(id),gz=el.dataset.gz==='1',s=atob(el.textContent.trim());const a=new Uint8Array(s.length);for(let i=0;i<s.length;i++)a[i]=s.charCodeAt(i);el.remove();if(!gz)return a;
  return new Uint8Array(await new Response(new Blob([a]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer())};
const status=t=>{$('load').textContent=t};
const tick=()=>new Promise(r=>setTimeout(r,20));

const canvas=$('c');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true,powerPreference:'high-performance'});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.08;
const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(62,1,.05,6000);camera.rotation.order='YXZ';

const layout=JSON.parse(atob($('layout').textContent.trim()));
const ROOMS=layout.rooms,colliders=layout.colliders.map(c=>({x1:PX(Math.min(c[0],c[2])),z1:PZ(Math.min(c[1],c[3])),x2:PX(Math.max(c[0],c[2])),z2:PZ(Math.max(c[1],c[3])),name:c[4]}));

const TINT={fwarm:[.96,.92,.85],fgrey:[.72,.71,.68],fkota:[.5,.51,.47],terra:[.62,.25,.12],jacquard:[.95,.8,.55],rustcurt:[.6,.25,.12],walnut:[.62,.46,.34],teak:[.8,.66,.52],fstone:[.8,.78,.74],plaster:[.75,.68,.6]};
// baked-light shader: diffuse light comes from the bake, reflections from the current room's panorama
const U={uBoxMin:{value:new THREE.Vector3()},uBoxMax:{value:new THREE.Vector3()},uProbe:{value:new THREE.Vector3()}};
function bakedMaterial(src,mode,lightTex){
  const m=src.clone();m.vertexColors=false;m.lightMap=null;m.aoMap=null;m.envMapIntensity=1;
  const tn=TINT[src.name];if(tn)m.color.setRGB(tn[0],tn[1],tn[2]);
  if(src.name==='cane'){m.alphaTest=0;m.transparent=true;m.depthWrite=false;m.side=THREE.DoubleSide}
  m.onBeforeCompile=sh=>{
    Object.assign(sh.uniforms,U);if(mode==='lm')sh.uniforms.uLM={value:lightTex};
    sh.vertexShader=sh.vertexShader.replace('#include <common>',`#include <common>
      varying vec3 vWP; ${mode==='lm'?'attribute vec2 uv1lm; varying vec2 vLM;':'attribute vec3 bakeColor; varying vec3 vBake;'}`)
      .replace('#include <begin_vertex>',`#include <begin_vertex>
      vWP=(modelMatrix*vec4(transformed,1.)).xyz; ${mode==='lm'?'vLM=uv1lm;':'vBake=bakeColor;'}`);
    const pars=THREE.ShaderChunk.envmap_physical_pars_fragment.replace('reflectVec = inverseTransformDirection( reflectVec, viewMatrix );',
      `reflectVec = inverseTransformDirection( reflectVec, viewMatrix );
       { vec3 rd=normalize(reflectVec); vec3 t1=(uBoxMax-vWP)/rd; vec3 t2=(uBoxMin-vWP)/rd; vec3 tm=max(t1,t2); float d=min(min(tm.x,tm.y),tm.z); reflectVec=normalize(vWP+rd*d-uProbe); }`);
    sh.fragmentShader=sh.fragmentShader.replace('#include <common>',`#include <common>
      varying vec3 vWP; uniform vec3 uBoxMin,uBoxMax,uProbe; ${mode==='lm'?'varying vec2 vLM; uniform sampler2D uLM;':'varying vec3 vBake;'}`)
      .replace('#include <envmap_physical_pars_fragment>',pars)
      .replace('#include <lights_fragment_end>',`#include <lights_fragment_end>
      { vec3 bk=${mode==='lm'?'texture2D(uLM,vLM).rgb':'vBake'}; bk=bk*bk*${(mode==='lm'?LSCALE:VSCALE).toFixed(1)};
        float nd=clamp(dot(normal,normalize(vNormal)),0.,1.); bk*=mix(.72,1.,nd*nd);
        reflectedLight.indirectDiffuse=bk*material.diffuseColor/1.0*RECIPROCAL_PI*PI; reflectedLight.directDiffuse=vec3(0.); }`);
  };
  m.customProgramCacheKey=()=>mode+(src.alphaTest>0?'a':'')+(src.name==='cane'?'c':'');return m}

function setupMaterials(root,lightTex){
  const cache=new Map();let stats={lm:0,v:0,other:0,noColor:[]};
  const special={glass:()=>new THREE.MeshPhysicalMaterial({color:0xdfeee9,transparent:true,opacity:.1,roughness:.02,metalness:0,side:THREE.DoubleSide,depthWrite:false}),
    sheer:()=>new THREE.MeshStandardMaterial({color:0xfff6e6,transparent:true,opacity:.72,roughness:1,side:THREE.DoubleSide,emissive:0xffe8cc,emissiveIntensity:.55,depthWrite:false}),
    led:()=>new THREE.MeshBasicMaterial({color:new THREE.Color(2.4,1.9,1.3)})};
  root.traverse(o=>{if(!o.isMesh)return;
    const g=o.geometry,nm=o.material.name||'',isShell=o.name.startsWith('SHELL')||(o.parent&&o.parent.name==='SHELL');
    if(special[nm]){const k='s'+nm;if(!cache.has(k))cache.set(k,special[nm]());o.material=cache.get(k);stats.other++;o.renderOrder=nm==='led'?0:2;return}
    const own=(o.name+' '+(o.parent?o.parent.name:'')).toLowerCase();if(/washer|basket/.test(own)){o.material=o.material.clone();o.material.metalness=0;o.material.roughness=.45;o.material.color.setRGB(.8,.8,.78);}
    const uvLM=g.attributes.uv1;
    if(isShell&&uvLM){g.setAttribute('uv1lm',uvLM);const k='L'+o.material.uuid;if(!cache.has(k))cache.set(k,bakedMaterial(o.material,'lm',lightTex));o.material=cache.get(k);stats.lm++;return}
    if(g.attributes.color){g.setAttribute('bakeColor',g.attributes.color);g.deleteAttribute('color')}
    if(g.attributes.bakeColor){const k='V'+o.material.uuid;if(!cache.has(k)){const c=bakedMaterial(o.material,'v');if(c.alphaTest>0)c.side=THREE.DoubleSide;cache.set(k,c)}o.material=cache.get(k);stats.v++;return}
    stats.other++;stats.noColor.push(o.name+'/'+nm)});
  return stats}

async function start(){
  status('Unpacking the flat…');await tick();
  const rgbe=new RGBELoader(),hdrFrom=async id=>{const d=await b64(id);const t=rgbe.parse(d.buffer);const x=new THREE.DataTexture(t.data,t.width,t.height,THREE.RGBAFormat,t.type);x.colorSpace=THREE.LinearSRGBColorSpace;x.minFilter=x.magFilter=THREE.LinearFilter;x.mapping=THREE.EquirectangularReflectionMapping;x.flipY=true;x.needsUpdate=true;return x};
  const lmBlob=new Blob([await b64('lightmap')],{type:'image/jpeg'});const lmBmp=await createImageBitmap(lmBlob,{imageOrientation:'none',colorSpaceConversion:'none'});
  const lightTex=new THREE.Texture(lmBmp);lightTex.flipY=false;lightTex.colorSpace=THREE.NoColorSpace;lightTex.generateMipmaps=true;lightTex.minFilter=THREE.LinearMipmapLinearFilter;lightTex.magFilter=THREE.LinearFilter;lightTex.anisotropy=8;lightTex.needsUpdate=true;
  status('Loading furniture and materials…');await tick();
  await MeshoptDecoder.ready;const glb=await b64('glb');const gltf=await new Promise((res,rej)=>new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).parse(glb.buffer,'',res,rej));
  scene.add(gltf.scene);window.__stats=setupMaterials(gltf.scene,lightTex);
  const aniso=renderer.capabilities.getMaxAnisotropy();gltf.scene.traverse(o=>{if(o.isMesh&&o.material&&o.material.map)o.material.map.anisotropy=aniso});
  status('Preparing daylight…');await tick();
  const sky=await hdrFrom('sky');sky.minFilter=sky.magFilter=THREE.LinearFilter;
  const skyMesh=new THREE.Mesh(new THREE.SphereGeometry(3000,48,24),new THREE.MeshBasicMaterial({map:sky,side:THREE.BackSide,depthWrite:false,toneMapped:true}));skyMesh.rotation.y=Math.PI*.5;scene.add(skyMesh);
  const ground=new THREE.Mesh(new THREE.CircleGeometry(2800,48),new THREE.MeshBasicMaterial({color:new THREE.Color(.82,.8,.72),fog:false}));ground.rotation.x=-Math.PI/2;ground.position.y=-30;scene.add(ground);
  const pm=new THREE.PMREMGenerator(renderer);const ENV=[];
  for(let i=0;i<ROOMS.length;i++){const id='env'+i;if(!$(id)){ENV.push(null);continue}const t=await hdrFrom(id);ENV.push(pm.fromEquirectangular(t).texture);t.dispose();if(i%4===0){status(`Preparing daylight… ${Math.round(i/ROOMS.length*100)}%`);await tick()}}
  scene.environmentRotation=new THREE.Euler(0,window.ENVROT??-Math.PI/2,0);
  buildUI();const applyEnv=R=>{const i=ROOMS.indexOf(R);if(i>=0&&ENV[i])scene.environment=ENV[i];const[a,b,c,d]=R.r;U.uBoxMin.value.set(PX(a),0,PZ(b));U.uBoxMax.value.set(PX(c),9*FT,PZ(d));U.uProbe.value.set((PX(a)+PX(c))/2,1.5,(PZ(b)+PZ(d))/2)};
  window.__applyEnv=applyEnv;applyEnv(ROOMS.find(r=>r.n==='Foyer'));
  renderer.compile(scene,camera);$('load').remove();
  let last=performance.now();const frame=now=>{const dt=Math.min(.05,(now-last)/1000);last=now;move(dt);camera.position.set(P.x,EYE,P.z);camera.rotation.set(P.pitch,P.yaw,0);const R=roomAt(P.x,P.z);if(R!==curRoom&&R)applyEnv(R);setRoom(R);drawMap(curRoom);renderer.render(scene,camera);requestAnimationFrame(frame)};requestAnimationFrame(frame)
}

// ---------- player ----------
const P={x:PX(4750),z:PZ(2130),yaw:Math.PI,pitch:-.03},vel={x:0,z:0},keys={};
addEventListener('keydown',e=>{keys[e.code]=true;if(e.code==='KeyN')$('notes').classList.toggle('on');if(e.code==='KeyL')toggleLabels();if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].includes(e.code))e.preventDefault()});
addEventListener('keyup',e=>keys[e.code]=false);addEventListener('blur',()=>{for(const k in keys)keys[k]=false});
let drag=false,lx=0,ly=0;canvas.addEventListener('pointerdown',e=>{drag=true;lx=e.clientX;ly=e.clientY;canvas.setPointerCapture(e.pointerId);canvas.style.cursor='grabbing'});
canvas.addEventListener('pointermove',e=>{if(!drag)return;P.yaw-=(e.clientX-lx)*.0042;P.pitch=Math.max(-1.35,Math.min(1.35,P.pitch-(e.clientY-ly)*.0036));lx=e.clientX;ly=e.clientY});
const endDrag=()=>{drag=false;canvas.style.cursor='grab'};canvas.addEventListener('pointerup',endDrag);canvas.addEventListener('pointercancel',endDrag);
const hit=(x,z,r=RAD)=>{for(const c of colliders)if(x>c.x1-r&&x<c.x2+r&&z>c.z1-r&&z<c.z2+r)return true;return false};
const roomAt=(x,z)=>{const px=x/FT*S+OX,pz=z/FT*S+OY;for(const R of ROOMS){const[a,b,c,d]=R.r;if(px>=a&&px<=c&&pz>=b&&pz<=d)return R}return null};
function move(dt){let f=(keys.KeyW||keys.ArrowUp?1:0)-(keys.KeyS||keys.ArrowDown?1:0),s=(keys.KeyD||keys.ArrowRight?1:0)-(keys.KeyA||keys.ArrowLeft?1:0);const L=Math.hypot(f,s)||1;f/=L;s/=L;const sp=keys.ShiftLeft||keys.ShiftRight?2.8:1.6;
  const si=Math.sin(P.yaw),co=Math.cos(P.yaw),tx=(-si*f+co*s)*sp,tz=(-co*f-si*s)*sp,a=Math.min(1,dt*11);vel.x+=(tx-vel.x)*a;vel.z+=(tz-vel.z)*a;
  const nx=P.x+vel.x*dt;if(!hit(nx,P.z))P.x=nx;else vel.x=0;const nz=P.z+vel.z*dt;if(!hit(P.x,nz))P.z=nz;else vel.z=0}

// ---------- labels, minimap, room names ----------
const labelGroup=new THREE.Group();labelGroup.visible=false;scene.add(labelGroup);let labelsBuilt=false;
function fmt(f){const t=Math.round(f*12),a=Math.floor(t/12),c=t%12;return c?`${a}'${c}"`:`${a}'`}
function toggleLabels(){if(!labelsBuilt){layout.items.filter(i=>i.label).forEach(i=>{const c=document.createElement('canvas');c.width=420;c.height=104;const g=c.getContext('2d');g.fillStyle='rgba(32,22,14,.86)';g.beginPath();g.roundRect(0,0,420,104,16);g.fill();g.textAlign='center';g.fillStyle='#fff3df';g.font='600 34px -apple-system,Helvetica,Arial';g.fillText(i.name,210,43);g.fillStyle='#f0c98c';g.font='30px -apple-system,Helvetica,Arial';g.fillText(`${fmt(i.dims[0])} x ${fmt(i.dims[1])}`,210,84);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;const s=new THREE.Sprite(new THREE.SpriteMaterial({map:t,toneMapped:false}));s.position.set(PX((i.r[0]+i.r[2])/2),1.5,PZ((i.r[1]+i.r[3])/2));s.scale.set(.75,.186,1);labelGroup.add(s)});labelsBuilt=true}labelGroup.visible=!labelGroup.visible}
const mm=$('mm'),mc=mm.getContext('2d'),mb={x1:760,y1:190,x2:5740,y2:4140},ms=mm.width/(mb.x2-mb.x1);mm.height=(mb.y2-mb.y1)*ms;const mx=p=>(p-mb.x1)*ms,my=p=>(p-mb.y1)*ms;const mmBase=document.createElement('canvas');mmBase.width=mm.width;mmBase.height=mm.height;
{const g=mmBase.getContext('2d');g.fillStyle='rgba(30,22,16,.84)';g.fillRect(0,0,mm.width,mm.height);g.fillStyle='rgba(255,240,220,.14)';ROOMS.forEach(R=>g.fillRect(mx(R.r[0]),my(R.r[1]),(R.r[2]-R.r[0])*ms,(R.r[3]-R.r[1])*ms));g.fillStyle='#f4e7d2';layout.colliders.filter(c=>['wall','window','glass','lift','rail'].includes(c[4])).forEach(c=>g.fillRect(mx(c[0]),my(c[1]),Math.max(1.3,(c[2]-c[0])*ms),Math.max(1.3,(c[3]-c[1])*ms)))}
function drawMap(cur){mc.clearRect(0,0,mm.width,mm.height);mc.drawImage(mmBase,0,0);if(cur){mc.fillStyle='rgba(232,150,70,.38)';mc.fillRect(mx(cur.r[0]),my(cur.r[1]),(cur.r[2]-cur.r[0])*ms,(cur.r[3]-cur.r[1])*ms)}const x=mx(P.x/FT*S+OX),y=my(P.z/FT*S+OY);mc.save();mc.translate(x,y);mc.rotate(-P.yaw);mc.fillStyle='rgba(255,120,60,.32)';mc.beginPath();mc.moveTo(0,0);mc.arc(0,0,22,-Math.PI/2-.55,-Math.PI/2+.55);mc.fill();mc.restore();mc.fillStyle='#ff5a2a';mc.strokeStyle='#fff';mc.lineWidth=1.5;mc.beginPath();mc.arc(x,y,4.4,0,7);mc.fill();mc.stroke()}
let curRoom=null,toastT;const toast=$('toast');
function setRoom(R){if(R===curRoom)return;curRoom=R;if(!R)return;toast.innerHTML=`<b>${R.n}</b><span>${R.size}</span>`;toast.classList.add('on');clearTimeout(toastT);toastT=setTimeout(()=>toast.classList.remove('on'),2600);$('now').textContent=R.n}
const VIEWS={'Drawing Room':[3760,2560,-112],'Living Room':[3150,2550,124],'Dining':[3200,1810,120],'Foyer':[4800,2300,82],'Balcony':[4680,3980,74],'Kitchen':[3150,1500,54],'Master Room':[2000,3500,30],"Son's Bedroom":[2150,950,50],"Daughter's Room":[3700,1300,-143],'Guest Room':[5100,2650,-120],'Theater Room':[1890,2320,34],'Temple':[3450,2040,-159],'Wash':[3200,600,70],'Utility':[3500,480,-150],"Son's Bath":[1450,1330,165],"Master's Bath":[1450,2610,15],"Daughter's Bath":[3880,1040,20],'Guest Bath':[5320,2260,10],"Son's Dressing":[2150,1340,90],"Master's Dressing":[2150,2610,90],'Passage':[2250,2300,20]};
function freeSpot(R){let best=null,bs=-1;const[a,b,c,d]=R.r;for(let i=1;i<18;i++)for(let j=1;j<18;j++){const x=PX(a+(c-a)*i/18),z=PZ(b+(d-b)*j/18);if(hit(x,z,RAD+.05))continue;let free=99;for(const k of colliders){const dx=Math.max(k.x1-x,0,x-k.x2),dz=Math.max(k.z1-z,0,z-k.z2);free=Math.min(free,Math.hypot(dx,dz))}if(free>bs){bs=free;best=[x,z]}}return best}
function go(name,yaw,x,z){const R=ROOMS.find(r=>r.n===name);if(!R)return false;const V=VIEWS[name];if(V&&x===undefined&&yaw===undefined){x=PX(V[0]);z=PZ(V[1]);yaw=V[2]}const p=x!==undefined&&!hit(x,z)?[x,z]:freeSpot(R);if(!p)return false;P.x=p[0];P.z=p[1];P.yaw=(yaw??0)*Math.PI/180;P.pitch=-.04;vel.x=vel.z=0;return true}
function buildUI(){const sel=$('jump');ROOMS.forEach(R=>{const o=document.createElement('option');o.value=R.n;o.textContent=R.n;sel.appendChild(o)});sel.addEventListener('change',()=>{if(sel.value)go(sel.value);sel.value='';sel.blur()})}
function reachability(){const st=.075,x0=-3,z0=-1,w=Math.ceil(30/st),h=Math.ceil(23/st),seen=new Uint8Array(w*h),q=[[PX(4750),PZ(2130)]],id=(x,z)=>Math.round((z-z0)/st)*w+Math.round((x-x0)/st);seen[id(q[0][0],q[0][1])]=1;const reached=new Set();while(q.length){const[x,z]=q.pop();const R=roomAt(x,z);if(R)reached.add(R.n);for(const[a,c]of[[st,0],[-st,0],[0,st],[0,-st]]){const nx=x+a,nz=z+c;if(nx<x0||nz<z0||nx>x0+30||nz>z0+23)continue;const k=id(nx,nz);if(seen[k]||hit(nx,nz))continue;seen[k]=1;q.push([nx,nz])}}return{reached:[...reached],missing:ROOMS.map(r=>r.n).filter(n=>!reached.has(n))}}
window.walk={go,P,hit,press:(c,v)=>keys[c]=v,reachability,renderer,scene,camera,info:()=>renderer.info.render,rooms:ROOMS,exposure:v=>renderer.toneMappingExposure=v};
function resize(){renderer.setSize(innerWidth,innerHeight,false);camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix()}addEventListener('resize',resize);resize();
start().catch(e=>{console.error(e);status('Could not load: '+e.message)});
