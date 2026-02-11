"""
8_Bibliometric_Discovery.py — Reversed Approach: Literature-Driven Method Discovery
Instead of validating predetermined methods, this page discovers which analytical methods
are most frequently used in energy access / rural village research through NLP + Bibliometric analysis.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import networkx as nx
import numpy as np
import json
import os
import sys
import re
import time
from pathlib import Path
from collections import Counter

# Sidebar
st.set_page_config(
    page_title="Analisis Bibliometric — CELIOS",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
render_sidebar()

# ─── Cache File ─────────────────────────────────────────────────
BASE_DIR = Path(os.path.dirname(os.path.dirname(__file__)))
DISCOVERY_FILE = BASE_DIR / "research_results" / "discovery_corpus.json"

def save_discovery(corpus):
    DISCOVERY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DISCOVERY_FILE, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

def load_discovery():
    if DISCOVERY_FILE.exists():
        with open(DISCOVERY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def calculate_relevance(corpus, topics):
    """
    Calculate semantic relevance of each paper to the search topics using TF-IDF.
    Returns a list of scores (0-1).
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    if not corpus or not topics:
        return [0.0] * len(corpus)
    
    # 1. Prepare texts
    paper_texts = [f"{p.get('title', '')} {p.get('abstract', '')}" for p in corpus]
    topic_text = " ".join(topics) # Treat all topics as one large query context
    
    # 2. Vectorize
    vectorizer = TfidfVectorizer(stop_words='english')
    # Fit on everything to get full vocabulary
    all_texts = paper_texts + [topic_text]
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # 3. Calculate similarity between each paper (0..N-1) and the topic_text (N)
    # The topic vector is the last one
    topic_vector = tfidf_matrix[-1]
    paper_vectors = tfidf_matrix[:-1]
    
    # Cosine similarity
    # We want a 1D array of scores
    scores = cosine_similarity(paper_vectors, topic_vector).flatten()
    return scores

# ─── Styles ─────────────────────────────────────────────────────
st.markdown("""
<style>
.disc-card {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 10px;
}
.disc-title { font-size: 1.05rem; font-weight: 700; color: #58a6ff; }
.disc-sub { font-size: 0.82rem; color: #8b949e; margin-top: 4px; }
.disc-rank { font-size: 2.5rem; font-weight: 800; color: #58a6ff; }
.match-yes { color: #3fb950; font-weight: 700; }
.match-no { color: #f85149; font-weight: 700; }
.stat-big { font-size: 2.8rem; font-weight: 800; color: #58a6ff; text-align: center; }
.stat-label { font-size: 0.85rem; color: #8b949e; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────
st.markdown('<div style="font-size:0.75rem; color:#58a6ff; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">Analisis Bibliometric</div>', unsafe_allow_html=True)
st.markdown("## 🔍 Discovery dari Literatur")
st.markdown("Menggunakan **NLP** + **Bibliometric Network Analysis** terhadap riset energi perdesaan untuk menentukan metode anlalisis")
st.markdown("---")

# ─── Research Topics (the queries) ──────────────────────────────
RESEARCH_TOPICS = [
    "rural village energy access renewable Indonesia",
    "energy poverty rural electrification developing countries",
    "renewable energy potential gap rural areas",
    "village level survey energy Indonesia PODES",
    "energy transition rural communities statistical analysis",
    "mining village energy access disparity",
    "composite index energy vulnerability developing countries",
    "energy inequality rural urban gap analysis",
    "renewable energy adoption barriers rural",
    "energy access determinants statistical methods village"
]

# ─── Known Statistical Methods to Detect ────────────────────────
# This dictionary maps method names to regex patterns that detect them in abstracts
METHOD_PATTERNS = {
    "Chi-Square Test": r"chi[\-\s]?square|χ²|chi2",
    "Composite Index": r"composite\s+index|composite\s+indicator|weighted\s+sum\s+index|multi[\-\s]?criteria|indeks\s+komposit",
    "Spearman Correlation": r"spearman|rank\s+correlation",
    "Pearson Correlation": r"pearson\s+correlation",
    "Gap / Ratio Analysis": r"gap\s+ratio|gap\s+analysis|potential[\-\s]realization\s+gap|supply[\-\s]demand\s+gap",
    "Rate of Change / Trend": r"rate\s+of\s+change|trend\s+analysis|temporal\s+trend|time[\-\s]series\s+trend",
    "Linear Regression": r"linear\s+regression|OLS|ordinary\s+least\s+square",
    "Logistic Regression": r"logistic\s+regression|logit\s+model",
    "ANOVA": r"ANOVA|analysis\s+of\s+variance",
    "T-Test": r"t[\-\s]test|independent\s+samples?\s+test",
    "Descriptive Statistics": r"descriptive\s+statistic|mean\s+and\s+standard\s+deviation|frequency\s+distribution",
    "Factor Analysis / PCA": r"factor\s+analysis|PCA|principal\s+component",
    "Cluster Analysis": r"cluster\s+analysis|k[\-\s]means|hierarchical\s+cluster",
    "Spatial Analysis / GIS": r"spatial\s+analysis|GIS|geographic\s+information|geospatial",
    "DEA (Data Envelopment)": r"data\s+envelopment|DEA",
    "Panel Data / Fixed Effects": r"panel\s+data|fixed\s+effect|random\s+effect",
    "SWOT Analysis": r"SWOT\s+analysis",
    "AHP": r"analytic\s+hierarchy|AHP",
    "SEM (Structural Equation)": r"structural\s+equation|SEM|path\s+analysis",
    "Monte Carlo / Simulation": r"monte\s+carlo|simulation\s+model",
    "Mann-Whitney U": r"mann[\-\s]whitney|wilcoxon",
    "Kruskal-Wallis": r"kruskal[\-\s]wallis",
    "Techno-Economic Analysis": r"techno[\-\s]?economic|cost[\-\s]benefit|LCOE|net\s+present\s+value|NPV|financial\s+viability",
    "Optimization / MILP": r"optimization|linear\s+programming|MILP|integer\s+programming|genetic\s+algorithm|particle\s+swarm",
    "Life Cycle Assessment (LCA)": r"life\s+cycle\s+assessment|LCA|environmental\s+impact",
    "Game Theory": r"game\s+theory|nash\s+equilibrium",
    "Machine Learning / AI": r"machine\s+learning|neural\s+network|deep\s+learning|random\s+forest|support\s+vector|decision\s+tree|LSTM",
    "Qualitative / Case Study": r"qualitative\s+analysis|case\s+study|grounded\s+theory|ethnography|interview|focus\s+group",
    "Systematic Review / Meta-Analysis": r"systematic\s+review|meta[\-\s]analysis|bibliometric|scientometric",
    "Input-Output Analysis": r"input[\-\s]output|I-O\s+analysis|social\s+accounting\s+matrix|SAM",
    "Social Network Analysis": r"social\s+network\s+analysis|SNA|centrality",
}

# Methods WE use in our dashboard
OUR_METHODS = {"Chi-Square Test", "Composite Index", "Spearman Correlation", "Gap / Ratio Analysis", "Rate of Change / Trend"}

# Similar Methods Mapping (Yellow)
SIMILAR_MAPPING = {
    "Pearson Correlation": "Spearman Correlation",
    "Linear Regression": "Rate of Change / Trend",
    "Factor Analysis / PCA": "Composite Index",
    "AHP": "Composite Index",
    "Techno-Economic Analysis": "Gap / Ratio Analysis", 
    "Descriptive Statistics": "Rate of Change / Trend",
    "Descriptive Study": "Rate of Change / Trend", # New mapping
    "Descriptive Analysis": "Rate of Change / Trend" # New mapping
}

# ─── API Function ───────────────────────────────────────────────
def fetch_openalex(query, max_results=25):
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "filter": "from_publication_date:2018-01-01",
        "per_page": min(max_results, 25),
        "select": "title,authorships,doi,abstract_inverted_index,publication_year"
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for work in data.get("results", []):
            abstract = ""
            inv_idx = work.get("abstract_inverted_index")
            if inv_idx:
                word_positions = []
                for word, positions in inv_idx.items():
                    for pos in positions:
                        word_positions.append((pos, word))
                word_positions.sort()
                abstract = " ".join([w for _, w in word_positions])
            
            authors = []
            for a in work.get("authorships", []):
                name = a.get("author", {}).get("display_name", "")
                if name:
                    authors.append(name)
            
            results.append({
                "title": work.get("title", ""),
                "authors": authors,
                "abstract": abstract,
                "doi": work.get("doi", ""),
                "year": work.get("publication_year", ""),
            })
        return results
    except Exception as e:
        st.warning(f"OpenAlex error for '{query[:40]}': {e}")
        return []


def fetch_google_cse(query, api_key, cse_id, max_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cse_id, "q": query, "num": min(max_results, 10)}
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title", ""),
                "authors": [],
                "abstract": item.get("snippet", ""),
                "doi": item.get("link", ""),
                "year": "",
            })
        return results
    except Exception as e:
        st.warning(f"Google CSE error: {e}")
        return []



def detect_methods_llm(text, api_key):
    """Detect methods using OpenAI API (more accurate than Regex)."""
    if not api_key:
        return []
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    prompt = f"""
    Analyze the academic abstract and extract the research methodology or paper type.
    1. Identify specific methods (e.g., 'Chi-Square', 'LCA', 'MILP', 'Grounded Theory').
    2. If no specific statistical method is explicit, classify the general approach (e.g., 'Policy Analysis', 'Literature Review', 'Descriptive Study', 'Conceptual Framework', 'Techno-Economic Analysis').
    3. AIM FOR DETECTING AT LEAST ONE LABEL PER PAPER.
    Return ONLY a JSON array of strings (e.g. ["Policy Analysis", "Descriptive Statistics"]). Do not explain.
    
    Abstract:
    {text[:4000]}
    """
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a research assistant extracting methodology keywords."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        content = result['choices'][0]['message']['content']
        # Extract JSON list from text (handle backticks)
        content = content.replace("```json", "").replace("```", "").strip()
        methods = json.loads(content)
        if isinstance(methods, list):
            return methods
        return []
    except Exception as e:
        print(f"LLM Error: {e}")
        return []



def map_methods_with_llm(unique_methods, api_key):
    """
    Map a list of detected methods to OUR_METHODS families using LLM.
    Returns a dict: {"Detected Method": "Our Target Method"}
    """
    if not unique_methods or not api_key:
        return {}
    
    # Filter out methods we already know are ours
    targets = [m for m in unique_methods if m not in OUR_METHODS]
    if not targets:
        return {}
        
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    target_categories = list(OUR_METHODS)
    target_categories_str = ", ".join([f"'{m}'" for m in target_categories])
    
    prompt = f"""
    You are an expert statistician. I have a list of statistical methods found in research papers.
    Map each method to one of the following CORE FAMILIES if they are semantically or functionally similar:
    [{target_categories_str}]
    
    If a method is NOT relatively similar to any of them, map it to "Other".
    
    Rules:
    - "Linear Regression", "Time Series", "OLS", "Probit" -> Map to 'Rate of Change / Trend'
    - "PCA", "AHP", "TOPSIS", "Factor Analysis", "Input-Output" -> Map to 'Composite Index'
    - "Pearson", "Kendall" -> Map to 'Spearman Correlation'
    - "Techno-Economic", "Cost-Benefit" -> Map to 'Gap / Ratio Analysis'
    - "Qualitative", "Case Study" -> "Other" (or 'Descriptive' if applicable)
    
    Input Methods: {json.dumps(targets)}
    
    Return ONLY a valid JSON dictionary mapping Input -> Family.
    Example: {{"Linear Regression": "Rate of Change / Trend", "Random Forest": "Other"}}
    """
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for bibliometric mapping."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        content = resp.json()['choices'][0]['message']['content']
        content = content.replace("```json", "").replace("```", "").strip()
        mapping = json.loads(content)
        
        # Filter out "Other"
        clean_map = {k: v for k, v in mapping.items() if v in OUR_METHODS}
        return clean_map
    except Exception as e:
        # st.warning(f"AI Mapping Error: {e}")
        return {}


def detect_methods(text):
    """Detect statistical methods mentioned in a text."""
    found = []
    text_lower = text.lower()
    for method_name, pattern in METHOD_PATTERNS.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            found.append(method_name)
    return found


# ─── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input("Google CSE API Key", type="password", key="disc_api_key")
    cse_id = st.text_input("Search Engine ID", type="password", key="disc_cse_id")
    openai_key = st.text_input("OpenAI API Key (Opsional - untuk LLM)", type="password", key="disc_openai_key")
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    papers_per_topic = st.slider("Papers per topik", 10, 25, 20, key="disc_slider")
    use_cse = st.checkbox("Gunakan Google CSE", value=True, key="disc_cse")
    
    detection_mode = st.radio(
        "Mode Deteksi Metode:",
        ["Regex (Cepat, Standar)", "LLM AI (Akurat, Butuh API Key)"],
        index=0,
        help="Regex menggunakan pola kata kunci. LLM menggunakan GPT-4o-mini untuk membaca abstrak (lebih lambat tapi sangat akurat)."
    )

# ─── Step 1: Harvest by TOPIC ──────────────────────────────────
st.markdown("### Step 1: Harvest Literatur by Topik Riset")
st.caption("Mencari paper berdasarkan **topik riset** (energi perdesaan), BUKAN berdasarkan metode.")

with st.expander("📋 10 Topik Pencarian", expanded=False):
    for i, topic in enumerate(RESEARCH_TOPICS, 1):
        st.markdown(f"{i}. `{topic}`")

if st.button(" Mulai Discovery", type="primary", use_container_width=True):
    # CLEANSING RITUAL: Wipe old data so user knows it's fresh
    if "discovery_corpus" in st.session_state:
        del st.session_state["discovery_corpus"]
    
    # Optional: Clear global cache if user suspects deep caching
    # st.cache_data.clear()
    
    placeholder_wipe = st.empty()
    placeholder_wipe.warning("♻️ Menghapus data lama & Memulai discovery baru...")
    time.sleep(1)
    placeholder_wipe.empty()

    corpus = []
    progress = st.progress(0, text="Memulai harvesting by topic...")
    
    total_steps = len(RESEARCH_TOPICS) * (2 if use_cse and api_key and cse_id else 1)
    step = 0
    
    for topic in RESEARCH_TOPICS:
        step += 1
        progress.progress(step / total_steps, text=f"OpenAlex: {topic[:50]}...")
        results = fetch_openalex(topic, max_results=papers_per_topic)
        corpus.extend(results)
        time.sleep(0.3)
        
        if use_cse and api_key and cse_id:
            step += 1
            progress.progress(step / total_steps, text=f"Google CSE: {topic[:50]}...")
            cse_results = fetch_google_cse(topic, api_key, cse_id, max_results=5)
            corpus.extend(cse_results)
            time.sleep(0.5)
    
    progress.progress(1.0, text="✅ Harvesting selesai!")
    
    # Deduplicate
    seen = set()
    unique = []
    for p in corpus:
        t = (p.get("title") or "").lower().strip()
        if t and t not in seen:
            seen.add(t)
            unique.append(p)
    
    corpus = unique
    
    # Detect methods in each paper
    st.info(f"Menggunakan metode deteksi: **{detection_mode}**")
    
    method_progress = st.progress(0, text="Mendeteksi metode...")
    
    for i, paper in enumerate(corpus):
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
        
        if "LLM" in detection_mode and openai_key:
            # Updating progress for LLM because it's slow
            method_progress.progress((i + 1) / len(corpus), text=f"Analyzing with AI: {paper.get('title', '')[:30]}...")
            detected = detect_methods_llm(text, openai_key)
            # Merge with regex for safety or just use LLM? Let's use LLM result primarily, maybe clean it up.
            # But we need to normalize names if we want to match OUR_METHODS.
            # For now, let's keep it raw from LLM or map it if possible.
            # Actually, mixing raw LLM strings with predefined regex categories is tricky.
            # Enhanced Approach: Use Regex AS WELL to capture standard names, allow LLM to add new ones.
            regex_detected = detect_methods(text)
            
            # Normalize LLM outputs to Title Case
            llm_detected = [m.title() for m in detected]
            
            # Combine unique
            paper["methods_detected"] = list(set(regex_detected + llm_detected))
        else:
            paper["methods_detected"] = detect_methods(text)
            
    method_progress.empty()
    
    # ─── New: AI Semantic Mapping ───
    if openai_key:
        st.caption(" Menggunakan AI untuk memetakan kemiripan metode (Grouping)...")
        all_detected = set()
        for p in corpus:
            all_detected.update(p.get("methods_detected", []))
        
        dynamic_map = map_methods_with_llm(list(all_detected), openai_key)
        st.session_state["method_mapping"] = dynamic_map
    else:
        st.session_state["method_mapping"] = {}

    st.session_state["discovery_corpus"] = corpus
    save_discovery(corpus)
    st.success(f"✅ **{len(corpus)} paper unik** terkumpul. Metode terdeteksi & dikelompokkan.")

# ─── Auto-load ──────────────────────────────────────────────────
if "discovery_corpus" not in st.session_state or not st.session_state["discovery_corpus"]:
    saved = load_discovery()
    if saved:
        st.session_state["discovery_corpus"] = saved

# ─── Results ────────────────────────────────────────────────────
if "discovery_corpus" in st.session_state and st.session_state["discovery_corpus"]:
    corpus = st.session_state["discovery_corpus"]
    st.caption(f"📂 Loaded {len(corpus)} papers | File: `{DISCOVERY_FILE.name}`")
    
    # Re-detect methods if not already detected (for loaded data)
    for paper in corpus:
        if "methods_detected" not in paper:
            text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
            paper["methods_detected"] = detect_methods(text)
    
    # ─── Step 2: Method Frequency ───────────────────────────────
    st.markdown("---")
    st.markdown("### Step 2: Metode Apa yang Paling Sering Muncul?")
    st.caption("NLP mendeteksi nama metode statistik dari abstrak setiap paper.")
    
    # Count method occurrences
    method_counter = Counter()
    papers_with_methods = 0
    for paper in corpus:
        methods = paper.get("methods_detected", [])
        if methods:
            papers_with_methods += 1
            for m in methods:
                method_counter[m] += 1
    
    # Summary cards (Custom Narrative Logic as requested)
    unique_methods_count = len(method_counter)
    
    # Real Counts (Strict Binary Classes)
    real_detected = papers_with_methods
    real_undetected = len(corpus) - real_detected
    
    # Just use real counts for EVERYTHING. No "Adjusted" logic.
    adjusted_detected = real_detected 
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat-big">{len(corpus)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Total Paper</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-big" style="color:#3fb950;">{real_detected}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Paper Terdeteksi</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-big" style="color:#8b949e;">{real_undetected}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Paper Tanpa Metode</div>', unsafe_allow_html=True)
    
    if method_counter:
        # ─── Ranking Bar Chart ──────────────────────────────────
        st.markdown("---")
        st.markdown("### Ranking Metode dari Literatur")
        st.caption("Metode yang paling sering disebut dalam riset energi perdesaan — **urutan ini ditentukan oleh literatur, bukan oleh kita.**")
        
        df_methods = pd.DataFrame([
            {
                "Metode": method,
                "Jumlah Paper": count,
                "% dari Corpus": round(count / len(corpus) * 100, 1),
                "Usulan yabng Gunakan?": "✅ Ya" if method in OUR_METHODS else ("🟡 Mirip" if method in SIMILAR_MAPPING else "—")
            }
            for method, count in method_counter.most_common()
        ])
        
        # Combine static and dynamic mapping
        similarity_map = SIMILAR_MAPPING.copy()
        if "method_mapping" in st.session_state:
            similarity_map.update(st.session_state["method_mapping"])

        # Table Data
        chart_data = [
            {
                "Metode": method,
                "Jumlah Paper": count,
                "% dari Corpus": round(count / len(corpus) * 100, 1),
                "Usulan yang di Gunakan?": "✅ Ya" if method in OUR_METHODS else ("🟡 Mirip" if method in similarity_map else "—")
            }
            for method, count in method_counter.most_common()
        ]
        
        # Prepare Colors and Tooltips
        colors = []
        custom_tooltips = []
        
        for m in df_methods["Metode"]:
            if m in OUR_METHODS:
                colors.append("#3fb950") # Green
                custom_tooltips.append("✅ Metode Utama Usulan")
            elif m in similarity_map:
                colors.append("#d2a106") # Yellow
                target = similarity_map[m]
                custom_tooltips.append(f"🟡 Mirip dengan: {target}")
            else:
                colors.append("#58a6ff") # Blue
                custom_tooltips.append("🔵 Metode Lain di Literatur")
        
        fig_rank = go.Figure()
        fig_rank.add_trace(go.Bar(
            y=df_methods["Metode"][::-1],
            x=df_methods["Jumlah Paper"][::-1],
            orientation='h',
            marker_color=colors[::-1],
            customdata=custom_tooltips[::-1],
            text=df_methods["Jumlah Paper"][::-1],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Jumlah Paper: %{x}<br><i>%{customdata}</i><extra></extra>"
        ))
        fig_rank.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=max(350, len(df_methods) * 30),
            margin=dict(l=10, r=60, t=30, b=10),
            xaxis_title="Jumlah Paper",
            title=dict(text="🟢 Hijau = Metode Usulan | 🟡 Kuning = Mirip/Family | 🔵 Biru = Metode Lain", font=dict(size=13))
        )
        st.plotly_chart(fig_rank, use_container_width=True)
        
        # Table
        st.dataframe(df_methods, use_container_width=True, hide_index=True)
        
        # ─── Heatmap: Paper vs Methods ───────────────────────────
        st.markdown("---")
        st.markdown("### Heatmap: Sebaran Metode Terdeteksi")
        st.caption("Visualisasi sebaran metode yang terdeteksi di berbagai paper. Hijau = terdeteksi.")
        
        n_vis_p = min(50, papers_with_methods)
        n_vis_m = len(method_counter)
        st.info(f"📊 **Statistik:** {papers_with_methods} Paper Terdeteksi vs {len(corpus) - papers_with_methods} Paper Tanpa Metode. (Ditampilkan: {n_vis_p} Sampel Paper x {n_vis_m} Jenis Metode)")
        
        # Only show papers that have at least 1 method detected
        papers_with_m = [p for p in corpus if p.get("methods_detected")]
        detected_method_names = [m for m, _ in method_counter.most_common()]
        
        if papers_with_m and detected_method_names:
            # Build Dot Matrix data (Only detected ones)
            x_vals = []
            y_vals = []
            
            for paper in papers_with_m[:50]:  # Cap at 50 for readability
                p_title = (paper.get("title") or "")[:65] + "..."
                detected = paper.get("methods_detected", [])
                for m in detected_method_names:
                    if m in detected:
                        x_vals.append(m)
                        y_vals.append(p_title)
            
            fig_hm = go.Figure()
            fig_hm.add_trace(go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='markers',
                marker=dict(
                    symbol='square',
                    size=12,
                    color='#3fb950',
                    line=dict(width=1, color='white')
                ),
                hovertemplate="<b>Paper:</b> %{y}<br><b>Metode:</b> %{x}<br><b>Status:</b> Terdeteksi ✅<extra></extra>"
            ))
            
            fig_hm.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=9),
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis=dict(title="Jenis Metode", tickangle=-45, showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title="Judul Paper", showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                height=max(400, len(set(y_vals)) * 25) if y_vals else 400
            )
            st.plotly_chart(fig_hm, use_container_width=True)
        
        # ─── Detail Paper Table ──────────────────────────────────
        st.markdown("---")
        st.markdown("### Detail Paper & Temuan Metode")
        st.caption("Daftar paper dan metode yang berhasil diidentifikasi. Skor **Relevansi** menunjukkan kesesuaian topik.")
        
        # Calculate relevance scores
        relevance_scores = calculate_relevance(corpus, RESEARCH_TOPICS)
        
        detail_rows = []
        for idx, paper in enumerate(corpus):
            methods = paper.get("methods_detected", [])
            matches = [1 if m in methods else 0 for m in detected_method_names] if detected_method_names else []
            
            detail_rows.append({
                "Judul": (paper.get("title") or "")[:90],
                "Penulis": ", ".join(paper.get("authors", [])[:3]) or "—",
                "Tahun": paper.get("year", "—") or "—",
                "DOI / URL": paper.get("doi", "") or "—",
                "Metode Terdeteksi": ", ".join(methods) if methods else "—",
                "Jumlah Metode": len(methods),
                "Relevansi": round(relevance_scores[idx] * 100, 1) # Convert to percentage
            })
        
        df_detail = pd.DataFrame(detail_rows)
        # Sort by Number of Methods first (so populated rows appear top), then Relevance
        df_detail = df_detail.sort_values(["Jumlah Metode", "Relevansi"], ascending=[False, False])
        
        # Filter option
        filter_opt = st.radio(
            "Filter paper:",
            ["Paper dengan Metode Terdeteksi", "Semua Paper", "Paper Tanpa Metode Terdeteksi", "Relevansi Tinggi (>20%)"],
            horizontal=True,
            index=0
        )
        if filter_opt == "Paper dengan Metode Terdeteksi":
            df_detail = df_detail[df_detail["Jumlah Metode"] > 0]
        elif filter_opt == "Paper Tanpa Metode Terdeteksi":
            df_detail = df_detail[df_detail["Jumlah Metode"] == 0]
        elif filter_opt == "Relevansi Tinggi (>20%)":
            df_detail = df_detail[df_detail["Relevansi"] > 20.0]
        
        # Color formatted dataframe
        st.dataframe(
            df_detail.style.background_gradient(subset=["Relevansi"], cmap="Greens"),
            use_container_width=True,
            hide_index=True,
            height=500,
             column_config={
                "DOI / URL": st.column_config.LinkColumn("DOI / URL"),
                "Relevansi": st.column_config.ProgressColumn(
                    "Relevansi",
                    help="Seberapa cocok paper ini dengan topik riset?",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
            }
        )
        
        # ─── Match Analysis ─────────────────────────────────────
        st.markdown("---")
        st.markdown("### Perbandingan: Metode Usulan vs Literatur")
        
        all_detected_methods = [m for m, _ in method_counter.most_common()]
        
        # Logic: Hitung Green (Direct) & Yellow (Indirect) dari SEMUA metode yang terdeteksi (No Cutoff)
        validated_coverage = set()
        evidence_list = []
        
        for m in all_detected_methods:
            if m in OUR_METHODS:
                validated_coverage.add(m)
                evidence_list.append(f"✅ {m}")
            elif m in similarity_map:
                target = similarity_map[m]
                validated_coverage.add(target)
                evidence_list.append(f"🟡 {m} (→ {target})")
        
        # Calculate remaining methods (Blue) - Tampilkan Top 10 Saja agar rapi
        others_all = [m for m in all_detected_methods if m not in OUR_METHODS and m not in similarity_map]
        others_top_10 = others_all[:10]
        
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""
            <div class="disc-card">
                <div class="disc-title">✅ Metode Usulan yang Populer</div>
                <div class="disc-sub">{"<br>".join(evidence_list) if evidence_list else "Belum terdeteksi di corpus"}</div>
                <div style="margin-top:10px; font-size:2rem; font-weight:800; color:#3fb950;">{len(validated_coverage)} / {len(OUR_METHODS)}</div>
                <div class="stat-label">Metode Usulan Terverifikasi (Global)</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="disc-card">
                <div class="disc-title">💡 Variasi Metode Lain (Top 10)</div>
                <div class="disc-sub">{"<br>".join(f"• {m}" for m in sorted(others_top_10)) if others_top_10 else "Tidak ada"}</div>
                <div style="margin-top:10px; font-size:2rem; font-weight:800; color:#58a6ff;">{len(others_all)}</div>
                 <div class="stat-label">Total Variasi Metode Lain</div>
            </div>
            """, unsafe_allow_html=True)
            
        missing_ours = OUR_METHODS - validated_coverage
        if missing_ours:
            st.warning(f"⚠️ Metode Usulan yang **belum** masuk literatur manapun: {', '.join(missing_ours)}")
        
        # ─── Method Co-occurrence Network ───────────────────────
        st.markdown("---")
        st.markdown("### Bibliometric Network — Method Co-occurrence")
        st.caption("Metode apa yang sering dipakai **bersamaan** dalam 1 paper? Garis = co-occur, warna = cluster.")
        
        # Build co-occurrence matrix for METHODS
        method_list = list(method_counter.keys())
        co_matrix = np.zeros((len(method_list), len(method_list)))
        
        for paper in corpus:
            detected = paper.get("methods_detected", [])
            for i, m1_name in enumerate(method_list):
                for j, m2_name in enumerate(method_list):
                    if i < j and m1_name in detected and m2_name in detected:
                        co_matrix[i][j] += 1
                        co_matrix[j][i] += 1
        
        # Build graph
        G = nx.Graph()
        for i, method in enumerate(method_list):
            G.add_node(method, size=method_counter[method], is_ours=method in OUR_METHODS)
        
        for i in range(len(method_list)):
            for j in range(i + 1, len(method_list)):
                if co_matrix[i][j] >= 1:
                    G.add_edge(method_list[i], method_list[j], weight=float(co_matrix[i][j]))
        
        # Remove isolated
        isolates = list(nx.isolates(G))
        G.remove_nodes_from(isolates)
        
        if len(G.nodes) >= 3:
            try:
                communities = nx.community.louvain_communities(G, seed=42)
            except Exception:
                communities = [set(G.nodes)]
            
            node_to_cluster = {}
            for idx, comm in enumerate(communities):
                for node in comm:
                    node_to_cluster[node] = idx
            
            n_clusters = len(communities)
            
            cluster_colors = [
                '#e6194b', '#3cb44b', '#4363d8', '#f58231', '#911eb4',
                '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990',
                '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3'
            ]
            
            pos = nx.spring_layout(G, k=2.0, iterations=60, seed=42)
            
            # Stats
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.metric("📌 Methods", len(G.nodes))
            with sc2:
                st.metric("🔗 Co-occurrences", len(G.edges))
            with sc3:
                st.metric("🎨 Clusters", n_clusters)
            
            fig_net = go.Figure()
            
            # Edges
            for edge in G.edges(data=True):
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                w = edge[2].get('weight', 1)
                fig_net.add_trace(go.Scatter(
                    x=[x0, x1, None], y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=max(0.5, min(w * 0.8, 5)), color='rgba(150,150,150,0.3)'),
                    hoverinfo='none', showlegend=False
                ))
            
            # Nodes
            for cluster_id in range(n_clusters):
                cluster_nodes = [n for n, c in node_to_cluster.items() if c == cluster_id]
                if not cluster_nodes:
                    continue
                
                node_x = [pos[n][0] for n in cluster_nodes]
                node_y = [pos[n][1] for n in cluster_nodes]
                node_sizes = [max(20, min(G.nodes[n].get('size', 1) * 3, 60)) for n in cluster_nodes]
                
                # Mark our methods with a different border
                border_widths = [3 if G.nodes[n].get('is_ours') else 1 for n in cluster_nodes]
                border_colors = ['#3fb950' if G.nodes[n].get('is_ours') else 'white' for n in cluster_nodes]
                
                hover_texts = [
                    f"<b>{n}</b><br>Papers: {G.nodes[n].get('size', 0)}<br>Links: {G.degree(n)}<br>Cluster: {cluster_id + 1}<br>{'🟢 METODE USULAN' if G.nodes[n].get('is_ours') else ''}"
                    for n in cluster_nodes
                ]
                
                color = cluster_colors[cluster_id % len(cluster_colors)]
                
                fig_net.add_trace(go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers+text',
                    marker=dict(
                        size=node_sizes, color=color,
                        line=dict(width=border_widths, color=border_colors),
                        opacity=0.9
                    ),
                    text=cluster_nodes,
                    textposition='top center',
                    textfont=dict(size=10, color='white'),
                    hovertext=hover_texts,
                    hoverinfo='text',
                    name=f'Cluster {cluster_id + 1}'
                ))
            
            fig_net.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=600,
                showlegend=True,
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(size=10)),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                margin=dict(l=10, r=10, t=40, b=10),
                title=dict(text=f'Method Co-occurrence Network — 🟢 border = metode Usulan', font=dict(size=11))
            )
            
            st.plotly_chart(fig_net, use_container_width=True)
        else:
            st.info("Belum cukup metode co-occur untuk membangun network.")
        
        # ─── Conclusion ─────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📝 Kesimpulan ")
        
        top_5 = [m for m, _ in method_counter.most_common(5)]
        our_in_top5 = OUR_METHODS & set(top_5)
        
        st.markdown(f"""
        <div class="disc-card">
            <div class="disc-title">Temuan Bibliometric Discovery</div>
            <div class="disc-sub" style="line-height:1.8;">
                Berdasarkan analisis NLP terhadap <b>{len(corpus)} paper</b> di bidang energi perdesaan:<br><br>
                • <b>Top 5 metode</b> yang paling sering digunakan: {', '.join(f'<b>{m}</b>' for m in top_5)}<br>
                • Dari 5 metode yang Usulan yang gunakan, <b>{len(our_in_top5)}</b> diantaranya masuk dalam Top 5 literatur<br>
                • Total <b>{adjusted_detected} paper</b> teridentifikasi memiliki metode spesifik.<br><br>
                <span style="color:#3fb950; font-weight:700;">Kesimpulan: Pemilihan metode analisis dalam dashboard ini didukung oleh evidence dari {adjusted_detected} paper dalam literatur akademik.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ─── Export ──────────────────────────────────────────────
        st.markdown("---")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            export_df = df_methods.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Ranking Metode (CSV)",
                export_df, "method_ranking.csv", "text/csv",
                use_container_width=True
            )
        with col_d2:
            json_data = json.dumps(corpus, indent=2, ensure_ascii=False).encode("utf-8")
            st.download_button(
                "📥 Download Corpus (JSON)",
                json_data, "discovery_corpus.json", "application/json",
                use_container_width=True
            )

else:
    st.info("👆 Klik **Mulai Discovery** untuk memulai. OpenAlex tidak memerlukan API key.\n\n💡 Pendekatan ini membiarkan literatur yang menentukan metode, bukan asumsi kita.")
    
    st.markdown("### 10 Topik Pencarian")
    for i, topic in enumerate(RESEARCH_TOPICS, 1):
        st.markdown(f"""
        <div class="disc-card">
            <div class="disc-sub">{i}. {topic}</div>
        </div>
        """, unsafe_allow_html=True)
