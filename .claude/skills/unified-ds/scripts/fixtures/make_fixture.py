"""자체 검사용 가짜 Figma 원시 변수(raw.json) 생성 — 최소 세트 42 + 브랜드 램프 + 비색상 일부.

    python3 make_fixture.py OUT_DIR
"""
import json, os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
P=[]; V=[]
def var(n,col,typ,vals,scopes,hidden=False): V.append(dict(id="V:"+n,name=n,collection=col,type=typ,scopes=scopes,description="",hidden=hidden,values=vals))
gray={"0":"#FFFFFFFF","50":"#F7F7F8FF","100":"#EEEEF0FF","200":"#DCDCE0FF","400":"#8A8A94FF","500":"#6B6B75FF","600":"#52525BFF","700":"#3F3F46FF","800":"#27272AFF","900":"#18181BFF"}
hues={"blue":("#E8F0FEFF","#1D5FD6FF","#8FB4F7FF"),"green":("#E6F6EDFF","#127A3EFF","#7FD3A2FF"),"yellow":("#FFF6DBFF","#F5B800FF","#FFD966FF"),"red":("#FDEAEAFF","#C62828FF","#F49A9AFF"),"orange":("#FFF0E6FF","#C2410CFF","#FDBA8CFF"),"purple":("#F2EBFEFF","#6D28D9FF","#C4A8F7FF")}
for k,v in gray.items(): var(f"color/gray/{k}","primitive","COLOR",{"value":v},[],True)
for h,(w,s,d) in hues.items():
  var(f"color/{h}/50","primitive","COLOR",{"value":w},[]); var(f"color/{h}/600","primitive","COLOR",{"value":s},[]); var(f"color/{h}/300","primitive","COLOR",{"value":d},[]); var(f"color/{h}/900","primitive","COLOR",{"value":"#1A1A2EFF"},[])
var("color/alpha/black-8","primitive","COLOR",{"value":"#00000014"},[]); var("color/alpha/black-16","primitive","COLOR",{"value":"#00000029"},[]); var("color/alpha/white-8","primitive","COLOR",{"value":"#FFFFFF14"},[]); var("color/alpha/white-16","primitive","COLOR",{"value":"#FFFFFF29"},[]); var("color/alpha/black-50","primitive","COLOR",{"value":"#00000080"},[])
steps=["50","100","200","300","400","500","600","700","800","900","950"]
A=lambda n:{"alias":n,"aliasCollection":"x"}
for r,(nv,ch) in {"primary":("orange","purple"),"secondary":("blue","green")}.items():
  for s in steps:
    src = "50" if s in ("50","100") else ("300" if s in ("200","300","400") else ("600" if s in("500","600","700") else "900"))
    var(f"brand/{r}/{s}","brand","COLOR",{"NOVERA":A(f"color/{nv}/{src}"),"1CHON":A(f"color/{ch}/{src}")},[])
var("font/family/base","brand","STRING",{"NOVERA":"Pretendard","1CHON":"SUIT"},["FONT_FAMILY"])
BG=["FRAME_FILL","SHAPE_FILL"]; FG=["TEXT_FILL","SHAPE_FILL","STROKE_COLOR"]; ST=["STROKE_COLOR"]
def sem(n,l,d,sc): var(n,"semantic","COLOR",{"Light":A(l),"Dark":A(d)},sc)
sem("bg/layer-default","color/gray/0","color/gray/900",BG); sem("bg/layer-basement","color/gray/50","color/gray/900",BG); sem("bg/layer-floating","color/gray/0","color/gray/800",BG); sem("bg/layer-fill","color/gray/100","color/gray/800",BG)
sem("bg/state-hover","color/alpha/black-8","color/alpha/white-8",BG); sem("bg/state-pressed","color/alpha/black-16","color/alpha/white-16",BG)
sem("bg/neutral-solid","color/gray/900","color/gray/50",BG); sem("bg/neutral-weak","color/gray/100","color/gray/800",BG)
sem("bg/brand-solid","brand/primary/600","brand/primary/300",BG); sem("bg/brand-weak","brand/primary/50","brand/primary/900",BG)
tm={"informative":"blue","positive":"green","warning":"yellow","critical":"red"}
for t,h in tm.items():
  sem(f"bg/{t}-solid",f"color/{h}/600",f"color/{h}/300",BG); sem(f"bg/{t}-weak",f"color/{h}/50",f"color/{h}/900",BG)
  sem(f"fg/{t}",f"color/{h}/600" if t!="warning" else "color/orange/600",f"color/{h}/300",FG); sem(f"stroke/{t}",f"color/{h}/600" if t!="warning" else "color/orange/600",f"color/{h}/300",ST)
sem("bg/disabled","color/gray/100","color/gray/800",BG); sem("bg/overlay","color/alpha/black-50","color/alpha/black-50",BG)
sem("fg/neutral","color/gray/900","color/gray/50",FG); sem("fg/neutral-subtle","color/gray/700","color/gray/200",FG); sem("fg/neutral-muted","color/gray/600","color/gray/400",FG); sem("fg/neutral-placeholder","color/gray/400","color/gray/500",FG); sem("fg/neutral-contrast","color/gray/0","color/gray/900",FG)
sem("fg/disabled","color/gray/400","color/gray/600",FG); sem("fg/brand","brand/primary/600","brand/primary/300",FG); sem("fg/contrast","color/gray/0","color/gray/900",FG); sem("fg/warning-contrast","color/gray/900","color/gray/900",FG)
sem("stroke/neutral","color/gray/200","color/gray/700",ST); sem("stroke/neutral-muted","color/gray/100","color/gray/800",ST); sem("stroke/neutral-strong","color/gray/500","color/gray/400",ST); sem("stroke/focus","color/blue/600","color/blue/300",ST); sem("stroke/brand","brand/primary/600","brand/primary/300",ST)
for n in [4,8,16]: var(f"spacing/{n}","Spacing","FLOAT",{"value":n},["GAP"])
var("radius/2xl","Radius","FLOAT",{"value":24},["CORNER_RADIUS"])
cols=[dict(id="c1",name="primitive",modes=["value"],hidden=True,count=0),dict(id="c2",name="brand",modes=["NOVERA","1CHON"],hidden=False),dict(id="c3",name="semantic",modes=["Light","Dark"],hidden=False),dict(id="c4",name="Spacing",modes=["value"],hidden=False),dict(id="c5",name="Radius",modes=["value"],hidden=False)]
json.dump(dict(extractedAt="2026-11-09",fileKey="TEST",collections=cols,variables=V),open(os.path.join(OUT,"raw.json"),"w"),ensure_ascii=False)
print(len(V))
