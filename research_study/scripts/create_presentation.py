#!/usr/bin/env python3
"""Build an editable 8-slide PowerPoint using measured results and generated plots."""
from __future__ import annotations
import csv,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
from pptx.util import Inches,Pt

NAVY=RGBColor(20,35,61); BLUE=RGBColor(54,103,201); TEAL=RGBColor(26,137,122); ORANGE=RGBColor(226,129,52); PALE=RGBColor(244,247,251); WHITE=RGBColor(255,255,255); MUTED=RGBColor(89,103,122); DARK=RGBColor(28,40,56); RED=RGBColor(174,67,69)
W,H=13.333,7.5

def add_box(slide,x,y,w,h,text='',size=18,color=DARK,bold=False,fill=None,align=PP_ALIGN.LEFT,margin=.12):
    shape=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)) if fill is None else slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is not None:
        shape.fill.solid();shape.fill.fore_color.rgb=fill;shape.line.fill.background()
    tf=shape.text_frame;tf.clear();tf.word_wrap=True;tf.margin_left=Inches(margin);tf.margin_right=Inches(margin);tf.margin_top=Inches(margin);tf.margin_bottom=Inches(margin)
    for i,line in enumerate(text.split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.alignment=align;p.space_after=Pt(4)
        for run in p.runs:run.font.name='Aptos';run.font.size=Pt(size);run.font.bold=bold;run.font.color.rgb=color
    return shape

def add_rich_paragraph(slide,x,y,w,h,parts,size=17,fill=None):
    shape=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)) if fill is None else slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is not None:shape.fill.solid();shape.fill.fore_color.rgb=fill;shape.line.fill.background()
    tf=shape.text_frame;tf.clear();tf.word_wrap=True;tf.margin_left=Inches(.15);tf.margin_right=Inches(.15);tf.margin_top=Inches(.12)
    p=tf.paragraphs[0]
    for text,bold,color in parts:
        r=p.add_run();r.text=text;r.font.name='Aptos';r.font.size=Pt(size);r.font.bold=bold;r.font.color.rgb=color
    return shape

def add_bullets(slide,x,y,w,h,items,size=18,color=DARK,fill=None):
    shape=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)) if fill is None else slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is not None:shape.fill.solid();shape.fill.fore_color.rgb=fill;shape.line.fill.background()
    tf=shape.text_frame;tf.clear();tf.word_wrap=True;tf.margin_left=Inches(.2);tf.margin_top=Inches(.15);tf.margin_right=Inches(.18)
    for i,item in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text='•  '+item;p.space_after=Pt(9);p.level=0
        for r in p.runs:r.font.name='Aptos';r.font.size=Pt(size);r.font.color.rgb=color
    return shape

def new_slide(prs,title,kicker=None):
    s=prs.slides.add_slide(prs.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=WHITE
    bar=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,Inches(W),Inches(.12));bar.fill.solid();bar.fill.fore_color.rgb=TEAL;bar.line.fill.background()
    if kicker:add_box(s,.52,.32,11,.25,kicker.upper(),10,TEAL,True)
    add_box(s,.52,.62,12.2,.62,title,27,NAVY,True)
    add_box(s,.55,7.17,12.2,.18,'WATERGPT RESEARCH STUDY  •  BEIR SCIFACT TEST  •  2026',8,MUTED,False)
    return s

def add_card(slide,x,y,w,h,title,body,accent=BLUE):
    card=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h));card.fill.solid();card.fill.fore_color.rgb=PALE;card.line.color.rgb=RGBColor(224,231,239)
    stripe=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(.08),Inches(h));stripe.fill.solid();stripe.fill.fore_color.rgb=accent;stripe.line.fill.background()
    add_box(slide,x+.22,y+.14,w-.4,.4,title,17,NAVY,True)
    add_box(slide,x+.22,y+.62,w-.42,h-.72,body,13,DARK)

def add_image(slide,path,x,y,w,h):
    slide.shapes.add_picture(str(path),Inches(x),Inches(y),width=Inches(w),height=Inches(h))

def main():
    metrics=list(csv.DictReader((ROOT/'results/metrics/comparative_results.csv').open()))
    by={r['Method']:r for r in metrics}
    stats=json.loads((ROOT/'results/metrics/paired_statistics.json').read_text())
    lat=json.loads((ROOT/'results/metrics/latency.json').read_text())['steady_state']
    ds=json.loads((ROOT/'results/metadata/dataset.json').read_text())['counts']
    bm=by['BM25'];de=by['Dense'];hy=by['Hybrid RRF']
    ndcg_hbm=next(r for r in stats if r['metric']=='ndcg@10' and r['method_a']=='BM25' and r['method_b']=='Hybrid RRF')
    ndcg_hde=next(r for r in stats if r['metric']=='ndcg@10' and r['method_a']=='Dense' and r['method_b']=='Hybrid RRF')
    rec_hbm=next(r for r in stats if r['metric']=='recall@100' and r['method_a']=='BM25' and r['method_b']=='Hybrid RRF')
    prs=Presentation();prs.slide_width=Inches(W);prs.slide_height=Inches(H)
    # 1 Problem
    s=prs.slides.add_slide(prs.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=NAVY
    add_box(s,.78,.68,10,.3,'WATERGPT  /  RESEARCH STUDY',12,RGBColor(126,211,195),True)
    add_box(s,.78,1.55,10.8,1.55,'Finding the right scientific evidence\nwith lexical, dense, and hybrid retrieval',31,WHITE,True)
    add_box(s,.82,3.62,9.9,1.0,'Research problem: scientific claims use precise terminology, but relevant evidence may describe the same concept with different words. Which retrieval signals best balance ranking quality, coverage, and latency?',19,RGBColor(224,232,242))
    for i,(n,label,c) in enumerate([('BM25','LEXICAL',BLUE),('MiniLM','DENSE',TEAL),('RRF','HYBRID',ORANGE)]):
        x=.85+i*3.4
        pill=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(5.45),Inches(2.65),Inches(.78));pill.fill.solid();pill.fill.fore_color.rgb=c;pill.line.fill.background()
        add_box(s,x,5.62,2.65,.3,f'{n}   /   {label}',15,WHITE,True,align=PP_ALIGN.CENTER)
    add_box(s,.83,7.0,11,.2,'Evaluating Lexical, Dense, and Hybrid Retrieval Methods for Scientific Literature Search',9,RGBColor(181,196,214))
    # 2 Research question / hypotheses
    s=new_slide(prs,'Question & hypotheses','01  •  study design')
    add_box(s,.65,1.42,12,.75,'Does combining lexical and semantic retrieval improve scientific literature discovery compared with either method alone?',22,NAVY,True,PALE)
    add_card(s,.65,2.55,3.9,2.55,'H1  Ranking quality','Hybrid RRF may improve ranking effectiveness over the independent lexical and dense systems.',BLUE)
    add_card(s,4.72,2.55,3.9,2.55,'H2 / H3  Coverage','Dense retrieval may find semantically related evidence missed by lexical matching; combining both may improve coverage.',TEAL)
    add_card(s,8.78,2.55,3.9,2.55,'H4  Cost','Hybrid search may add query-time and indexing overhead.',ORANGE)
    add_box(s,.72,5.55,11.8,.8,'These are testable hypotheses—not assumed conclusions. Primary settings were fixed before evaluation; SciFact test results were not used to tune the main configuration.',15,MUTED,False,PALE)
    # 3 Dataset/methodology
    s=new_slide(prs,'Dataset & controlled methodology','02  •  benchmark')
    cards=[(str(ds['documents']),'corpus documents'),(str(ds['test_queries']),'official test queries'),(str(ds['positive_qrels']),'positive qrels')]
    for i,(v,l) in enumerate(cards):
        x=.7+i*2.55;add_box(s,x,1.5,2.2,.65,v,27,[BLUE,TEAL,ORANGE][i],True,align=PP_ALIGN.CENTER,fill=PALE);add_box(s,x,2.18,2.2,.3,l,12,MUTED,False,align=PP_ALIGN.CENTER)
    add_card(s,8.55,1.48,4.0,1.32,'Benchmark scope','SciFact is claim-to-evidence retrieval over scientific abstracts; not an arXiv-only or all-disciplines test.',ORANGE)
    # flow boxes
    labels=[('Official corpus + test qrels','same 300 query IDs'),('BM25 / Dense','same title + abstract'),('RRF + evaluation','top 1,000 candidates')]
    for i,(title,sub) in enumerate(labels):
        x=.68+i*4.22
        add_box(s,x,3.15,3.55,.78,title,17,NAVY,True,PALE,PP_ALIGN.CENTER)
        add_box(s,x+.12,4.03,3.3,.46,sub,12,MUTED,False,align=PP_ALIGN.CENTER)
        if i<2:add_box(s,x+3.63,3.34,.45,.4,'→',25,TEAL,True,align=PP_ALIGN.CENTER)
    add_bullets(s,.8,4.85,11.7,1.5,['5,183 documents; 300 test queries selected by official test qrels; 339 positive judgments.','Macro nDCG@10, MRR@10, Recall@10 and Recall@100; paired query-level analysis.','Official archive checksum verified; raw dataset is locally downloaded and excluded from Git.'],14)
    # 4 BM25/Dense
    s=new_slide(prs,'Two independent retrieval baselines','03  •  component systems')
    add_card(s,.68,1.55,5.85,3.65,'A  Lexical BM25','BM25Okapi\nk1 = 1.5  •  b = 0.75\nShared lowercase alphanumeric tokenization\nTitle + abstract indexed\nStrong exact-term baseline; sparse vocabulary overlap can limit recall.',BLUE)
    add_card(s,6.78,1.55,5.85,3.65,'B  Dense semantic retrieval','sentence-transformers/all-MiniLM-L6-v2\n384-dimensional normalized embeddings\nFAISS IndexFlatIP = exact cosine ranking\nLoaded max sequence length: 256 tokens\nCaptures embedding similarity; long inputs are truncated.',TEAL)
    add_box(s,.9,5.65,11.5,.8,'The measured test results show different query-level wins: BM25 ranked a CTCF evidence abstract first for one claim; Dense ranked a BCL-2 leukemia abstract first for another. Scores alone do not imply scientific understanding.',14,MUTED,False,PALE)
    # 5 Hybrid
    s=new_slide(prs,'Hybrid system: Reciprocal Rank Fusion','04  •  rank aggregation')
    add_card(s,.7,1.55,3.4,1.38,'BM25 top-1,000','ranked IDs + BM25 scores',BLUE)
    add_card(s,.7,3.3,3.4,1.38,'Dense top-1,000','ranked IDs + cosine scores',TEAL)
    add_box(s,4.4,1.95,2.1,.55,'RRF  k = 60',19,NAVY,True,PALE,PP_ALIGN.CENTER)
    add_box(s,4.42,2.62,2.05,1.4,'RRF(d) = Σ 1 / (60 + rankᵢ(d))',16,DARK,True,align=PP_ALIGN.CENTER)
    add_box(s,6.9,2.05,.55,.5,'→',28,ORANGE,True,align=PP_ALIGN.CENTER)
    add_card(s,7.62,1.85,4.75,2.15,'Fused ranking','Rank-based combination; raw BM25 and cosine scores are never blended. Deterministic document-ID tie-break. Same queries, corpus, IDs, text fields, and evaluation depth.',ORANGE)
    add_box(s,.82,5.0,11.55,1.05,'Why fuse? Lexical and dense systems can contribute complementary ranks. On this SciFact split, RRF improved the aggregate point estimates—but its nDCG@10 advantage over Dense was statistically inconclusive.',16,NAVY,True,PALE)
    # 6 Findings
    s=new_slide(prs,'Measured results: quality and cost','05  •  primary test results')
    table=s.shapes.add_table(4,5,Inches(.55),Inches(1.42),Inches(7.3),Inches(2.15)).table
    widths=[2.15,1.25,1.2,1.3,1.4]
    for i,w in enumerate(widths):table.columns[i].width=Inches(w)
    headers=['Method','nDCG@10','MRR@10','Recall@10','Recall@100']
    data=[['BM25',bm['ndcg@10'],bm['mrr@10'],bm['recall@10'],bm['recall@100']],['Dense',de['ndcg@10'],de['mrr@10'],de['recall@10'],de['recall@100']],['Hybrid RRF',hy['ndcg@10'],hy['mrr@10'],hy['recall@10'],hy['recall@100']]]
    for c,h in enumerate(headers):
        cell=table.cell(0,c);cell.text=h;cell.fill.solid();cell.fill.fore_color.rgb=NAVY
    for ri,row in enumerate(data,1):
        for ci,val in enumerate(row):
            cell=table.cell(ri,ci);cell.text=val if ci==0 else f'{float(val):.4f}';cell.fill.solid();cell.fill.fore_color.rgb=RGBColor(238,247,245) if ri==3 else WHITE
    for ri,row in enumerate(table.rows):
        for ci,cell in enumerate(row.cells):
            cell.margin_left=Inches(.07);cell.margin_right=Inches(.04);cell.margin_top=Inches(.05);cell.margin_bottom=Inches(.03);cell.vertical_anchor=MSO_ANCHOR.MIDDLE
            for p in cell.text_frame.paragraphs:
                p.alignment=PP_ALIGN.CENTER
                for r in p.runs:r.font.name='Aptos';r.font.size=Pt(11);r.font.bold=(ri==0 or (ri==3 and ci==0));r.font.color.rgb=WHITE if ri==0 else DARK
    add_image(s,ROOT/'results/plots/effectiveness.png',8.05,1.35,4.75,3.55)
    add_box(s,.65,4.0,7.15,.75,f"Hybrid − BM25 nDCG@10 = {abs(ndcg_hbm['mean_difference']):.4f}; 95% CI [{abs(ndcg_hbm['ci_high']):.4f}, {abs(ndcg_hbm['ci_low']):.4f}], Holm p={ndcg_hbm['p_holm']:.4f}.",14,TEAL,True,PALE)
    add_box(s,.65,5.0,7.1,.8,f"Median single-query latency: BM25 {lat['BM25']['median_seconds']*1000:.2f} ms  •  Dense {lat['Dense']['median_seconds']*1000:.2f} ms  •  Hybrid {lat['Hybrid RRF']['median_seconds']*1000:.2f} ms.",14,NAVY,True)
    add_box(s,8.1,5.05,4.7,.58,f"Hybrid Recall@100 = {float(hy['recall@100']):.3f}; hybrid is about {lat['Hybrid RRF']['median_seconds']/lat['BM25']['median_seconds']:.2f}× BM25 median latency.",13,ORANGE,True,PALE)
    # 7 Statistical analysis/limitations
    s=new_slide(prs,'Statistical evidence & limitations','06  •  paired analysis')
    add_image(s,ROOT/'results/plots/confidence_intervals.png',6.4,1.45,6.3,4.5)
    add_box(s,.72,1.48,5.35,.62,'Difference convention: method A − method B',15,NAVY,True)
    add_bullets(s,.76,2.18,5.35,2.9,[f"BM25 vs Hybrid nDCG@10: mean diff {ndcg_hbm['mean_difference']:.4f}; CI [{ndcg_hbm['ci_low']:.4f}, {ndcg_hbm['ci_high']:.4f}], adjusted p={ndcg_hbm['p_holm']:.4f} (significant).",f"Dense vs Hybrid nDCG@10: mean diff {ndcg_hde['mean_difference']:.4f}; CI [{ndcg_hde['ci_low']:.4f}, {ndcg_hde['ci_high']:.4f}], adjusted p={ndcg_hde['p_holm']:.4f} (inconclusive).",f"BM25 vs Hybrid Recall@100: diff {rec_hbm['mean_difference']:.4f}; adjusted p={rec_hbm['p_holm']:.2g} (significant)."],13)
    add_box(s,.75,5.25,5.35,1.2,'Limitations: claim-to-abstract SciFact task; qrels may be incomplete; one compact English benchmark; CPU-only latency; test-set ablations are descriptive, not tuning.',13,MUTED,False,PALE)
    # 8 Conclusion
    s=new_slide(prs,'Conclusion & future work','07  •  takeaways')
    add_card(s,.72,1.48,3.85,2.0,'Finding 1','RRF improved over BM25 on nDCG@10 and Recall@100 with paired evidence.',TEAL)
    add_card(s,4.75,1.48,3.85,2.0,'Finding 2','Hybrid did not establish a significant nDCG@10 improvement over Dense.',BLUE)
    add_card(s,8.78,1.48,3.85,2.0,'Finding 3','Hybrid improved coverage but incurred higher single-query latency.',ORANGE)
    add_bullets(s,.88,4.0,11.5,1.45,['Next: evaluate SciDocs or an arXiv-domain pilot with a separately prespecified protocol and no pooling with SciFact.','Keep validation-based parameter selection separate from final test evaluation.','All systems, code, runfiles, confidence intervals, error examples, and plots are available in the independent research_study workspace.'],15)
    add_box(s,.84,5.82,11.8,.62,'References: Wadden et al. (EMNLP 2020); Thakur et al. (BEIR, 2021); Cormack et al. (SIGIR 2009); Reimers & Gurevych (2019); Johnson et al. (IEEE TBD, 2021).',11,MUTED,False,PALE)
    out=ROOT/'reports/presentation.pptx';prs.save(out)
    if len(prs.slides)!=8:raise AssertionError(f'Expected 8 slides, got {len(prs.slides)}')
    print(f'Wrote editable PowerPoint with {len(prs.slides)} slides: {out}')
if __name__=='__main__':main()
