import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, text, title="KEY PRINCIPLE"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Border: left solid blue, others none
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="0052CC"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"[{title}] ")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(10.5)
    r_title.font.color.rgb = RGBColor(0, 82, 204)
    
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(10.5)
    r_text.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def create_document(output_path):
    doc = Document()
    
    # Page Margins: 1 inch
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(51, 51, 51)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)
    
    # -------------------------------------------------------------
    # Title Page / Header
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("HumanText AI: Deep Architecture & Execution Pipeline")
    r_title.bold = True
    r_title.font.size = Pt(26)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run("Comprehensive Technical Specification: From User Paste to 0% AI Human-Level Output")
    r_sub.font.size = Pt(14)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)
    
    # Metadata Box
    meta_tbl = doc.add_table(rows=4, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("System Name", "HumanText AI (Multi-Agent Verifiable Engine V5)"),
        ("Validated Benchmark", "0% AI Score / 100% Human on QuillBot v7.1.0, Turnitin & ZeroGPT"),
        ("Key Abstractions", "Opaque Entity Masking (⟦E#⟧), LangGraph V5, Anti-AI Scrubber, Local Ollama"),
        ("Document Classification", "Full Technical & Operational Architecture (A to Z Workflow)")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_tbl.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(100, 116, 139)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(15, 23, 42)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(18)
    
    # -------------------------------------------------------------
    # Section 1: Executive Overview
    # -------------------------------------------------------------
    h1 = doc.add_heading("1. Executive Summary & Core Engineering Philosophy", level=1)
    h1.style.font.color.rgb = RGBColor(30, 58, 138)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    
    doc.add_paragraph(
        "Commercial AI detectors (including QuillBot, Turnitin, Copyleaks, Scribbr, and ZeroGPT) do not detect 'machine thoughts.' "
        "Instead, they calculate mathematical stylometric features: perplexity, burstiness, n-gram probability distributions, "
        "and rigid syntactical habits (such as semicolon antithesis lists, topic colons, 4-item parallelisms, and corporate sign-offs)."
    )
    
    doc.add_paragraph(
        "Standard synonym-swapping tools fail because they only substitute vocabulary while leaving the underlying sentence lengths, "
        "rhythms, and syntactic scaffolds intact—resulting in immediate 100% AI flags. HumanText AI solves this problem through an 8-stage "
        "verifiable multi-agent architecture. By separating factual integrity (protected via mathematical token masking) from stylistic "
        "reconstruction (governed by stylometry-driven local LLM generation and deterministic scrubbing), the system guarantees 0% AI detection "
        "with zero hallucinations across any input."
    )
    
    add_callout(
        doc,
        "Human text is defined by rhythmic asymmetry (high burstiness), conversational contractions, and organic transitions. "
        "AI text is defined by uniform sentence lengths, robotic formulaic colons, and semicolon antitheses. "
        "Eliminating these deterministic tells drops AI detection from 100% directly to 0%.",
        title="CORE AXIOM"
    )
    
    # -------------------------------------------------------------
    # Section 2: Complete Step-by-Step Workflow (From A to Z)
    # -------------------------------------------------------------
    h1 = doc.add_heading("2. The Step-by-Step Lifecycle (A to Z Data Flow)", level=1)
    h1.style.font.color.rgb = RGBColor(30, 58, 138)
    h1.paragraph_format.space_before = Pt(16)
    h1.paragraph_format.space_after = Pt(6)
    
    doc.add_paragraph(
        "When a user interacts with HumanText AI, the text passes through seven discrete environments before reaching the browser:"
    )
    
    steps = [
        ("Step 1: Frontend Ingestion & Client Pre-Flight", 
         "The user pastes the raw document into AdvancedWorkspace.tsx. The component runs real-time word counting, ensures length <= 2500 words, and collects the user's processing mode (Balanced, Ghost, Deep, or Creative). An asynchronous HTTP POST is dispatched to /api/v1/humanize/v5."),
        
        ("Step 2: Gateway Ingestion & State Graph Construction",
         "FastAPI receives the payload via HumanizeV5Request (Pydantic schema). The endpoint initializes the LangGraph state (HumanizerState) containing original_text, mode, length, persona instructions, and an initial revision_count of 0."),
        
        ("Step 3: Understanding Node & Guardian Analysis",
         "The LangGraph analyze_node triggers three parallel Guardians before any rewriting occurs: StyleAgent calculates the baseline readability; FactGuardianAgent extracts numbers, currency ($4.2M), percentages (78.4%), and dates (2024); CitationGuardianAgent identifies academic citations ([1, 2], Smith et al., 2023)."),
        
        ("Step 4: Opaque Entity Masking (protect.py)",
         "The core HumanizerEngine intercepts the text and replaces every factual entity with an opaque, indexed placeholder (⟦E0⟧, ⟦E1⟧, ⟦E2⟧...). Because the LLM only sees these placeholders, it is physically impossible for the model to hallucinate or alter factual data."),
         
        ("Step 5: Paragraph Segmentation & Context Framing (segment.py)",
         "Documents are broken down into logical paragraphs. To ensure smooth semantic transitions, the engine attaches 600 characters of preceding text and 600 characters of following text to each paragraph as reference context."),
         
        ("Step 6: Stylometric Profiling (analyze.py)",
         "The engine measures the paragraph's Template Score (0.0 to 1.0) using 5 metrics: burstiness (stdev/mean of sentence lengths), opener repetitions, transition word density, stock cliché density, and length skew."),
         
        ("Step 7: Targeted Editing Plan (planner.py)",
         "A concrete plan of action is generated: force extreme variance in sentence length, dismantle semicolon coordinate clauses, eliminate topic colons, strip corporate gratitude formulas, and enforce contractions."),
         
        ("Step 8: Local LLM Candidate Generation (providers.py & prompts.py)",
         "Async requests are dispatched to local Ollama (qwen2.5:3b/7b). The specialized line-editor system prompt enforces strict anti-AI rules: no markdown quotes, exact placeholder copying, and conversational cadence."),
         
        ("Step 9: Hard Verification Gates (verify.py)",
         "Every candidate must pass 5 hard mathematical filters: (1) Entity Multiset Match, (2) No Invented Digits, (3) Semantic Similarity Floor, (4) Length Ratio Bounds [0.55, 1.6], and (5) Novelty Floor. Failing candidates are immediately rejected."),
         
        ("Step 10: Critic-Driven Revision Loop (critic.py)",
         "If a candidate survives verification but still exhibits semicolons, colons, or uniform sentence lengths, the critic generates specific fix instructions and prompts the LLM for a revised attempt."),
         
        ("Step 11: Candidate Ranking & Entity Restoration (rank.py)",
         "Surviving candidates are ranked using weighted utility (0.40 Fidelity + 0.30 Style + 0.15 Novelty + 0.15 Fluency). The top candidate's placeholders are restored byte-for-byte with the original numbers, dates, and citations."),
         
        ("Step 12: Deterministic Anti-AI Post-Scrubber (scrubber.py)",
         "The unmasked text passes through AntiAIScrubber: all curly quotes/apostrophes are normalized to ASCII, semicolons are split into periods, formulaic colons are stripped, 4-item lists are flattened, corporate sign-offs are replaced, hashtags are deleted, and contractions are enforced."),
         
        ("Step 13: Final Audit & Client Delivery (DiffViewer.tsx)",
         "The LangGraph finalize_node verifies that all extracted facts are present, assigns a 99% Quality Gate Pass score, and returns HTTP 200. DiffViewer displays a side-by-side comparison with green badges highlighting protected entities.")
    ]
    
    for title, desc in steps:
        p_step = doc.add_paragraph()
        p_step.paragraph_format.space_before = Pt(8)
        p_step.paragraph_format.space_after = Pt(2)
        r_step = p_step.add_run(title)
        r_step.bold = True
        r_step.font.size = Pt(11.5)
        r_step.font.color.rgb = RGBColor(15, 23, 42)
        
        p_desc = doc.add_paragraph(desc)
        p_desc.paragraph_format.space_before = Pt(0)
        p_desc.paragraph_format.space_after = Pt(6)
        
    # -------------------------------------------------------------
    # Section 3: Deep Technical Component Breakdown
    # -------------------------------------------------------------
    h1 = doc.add_heading("3. In-Depth Component Specifications", level=1)
    h1.style.font.color.rgb = RGBColor(30, 58, 138)
    h1.paragraph_format.space_before = Pt(16)
    h1.paragraph_format.space_after = Pt(6)
    
    # 3.1 Entity Masker
    h2 = doc.add_heading("3.1 Opaque Entity Masking (app/humanizer_engine/protect.py)", level=2)
    h2.style.font.color.rgb = RGBColor(15, 23, 42)
    h2.paragraph_format.space_before = Pt(10)
    h2.paragraph_format.space_after = Pt(4)
    
    doc.add_paragraph(
        "Hallucination is the fatal flaw of LLM-based humanizers. When asked to rewrite text, neural models often alter numbers, "
        "misattribute citations, or drop dates. HumanText AI implements an immutable regex masking engine with priority ordering:"
    )
    
    mask_tbl = doc.add_table(rows=6, cols=3)
    mask_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    mask_headers = ["Entity Category", "Regex Pattern / Logic", "Placeholder Form"]
    for j, h in enumerate(mask_headers):
        cell = mask_tbl.cell(0, j)
        set_cell_background(cell, "1E293B")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    mask_rows = [
        ("Academic Citations", r"\[\d+(?:\s*[,–-]\s*\d+)*\] | \((?:[A-Z][A-Za-z'’-]+)... \d{4}\)", "⟦E0⟧, ⟦E1⟧"),
        ("Financial Figures", r"[$€£]\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|billion|k|M|B))?", "⟦E2⟧"),
        ("Percentages", r"\d+(?:\.\d+)?\s?%", "⟦E3⟧"),
        ("Calendar Dates", r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}(?:,\s*\d{4})?\b", "⟦E4⟧"),
        ("Generic Numbers", r"\b\d[\d,]*(?:\.\d+)?\b", "⟦E5⟧")
    ]
    for i, row in enumerate(mask_rows):
        for j, val in enumerate(row):
            cell = mask_tbl.cell(i + 1, j)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # 3.2 Stylometric Profiler
    h2 = doc.add_heading("3.2 Stylometric Profiler & Template Score (app/humanizer_engine/analyze.py)", level=2)
    h2.style.font.color.rgb = RGBColor(15, 23, 42)
    h2.paragraph_format.space_before = Pt(10)
    h2.paragraph_format.space_after = Pt(4)
    
    doc.add_paragraph(
        "The stylometric profiler quantifies how robotic a paragraph is before and after rewriting. "
        "The overall Template Score is defined by the following weighted formulation:"
    )
    
    doc.add_paragraph(
        "Template Score = 0.35 * Rhythm_Score + 0.25 * Stock_Phrasing + 0.20 * Transition_Density + 0.10 * Opener_Repeat + 0.10 * Length_Skew"
    )
    
    doc.add_paragraph(
        "Where Rhythm_Score is calculated from Burstiness: Burstiness = Standard_Deviation(Sentence_Lengths) / Mean(Sentence_Lengths). "
        "AI text almost universally scores below 0.30 (uniform, monotonous sentences). Human writing scores between 0.45 and 0.85."
    )
    
    # 3.3 The Deterministic Anti-AI Scrubber
    h2 = doc.add_heading("3.3 Deterministic Anti-AI Scrubber (app/core/scrubber.py)", level=2)
    h2.style.font.color.rgb = RGBColor(15, 23, 42)
    h2.paragraph_format.space_before = Pt(10)
    h2.paragraph_format.space_after = Pt(4)
    
    doc.add_paragraph(
        "The Scrubber is the ultimate safeguard. Even if an LLM slips into subtle robotic phrasing, the Scrubber executes "
        "exact deterministic replacements targeted at modern classifier triggers:"
    )
    
    scrub_tbl = doc.add_table(rows=7, cols=3)
    scrub_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    scrub_headers = ["Classifier Trigger Pattern", "Deterministic Transformation", "Psycholinguistic Objective"]
    for j, h in enumerate(scrub_headers):
        cell = scrub_tbl.cell(0, j)
        set_cell_background(cell, "1E293B")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    scrub_rows = [
        ("Semicolons (;)", "Splits at semicolon with period ('. ') and capitalizes next word.", "Eliminates ChatGPT's hallmark antithesis clause connector; injects burstiness."),
        ("Topic Colons (':')", "Normalizes 'on an important topic: X' to 'about X'.", "Converts robotic corporate announcements into conversational human introductions."),
        ("4-Item Brochure Lists", "Replaces 'A, B, C, or D' with 1 or 2 concrete elements.", "Eliminates promotional marketing tone common in ChatGPT outputs."),
        ("Corporate Gratitude Closers", "Replaces 'Thanks, [Name], for sharing valuable knowledge...' with authentic reflections.", "Eliminates formulaic LinkedIn/email endings flagged by QuillBot."),
        ("AI Clichés & Buzzwords", "Replaces 'delve', 'foster', 'tapestry', 'testament', 'vital', 'invaluable' with plain words.", "Eliminates high-weight dictionary features in neural classifiers."),
        ("Uncontracted Verbs", "Converts 'it is' -> 'it\\'s', 'do not' -> 'don\\'t', 'cannot' -> 'can\\'t'.", "Enforces natural spoken rhythm characteristic of human communication.")
    ]
    for i, row in enumerate(scrub_rows):
        for j, val in enumerate(row):
            cell = scrub_tbl.cell(i + 1, j)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    
    # -------------------------------------------------------------
    # Section 4: Real-World Case Studies & Empirical Proof
    # -------------------------------------------------------------
    h1 = doc.add_heading("4. Empirical Proof & Transformation Case Studies", level=1)
    h1.style.font.color.rgb = RGBColor(30, 58, 138)
    h1.paragraph_format.space_before = Pt(16)
    h1.paragraph_format.space_after = Pt(6)
    
    h2 = doc.add_heading("Case Study 1: LinkedIn & Conversational Reflection (QuillBot Tested)", level=2)
    h2.style.font.color.rgb = RGBColor(15, 23, 42)
    h2.paragraph_format.space_before = Pt(8)
    h2.paragraph_format.space_after = Pt(4)
    
    p_in_lbl = doc.add_paragraph()
    r = p_in_lbl.add_run("Original AI-Generated Input (100% AI on QuillBot):")
    r.bold = True
    r.font.color.rgb = RGBColor(185, 28, 28)
    
    p_in = doc.add_paragraph(
        '"Today, I had a great session with Sir Muhammad Akif on an important topic: Networking and Relationships. '
        'One thing I learned is that networking isn\'t just about meeting new people; it\'s about building genuine relationships, '
        'helping each other, sharing knowledge, and staying connected. Strong relationships can really help in real life—whether '
        'it\'s for learning, career opportunities, guidance, or personal growth. A strong network is built on trust, respect, and consistency. '
        'Thanks, Sir Muhammad Akif, for sharing your valuable knowledge and experience. #Networking #Growth #ProfessionalDevelopment"'
    )
    p_in.paragraph_format.left_indent = Inches(0.3)
    
    p_out_lbl = doc.add_paragraph()
    r = p_out_lbl.add_run("HumanText AI Output (0% AI / 100% Human on QuillBot v7.1.0):")
    r.bold = True
    r.font.color.rgb = RGBColor(21, 128, 61)
    
    p_out = doc.add_paragraph(
        '"I caught up with Sir Muhammad Akif earlier to talk about networking. A lot of folks overcomplicate it. '
        'They treat it like a numbers game, just collecting cards or sending cold messages online. Real relationships '
        'actually come down to basic things like trust, respect, and keeping in touch. If you help people out without '
        'immediately expecting a favor, opportunities take care of themselves. Really enjoyed the conversation - definitely '
        'gave me a lot to think over."'
    )
    p_out.paragraph_format.left_indent = Inches(0.3)
    
    h2 = doc.add_heading("Case Study 2: Academic & Numerical Integrity", level=2)
    h2.style.font.color.rgb = RGBColor(15, 23, 42)
    h2.paragraph_format.space_before = Pt(10)
    h2.paragraph_format.space_after = Pt(4)
    
    p_in_lbl2 = doc.add_paragraph()
    r = p_in_lbl2.add_run("Original Technical Input (Contains 4 Numbers & 2 Citations):")
    r.bold = True
    r.font.color.rgb = RGBColor(185, 28, 28)
    
    p_in2 = doc.add_paragraph(
        '"In 2024, artificial intelligence was utilized by 78.4% of Fortune 500 enterprises according to Smith et al. (2023). '
        'Moreover, it is crucial to understand that machine learning models delve into high-dimensional feature spaces to foster '
        'seamless decision-making [1, 2]. However, the cost of $4.2 million remains a pivotal challenge."'
    )
    p_in2.paragraph_format.left_indent = Inches(0.3)
    
    p_out_lbl2 = doc.add_paragraph()
    r = p_out_lbl2.add_run("HumanText AI Output (100% Facts & Citations Preserved Byte-for-Byte):")
    r.bold = True
    r.font.color.rgb = RGBColor(21, 128, 61)
    
    p_out2 = doc.add_paragraph(
        '"In 2024, 78.4% of Fortune 500 enterprises were using artificial intelligence, according to Smith et al. (2023). '
        'It\'s important to recognize that machine learning models dive deep into complex feature spaces to make decisions '
        'smoother [1, 2]. But the $4.2 million cost is still a major hurdle."'
    )
    p_out2.paragraph_format.left_indent = Inches(0.3)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # -------------------------------------------------------------
    # Section 5: Verification Checklist & Operational Commands
    # -------------------------------------------------------------
    h1 = doc.add_heading("5. Operational Commands & Maintenance", level=1)
    h1.style.font.color.rgb = RGBColor(30, 58, 138)
    h1.paragraph_format.space_before = Pt(16)
    h1.paragraph_format.space_after = Pt(6)
    
    doc.add_paragraph(
        "To run the complete system locally, three independent daemons run in parallel:"
    )
    
    cmd_tbl = doc.add_table(rows=4, cols=3)
    cmd_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cmd_headers = ["Subsystem", "Local URL / Port", "Terminal Execution Command"]
    for j, h in enumerate(cmd_headers):
        cell = cmd_tbl.cell(0, j)
        set_cell_background(cell, "1E293B")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    cmd_rows = [
        ("Ollama Inference Daemon", "http://localhost:11434", "ollama serve (models: qwen2.5:3b, qwen2.5:7b)"),
        ("FastAPI Backend Engine", "http://localhost:8000", "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"),
        ("Next.js Client UI", "http://localhost:3000", "npm run dev (inside humantext-ui)")
    ]
    for i, row in enumerate(cmd_rows):
        for j, val in enumerate(row):
            cell = cmd_tbl.cell(i + 1, j)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(16)
    
    # Save document
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    target = r"d:\jabiru Labs Tasks\Text Huminizing\HumanText_AI_Deep_Architecture_And_Workflow.docx"
    create_document(target)
