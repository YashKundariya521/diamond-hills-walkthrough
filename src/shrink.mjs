import {NodeIO,PropertyType} from '@gltf-transform/core';
import {ALL_EXTENSIONS} from '@gltf-transform/extensions';
import {dedup,prune,weld,simplify,meshopt} from '@gltf-transform/functions';
import {MeshoptEncoder,MeshoptSimplifier} from 'meshoptimizer';
import fs from 'fs';
const ERR=+(process.argv[2]||0.0004);
await MeshoptEncoder.ready;await MeshoptSimplifier.ready;
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.encoder':MeshoptEncoder});
const doc=await io.read('out/scene.glb');
const tris=()=>{let t=0;for(const m of doc.getRoot().listMeshes())for(const p of m.listPrimitives()){const i=p.getIndices();t+=(i?i.getCount():p.getAttribute('POSITION').getCount())/3}return t};
console.log('before tris',Math.round(tris()));
await doc.transform(dedup({propertyTypes:[PropertyType.ACCESSOR,PropertyType.TEXTURE,PropertyType.MATERIAL]}),prune({keepAttributes:true,keepIndices:true,keepLeaves:true}),weld());
await doc.transform(simplify({simplifier:MeshoptSimplifier,ratio:0,error:ERR,lockBorder:true,cleanup:false,
  }));
console.log('after tris',Math.round(tris()));
await doc.transform(meshopt({encoder:MeshoptEncoder,level:'medium',quantizePosition:14,quantizeNormal:10,quantizeColor:8,quantizeTexcoord:16}));
await io.write('out/scene.min.glb',doc);
console.log('MB',(fs.statSync('out/scene.min.glb').size/1e6).toFixed(1));
