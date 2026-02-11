"""
7_Validasi_Metode.py — NLP Validation Page
Validates that the 5 analytical methods used in this research are grounded in real published literature.
Uses OpenAlex API (free) + Google CSE (user-provided key) to harvest papers, then TF-IDF + cosine similarity to measure alignment.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import networkx as nx
from collections import Counter
import numpy as np
import json
import os
import sys
import time
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Validasi Metode NLP — CELIOS EBT",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)

# ─── Cache File Path ────────────────────────────────────────────
BASE_DIR = Path(os.path.dirname(os.path.dirname(__file__)))
CORPUS_FILE = BASE_DIR / "research_results" / "corpus.json"

def save_corpus(corpus):
    """Save corpus to JSON file for persistence."""
    CORPUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CORPUS_FILE, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

def load_corpus():
    """Load corpus from JSON file if it exists."""
    if CORPUS_FILE.exists():
        with open(CORPUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# Sidebar
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
render_sidebar()

# ─── Page Config ────────────────────────────────────────────────
st.markdown("""
<style>
.method-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #ffffff15;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
}
.method-title { font-size: 1.1rem; font-weight: 700; color: #66BB6A; }
.method-desc { font-size: 0.85rem; color: #B0BEC5; margin-top: 4px; }
.stat-big { font-size: 2.8rem; font-weight: 800; color: #66BB6A; text-align: center; }
.stat-label { font-size: 0.85rem; color: #90A4AE; text-align: center; }
.status-ok { color: #66BB6A; font-weight: 700; }
.status-fail { color: #EF5350; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="org-badge" style="font-size:0.75rem; color:#66BB6A; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">CELIOS — Validasi Metodologi</div>', unsafe_allow_html=True)
st.markdown("## 🔬 Validasi Metode Analisis")
st.markdown("Membuktikan bahwa 5 metode analisis data EBT **grounded** di literatur ilmiah menggunakan pendekatan **NLP** (*TF-IDF Cosine Similarity*) dan **Bibliometric Network Analysis** (*Keyword Co-occurrence + Louvain Clustering*).")
st.markdown("---")

# ─── 5 Methods Definition ──────────────────────────────────────
METHODS = {
    "Chi-Square Crosstab": {
        "desc": "Uji independensi antara status desa tambang dengan akses EBT",
        "keywords": "chi-square test village energy access mining rural",
        "keywords_id": "chi-square desa tambang energi terbarukan"
    },
    "Indeks Komposit (IKE)": {
        "desc": "Min-Max Normalization + Weighted Sum untuk skor kerentanan energi per provinsi",
        "keywords": "composite energy vulnerability index normalization weighted sum province",
        "keywords_id": "indeks komposit energi kerentanan provinsi"
    },
    "Gap Ratio Analysis": {
        "desc": "Rasio potensi vs realisasi energi terbarukan per provinsi",
        "keywords": "renewable energy potential realization gap ratio rural village",
        "keywords_id": "gap potensi realisasi energi terbarukan desa"
    },
    "Spearman Correlation": {
        "desc": "Korelasi rank antar dimensi EBT per provinsi",
        "keywords": "spearman rank correlation energy access pollution environment",
        "keywords_id": "korelasi spearman energi lingkungan"
    },
    "Rate of Change (Tren)": {
        "desc": "Analisis perubahan 2021→2024 per provinsi per dimensi",
        "keywords": "rate of change trend analysis rural electrification renewable energy adoption",
        "keywords_id": "tren perubahan elektrifikasi energi terbarukan"
    }
}

# ─── API Functions ──────────────────────────────────────────────
def fetch_openalex(query, max_results=20):
    """Fetch papers from OpenAlex API (free, no key needed)."""
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "filter": "from_publication_date:2021-01-01",
        "per_page": min(max_results, 25),
        "select": "title,authorships,doi,abstract_inverted_index"
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for work in data.get("results", []):
            # Reconstruct abstract from inverted index
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
                "source_type": "journal",
                "fetch_method": "openalex"
            })
        return results
    except Exception as e:
        st.warning(f"OpenAlex error: {e}")
        return []


def fetch_google_cse(query, api_key, cse_id, max_results=10):
    """Fetch results from Google Custom Search Engine."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": min(max_results, 10)
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title", ""),
                "authors": [],  # CSE doesn't provide authors
                "abstract": item.get("snippet", ""),
                "doi": item.get("link", ""),
                "source_type": "web",
                "fetch_method": "google_cse"
            })
        return results
    except Exception as e:
        st.warning(f"Google CSE error: {e}")
        return []


# ─── NLP Functions ──────────────────────────────────────────────
def compute_similarity(corpus_texts, method_descriptions):
    """Compute TF-IDF cosine similarity between corpus and methods."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    all_texts = method_descriptions + corpus_texts
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    n_methods = len(method_descriptions)
    method_vectors = tfidf_matrix[:n_methods]
    corpus_vectors = tfidf_matrix[n_methods:]
    
    sim_matrix = cosine_similarity(corpus_vectors, method_vectors)
    return sim_matrix, vectorizer


def get_top_keywords(vectorizer, tfidf_matrix, n_methods, top_n=20):
    """Extract top keywords from the corpus."""
    feature_names = vectorizer.get_feature_names_out()
    corpus_vectors = tfidf_matrix[n_methods:]
    mean_tfidf = corpus_vectors.mean(axis=0).A1
    top_indices = mean_tfidf.argsort()[-top_n:][::-1]
    return [(feature_names[i], mean_tfidf[i]) for i in top_indices]


# ─── Sidebar: API Key Input ────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input("Google CSE API Key", type="password", help="Dari console.cloud.google.com")
    cse_id = st.text_input("Search Engine ID", type="password", help="Dari programmablesearchengine.google.com")
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    papers_per_method = st.slider("Papers per metode (OpenAlex)", 5, 25, 15)
    use_google_cse = st.checkbox("Gunakan Google CSE (hybrid)", value=True)
    
    if api_key:
        st.session_state["gcs_api_key"] = api_key
    if cse_id:
        st.session_state["gcs_cse_id"] = cse_id

# ─── Main: Run Harvester ───────────────────────────────────────
st.markdown("### 📡 Step 1: Harvest Literature")

col_info1, col_info2 = st.columns(2)
with col_info1:
    st.markdown("""
    <div class="method-card">
        <div class="method-title">🟢 OpenAlex API</div>
        <div class="method-desc">Gratis, tanpa API key. 250M+ paper akademik. Fetch otomatis berdasarkan 5 keyword metode.</div>
    </div>
    """, unsafe_allow_html=True)
with col_info2:
    st.markdown(f"""
    <div class="method-card">
        <div class="method-title">🔵 Google CSE</div>
        <div class="method-desc">Untuk sumber non-jurnal (BPS, CELIOS, IESR, IRENA). Butuh API key. Status: {"<span class='status-ok'>✅ Key tersedia</span>" if api_key and cse_id else "<span class='status-fail'>❌ Belum diisi</span>"}</div>
    </div>
    """, unsafe_allow_html=True)

# Methods Display
with st.expander("📋 5 Metode yang Divalidasi", expanded=False):
    for name, info in METHODS.items():
        st.markdown(f"**{name}** — {info['desc']}")
        st.caption(f"Keywords: `{info['keywords']}`")

# Run Button
if st.button("🚀 Mulai Harvesting & Validasi", type="primary", use_container_width=True):
    corpus = []
    
    # Progress
    progress = st.progress(0, text="Memulai harvesting...")
    status_container = st.empty()
    
    total_steps = len(METHODS) * (2 if use_google_cse and api_key and cse_id else 1)
    current_step = 0
    
    for method_name, method_info in METHODS.items():
        # ─── OpenAlex ───
        current_step += 1
        progress.progress(current_step / total_steps, text=f"OpenAlex: {method_name}...")
        results = fetch_openalex(method_info["keywords"], max_results=papers_per_method)
        for r in results:
            r["method_query"] = method_name
        corpus.extend(results)
        time.sleep(0.3)  # Rate limiting
        
        # ─── Google CSE (if enabled) ───
        if use_google_cse and api_key and cse_id:
            current_step += 1
            progress.progress(current_step / total_steps, text=f"Google CSE: {method_name}...")
            cse_results = fetch_google_cse(
                method_info["keywords_id"],
                api_key, cse_id, max_results=5
            )
            for r in cse_results:
                r["method_query"] = method_name
            corpus.extend(cse_results)
            time.sleep(0.5)  # Rate limiting
    
    progress.progress(1.0, text="✅ Harvesting selesai!")
    
    # Deduplicate by title
    seen_titles = set()
    unique_corpus = []
    for paper in corpus:
        title_lower = (paper.get("title") or "").lower().strip()
        if title_lower and title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_corpus.append(paper)
    
    corpus = unique_corpus
    st.session_state["corpus"] = corpus
    save_corpus(corpus)
    st.success(f"✅ Berhasil mengumpulkan **{len(corpus)} paper unik** dari {total_steps} queries. Data tersimpan otomatis.")

# ─── Results ────────────────────────────────────────────────────
# Auto-load from file if session is empty
if "corpus" not in st.session_state or not st.session_state["corpus"]:
    saved = load_corpus()
    if saved:
        st.session_state["corpus"] = saved

if "corpus" in st.session_state and st.session_state["corpus"]:
    corpus = st.session_state["corpus"]
    st.caption(f"📂 Loaded {len(corpus)} papers | File: `{CORPUS_FILE.name}`")
    
    st.markdown("---")
    st.markdown("### 🧠 Step 2: NLP Similarity Analysis")
    
    # Prepare texts
    corpus_texts = []
    valid_papers = []
    for paper in corpus:
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}".strip()
        if len(text) > 20:  # Filter out empty/short entries
            corpus_texts.append(text)
            valid_papers.append(paper)
    
    if len(corpus_texts) < 3:
        st.error("Terlalu sedikit paper dengan abstrak. Coba tambah jumlah papers per metode.")
    else:
        # Method descriptions for comparison
        method_names = list(METHODS.keys())
        method_descriptions = [
            f"{name} {info['desc']} {info['keywords']}"
            for name, info in METHODS.items()
        ]
        
        # Compute similarity
        sim_matrix, vectorizer = compute_similarity(corpus_texts, method_descriptions)
        
        # ─── Summary Cards ───
        st.markdown("### 📊 Hasil Validasi")
        
        avg_similarity = sim_matrix.max(axis=1).mean()
        supported_count = (sim_matrix.max(axis=1) > 0.05).sum()
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="stat-big">{len(valid_papers)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-label">Paper Tervalidasi</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-big">{supported_count}</div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-label">Paper Mendukung Metode</div>', unsafe_allow_html=True)
        with c3:
            pct = (supported_count / len(valid_papers) * 100) if valid_papers else 0
            st.markdown(f'<div class="stat-big">{pct:.0f}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-label">Coverage Rate</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ─── Heatmap ───
        st.markdown("### 🗺️ Heatmap: Similarity Paper vs 5 Metode")
        st.caption("Semakin hijau = semakin mirip kontennya dengan metode kita.")
        
        # Show top 30 papers for readability
        top_n = min(30, len(valid_papers))
        top_indices = sim_matrix.max(axis=1).argsort()[-top_n:][::-1]
        
        heatmap_data = sim_matrix[top_indices]
        heatmap_labels = [valid_papers[i].get("title", "")[:60] + "..." for i in top_indices]
        
        fig_heatmap = px.imshow(
            heatmap_data,
            labels=dict(x="Metode Analisis", y="Paper", color="Similarity"),
            x=method_names,
            y=heatmap_labels,
            color_continuous_scale="Greens",
            aspect="auto",
            height=max(400, top_n * 25)
        )
        fig_heatmap.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=10),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # ─── Per-Method Score ───
        st.markdown("### 📈 Skor Validasi per Metode")
        
        method_scores = []
        for i, name in enumerate(method_names):
            col_sim = sim_matrix[:, i]
            method_scores.append({
                "Metode": name,
                "Rata-rata Similarity": round(col_sim.mean(), 4),
                "Max Similarity": round(col_sim.max(), 4),
                "Paper Terkait (>0.05)": int((col_sim > 0.05).sum()),
                "Status": "✅ Validated" if col_sim.max() > 0.05 else "⚠️ Weak"
            })
        
        df_scores = pd.DataFrame(method_scores)
        
        fig_bar = px.bar(
            df_scores, x="Metode", y="Rata-rata Similarity",
            color="Rata-rata Similarity",
            color_continuous_scale="Greens",
            text="Paper Terkait (>0.05)",
            height=350
        )
        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.dataframe(df_scores, use_container_width=True, hide_index=True)
        
        # ─── Detail Table ───
        st.markdown("---")
        st.markdown("### 📄 Detail Paper yang Ditemukan")
        
        detail_rows = []
        for i, paper in enumerate(valid_papers):
            best_method_idx = sim_matrix[i].argmax()
            detail_rows.append({
                "Judul": paper.get("title", "")[:80],
                "Penulis": ", ".join(paper.get("authors", [])[:3]) or "—",
                "DOI / URL": paper.get("doi", "") or "—",
                "Sumber": paper.get("fetch_method", ""),
                "Metode Terdekat": method_names[best_method_idx],
                "Similarity": round(sim_matrix[i, best_method_idx], 4)
            })
        
        df_detail = pd.DataFrame(detail_rows)
        df_detail = df_detail.sort_values("Similarity", ascending=False)
        
        st.dataframe(
            df_detail,
            use_container_width=True,
            hide_index=True,
            height=500
        )
        
        # ─── Bibliometric Network (VOSviewer-style) ───
        st.markdown("---")
        st.markdown("### 🌐 Bibliometric Network — Keyword Co-occurrence")
        st.caption("Visualisasi jaringan kata kunci seperti VOSviewer. Node = keyword, garis = co-occurrence, warna = cluster.")
        
        # Extract keywords from all papers
        from sklearn.feature_extraction.text import TfidfVectorizer as TV2
        
        kw_vectorizer = TV2(
            stop_words="english", 
            max_features=80, 
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        kw_matrix = kw_vectorizer.fit_transform(corpus_texts)
        kw_names = kw_vectorizer.get_feature_names_out()
        
        # Build co-occurrence matrix
        co_matrix = (kw_matrix.T @ kw_matrix).toarray()
        np.fill_diagonal(co_matrix, 0)
        
        # Build NetworkX graph
        G = nx.Graph()
        for i, kw in enumerate(kw_names):
            freq = int(kw_matrix[:, i].sum())
            G.add_node(kw, size=freq)
        
        # Add edges (only significant co-occurrences)
        threshold = max(1, np.percentile(co_matrix[co_matrix > 0], 30) if co_matrix.max() > 0 else 1)
        edges_added = 0
        for i in range(len(kw_names)):
            for j in range(i + 1, len(kw_names)):
                if co_matrix[i][j] >= threshold:
                    G.add_edge(kw_names[i], kw_names[j], weight=float(co_matrix[i][j]))
                    edges_added += 1
        
        # Remove isolated nodes
        isolates = list(nx.isolates(G))
        G.remove_nodes_from(isolates)
        
        if len(G.nodes) > 5:
            # Community detection
            try:
                communities = nx.community.louvain_communities(G, seed=42)
            except Exception:
                communities = [set(G.nodes)]
            
            node_to_cluster = {}
            for idx, comm in enumerate(communities):
                for node in comm:
                    node_to_cluster[node] = idx
            
            n_clusters = len(communities)
            
            # VOSviewer-like colors
            cluster_colors = [
                '#e6194b', '#3cb44b', '#4363d8', '#f58231', '#911eb4',
                '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990',
                '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3'
            ]
            
            # Layout
            pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
            
            # Stats bar
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.metric("📌 Items (Keywords)", len(G.nodes))
            with sc2:
                st.metric("🔗 Links", len(G.edges))
            with sc3:
                st.metric("🎨 Clusters", n_clusters)
            
            # Build Plotly figure
            fig_net = go.Figure()
            
            # Draw edges
            for edge in G.edges(data=True):
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                weight = edge[2].get('weight', 1)
                fig_net.add_trace(go.Scatter(
                    x=[x0, x1, None], y=[y0, y1, None],
                    mode='lines',
                    line=dict(
                        width=max(0.3, min(weight * 0.4, 3)),
                        color='rgba(150,150,150,0.25)'
                    ),
                    hoverinfo='none',
                    showlegend=False
                ))
            
            # Draw nodes per cluster
            for cluster_id in range(n_clusters):
                cluster_nodes = [n for n, c in node_to_cluster.items() if c == cluster_id]
                if not cluster_nodes:
                    continue
                
                node_x = [pos[n][0] for n in cluster_nodes]
                node_y = [pos[n][1] for n in cluster_nodes]
                node_sizes = [max(12, min(G.nodes[n].get('size', 1) * 4, 50)) for n in cluster_nodes]
                node_texts = cluster_nodes
                hover_texts = [
                    f"<b>{n}</b><br>Frequency: {G.nodes[n].get('size', 0)}<br>Links: {G.degree(n)}<br>Cluster: {cluster_id + 1}"
                    for n in cluster_nodes
                ]
                
                color = cluster_colors[cluster_id % len(cluster_colors)]
                
                fig_net.add_trace(go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers+text',
                    marker=dict(
                        size=node_sizes,
                        color=color,
                        line=dict(width=1, color='white'),
                        opacity=0.85
                    ),
                    text=node_texts,
                    textposition='top center',
                    textfont=dict(size=9, color='white'),
                    hovertext=hover_texts,
                    hoverinfo='text',
                    name=f'Cluster {cluster_id + 1} ({len(cluster_nodes)})'
                ))
            
            fig_net.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=650,
                showlegend=True,
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(size=10)),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                margin=dict(l=10, r=10, t=40, b=10),
                title=dict(text=f'Keyword Co-occurrence Network — {len(G.nodes)} items, {len(G.edges)} links, {n_clusters} clusters', font=dict(size=12))
            )
            
            st.plotly_chart(fig_net, use_container_width=True)
        else:
            st.warning("Tidak cukup keyword untuk membangun network. Coba harvest lebih banyak paper.")
        
        # ─── Export ───
        st.markdown("---")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            csv_data = df_detail.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Hasil (CSV)",
                csv_data,
                "validasi_metode_results.csv",
                "text/csv",
                use_container_width=True
            )
        with col_dl2:
            json_data = json.dumps(corpus, indent=2, ensure_ascii=False).encode("utf-8")
            st.download_button(
                "📥 Download Corpus (JSON)",
                json_data,
                "corpus.json",
                "application/json",
                use_container_width=True
            )

else:
    # No data yet — show instructions
    st.info("👆 Klik tombol **Mulai Harvesting & Validasi** untuk memulai. OpenAlex tidak memerlukan API key.\n\n💾 Hasil akan tersimpan otomatis dan tetap ada setelah refresh.")
    
    st.markdown("### 📋 5 Metode yang Akan Divalidasi")
    for name, info in METHODS.items():
        st.markdown(f"""
        <div class="method-card">
            <div class="method-title">{name}</div>
            <div class="method-desc">{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
