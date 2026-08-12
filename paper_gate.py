#!/usr/bin/env python3
"""PaperGate-IEEE: zero-dependency LaTeX pre-submission risk auditor.
Independent project; not affiliated with IEEE.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from dataclasses import dataclass, asdict

SECTION_RE=re.compile(r"\\section\*?\{([^}]*)\}",re.I)
LABEL_RE=re.compile(r"\\label\{([^}]+)\}")
REF_RE=re.compile(r"\\(?:ref|eqref|autoref|cref|Cref)\{([^}]+)\}")
CITE_RE=re.compile(r"\\cite(?:t|p|alp|author|year)?\*?\{([^}]+)\}")
BIBITEM_RE=re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}")
WORD_RE=re.compile(r"\b[\w'-]+\b",re.UNICODE)

@dataclass
class Finding:
    severity:str; category:str; message:str; recommendation:str; penalty:int=0

def strip_comments(text):
    out=[]
    for line in text.splitlines():
        buf=[]
        for i,ch in enumerate(line):
            if ch=='%' and (i==0 or line[i-1] != '\\'): break
            buf.append(ch)
        out.append(''.join(buf))
    return '\n'.join(out)

def env(text,name):
    m=re.search(rf"\\begin\{{{re.escape(name)}\}}(.*?)\\end\{{{re.escape(name)}\}}",text,re.S|re.I)
    return m.group(1).strip() if m else ''

def plain(text):
    x=re.sub(r"\\(?:cite|ref|eqref|autoref|cref|Cref)\*?(?:\[[^\]]*\])?\{[^}]*\}",' ',text)
    x=re.sub(r"\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}",r"\1",x)
    x=re.sub(r"\\[a-zA-Z@]+\*?",' ',x)
    x=re.sub(r"[{}$~_^]",' ',x)
    return re.sub(r"\s+",' ',x).strip()

def has(text,*phrases):
    t=text.lower(); return any(p.lower() in t for p in phrases)

def audit(text):
    clean=strip_comments(text); p=plain(clean); sections=SECTION_RE.findall(clean); s=' | '.join(sections).lower(); f=[]
    def add(sev,cat,msg,fix,pen): f.append(Finding(sev,cat,msg,fix,pen))
    abstract=plain(env(clean,'abstract')); nabs=len(WORD_RE.findall(abstract))
    if not abstract: add('HIGH','submission','No abstract detected.','Add a self-contained abstract with problem, method, evidence, and a key result.',12)
    else:
        if nabs<80: add('MEDIUM','submission',f'Abstract appears short ({nabs} words).','Ensure it states context, method, setting, and quantitative outcome.',4)
        if nabs>250: add('MEDIUM','submission',f'Abstract appears long ({nabs} words).','Check the target venue limit and compress if needed.',4)
        if not re.search(r"\b\d+(?:\.\d+)?\s*%|\b\d+(?:\.\d+)?\b",abstract): add('MEDIUM','evidence','No obvious quantitative result in abstract.','Add one or two representative metrics.',5)
    if not has(s,'introduction','background'): add('HIGH','story','No Introduction/Background section detected.','Make the problem, gap, and contribution path explicit.',8)
    if not has(s,'method','methodology','proposed','framework','approach','system'): add('HIGH','story','No obvious method/system section detected.','Use a clearly named section for the proposed method and system flow.',8)
    if not has(s,'experiment','evaluation','results','validation'): add('HIGH','evidence','No obvious evaluation/results section detected.','Add baselines, protocols, ablations, robustness, and deployment evidence.',10)
    if not has(s,'conclusion'): add('MEDIUM','story','No Conclusion section detected.','Summarize supported findings, limitations, and practical implications.',3)
    intro_m=re.search(r"\\section\*?\{[^}]*(?:Introduction|Background)[^}]*\}(.*?)(?=\\section\*?\{|\\end\{document\})",clean,re.S|re.I)
    intro=plain(intro_m.group(1)) if intro_m else p[:6000]
    if not has(intro,'our contributions','main contributions','we contribute','contribution'): add('MEDIUM','novelty','No explicit contribution statement detected.','State 2–4 precise algorithmic, system, and empirical contributions.',6)
    if not has(intro,'however','remain','gap','limitation','existing methods','prior work'): add('MEDIUM','novelty','Problem gap is weakly signposted.','Explain what existing methods fail to handle and the operational consequence.',4)
    labels=LABEL_RE.findall(clean); refs=REF_RE.findall(clean)
    dup=sorted({x for x in labels if labels.count(x)>1}); missing=sorted(set(refs)-set(labels))
    if dup: add('HIGH','submission','Duplicate labels: '+', '.join(dup[:8])+'.','Make every LaTeX label unique.',8)
    if missing: add('HIGH','submission','Undefined referenced labels: '+', '.join(missing[:8])+'.','Repair broken cross-references.',8)
    cites=[]
    for g in CITE_RE.findall(clean): cites += [x.strip() for x in g.split(',') if x.strip()]
    bib=BIBITEM_RE.findall(clean)
    misscite=sorted(set(cites)-set(bib)) if bib else []
    if misscite: add('HIGH','submission','Citation keys missing from inline bibliography: '+', '.join(misscite[:8])+'.','Repair citation keys.',8)
    nfig=len(re.findall(r"\\begin\{figure\*?\}",clean)); ntab=len(re.findall(r"\\begin\{table\*?\}",clean))
    if nfig==0 and ntab==0: add('MEDIUM','evidence','No figures or tables detected.','Add concise visual evidence where appropriate.',4)
    if not has(p,'ablation','component analysis','module analysis','w/o ','without the'): add('MEDIUM','evidence','No obvious ablation/component analysis detected.','Isolate the effect of each proposed component.',6)
    if not has(p,'standard deviation','std.','confidence interval','95% ci','mean ±','mean+/-','multiple runs','three runs','five runs'): add('MEDIUM','evidence','No repeated-run variability/confidence interval cue detected.','Report variability where stochasticity affects conclusions.',4)
    if not has(p,'limitation','limitations','failure case','failure cases','threats to validity'): add('LOW','evidence','No explicit limitations/failure-case discussion detected.','State deployment boundaries and known failure modes.',2)
    if not has(p,'code is available','source code','github','reproducib','implementation details'): add('LOW','evidence','No obvious reproducibility/code cue detected.','Provide implementation details and artifacts where feasible.',1)
    if not has(p,'industrial','deployment','edge device','real-world','field data','production','maintenance','plant','factory','operator','latency','memory footprint','throughput'): add('MEDIUM','industrial','Industrial/deployment relevance is weakly signposted.','Connect the method to a concrete workflow, constraint, and decision consequence.',6)
    rel=has(p,'uncertainty','reliability','calibration','selective prediction','abstain','risk control','confidence')
    if rel and not has(p,'ece','expected calibration error','brier','negative log-likelihood','nll','reliability diagram','calibration error'): add('HIGH','reliability','Reliability/uncertainty is discussed without an obvious calibration metric.','Add calibration metrics and preferably a calibration curve.',9)
    if rel and not has(p,'coverage','risk-coverage','selective risk','abstain','reject option','acquire','selective'): add('MEDIUM','reliability','No selective-decision/coverage evidence detected.','Report coverage versus risk/cost if decisions can defer, acquire, or abstain.',5)
    strong=re.findall(r"\b(state[- ]of[- ]the[- ]art|sota|outperform(?:s|ed)? all|guarantee(?:s|d)?|always|never fails?|universally)\b",p,re.I)
    if strong: add('MEDIUM','claims','Potentially over-strong claim language detected.','Qualify claims to the tested setting and support them with adequate evidence.',4)
    score=max(0,100-min(100,sum(x.penalty for x in f)))
    verdict='READY' if score>=90 else 'MINOR RISKS' if score>=75 else 'REVISE BEFORE SUBMISSION' if score>=55 else 'HIGH RISK'
    groups={'submission_hygiene':{'submission'},'technical_story':{'story','novelty','claims','industrial'},'evidence':{'evidence','reliability'}}
    gates={k:max(0,100-min(100,sum(x.penalty for x in f if x.category in cats))) for k,cats in groups.items()}
    rank={'HIGH':0,'MEDIUM':1,'LOW':2}; f.sort(key=lambda x:(rank[x.severity],-x.penalty,x.category))
    return {'tool':'PaperGate-IEEE','score':score,'verdict':verdict,'gates':gates,'detected':{'sections':sections,'figures':nfig,'tables':ntab,'citations':len(cites),'labels':len(labels),'abstract_words':nabs},'findings':[asdict(x) for x in f],'disclaimer':'Heuristic preflight tool; not affiliated with IEEE and not a substitute for current venue instructions or peer review.'}

def render(r):
    lines=['PaperGate-IEEE — Pre-Submission Audit','='*42,f"Score: {r['score']}/100   Verdict: {r['verdict']}",'Gates: '+' | '.join(f'{k}={v}' for k,v in r['gates'].items()),f"Detected: {len(r['detected']['sections'])} sections, {r['detected']['figures']} figures, {r['detected']['tables']} tables, {r['detected']['citations']} citations",'']
    if not r['findings']: lines.append('No heuristic risks detected. Still verify the target venue instructions.')
    for i,x in enumerate(r['findings'],1): lines += [f"[{i:02d}] {x['severity']:<6} | {x['category']} | {x['message']}",f"     Fix: {x['recommendation']}"]
    return '\n'.join(lines+['',r['disclaimer']])

def main():
    ap=argparse.ArgumentParser(description='Audit a LaTeX manuscript for common IEEE-style pre-submission risks.')
    ap.add_argument('tex'); ap.add_argument('--json',action='store_true'); ap.add_argument('--out')
    a=ap.parse_args(); r=audit(Path(a.tex).read_text(encoding='utf-8',errors='replace'))
    out=json.dumps(r,indent=2,ensure_ascii=False) if a.json else render(r)
    Path(a.out).write_text(out,encoding='utf-8') if a.out else print(out)
if __name__=='__main__': main()
