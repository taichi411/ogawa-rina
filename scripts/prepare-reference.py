"""Extract reusable illustration and typography layers, never whole video frames.

Input: user-supplied sample.mp4, decoded into analysis/frames by FFmpeg.
The 486x274 drawing area begins at (652,446) in the 1920x1080 recording.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public' / 'sample-recreation'
OUT.mkdir(parents=True, exist_ok=True)
manifest = {}

def layer(name, frame, box, polygon=None, remove_teal=False, erase=None, opaque=False):
    source = Image.open(ROOT / 'analysis' / 'frames' / f'{frame+1:04d}.png').convert('RGBA')
    im = source.crop(box)
    ar = np.asarray(im).copy()
    rgb = ar[:,:,:3].astype(float)
    # Remove only the mint paper, keeping the white clothing and black halftone.
    mint = np.array([230,246,242])
    dist = np.max(abs(rgb-mint),axis=2)
    alpha = np.clip((dist-5)/15,0,1)
    ar[:,:,3] = 255 if opaque or polygon else (alpha*255).astype('uint8')
    if remove_teal:
        teal = (rgb[:,:,0]<160)&(rgb[:,:,1]>rgb[:,:,0]+22)&(rgb[:,:,2]>rgb[:,:,0]+18)
        ar[teal,3] = 0
    im = Image.fromarray(ar)
    if polygon:
        mask = Image.new('L',im.size)
        ImageDraw.Draw(mask).polygon([(x-box[0],y-box[1]) for x,y in polygon],fill=255)
        im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')),np.array(mask))))
    if erase:
        draw=ImageDraw.Draw(im)
        for b in erase: draw.rectangle(b, fill=(0,0,0,0))
    im.save(OUT / f'{name}.png')
    manifest[name] = {'x':box[0],'y':box[1],'w':box[2]-box[0],'h':box[3]-box[1]}

layer('intro-title',90,(139,54,331,94),opaque=True)
layer('intro-problem',90,(149,97,326,133),opaque=True)
layer('intro-question',90,(146,136,326,167),opaque=True)
layer('intro-woman',90,(343,141,425,259),polygon=[(345,259),(349,211),(355,198),(358,182),(356,166),(361,150),(376,142),(391,143),(402,150),(408,171),(405,185),(409,203),(416,215),(423,259)])
layer('question',90,(398,95,429,139))
layer('background-question',690,(18,47,48,88))
layer('problem-copy',210,(58,43,204,134),opaque=True)
for i,(top,bottom) in enumerate([(43,65),(65,87),(87,108),(108,134)]):
    layer(f'problem-line-{i}',210,(58,top,204,bottom),opaque=True)
layer('problem-right-copy',270,(330,180,450,229),opaque=True)
layer('problem-right-0',270,(330,180,450,205),opaque=True)
layer('problem-right-1',270,(330,205,450,229),opaque=True)
# A static torso and independently pivoted arms preserve the original halftone.
layer('shrug-body',210,(210,60,297,260),polygon=[(224,60),(281,60),(280,114),(291,125),(284,164),(288,213),(296,260),(217,260),(224,212),(229,169),(211,143),(214,125),(227,114)])
layer('shrug-left',210,(163,132,234,189),polygon=[(212,132),(231,144),(234,179),(211,187),(164,187),(164,157),(208,160)])
layer('shrug-right',210,(276,117,349,180),polygon=[(283,117),(300,141),(320,124),(349,124),(348,154),(308,179),(283,175),(276,135)])
layer('sweat',210,(279,51,299,76))
layer('solution-heading',465,(128,51,376,75),opaque=True)
layer('solution-title',465,(129,85,370,122),opaque=True)
layer('solution-copy',465,(102,128,395,157),opaque=True)
layer('city',390,(15,184,472,259),erase=[(309,0,429,76)])
layer('city-back',465,(15,184,472,259),erase=[(309,0,429,76)])
layer('happy-woman',390,(326,158,444,259),polygon=[(330,259),(330,231),(326,207),(347,205),(350,211),(360,205),(363,198),(357,184),(357,174),(365,163),(381,158),(397,162),(405,175),(405,198),(412,211),(416,208),(423,206),(436,210),(430,231),(432,259)])
layer('benefit-heading',570,(119,21,367,44),opaque=True)
layer('benefit-title',570,(69,48,416,92),opaque=True)
layer('folder-papers',570,(183,124,301,204),opaque=True)
layer('folder-alone',525,(211,151,278,205),opaque=True)
layer('person-left',570,(77,149,141,259),polygon=[(80,170),(90,169),(93,160),(95,151),(110,150),(120,167),(132,169),(140,175),(124,193),(123,220),(126,241),(119,244),(119,259),(96,259),(97,242),(93,241),(94,216),(96,194),(87,187)])
layer('person-center',570,(305,151,348,259),polygon=[(314,155),(331,153),(338,164),(334,179),(340,187),(343,201),(338,215),(345,246),(339,246),(339,259),(314,259),(315,247),(308,246),(311,217),(308,207),(307,190),(315,182),(313,170)])
layer('person-right',570,(357,151,406,259),polygon=[(372,152),(386,153),(392,169),(398,180),(403,197),(397,210),(393,214),(394,259),(369,259),(367,214),(360,202),(360,185),(369,173)])
layer('question-copy',690,(122,52,376,110),opaque=True)
layer('desk-woman',690,(190,139,325,259),opaque=True)
# Follow the actual grayscale ink outline, rather than a polygon approximation,
# to retain the round hair contour while rejecting teal background question marks.
person=Image.open(OUT/'desk-woman.png').convert('RGBA')
rgb=np.asarray(person)[:,:,:3].astype(int)
ink=(rgb[:,:,0]<205)&(abs(rgb[:,:,0]-rgb[:,:,1])<28)&(abs(rgb[:,:,1]-rgb[:,:,2])<28)
mask=Image.fromarray((ink*255).astype('uint8')).filter(ImageFilter.MaxFilter(3))
ImageDraw.Draw(mask).line((13,119,132,119),fill=255,width=2)
for x,y in [(0,0),(134,0),(0,119),(134,119)]:
    if mask.getpixel((x,y))==0:ImageDraw.floodfill(mask,(x,y),128,thresh=0)
binary=np.array(mask)!=128
components=[]
for yy,xx in zip(*np.where(binary)):
    if not binary[yy,xx]:continue
    stack=[(int(yy),int(xx))]; points=[]; binary[yy,xx]=False
    while stack:
        y,x=stack.pop(); points.append((y,x))
        for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
            ny,nx=y+dy,x+dx
            if 0<=ny<120 and 0<=nx<135 and binary[ny,nx]:
                binary[ny,nx]=False;stack.append((ny,nx))
    components.append(points)
clean=np.zeros((120,135),dtype='uint8')
for y,x in max(components,key=len):clean[y,x]=255
person.putalpha(Image.fromarray(clean))
person.save(OUT/'desk-woman.png')
layer('books-left',690,(141,211,189,259),polygon=[(143,212),(186,212),(188,259),(142,259)])
layer('books-right',690,(328,211,377,259),polygon=[(330,212),(373,212),(375,259),(329,259)])
layer('cta-heading',870,(28,33,456,66),opaque=True)
layer('cta-subheading',870,(312,65,452,83),opaque=True)
layer('cta-woman',870,(24,146,139,259),opaque=True)
layer('cta-url',870,(217,239,453,254),opaque=True)
layer('browser',870,(241,119,323,177),opaque=True)
layer('browser-row-0',870,(249,136,314,153),opaque=True)
layer('browser-row-1',870,(249,153,314,169),opaque=True)
shell=Image.open(OUT/'browser.png')
ImageDraw.Draw(shell).rectangle((8,17,73,50),fill=(253,253,253,255))
shell.save(OUT/'browser-shell.png')
manifest['browser-shell']=manifest['browser']

# Measure the actual vertical wipe panels from every transition frame.
# Only near-constant full-height columns are retained, not frame images.
wipe={}
for frame in list(range(9,31))+list(range(739,770)):
    ar=np.asarray(Image.open(ROOT/'analysis/frames'/f'{frame+1:04d}.png'))[16:258,:,:3].astype(float)
    median=np.median(ar,axis=0)
    solid=np.mean(np.max(abs(ar-median[None,:,:]),axis=2)<10,axis=0)>.97
    black=np.max(median,axis=1)<25
    teal=np.max(abs(median-np.array([57,135,132])),axis=1)<15
    labels=np.where(solid&black,1,np.where(solid&teal,2,0))
    runs=[]; start=0
    for x in range(1,487):
        if x==486 or labels[x]!=labels[start]:
            if labels[start] and x-start>=2:runs.append([int(start),int(x-start),int(labels[start])])
            start=x
    wipe[frame]=runs
(ROOT/'src/sample/wipe.ts').write_text('export const wipe:Record<number,number[][]> = '+json.dumps(wipe)+';\n',encoding='utf8')
(OUT/'layers.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print(f'Prepared {len(manifest)} independent layers in {OUT}')
(ROOT/'src/sample/layers.ts').write_text('export const layers = '+json.dumps(manifest,indent=2)+' as const;\n',encoding='utf8')
