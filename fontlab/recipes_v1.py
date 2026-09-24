"""Original, bounded Phase 1b recipe evaluator; it imports no font outlines."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json, math, re
from pathlib import Path
from typing import Any
from fontTools.pens.areaPen import AreaPen

ROOT = Path(__file__).resolve().parent
PROJECT_PATH, SCHEMA_PATH = ROOT / "project.json", ROOT / "project.schema.json"
MAX_SOURCE_BYTES = 65536
KAPPA = .5522847498307936
AXIS_RANGES = {"weight": (40., 160.), "width": (.85, 1.15), "xHeight": (460., 540.), "roundness": (0., 1.), "aperture": (0., 1.)}
PRESETS = {"text": {"axes": {"weight": 88, "width": 1., "xHeight": 500, "roundness": .74, "aperture": .58}, "switches": {"aConstruction": "double", "zeroStyle": "plain"}}, "display": {"axes": {"weight": 124, "width": 1.08, "xHeight": 520, "roundness": .9, "aperture": .72}, "switches": {"aConstruction": "single", "zeroStyle": "slashed"}}}
CYRL_UPPER, CYRL_LOWER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ", "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

class ProjectValidationError(ValueError): pass

def _name(code, char):
    if char == " ": return "space"
    if char == "\u00a0": return "nbspace"
    if 48 <= code <= 57: return ("zero","one","two","three","four","five","six","seven","eight","nine")[code-48]
    if char.isascii() and char.isalpha(): return char
    return {0x301:"acutecomb", 0x308:"dieresiscomb"}.get(code, f"uni{code:04X}")

def _entry(char, script, recipe):
    code = ord(char)
    return {"id": f"{script.lower()}-{code:04x}", "name": _name(code,char), "recipe": recipe, "script": script, "unicode": code}

def _repertoire():
    result=[]
    for code in range(32,127):
        char=chr(code)
        recipe,script=(f"latin-upper-{char}","Latn") if char.isupper() else (f"latin-lower-{char}","Latn") if char.islower() else (f"digit-{char}","Zyyy") if char.isdigit() else (f"common-{code:04x}","Zyyy")
        result.append(_entry(char,script,recipe))
    result.append(_entry("\u00a0","Zyyy","blank-nbsp"))
    result += [_entry(c,"Cyrl",f"cyrillic-upper-{c}") for c in CYRL_UPPER]
    result += [_entry(c,"Cyrl",f"cyrillic-lower-{c}") for c in CYRL_LOWER]
    return result + [_entry("\u0301","Zinh","mark-acute"),_entry("\u0308","Zinh","mark-dieresis")]

GLYPH_DEFINITIONS = _repertoire()

def canonical_json(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def source_hash(project): return sha256(canonical_json(project).encode()).hexdigest()
def _keys(value, expected, label):
    if not isinstance(value,dict) or set(value)!=expected: raise ProjectValidationError(f"{label} fields must be exactly {sorted(expected)}")
def _range(value, limits, label):
    if not isinstance(value,(int,float)) or isinstance(value,bool) or not math.isfinite(value) or not limits[0]<=value<=limits[1]: raise ProjectValidationError(f"{label} must be within {limits[0]}..{limits[1]}")
def validate_project(p):
    required={"schemaVersion","id","name","engine","axes","localOverrides","switches","metrics","kerning","activePreset","glyphs"}; _keys(p,required,"project")
    if p["schemaVersion"] != 1 or p["engine"] != {"id":"technical-sans","version":"1.0"}: raise ProjectValidationError("unsupported project version or engine")
    if not isinstance(p["id"],str) or re.fullmatch(r"[a-z0-9-]{1,80}",p["id"]) is None or not isinstance(p["name"],str) or not 1<=len(p["name"])<=100: raise ProjectValidationError("invalid project identity")
    _keys(p["axes"],set(AXIS_RANGES),"axes")
    for key,limits in AXIS_RANGES.items(): _range(p["axes"][key],limits,key)
    _keys(p["localOverrides"],{"O"},"localOverrides"); _keys(p["localOverrides"]["O"],{"counter"},"localOverrides.O"); _range(p["localOverrides"]["O"]["counter"],(.5,1.5),"O counter")
    _keys(p["switches"],{"aConstruction","zeroStyle"},"switches")
    if p["switches"]["aConstruction"] not in {"single","double"} or p["switches"]["zeroStyle"] not in {"plain","slashed"}: raise ProjectValidationError("invalid switch")
    if p["metrics"]!={"profile":"technical-proportional-v1"} or p["kerning"]!={"profile":"script-aware-v1"} or p["glyphs"]!={"repertoire":"basic-latin-russian-v1"} or p["activePreset"] not in {*PRESETS,"custom"}: raise ProjectValidationError("unsupported Phase 1b profile")
def load_project(path=None):
    raw=(path or PROJECT_PATH).read_bytes()
    if len(raw)>MAX_SOURCE_BYTES: raise ProjectValidationError(f"project exceeds {MAX_SOURCE_BYTES} bytes")
    try: p=json.loads(raw.decode())
    except (UnicodeDecodeError,json.JSONDecodeError) as e: raise ProjectValidationError(f"malformed UTF-8 JSON: {e}") from e
    validate_project(p); return p

def rect(x0,y0,x1,y1,reverse=False):
    points=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
    if reverse: points.reverse()
    return [("M",*points[0]),*(("L",*q) for q in points[1:]),("Z",)]
def oval(cx,cy,rx,ry,roundness=1,reverse=False):
    if rx<=0 or ry<=0: raise ProjectValidationError("counter collapsed")
    k=.18+.3722847498307936*roundness; out=[("M",cx+rx,cy),("C",cx+rx,cy+k*ry,cx+k*rx,cy+ry,cx,cy+ry),("C",cx-k*rx,cy+ry,cx-rx,cy+k*ry,cx-rx,cy),("C",cx-rx,cy-k*ry,cx-k*rx,cy-ry,cx,cy-ry),("C",cx+k*rx,cy-ry,cx+rx,cy-k*ry,cx+rx,cy),("Z",)]
    if not reverse:return out
    return [("M",cx+rx,cy),("C",cx+rx,cy-k*ry,cx+k*rx,cy-ry,cx,cy-ry),("C",cx-k*rx,cy-ry,cx-rx,cy-k*ry,cx-rx,cy),("C",cx-rx,cy+k*ry,cx-k*rx,cy+ry,cx,cy+ry),("C",cx+k*rx,cy+ry,cx+rx,cy+k*ry,cx+rx,cy),("Z",)]
def ring(cx,cy,rx,ry,w,r): return [oval(cx,cy,rx,ry,r),oval(cx,cy,rx-w,ry-w,r,True)]
def stroke(x0,y0,x1,y1,w):
    dx,dy=x1-x0,y1-y0; d=math.hypot(dx,dy)
    if not d: raise ProjectValidationError("zero length stroke")
    px,py=-dy/d*w/2,dx/d*w/2
    # Outer contours must share one winding direction. A stroked diagonal used
    # to run opposite to rect()/oval(), punching holes at overlapping joins.
    return [("M",x0+px,y0+py),("L",x0-px,y0-py),("L",x1-px,y1-py),("L",x1+px,y1+py),("Z",)]

def _advance(d):
    c=chr(d["unicode"]); q=d["recipe"]
    if q.startswith("mark-"):return 0
    if c in " \u00a0":return 280
    if q.startswith("common-"):return 360
    if q.startswith("digit-"):return 620
    if "upper" in q:return 820 if c in "MWЖШЩЮ" else 420 if c == "I" else 540 if c == "J" else 680
    return 760 if c in "mwжшщю" else 330 if c in "iljт" else 420 if c in "fr" else 560 if c == "h" else 540
def _scale(contours,f):
    return [[cmd if cmd[0]=="Z" else (cmd[0],*(v*f if i%2==0 else v for i,v in enumerate(cmd[1:]))) for cmd in contour] for contour in contours]
def _bars(a,h,w,kind):
    l,r,m=80,a-80,a/2; v=lambda x,y0=0,y1=h:rect(x-w/2,y0,x+w/2,y1); bar=lambda y,x0=l,x1=r:rect(x0,y-w/2,x1,y+w/2)
    if kind in "HН":return [v(l),v(r),bar(h/2)]
    if kind in "AА":return [stroke(l,0,m,h,w),stroke(r,0,m,h,w),rect(l+w,h*.42-w/2,r-w,h*.42+w/2)]
    if kind in "EЕ":return [v(l),bar(h),bar(h/2),bar(0)]
    if kind=="F":return [v(l),bar(h),bar(h/2)]
    if kind=="I":return [bar(h),v(m),bar(0)]
    if kind=="T":return [bar(h),v(m)]
    if kind=="Г":return [v(l),bar(h)]
    if kind=="M":return [v(l),v(r),stroke(l,h,m,0,w),stroke(m,0,r,h,w)]
    if kind in "NИ":return [v(l),v(r),stroke(l,0 if kind=="И" else h,r,h if kind=="И" else 0,w)]
    if kind=="V":return [stroke(l,h,m,0,w),stroke(r,h,m,0,w)]
    if kind=="X":return [stroke(l,0,r,h,w),stroke(l,h,r,0,w)]
    if kind=="Y":return [stroke(l,h,m,h*.45,w),stroke(r,h,m,h*.45,w),v(m,0,h*.45)]
    if kind in "KК":return [v(l),stroke(l,h*.5,r,h,w),stroke(l,h*.5,r,0,w)]
    if kind=="Ж":return [v(m),stroke(m,h*.5,l,h,w),stroke(m,h*.5,l,0,w),stroke(m,h*.5,r,h,w),stroke(m,h*.5,r,0,w)]
    if kind=="W":return [stroke(l,h,a*.31,0,w),stroke(a*.31,0,m,h*.42,w),stroke(m,h*.42,a*.69,0,w),stroke(a*.69,0,r,h,w)]
    if kind in "ШЩ":return [v(l),v(m),v(r),bar(0)]
    if kind=="Z":return [bar(h),stroke(r,h,l,0,w),bar(0)]
    if kind in "BВ":return [v(l),*ring(m+40,h*.72,a*.26,h*.25,w,.8),*ring(m+40,h*.27,a*.26,h*.25,w,.8)]
    if kind in "PR":return [v(l),*ring(m,h*.72,a*.38,h*.28,w,.8)]
    if kind=="Ь":return [v(l),*ring(m,h*.27,a*.38,h*.28,w,.8)]
    if kind=="Ф":return [*ring(m,h/2,a*.36,h/2+12,w,.8),v(m,-40,h+40)]
    if kind in "CDGСЭ":return [v(l,h*.18,h*.82),bar(h,l+35,r),bar(0,l+35,r)]
    if kind in "ДЛ":return [bar(0,l-35,r+35),stroke(l,0,m,h,w),stroke(r,0,m,h,w)]
    if kind=="Я":return [v(r),*ring(m,h*.70,a*.38,h*.30,w,.8),stroke(m-45,h*.40,l,0,w)]
    if kind in "УуYy":return [stroke(l,h,m,h*.35,w),stroke(r,h,m,h*.35,w),stroke(m,h*.35,l,-180,w)]
    raise ProjectValidationError(f"unreviewed bar construction {kind!r}")

def _common_shape(code,a,w,r):
    l,right,m=80,a-80,a/2; v=lambda x,y0=0,y1=700:rect(x-w/2,y0,x+w/2,y1); bar=lambda y,x0=l,x1=right:rect(x0,y-w/2,x1,y+w/2)
    dot=lambda x,y:ring(x,y,w*.55,w*.55,w*.3,r)
    if code in {32,160}:return []
    if code==33:return [v(m,150,700),*dot(m,55)]
    if code==34:return [v(a*.34,510,700),v(a*.66,510,700)]
    if code==35:return [v(a*.37,80,620),v(a*.63,80,620),bar(470),bar(230)]
    if code==36:return [bar(700),v(m),bar(350),bar(0),v(l,350,700),v(right,0,350)]
    if code==37:return [*dot(a*.30,545),*dot(a*.70,155),stroke(a*.24,65,a*.76,635,w*.72)]
    if code==38:return [bar(700,a*.28,a*.62),v(a*.28,350,700),bar(350,a*.28,a*.72),v(a*.72,0,350),bar(0,a*.38,a*.72),stroke(a*.28,0,a*.72,700,w*.72)]
    if code in {39,96}:return [stroke(a*.55 if code==39 else a*.45,560,a*.45 if code==39 else a*.55,700,w*.72)]
    if code==40:return [stroke(a*.62,700,a*.38,350,w),stroke(a*.38,350,a*.62,0,w)]
    if code==41:return [stroke(a*.38,700,a*.62,350,w),stroke(a*.62,350,a*.38,0,w)]
    if code==42:return [stroke(m,170,m,530,w*.72),stroke(a*.30,260,a*.70,440,w*.72),stroke(a*.30,440,a*.70,260,w*.72)]
    if code==43:return [v(m,170,530),bar(350)]
    if code==44:return [*dot(m,55),stroke(m,25,a*.40,-110,w*.72)]
    if code==45:return [bar(350)]
    if code==46:return [*dot(m,55)]
    if code==47:return [stroke(a*.25,0,a*.75,700,w)]
    if code==58:return [*dot(m,525),*dot(m,80)]
    if code==59:return [*dot(m,525),*dot(m,80),stroke(m,50,a*.40,-100,w*.72)]
    if code==60:return [stroke(a*.68,610,a*.30,350,w),stroke(a*.30,350,a*.68,90,w)]
    if code==61:return [bar(450),bar(250)]
    if code==62:return [stroke(a*.32,610,a*.70,350,w),stroke(a*.70,350,a*.32,90,w)]
    if code==63:return [bar(585,l,a*.62),v(a*.62,390,585),bar(350,a*.44,a*.62),*dot(m,60)]
    if code==64:return [bar(700),bar(0),v(l),v(right),bar(350,l,right*.72),v(right*.72,180,520)]
    if code==91:return [bar(700,a*.42,a*.62),v(a*.42),bar(0,a*.42,a*.62)]
    if code==92:return [stroke(a*.25,700,a*.75,0,w)]
    if code==93:return [bar(700,a*.38,a*.58),v(a*.58),bar(0,a*.38,a*.58)]
    if code==94:return [stroke(a*.28,410,m,650,w),stroke(m,650,a*.72,410,w)]
    if code==95:return [bar(0)]
    if code==123:return [bar(700,a*.48,a*.66),v(a*.48,390,700),bar(350,a*.48,a*.64),v(a*.48,0,310),bar(0,a*.48,a*.66)]
    if code==124:return [v(m)]
    if code==125:return [bar(700,a*.34,a*.52),v(a*.52,390,700),bar(350,a*.36,a*.52),v(a*.52,0,310),bar(0,a*.34,a*.52)]
    if code==126:return [stroke(a*.24,320,a*.42,390,w*.72),stroke(a*.42,390,a*.60,320,w*.72),stroke(a*.60,320,a*.78,390,w*.72)]
    raise ProjectValidationError(f"unreviewed common codepoint U+{code:04X}")

def _digit_shape(c,a,w,r,p):
    l,right,m=80,a-80,a/2; v=lambda x,y0=0,y1=700:rect(x-w/2,y0,x+w/2,y1); bar=lambda y,x0=l,x1=right:rect(x0,y-w/2,x1,y+w/2)
    if c=="0":return ring(m,350,a*.34,362,w+8,r)+([stroke(a*.27,85,a*.73,615,w*.5)] if p["switches"]["zeroStyle"]=="slashed" else [])
    if c=="1":return [v(m),stroke(a*.32,570,m,700,w),bar(0,a*.32,a*.68)]
    if c=="2":return [bar(700),v(right,400,700),bar(350),v(l,0,350),bar(0)]
    if c=="3":return [bar(700),bar(350),bar(0),v(right)]
    if c=="4":return [v(l,350,700),bar(350),v(right),stroke(l,350,right,700,w)]
    if c=="5":return [bar(700),v(l,350,700),bar(350),v(right,0,350),bar(0)]
    if c=="6":return [bar(700),v(l),bar(350),v(right,0,350),bar(0)]
    if c=="7":return [bar(700),stroke(right,700,l,0,w)]
    if c=="8":return ring(m,525,a*.29,175,w,r)+ring(m,175,a*.29,175,w,r)
    if c=="9":return [bar(700),v(l,350,700),bar(350),v(right),bar(0)]
    raise ProjectValidationError(f"unreviewed digit {c!r}")

def _open_round(a,h,w,r,opening,reverse=False):
    l,right=80,a-80
    if reverse:return [rect(right-w/2,0,right+w/2,h),rect(l+opening,h+12-w,right,h+12),rect(l+opening,-12,right,w-12)]
    return [rect(l-w/2,0,l+w/2,h),rect(l,h+12-w,right-opening,h+12),rect(l,-12,right-opening,w-12)]

def _latin_upper_shape(c,a,w,r,p):
    l,right,m=80,a-80,a/2; v=lambda x,y0=0,y1=700:rect(x-w/2,y0,x+w/2,y1); bar=lambda y,x0=l,x1=right:rect(x0,y-w/2,x1,y+w/2)
    if c=="A":return _bars(a,700,w,"A")
    if c=="B":return _bars(a,700,w,"B")
    if c=="C":return _open_round(a,700,w,r,a*(.06+.12*p["axes"]["aperture"]))
    if c=="D":return [v(l),*ring(m+20,350,a*.30,315,w,r)]
    if c in "EF":return _bars(a,700,w,c)
    if c=="G":return [*_open_round(a,700,w,r,a*(.06+.12*p["axes"]["aperture"])),bar(350,m,right)]
    if c=="H":return _bars(a,700,w,"H")
    if c=="I":return _bars(a,700,w,"I")
    if c=="J":return [bar(700),v(right,170,700),bar(0,l,right),v(l,0,170)]
    if c=="K":return _bars(a,700,w,"K")
    if c=="L":return [v(l),bar(0)]
    if c=="M":return _bars(a,700,w,"M")
    if c=="N":return _bars(a,700,w,"N")
    if c=="O":return ring(m,350,a*.36,362,w+24*(1-p["localOverrides"]["O"]["counter"]),r)
    if c=="P":return _bars(a,700,w,"P")
    if c=="Q":return ring(m,350,a*.36,362,w,r)+[stroke(m,190,right+30,-55,w)]
    if c=="R":return _bars(a,700,w,"R")+[stroke(m+45,350,right,0,w)]
    if c=="S":return [bar(700),v(l,350,700),bar(350),v(right,0,350),bar(0)]
    if c=="T":return _bars(a,700,w,"T")
    if c=="U":return [v(l,160,700),v(right,160,700),bar(0),v(l,0,170),v(right,0,170)]
    if c=="V":return _bars(a,700,w,"V")
    if c=="W":return _bars(a,700,w,"W")
    if c=="X":return _bars(a,700,w,"X")
    if c=="Y":return _bars(a,700,w,"Y")
    if c=="Z":return _bars(a,700,w,"Z")
    raise ProjectValidationError(f"unreviewed Latin cap {c!r}")

def _lower_a(a,h,w,r):
    return ring(a*.43,h*.40,a*.32,h*.38,w,r)+[rect(a*.70-w,0,a*.70,h),rect(a*.43,h*.42,a*.70,h*.42+w)]

def _latin_lower_shape(c,a,h,w,r,p):
    l,right,m=80,a-80,a/2; v=lambda x,y0=0,y1=h:rect(x-w/2,y0,x+w/2,y1); bar=lambda y,x0=l,x1=right:rect(x0,y-w/2,x1,y+w/2)
    if c=="a":
        if p["switches"]["aConstruction"]=="single":return ring(a*.46,h*.42,a*.32,h*.38,w,r)+[rect(a*.72-w,0,a*.72,h)]
        return _lower_a(a,h,w,r)
    if c=="b":return [v(l),*ring(m,h*.40,a*.36,h*.40,w,r)]
    if c=="c":return _open_round(a,h,w,r,a*(.06+.12*p["axes"]["aperture"]))
    if c=="d":return [*ring(m,h*.40,a*.36,h*.40,w,r),v(right)]
    if c=="e":return ring(m,h/2,a*.32,h/2+10,w,r)+[bar(h/2,l,m)]
    if c=="f":return [v(m,-90,h),bar(h),bar(h*.48,l,right*.80)]
    if c=="g":return ring(m,h*.45,a*.31,h*.38,w,r)+[v(right,-180,h*.35),bar(0,m,right)]
    if c=="h":return [v(l,0,700),v(right,0,h*.52),bar(h*.52,l,right)]
    if c=="i":return [v(m,0,h*.62),*ring(m,h+85,w*.52,w*.52,w*.28,r)]
    if c=="j":return [v(m,-180,h*.62),bar(0,l,m),*ring(m,h+85,w*.52,w*.52,w*.28,r)]
    if c=="k":return [v(l),stroke(l,h*.48,right,h,w),stroke(l,h*.48,right,0,w)]
    if c=="l":return [v(m)]
    if c=="m":return [v(l),v(m),v(right),bar(h*.52,l,right)]
    if c=="n":return [v(l,0,h),v(right,0,h*.52),bar(h*.52,l,right)]
    if c=="o":return ring(m,h/2,a*.32,h/2+10,w,r)
    if c=="p":return [v(l,-180,h),*ring(m,h*.40,a*.36,h*.40,w,r)]
    if c=="q":return [*ring(m,h*.40,a*.36,h*.40,w,r),v(right,-180,h)]
    if c=="r":return [v(l),bar(h*.55,l,right),stroke(l,h*.55,right,h,w)]
    if c=="s":return [bar(h),v(l,h*.48,h),bar(h*.48),v(right,0,h*.48),bar(0)]
    if c=="t":return [v(m,-30,h),bar(h),bar(0,l,right*.75)]
    if c=="u":return [v(l,h*.48,h),v(right),bar(0),v(l,0,h*.22)]
    if c=="v":return [stroke(l,h,m,0,w),stroke(right,h,m,0,w)]
    if c=="w":return [stroke(l,h,a*.31,0,w),stroke(a*.31,0,m,h*.42,w),stroke(m,h*.42,a*.69,0,w),stroke(a*.69,0,right,h,w)]
    if c=="x":return [stroke(l,0,right,h,w),stroke(l,h,right,0,w)]
    if c=="y":return [stroke(l,h,m,h*.35,w),stroke(right,h,m,h*.35,w),stroke(m,h*.35,l,-180,w)]
    if c=="z":return [bar(h),stroke(right,h,l,0,w),bar(0)]
    raise ProjectValidationError(f"unreviewed Latin lower {c!r}")

def _cyrillic_upper_shape(c,a,w,r,p):
    l,right,m=80,a-80,a/2; v=lambda x,y0=0,y1=700:rect(x-w/2,y0,x+w/2,y1); bar=lambda y,x0=l,x1=right:rect(x0,y-w/2,x1,y+w/2)
    if c=="А":return _bars(a,700,w,"А")
    if c=="Б":return [v(l),bar(700),bar(350),*ring(m+28,175,a*.31,175,w,r)]
    if c=="В":return _bars(a,700,w,"В")
    if c=="Г":return _bars(a,700,w,"Г")
    if c=="Д":return _bars(a,700,w,"Д")
    if c=="Е":return _bars(a,700,w,"Е")
    if c=="Ё":return _bars(a,700,w,"Е")+ring(a*.36,800,w*.5,w*.5,w*.28,r)+ring(a*.64,800,w*.5,w*.5,w*.28,r)
    if c=="Ж":return _bars(a,700,w,"Ж")
    if c=="З":return [bar(700),bar(350),bar(0),v(right)]
    if c=="И":return _bars(a,700,w,"И")
    if c=="Й":return _bars(a,700,w,"И")+[stroke(a*.34,785,m,845,w*.42),stroke(m,845,a*.66,785,w*.42)]
    if c=="К":return _bars(a,700,w,"К")
    if c=="Л":return _bars(a,700,w,"Л")
    if c=="М":return _bars(a,700,w,"M")
    if c=="Н":return _bars(a,700,w,"Н")
    if c=="О":return ring(m,350,a*.36,362,w,r)
    if c=="П":return [v(l),v(right),bar(700)]
    if c=="Р":return _bars(a,700,w,"P")
    if c=="С":return _open_round(a,700,w,r,a*(.06+.12*p["axes"]["aperture"]))
    if c=="Т":return _bars(a,700,w,"T")
    if c=="У":return _bars(a,700,w,"У")
    if c=="Ф":return _bars(a,700,w,"Ф")
    if c=="Х":return _bars(a,700,w,"X")
    if c=="Ц":return [v(l),v(right,-120,700),bar(700),bar(0)]
    if c=="Ч":return [v(l,350,700),v(right),bar(350,l,right)]
    if c=="Ш":return _bars(a,700,w,"Ш")
    if c=="Щ":return [v(l),v(m),v(right,-120,700),bar(700),bar(0)]
    if c=="Ъ":return [v(l),bar(700),bar(350,m,right),v(m,0,350),*ring(m+50,175,a*.24,175,w,r)]
    if c=="Ы":return [v(l),v(m),bar(700,m,right),bar(350,m,right),*ring(m+75,175,a*.27,175,w,r)]
    if c=="Ь":return _bars(a,700,w,"Ь")
    if c=="Э":return _open_round(a,700,w,r,a*(.06+.12*p["axes"]["aperture"]),True)+[bar(350,l,m)]
    if c=="Ю":return [v(l),*ring(m+65,350,a*.28,362,w,r)]
    if c=="Я":return _bars(a,700,w,"Я")
    raise ProjectValidationError(f"unreviewed Cyrillic cap {c!r}")

def _cyrillic_lower_shape(c,a,h,w,r,p):
    l,right,m=80,a-80,a/2; v=lambda x,y0=0,y1=h:rect(x-w/2,y0,x+w/2,y1); bar=lambda y,x0=l,x1=right:rect(x0,y-w/2,x1,y+w/2)
    if c=="а":return _lower_a(a,h,w,r)
    if c=="б":return [bar(h),v(l),*ring(m+25,h*.4,a*.36,h*.38,w,r)]
    if c=="в":return [v(l),*ring(m+30,h*.70,a*.34,h*.36,w,r),*ring(m+30,h*.25,a*.34,h*.36,w,r)]
    if c=="г":return [v(l),bar(h)]
    if c=="д":return [bar(0,l-30,right+30),stroke(l,0,m,h,w),stroke(right,0,m,h,w),stroke(l,0,l-35,-120,w),stroke(right,0,right+35,-120,w)]
    if c in "её":
        form=ring(m,h/2,a*.32,h/2+10,w,r)+[bar(h/2,l,m)]
        return form if c=="е" else form+ring(a*.36,h+95,w*.5,w*.5,w*.28,r)+ring(a*.64,h+95,w*.5,w*.5,w*.28,r)
    if c=="ж":return [v(m),stroke(m,h*.5,l,h,w),stroke(m,h*.5,l,0,w),stroke(m,h*.5,right,h,w),stroke(m,h*.5,right,0,w)]
    if c=="з":return [bar(h),bar(h*.48),bar(0),v(right)]
    if c=="и":return [v(l),v(right),stroke(l,0,right,h,w)]
    if c=="й":return [v(l),v(right),stroke(l,0,right,h,w),stroke(a*.34,h+70,m,h+125,w*.42),stroke(m,h+125,a*.66,h+70,w*.42)]
    if c=="к":return [v(l),stroke(l,h*.5,right,h,w),stroke(l,h*.5,right,0,w)]
    if c=="л":return [stroke(l,0,m,h,w),stroke(right,0,m,h,w)]
    if c=="м":return [v(l),v(right),stroke(l,h,right,h*.45,w),stroke(right,h*.45,m,0,w)]
    if c=="н":return [v(l),v(right),bar(h*.5)]
    if c=="о":return ring(m,h/2,a*.32,h/2+10,w,r)
    if c=="п":return [v(l),v(right),bar(h)]
    if c=="р":return [v(l,-180,h),*ring(m,h*.4,a*.36,h*.4,w,r)]
    if c=="с":return _open_round(a,h,w,r,a*(.06+.12*p["axes"]["aperture"]))
    if c=="т":return [bar(h),v(m)]
    if c=="у":return _latin_lower_shape("y",a,h,w,r,p)
    if c=="ф":return ring(m,h/2,a*.32,h/2+10,w,r)+[v(m,-40,h+40)]
    if c=="х":return _latin_lower_shape("x",a,h,w,r,p)
    if c=="ц":return [v(l),v(right,-120,h),bar(h),bar(0)]
    if c=="ч":return [v(l,h*.5,h),v(right),bar(h*.5,l,right)]
    if c=="ш":return [v(l),v(m),v(right),bar(h),bar(0)]
    if c=="щ":return [v(l),v(m),v(right,-120,h),bar(h),bar(0)]
    if c=="ъ":return [v(l),bar(h),bar(h*.5,m,right),v(m,0,h*.5),*ring(m+50,h*.34,a*.34,h*.36,w,r)]
    if c=="ы":return [v(l),v(m),bar(h,m,right),bar(h*.5,m,right),*ring(m+75,h*.34,a*.32,h*.36,w,r)]
    if c=="ь":return [v(l),*ring(m,h*.4,a*.36,h*.4,w,r)]
    if c=="э":return _open_round(a,h,w,r,a*(.06+.12*p["axes"]["aperture"]),True)+[bar(h/2,l,m)]
    if c=="ю":return [v(l),*ring(m+65,h/2,a*.32,h/2+10,w,r)]
    if c=="я":return [v(right),*ring(m-35,h*.60,a*.32,h*.36,w,r),stroke(m-35,h*.36,l,0,w)]
    raise ProjectValidationError(f"unreviewed Cyrillic lower {c!r}")
def _shape(d,p):
    q,c,a,w,r,xh=d["recipe"],chr(d["unicode"]),_advance(d),p["axes"]["weight"],p["axes"]["roundness"],p["axes"]["xHeight"]
    if q=="mark-acute":return [stroke(180,720,340,890,w*.5)]
    if q=="mark-dieresis":return ring(180,800,w*.52,w*.52,w*.28,r)+ring(340,800,w*.52,w*.52,w*.28,r)
    if q.startswith("common-") or q=="blank-nbsp":return _common_shape(d["unicode"],a,w,r)
    if q.startswith("digit-"):return _digit_shape(c,a,w,r,p)
    if q.startswith("latin-upper-"):return _latin_upper_shape(c,a,w,r,p)
    if q.startswith("latin-lower-"):return _latin_lower_shape(c,a,xh,w,r,p)
    if q.startswith("cyrillic-upper-"):return _cyrillic_upper_shape(c,a,w,r,p)
    if q.startswith("cyrillic-lower-"):return _cyrillic_lower_shape(c,a,xh,w,r,p)
    raise ProjectValidationError(f"unreviewed recipe {q!r}")
def _metrics_class(d):
    q=d["recipe"]
    return "mark" if q.startswith("mark-") else "punctuation" if q.startswith(("common-","blank-")) else "tabular" if q.startswith("digit-") else "cyrillic" if q.startswith("cyrillic-") else "latin"
def _anchors(d,a,p):
    q=d["recipe"]
    if q.startswith("mark-"):return {"_top":(260*p["axes"]["width"],760)}
    if "upper" in q:return {"top":(a/2,760),"bottom":(a/2,0)}
    if "lower" in q:return {"top":(a/2,p["axes"]["xHeight"]+55),"bottom":(a/2,0)}
    return {}

KERNING_GROUPS={"public.kern1.Latn.diagonal":["A","V","W","Y"],"public.kern2.Latn.round":["O","C","G","Q","o","c","e"],"public.kern1.Cyrl.diagonal":["uni0410","uni0414","uni041B","uni0423","uni0422","uni0416","uni0425"],"public.kern2.Cyrl.round":["uni041E","uni0421","uni0424","uni042E","uni043E","uni0441","uni044D","uni044E","uni0444"]}
KERNING_PAIRS={("public.kern1.Latn.diagonal","public.kern2.Latn.round"):-72,("public.kern1.Cyrl.diagonal","public.kern2.Cyrl.round"):-66,("A","V"):-60,("V","A"):-60,("A","W"):-44,("A","Y"):-52,("T","A"):-52,("T","O"):-58,("T","a"):-42,("T","o"):-42,("uni0422","uni0410"):-54,("uni0422","uni0430"):-48,("uni0422","uni043E"):-48}
def kerning_value(left,right):
    if (left,right) in KERNING_PAIRS:return KERNING_PAIRS[(left,right)]
    lg=[k for k,v in KERNING_GROUPS.items() if k.startswith("public.kern1") and left in v]; rg=[k for k,v in KERNING_GROUPS.items() if k.startswith("public.kern2") and right in v]
    return next((KERNING_PAIRS[(x,y)] for x in lg for y in rg if (x,y) in KERNING_PAIRS),0)
def validate_glyph(g):
    if g["advance"]<0 or (g["advance"]==0 and g["metricsClass"]!="mark"):raise ProjectValidationError(f"{g['name']}: invalid advance")
    for contour in g["contours"]:
        if len(contour)<4 or contour[0][0]!="M" or contour[-1]!=("Z",):raise ProjectValidationError(f"{g['name']}: contour is not closed")
        pen=AreaPen(); pen.moveTo(contour[0][1:]); segments=[]; previous=contour[0][1:]
        for cmd in contour[1:]:
            if cmd[0]=="L":pen.lineTo(cmd[1:]);segments.append((previous,cmd[1:]));previous=cmd[1:]
            elif cmd[0]=="C":pen.curveTo(cmd[1:3],cmd[3:5],cmd[5:]);previous=cmd[5:]
            elif cmd[0]=="Z":pen.closePath();segments.append((previous,contour[0][1:]))
            else:raise ProjectValidationError(f"{g['name']}: invalid contour command")
        if not math.isfinite(pen.value) or abs(pen.value)<1e-6:raise ProjectValidationError(f"{g['name']}: zero area")
        for index,(a,b) in enumerate(segments):
            for other,(c,d) in enumerate(segments[index+2:],index+2):
                if index==0 and other==len(segments)-1:continue
                if _line_intersects(a,b,c,d):raise ProjectValidationError(f"{g['name']}: self-intersecting contour")
def _line_intersects(a,b,c,d):
    cross=lambda p,q,r:(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    u,v,x,y=cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b)
    return u*v<0 and x*y<0
def evaluate_project(p):
    validate_project(p); out=[]
    for d in GLYPH_DEFINITIONS:
        a=round(_advance(d)*p["axes"]["width"]); g={**d,"advance":a,"contours":_scale(_shape(d,p),p["axes"]["width"]),"metricsClass":_metrics_class(d),"anchors":_anchors(d,a,p)}; validate_glyph(g); out.append(g)
    return {"sourceHash":source_hash(p),"glyphs":out,"kerning":KERNING_PAIRS}
def svg_path(contour):return " ".join(c[0] if c[0]=="Z" else c[0]+" "+" ".join(f"{x:.4f}".rstrip("0").rstrip(".") for x in c[1:]) for c in contour)
def glyph_signature(g):
    points=[c[-2:] for q in g["contours"] for c in q if c[0] in {"M","L","C"}]
    return {"name":g["name"],"advance":g["advance"],"contours":len(g["contours"]),"bounds":[round(min((x for x,y in points),default=0),4),round(min((y for x,y in points),default=0),4),round(max((x for x,y in points),default=0),4),round(max((y for x,y in points),default=0),4)],"outline":"|".join(svg_path(q) for q in g["contours"])}
def parity_signature(p):return [glyph_signature(g) for g in evaluate_project(p)["glyphs"]]
def with_controls(p,**values):
    copy=deepcopy(p); mapping={"weight":"weight","width":"width","x_height":"xHeight","roundness":"roundness","aperture":"aperture"}
    for source,target in mapping.items():
        if values.get(source) is not None:copy["axes"][target]=values[source]
    if values.get("counter") is not None:copy["localOverrides"]["O"]["counter"]=values["counter"]
    if values.get("construction") is not None:copy["switches"]["aConstruction"]=values["construction"]
    if values.get("zero_style") is not None:copy["switches"]["zeroStyle"]=values["zero_style"]
    if values.get("active_preset") is not None:copy["activePreset"]=values["active_preset"]
    validate_project(copy);return copy
