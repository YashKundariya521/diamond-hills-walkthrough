import {createCanvas,loadImage} from 'canvas';import fs from 'fs';
const [src,dst,r,g,b,gain='1.0']=process.argv.slice(2);const im=await loadImage(src);const c=createCanvas(im.width,im.height),x=c.getContext('2d');x.drawImage(im,0,0);const d=x.getImageData(0,0,im.width,im.height),p=d.data;
for(let i=0;i<p.length;i+=4){const R=p[i],G=p[i+1],B=p[i+2],mx=Math.max(R,G,B),mn=Math.min(R,G,B),sat=mx?(mx-mn)/mx:0;if(sat<.24){const l=(R+G+B)/3/255;const k=Math.pow(l/.42,.75)*(+gain);p[i]=Math.min(255,r*k);p[i+1]=Math.min(255,g*k);p[i+2]=Math.min(255,b*k)}}
x.putImageData(d,0,0);fs.writeFileSync(dst,c.toBuffer('image/jpeg',{quality:.92}));
