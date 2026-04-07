import streamlit as st
import streamlit.components.v1 as components
import random
import time
import math

from utils.styles import load_css
from algorithms.slidingWindow import build_animated_sliding_window_html
from algorithms.hamiltonian import (
    hamiltonian_cycle_visual,
    generate_graph_with_cycle,
    generate_graph_without_cycle
)
from algorithms.mergeSort import build_animated_merge_html

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AlgoVista",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_css()

# ---------------- Navigation State ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    st.session_state.page = "home"
    for k in ["merge_arr_tree", "slide_arr", "merge_started"]:
        if k in st.session_state:
            del st.session_state[k]

def go_merge():
    st.session_state.page = "merge"

def go_sliding():
    st.session_state.page = "sliding"

def go_hamiltonian():
    st.session_state.page = "hamiltonian"


# ─────────────────────────────────────────────
#  SLIDING WINDOW HELPER
# ─────────────────────────────────────────────
def draw_boxes(arr, highlight=None, best=None):
    if highlight is None: highlight = []
    if best is None:      best = []

    boxes = ""
    for i, num in enumerate(arr):
        if i in best:
            bg    = "linear-gradient(135deg,#10B981,#059669)"
            glow  = "0 0 14px rgba(16,185,129,0.55)"
            scale = "scale(1.12)"
            border= "2px solid #10B98188"
        elif i in highlight:
            bg    = "linear-gradient(135deg,#F59E0B,#D97706)"
            glow  = "0 0 14px rgba(245,158,11,0.55)"
            scale = "scale(1.08)"
            border= "2px solid #F59E0B88"
        else:
            bg    = "linear-gradient(145deg,#1E293B,#0F172A)"
            glow  = "none"
            scale = "scale(1)"
            border= "1px solid rgba(255,255,255,0.07)"

        boxes += f'''
        <div style="width:62px;height:62px;border-radius:16px;background:{bg};
                    display:flex;align-items:center;justify-content:center;
                    color:white;font-size:24px;font-weight:800;
                    box-shadow:{glow};transform:{scale};transition:all 0.3s ease;
                    border:{border};">{num}</div>'''

    return f'''
    <style>body{{margin:0;padding:8px;}}</style>
    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;padding:12px 0;">
        {boxes}
    </div>'''


# ─────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────
if st.session_state.page == "home":

    st.markdown("""
    <div style="text-align:center;padding:40px 0 10px;">
        <div style="font-size:3.6rem;font-weight:900;letter-spacing:-1px;
                    background:linear-gradient(135deg,#A78BFA,#38BDF8,#10B981);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            🧠 AlgoVista
        </div>
        <div style="color:#94A3B8;font-size:1.15rem;margin-top:10px;">
            A premium visual learning platform for core DAA concepts
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(15,23,42,0.72);border:1px solid rgba(255,255,255,0.06);
                border-radius:24px;padding:28px 36px;margin:24px 0 32px;
                box-shadow:0 12px 40px rgba(0,0,0,0.28);backdrop-filter:blur(16px);">
        <div style="font-size:1.3rem;font-weight:800;color:#F8FAFC;margin-bottom:14px;">🚀 Project Overview</div>
        <div style="color:#CBD5E1;font-size:1rem;line-height:1.9;">
            <b style="color:#F8FAFC;">AlgoVista</b> is an interactive algorithm visualization platform built to simplify
            understanding of key <b style="color:#F8FAFC;">Design and Analysis of Algorithms (DAA)</b> concepts.<br><br>
            <span style="color:#A78BFA;">🔀 <b>Merge Sort</b></span> &nbsp;→&nbsp; Divide and Conquer &nbsp;&nbsp;|&nbsp;&nbsp;
            <span style="color:#F59E0B;">🪟 <b>Max Sum Subarray</b></span> &nbsp;→&nbsp; Sliding Window &nbsp;&nbsp;|&nbsp;&nbsp;
            <span style="color:#60A5FA;">🔵 <b>Hamiltonian Cycle</b></span> &nbsp;→&nbsp; Graph Backtracking
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    card_style = """background:rgba(15,23,42,0.72);border:1px solid rgba(255,255,255,0.06);
                   border-radius:22px;padding:28px 24px;min-height:230px;
                   box-shadow:0 12px 35px rgba(0,0,0,0.28);margin-bottom:12px;"""

    with c1:
        st.markdown(f"""
        <div style="{card_style}border-top:3px solid #A78BFA;">
            <div style="display:inline-block;padding:5px 14px;border-radius:999px;
                        background:linear-gradient(135deg,#4F46E5,#7C3AED);color:white;
                        font-size:0.78rem;font-weight:700;margin-bottom:16px;letter-spacing:0.5px;">
                Divide &amp; Conquer
            </div>
            <div style="font-size:1.5rem;font-weight:800;color:#F8FAFC;margin-bottom:12px;">🔀 Merge Sort</div>
            <div style="color:#CBD5E1;font-size:0.97rem;line-height:1.7;">
                Watch the full split tree and merge tree side-by-side, animated level by level.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Open Merge Sort →", key="merge_btn", on_click=go_merge)

    with c2:
        st.markdown(f"""
        <div style="{card_style}border-top:3px solid #F59E0B;">
            <div style="display:inline-block;padding:5px 14px;border-radius:999px;
                        background:linear-gradient(135deg,#D97706,#F59E0B);color:white;
                        font-size:0.78rem;font-weight:700;margin-bottom:16px;letter-spacing:0.5px;">
                Sliding Window
            </div>
            <div style="font-size:1.5rem;font-weight:800;color:#F8FAFC;margin-bottom:12px;">🪟 Max Sum Subarray</div>
            <div style="color:#CBD5E1;font-size:0.97rem;line-height:1.7;">
                See how the window glides across the array, tracking current and best sums in real time.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Open Sliding Window →", key="slide_btn", on_click=go_sliding)

    with c3:
        st.markdown(f"""
        <div style="{card_style}border-top:3px solid #60A5FA;">
            <div style="display:inline-block;padding:5px 14px;border-radius:999px;
                        background:linear-gradient(135deg,#2563EB,#60A5FA);color:white;
                        font-size:0.78rem;font-weight:700;margin-bottom:16px;letter-spacing:0.5px;">
                Graph Backtracking
            </div>
            <div style="font-size:1.5rem;font-weight:800;color:#F8FAFC;margin-bottom:12px;">🔵 Hamiltonian Cycle</div>
            <div style="color:#CBD5E1;font-size:0.97rem;line-height:1.7;">
                Explore paths that visit every node exactly once and see backtracking live on the graph.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Open Hamiltonian Cycle →", key="ham_btn", on_click=go_hamiltonian)

    st.markdown("""
    <div style="text-align:center;color:#475569;margin-top:48px;font-size:0.9rem;">
        Built for DAA Project &nbsp;•&nbsp; AlgoVista Premium UI
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MERGE SORT PAGE
# ─────────────────────────────────────────────
elif st.session_state.page == "merge":

    # ── top bar ───────────────────────────────
    col_back, col_title = st.columns([1, 5])
    with col_back:
        st.button("⬅ Home", on_click=go_home)
    with col_title:
        st.markdown("""
        <div style="padding:4px 0;">
            <span style="font-size:2rem;font-weight:900;
                         background:linear-gradient(135deg,#A78BFA,#7C3AED);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                🔀 Merge Sort
            </span>
            <span style="color:#64748B;font-size:0.95rem;margin-left:12px;">
                Divide &amp; Conquer · Split tree and Merge tree simultaneously
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    left, right = st.columns([2.4, 1])

    with right:
        st.markdown("""
        <div style="background:rgba(15,23,42,0.8);border:1px solid rgba(255,255,255,0.07);
                    border-radius:20px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,0.3);">
            <div style="font-size:1.1rem;font-weight:800;color:#F8FAFC;margin-bottom:18px;">⚙ Controls</div>
        """, unsafe_allow_html=True)

        size  = st.slider("Array Size", 4, 12, 6)
        speed = st.slider("Animation Speed (s/step)", 0.1, 1.5, 0.5)

        generate = st.button("🎲 Generate Array", use_container_width=True)
        start    = st.button("▶ Start Visualization", use_container_width=True)

        # Legend
        st.markdown("""
        <div style="margin-top:20px;border-top:1px solid rgba(255,255,255,0.07);padding-top:16px;">
            <div style="font-size:0.8rem;font-weight:700;color:#64748B;letter-spacing:1px;margin-bottom:10px;">LEGEND</div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <div style="width:12px;height:12px;border-radius:3px;background:#A78BFA;"></div>
                <span style="color:#CBD5E1;font-size:0.85rem;">Split phase</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <div style="width:12px;height:12px;border-radius:3px;background:#38BDF8;"></div>
                <span style="color:#CBD5E1;font-size:0.85rem;">Merge phase</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="width:12px;height:12px;border-radius:3px;background:#10B981;"></div>
                <span style="color:#CBD5E1;font-size:0.85rem;">Base case (single element)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with left:

        if generate:
            st.session_state.merge_arr_tree = [random.randint(-49, 99) for _ in range(size)]
            if "merge_started" in st.session_state:
                del st.session_state["merge_started"]

        # ── Nothing generated yet ─────────────────────────────
        if "merge_arr_tree" not in st.session_state:
            st.markdown("""
            <div style="background:rgba(15,23,42,0.6);border:1px solid rgba(255,255,255,0.06);
                        border-radius:20px;padding:48px 32px;text-align:center;margin-top:16px;">
                <div style="font-size:2rem;margin-bottom:12px;">🎲</div>
                <div style="color:#F8FAFC;font-size:1.2rem;font-weight:700;margin-bottom:8px;">
                    No Array Yet
                </div>
                <div style="color:#64748B;font-size:0.95rem;">
                    Click <b style="color:#A78BFA;">Generate Array</b> to create an array, then hit Start.
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            arr = st.session_state.merge_arr_tree.copy()

            if start:
                # ── Build and inject the fully self-contained animated page ──
                # This renders exactly ONCE – no Streamlit rerenders, no scroll jump.
                animated_html = build_animated_merge_html(arr, speed)
                components.html(animated_html, height=820, scrolling=True)

            else:
                # ── Show array preview only (awaiting Start click) ───────────
                boxes = "".join(f'''
                    <div style="min-width:52px;height:52px;padding:0 12px;border-radius:14px;
                                background:linear-gradient(135deg,#4F46E5,#7C3AED);
                                display:flex;align-items:center;justify-content:center;
                                color:white;font-size:20px;font-weight:800;
                                box-shadow:0 4px 14px rgba(99,102,241,0.4);">{v}</div>''' for v in arr)

                components.html(f"""
                <style>body{{margin:0;padding:12px;}}</style>
                <div style="background:rgba(15,23,42,0.85);border:1px solid rgba(167,139,250,0.2);
                            border-radius:20px;padding:24px;text-align:center;">
                    <div style="color:#A78BFA;font-size:12px;font-weight:700;letter-spacing:2px;margin-bottom:16px;">
                        GENERATED ARRAY
                    </div>
                    <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
                        {boxes}
                    </div>
                    <div style="color:#475569;font-size:12px;margin-top:16px;">
                        Click ▶ Start Visualization to animate
                    </div>
                </div>
                """, height=160)


# ─────────────────────────────────────────────
#  SLIDING WINDOW PAGE
# ─────────────────────────────────────────────
elif st.session_state.page == "sliding":

    col_back, col_title = st.columns([1, 5])
    with col_back:
        st.button("⬅ Home", on_click=go_home)
    with col_title:
        st.markdown("""
        <div style="padding:4px 0;">
            <span style="font-size:2rem;font-weight:900;
                         background:linear-gradient(135deg,#F59E0B,#D97706);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                🪟 Sliding Window
            </span>
            <span style="color:#64748B;font-size:0.95rem;margin-left:12px;">
                Maximum Sum Subarray of Size K
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    left, right = st.columns([2.4, 1])

    with right:
        st.markdown("""
        <div style="background:rgba(15,23,42,0.8);border:1px solid rgba(255,255,255,0.07);
                    border-radius:20px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,0.3);">
            <div style="font-size:1.1rem;font-weight:800;color:#F8FAFC;margin-bottom:18px;">⚙ Controls</div>
        """, unsafe_allow_html=True)

        size  = st.slider("Array Size", 5, 15, 8)
        k     = st.slider("Window Size (K)", 2, 6, 3)
        speed = st.slider("Animation Speed (s/step)", 0.1, 1.5, 0.5)

        generate = st.button("🎲 Generate Array", use_container_width=True)
        start    = st.button("▶ Start Visualization", use_container_width=True)

        st.markdown("""
        <div style="margin-top:20px;border-top:1px solid rgba(255,255,255,0.07);padding-top:16px;">
            <div style="font-size:0.8rem;font-weight:700;color:#64748B;letter-spacing:1px;margin-bottom:10px;">LEGEND</div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <div style="width:12px;height:12px;border-radius:3px;background:#F59E0B;"></div>
                <span style="color:#CBD5E1;font-size:0.85rem;">Current window</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="width:12px;height:12px;border-radius:3px;background:#10B981;"></div>
                <span style="color:#CBD5E1;font-size:0.85rem;">Best window so far</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with left:

        if generate:
            st.session_state.slide_arr = [random.randint(-49, 99) for _ in range(size)]

        # ── Nothing generated yet ─────────────────────────────
        if "slide_arr" not in st.session_state:
            st.markdown("""
            <div style="background:rgba(15,23,42,0.6);border:1px solid rgba(255,255,255,0.06);
                        border-radius:20px;padding:48px 32px;text-align:center;margin-top:16px;">
                <div style="font-size:2rem;margin-bottom:12px;">🎲</div>
                <div style="color:#F8FAFC;font-size:1.2rem;font-weight:700;margin-bottom:8px;">
                    No Array Yet
                </div>
                <div style="color:#64748B;font-size:0.95rem;">
                    Click <b style="color:#F59E0B;">Generate Array</b> to begin.
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            arr = st.session_state.slide_arr

            if start:
                # Single render — JS drives the entire animation client-side.
                # No Streamlit rerenders → no scroll jump, no raw-HTML display bug.
                animated_html = build_animated_sliding_window_html(arr, k, speed)
                components.html(animated_html, height=340, scrolling=False)

            else:
                # Show array preview only (not before Generate is clicked)
                components.html(draw_boxes(arr), height=110)
                st.markdown("""
                <div style="color:#475569;font-size:13px;text-align:center;margin-top:4px;">
                    Click ▶ Start Visualization to animate
                </div>
                """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HAMILTONIAN CYCLE PAGE
# ─────────────────────────────────────────────
elif st.session_state.page == "hamiltonian":

    col_back, col_title = st.columns([1, 5])
    with col_back:
        st.button("⬅ Home", on_click=go_home)
    with col_title:
        st.markdown("""
        <div style="padding:4px 0;">
            <span style="font-size:2rem;font-weight:900;
                         background:linear-gradient(135deg,#60A5FA,#2563EB);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                🔵 Hamiltonian Cycle
            </span>
            <span style="color:#64748B;font-size:0.95rem;margin-left:12px;">
                Graph Backtracking · Visit every vertex exactly once
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    left, right = st.columns([2.4, 1])

    with right:
        st.markdown("""
        <div style="background:rgba(15,23,42,0.8);border:1px solid rgba(255,255,255,0.07);
                    border-radius:20px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,0.3);">
            <div style="font-size:1.1rem;font-weight:800;color:#F8FAFC;margin-bottom:18px;">⚙ Controls</div>
        """, unsafe_allow_html=True)

        node_count = st.slider("Number of Nodes", 4, 8, 5)
        graph_type = st.selectbox("Graph Type", ["Graph WITH Hamiltonian Cycle", "Graph WITHOUT Hamiltonian Cycle"])
        speed      = st.slider("Animation Speed (s/step)", 0.2, 2.0, 0.8)

        generate = st.button("🎲 Generate Graph", use_container_width=True)
        start    = st.button("▶ Start Check", use_container_width=True)

        st.markdown("""
        <div style="margin-top:20px;border-top:1px solid rgba(255,255,255,0.07);padding-top:16px;">
            <div style="font-size:0.8rem;font-weight:700;color:#64748B;letter-spacing:1px;margin-bottom:10px;">LEGEND</div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <div style="width:12px;height:12px;border-radius:50%;background:#F59E0B;"></div>
                <span style="color:#CBD5E1;font-size:0.85rem;">Exploring path</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <div style="width:12px;height:12px;border-radius:50%;background:#EF4444;"></div>
                <span style="color:#CBD5E1;font-size:0.85rem;">Dead-end (backtracking)</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <div style="width:12px;height:12px;border-radius:50%;background:#10B981;"></div>
                <span style="color:#CBD5E1;font-size:0.85rem;">Cycle found!</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="width:12px;height:12px;border-radius:50%;background:#60A5FA;"></div>
                <span style="color:#CBD5E1;font-size:0.85rem;">Unvisited node</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with left:
        if "ham_graph" not in st.session_state:
            st.session_state.ham_graph = None

        if generate:
            if graph_type == "Graph WITH Hamiltonian Cycle":
                st.session_state.ham_graph = generate_graph_with_cycle(node_count)
            else:
                st.session_state.ham_graph = generate_graph_without_cycle(node_count)

        graph_matrix = st.session_state.ham_graph

        def draw_graph_html(graph_matrix, path=None, state="normal"):
            """Render graph as a self-contained SVG inside an HTML page.
            state = 'normal'    → amber  (exploring)
            state = 'backtrack' → red    (dead-end, about to backtrack)
            state = 'found'     → green  (Hamiltonian cycle confirmed)
            """
            if path is None:
                path = []

            # Palette
            if state == "found":
                path_edge_color  = "#10B981"
                node_fill_active = "#059669"
                node_stroke_act  = "#34D399"
            elif state == "backtrack":
                path_edge_color  = "#EF4444"
                node_fill_active = "#B91C1C"
                node_stroke_act  = "#FCA5A5"
            else:  # "normal"
                path_edge_color  = "#F59E0B"
                node_fill_active = "#D97706"
                node_stroke_act  = "#FCD34D"

            n = len(graph_matrix)
            cx, cy, r_layout, r_node = 300, 220, 160, 22

            positions = []
            for i in range(n):
                angle = math.radians(-90 + 360 * i / n)
                positions.append((cx + r_layout * math.cos(angle),
                                  cy + r_layout * math.sin(angle)))

            visited_set = set(path)
            path_edges  = set()
            for i in range(len(path) - 1):
                a, b = path[i], path[i + 1]
                path_edges.add((min(a, b), max(a, b)))

            # Edges
            edges_svg = []
            for u in range(n):
                for v in range(u + 1, n):
                    if graph_matrix[u][v]:
                        x1, y1 = positions[u]
                        x2, y2 = positions[v]
                        is_pe   = (min(u, v), max(u, v)) in path_edges
                        color   = path_edge_color if is_pe else "#334155"
                        width   = "3.5" if is_pe else "1.5"
                        edges_svg.append(
                            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
                        )

            # Nodes
            nodes_svg = []
            for i, (px, py) in enumerate(positions):
                in_path = i in visited_set
                fill   = node_fill_active if in_path else "#1E40AF"
                stroke = node_stroke_act  if in_path else "#60A5FA"
                shadow = 'filter="url(#glow)"' if in_path else ''
                nodes_svg.append(
                    f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_node}" '
                    f'fill="{fill}" stroke="{stroke}" stroke-width="2.5" {shadow}/>'
                    f'<text x="{px:.1f}" y="{py + 6:.1f}" text-anchor="middle" '
                    f'font-size="15" font-weight="bold" fill="white" '
                    f'font-family="Segoe UI, sans-serif">{i}</text>'
                )

            svg = f"""
            <svg width="600" height="440" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur stdDeviation="4" result="blur"/>
                  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
              </defs>
              {''.join(edges_svg)}
              {''.join(nodes_svg)}
            </svg>"""

            return f"""<!DOCTYPE html><html><head>
            <style>body{{margin:0;padding:0;background:transparent;display:flex;
            justify-content:center;align-items:center;}}</style></head>
            <body>{svg}</body></html>"""

        if graph_matrix is None:
            st.markdown("""
            <div style="background:rgba(15,23,42,0.6);border:1px solid rgba(255,255,255,0.06);
                        border-radius:20px;padding:48px 32px;text-align:center;margin-top:16px;">
                <div style="font-size:2rem;margin-bottom:12px;">🔵</div>
                <div style="color:#F8FAFC;font-size:1.2rem;font-weight:700;margin-bottom:8px;">
                    No Graph Yet
                </div>
                <div style="color:#64748B;font-size:0.95rem;">
                    Click <b style="color:#60A5FA;">Generate Graph</b> first to create a graph.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            graph_ph  = st.empty()
            status_ph = st.empty()
            # Initial graph inside the placeholder so animation can replace it cleanly
            with graph_ph.container():
                components.html(draw_graph_html(graph_matrix), height=440)

            if start:
                for path, state, status in hamiltonian_cycle_visual(graph_matrix):
                    with graph_ph.container():
                        components.html(draw_graph_html(graph_matrix, path, state), height=440)
                    # Status panel color matches state
                    if state == "found":
                        panel_color = "#10B981"
                        border_col  = "rgba(16,185,129,0.35)"
                    elif state == "backtrack":
                        panel_color = "#EF4444"
                        border_col  = "rgba(239,68,68,0.35)"
                    else:
                        panel_color = "#F59E0B"
                        border_col  = "rgba(245,158,11,0.25)"
                    status_ph.markdown(f"""
                    <div style="background:rgba(15,23,42,0.85);border:1px solid {border_col};
                                border-radius:16px;padding:16px 22px;margin-top:8px;">
                        <div style="color:#64748B;font-size:11px;font-weight:700;letter-spacing:1px;">STATUS</div>
                        <div style="color:{panel_color};font-weight:800;font-size:1rem;margin-top:4px;">{status}</div>
                        <div style="color:#64748B;font-size:11px;font-weight:700;letter-spacing:1px;margin-top:12px;">CURRENT PATH</div>
                        <div style="color:#CBD5E1;font-size:0.95rem;margin-top:4px;">{"  →  ".join(str(p) for p in path)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(speed)


st.markdown("""
<div style="text-align:center;color:#1E293B;margin-top:48px;margin-bottom:16px;font-size:0.85rem;">
    Built for DAA Project &nbsp;•&nbsp; AlgoVista
</div>
""", unsafe_allow_html=True)
