import base64,json,os,subprocess,sys
hq=os.path.dirname(os.path.abspath(__file__));out=f'{hq}/out';dst=sys.argv[1]
env=dict(os.environ)
subprocess.check_call(['npx','esbuild','viewer.js','--bundle','--minify','--format=iife','--target=es2020','--outfile=viewer.bundle.js','--log-level=warning'],cwd=hq,env=env)
js=open(f'{hq}/viewer.bundle.js',encoding='utf-8').read().replace('</script>','<\\/script>')
b=lambda p:base64.b64encode(open(p,'rb').read()).decode()
lay=json.load(open(f'{out}/layout.json'))
notes=[
 'Every room is furnished. Bath fixtures, kitchen cabinets, rugs, poufs, the jhula and most plants are additions; none are drawn on the plan.',
 'The mandir holds a plain brass kalash, not a murti.',
 'Light was calculated once in Blender and stored, so it does not change as you move. Reflections are approximate.',
 'The mural, bird panels and jute are drawn in code, so they are simpler than your photos.',
 'Sofas, chairs and plants are from your model packs, recoloured and resized to fit the plan.',
]
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Diamond Hills Walkthrough</title>
<style>:root{{--ink:#fff3df;--bg:rgba(30,22,16,.84);--ac:#e8964a}}html,body{{margin:0;height:100%;background:#1e1610;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;color:var(--ink)}}
#c{{position:fixed;inset:0;width:100%;height:100%;display:block;cursor:grab;touch-action:none}}#mm{{position:fixed;top:14px;right:14px;width:250px;border-radius:10px;box-shadow:0 4px 18px rgba(0,0,0,.4)}}
#hud{{position:fixed;top:14px;left:14px;background:var(--bg);border-radius:10px;padding:10px 12px;font-size:13px;line-height:1.55;max-width:300px}}#hud b{{color:var(--ac);font-weight:600}}#now{{display:block;font-size:15px;font-weight:600;margin-bottom:4px}}#hud select{{margin-top:7px;width:100%;background:#3a2b1f;color:var(--ink);border:1px solid #6b5138;border-radius:6px;padding:4px;font:inherit}}
#toast{{position:fixed;left:50%;bottom:34px;transform:translate(-50%,10px);background:var(--bg);padding:11px 22px;border-radius:12px;text-align:center;opacity:0;transition:.35s;pointer-events:none}}#toast.on{{opacity:1;transform:translate(-50%,0)}}#toast b{{display:block;font-size:20px;font-weight:600}}#toast span{{font-size:13px;color:#f0c98c}}
#notes{{position:fixed;left:14px;bottom:14px;background:var(--bg);border-radius:10px;padding:12px 14px;font-size:13px;line-height:1.5;max-width:430px;display:none}}#notes.on{{display:block}}#notes h2{{margin:0 0 6px;font-size:14px;color:var(--ac)}}#notes ul{{margin:0;padding-left:17px}}
#load{{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;font-size:16px;background:#1e1610;z-index:5}}@media(max-width:640px){{#mm{{width:150px}}#hud{{font-size:12px;max-width:170px}}}}</style></head><body>
<canvas id="c"></canvas><div id="load">Opening the flat. This large file can take a minute…</div><canvas id="mm" width="500" height="400"></canvas>
<div id="hud"><span id="now">Foyer</span><b>WASD</b> move &middot; <b>drag</b> look &middot; <b>Shift</b> faster<br><b>L</b> furniture sizes &middot; <b>N</b> notes<select id="jump"><option value="">Jump to a room&hellip;</option></select></div>
<div id="toast"></div><div id="notes"><h2>Notes</h2><ul>{''.join('<li>'+n+'</li>' for n in notes)}</ul></div>
<script type="text/plain" id="layout">{base64.b64encode(json.dumps(lay).encode()).decode()}</script>
<script type="text/plain" id="lightmap">{b(f'{out}/lightmap.jpg')}</script>
<script type="text/plain" id="glb">{b(f'{out}/scene.glb')}</script>
<script type="text/plain" id="sky">{b(f'{out}/sky.hdr')}</script>
{''.join(f'<script type="text/plain" id="env{i}">{b(f"{out}/env_{i}.hdr")}</script>' for i in range(len(lay['rooms'])) if os.path.exists(f"{out}/env_{i}.hdr"))}
<script>{js}</script></body></html>'''
open(dst,'w',encoding='utf-8').write(html);print(dst,round(os.path.getsize(dst)/1e6,1),'MB')
