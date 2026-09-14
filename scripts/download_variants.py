"""Import product images observed on Equip Club's public product galleries."""
import json
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen, Request
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE='https://le-de.cdn-website.com/cc28d4e2b1154e3e993b901fa9e9c5c4/dms3rep/multi/opt/'
CAP='Capture+d-%C3%A9cran+2026-09-10+%C3%A0+'
names={1:['AB-2205b5c7','AB+2'],2:['11.12.30','11.13.11'],3:['11.16.47','11.17.20'],4:['11.20.24','11.21.02'],5:['11.24.18','11.25.01'],6:['11.41.11'],7:['11.41.44'],8:['11.28.19','11.28.58'],9:['11.31.28','11.32.11'],10:['11.36.01','11.36.31'],11:['11.39.05','11.39.35'],12:['11.45.36','11.46.02','AB10','AB9'],13:['11.47.56','11.48.41','11.49.08'],14:['11.53.39','11.54.06','Boutique-87','Boutique-86'],15:['11.51.25','11.51.50','Boutique-83','Boutique-82.png'],16:['Boutique-80','Boutique-81','11.51.25'],17:['12.00.35'],18:['13.37.03'],19:['13.51.17','13.51.49'],20:['13.47.27'],21:['13.43.15']}
products=json.loads((ROOT/'data/boutique.json').read_text(encoding='utf-8'))
for number,files in names.items():
    images=[]
    for j,name in enumerate(files):
        url=BASE+(CAP if name[0].isdigit() else '')+name+'-1920w.'+('webp' if name.endswith('.png') else 'png')
        path=f'assets/boutique/produit-{number:02d}-vue-{j+1}.webp'
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response:
            im=Image.open(BytesIO(response.read())).convert('RGB')
            im.thumbnail((900,900))
            im.save(ROOT/path,'WEBP',quality=88)
        images.append({'image':path,'label':f'Vue {j+1}','source':url})
    products[number-1]['variants']=images
    products[number-1]['colors']=['Noir','Rouge'] if number<=11 else []
    print(number,len(images))
(ROOT/'data/boutique.json').write_text(json.dumps(products,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
