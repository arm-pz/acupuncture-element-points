import os, io, base64, json, re
from PIL import Image

def get_base64_images():
    codes = ['CV13', 'CV9', 'CV7', 'CV6', 'CV5', 'CV8']
    data_uris = {}
    for code in codes:
        path = f'data/cv_images/{code}.png'
        if not os.path.exists(path):
            continue
        im = Image.open(path)
        bg = Image.new('RGB', im.size, (255, 255, 255))
        if im.mode == 'RGBA':
            bg.paste(im, mask=im.split()[3])
        else:
            bg.paste(im)
        buf = io.BytesIO()
        bg.save(buf, format='JPEG', quality=85, optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode('ascii')
        data_uris[code] = f"data:image/jpeg;base64,{b64}"
    return data_uris

def update():
    imgs = get_base64_images()
    print(f"Loaded {len(imgs)} images")
    
    chart_py = 'tools/create_cv_chart.py'
    with open(chart_py, 'r', encoding='utf-8') as f:
        content = f.read()

    imgs_js = "var IMGS = " + json.dumps(imgs) + ";\n"
    
    # Check if IMGS already in create_cv_chart.py
    if "var IMGS =" in content:
        content = re.sub(r'var IMGS = \{.*?\};\n', imgs_js, content, flags=re.DOTALL)
    else:
        # insert right before var currentId = null;
        content = content.replace("var currentId = null;", imgs_js + "var currentId = null;")
        
    # Update render function to include figure/img
    old_render = """function render(id){
  var d = DATA[id];
  if(!d) return;
  var col = 'var(--' + d.elem.toLowerCase() + ')';
  panel.innerHTML = '<div class="p-hdr">' +
    '<div><span class="p-code" style="--c:' + col + '">' + d.code + '</span> · <span class="p-hz">' + d.hz + '</span></div>' +
    '<div class="p-badge" style="--c:' + col + '"><span class="dot"></span>' + d.shu + '</div>' +
  '</div>' +
  '<h3 class="p-name">' + d.pinyin + ' <span style="font-size:16px;font-weight:400;color:var(--mute)">"' + d.en + '"</span></h3>' +
  '<p class="p-py"><b>' + d.tamil + '</b> · Conception Vessel (Ren Mai)</p>' +
  '<div class="p-sec"><h4>Location</h4><p>' + d.loc + '</p></div>' +
  '<div class="p-sec"><h4>Proportional Cun Distance</h4><p>' + d.cun + '</p></div>' +
  '<div class="p-sec"><h4>Clinical Indications</h4><p>' + d.ind + '</p></div>';
}"""

    new_render = """function render(id){
  var d = DATA[id];
  if(!d) return;
  var col = 'var(--' + d.elem.toLowerCase() + ')';
  var im = IMGS[d.code];
  panel.innerHTML = '<div class="p-hdr">' +
    '<div><span class="p-code" style="--c:' + col + '">' + d.code + '</span> · <span class="p-hz">' + d.hz + '</span></div>' +
    '<div class="p-badge" style="--c:' + col + '"><span class="dot"></span>' + d.shu + '</div>' +
  '</div>' +
  '<h3 class="p-name">' + d.pinyin + ' <span style="font-size:16px;font-weight:400;color:var(--mute)">"' + d.en + '"</span></h3>' +
  '<p class="p-py"><b>' + d.tamil + '</b> · Conception Vessel (Ren Mai)</p>' +
  '<div class="p-sec"><h4>Location</h4><p>' + d.loc + '</p></div>' +
  '<div class="p-sec"><h4>Proportional Cun Distance</h4><p>' + d.cun + '</p></div>' +
  '<div class="p-sec"><h4>Clinical Indications</h4><p>' + d.ind + '</p></div>' +
  (im ? '<figure class="p-diag" style="margin:20px 0 0;"><img src="' + im + '" alt="' + d.code + ' ' + d.pinyin + ' Anatomical Diagram" style="display:block;width:100%;max-width:320px;border-radius:10px;background:#faf6ee;box-shadow:0 0 0 1px rgba(0,0,0,.3);margin:0 auto;"><figcaption style="font-size:11px;color:var(--mute);text-align:center;margin-top:8px;">' + d.code + ' Location Anatomical Diagram (Nalaayan)</figcaption></figure>' : '');
}"""

    if old_render in content:
        content = content.replace(old_render, new_render)
    elif "var im = IMGS[d.code];" not in content:
        print("Warning: old_render exact string match not found, inspecting...")

    with open(chart_py, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated tools/create_cv_chart.py successfully!")

if __name__ == '__main__':
    update()
