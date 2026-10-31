import {NodeIO,PropertyType} from '@gltf-transform/core';
import {ALL_EXTENSIONS} from '@gltf-transform/extensions';
import {dedup,prune,weld,meshopt} from '@gltf-transform/functions';
import {MeshoptEncoder,MeshoptSimplifier} from 'meshoptimizer';
import fs from 'fs';
// Baked light lives on the vertices, so flat surfaces must keep enough of them. Each mesh keeps at least KEEP of its triangles.
const KEEP=+(process.argv[2]||0.25),ERR=+(process.argv[3]||0.002),MIN=20000;
await MeshoptEncoder.ready;await MeshoptSimplifier.ready;
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.encoder':MeshoptEncoder});
const doc=await io.read('out/scene.glb');
const count=()=>{let t=0;for(const m of doc.getRoot().listMeshes())for(const p of m.listPrimitives())t+=p.getIndices().getCount()/3;return t};
console.log('before tris',Math.round(count()));
await doc.transform(dedup({propertyTypes:[PropertyType.ACCESSOR,PropertyType.TEXTURE,PropertyType.MATERIAL]}),prune({keepAttributes:true,keepIndices:true,keepLeaves:true}),weld());
if(KEEP<1){const seen=new Set();for(const m of doc.getRoot().listMeshes())for(const p of m.listPrimitives()){
  const ix=p.getIndices(),pos=p.getAttribute('POSITION');if(ix.getCount()/3<MIN||seen.has(ix))continue;seen.add(ix);
  const target=Math.floor(ix.getCount()*KEEP/3)*3;const [out]=MeshoptSimplifier.simplify(Uint32Array.from(ix.getArray()),new Float32Array(pos.getArray()),3,target,ERR,['LockBorder']);
  ix.setArray(out.length<65536||pos.getCount()<65536?Uint16Array.from(out):out)}}
console.log('after tris',Math.round(count()));
await doc.transform(prune({keepAttributes:true,keepIndices:true,keepLeaves:true}));
await doc.transform(meshopt({encoder:MeshoptEncoder,level:'medium',quantizePosition:14,quantizeNormal:10,quantizeColor:8,quantizeTexcoord:16}));
await io.write('out/scene.min.glb',doc);
console.log('MB',(fs.statSync('out/scene.min.glb').size/1e6).toFixed(1));
