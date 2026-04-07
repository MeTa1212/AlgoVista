"""
Merge Sort visualiser.

Diamond layout:
  SPLIT  phase → root at top,  leaves at bottom  (pre-order reveal, top-down)
  MERGE  phase → leaves at top, root at bottom   (post-order reveal, bottom-up)

Everything is pre-computed Python-side and injected into a single self-contained
HTML page that animates with JS timers, so Streamlit never re-renders during the
animation and the browser scroll position is preserved.
"""


# ─────────────────────────────────────────────────────────────────
#  TREE BUILDER
# ─────────────────────────────────────────────────────────────────

def build_merge_tree(arr):
    """Recursively build a dict tree of every split/merge step."""
    if len(arr) <= 1:
        return {"arr": arr, "left": None, "right": None, "sorted": arr}
    mid        = len(arr) // 2
    left_node  = build_merge_tree(arr[:mid])
    right_node = build_merge_tree(arr[mid:])
    merged     = sorted(left_node["sorted"] + right_node["sorted"])
    return {"arr": arr, "left": left_node, "right": right_node, "sorted": merged}


def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node["left"]) + count_nodes(node["right"])


# ─────────────────────────────────────────────────────────────────
#  SHARED BOX BUILDER
# ─────────────────────────────────────────────────────────────────

def _boxes_html(values, box_bg):
    return "".join(
        f'<div style="min-width:36px;height:36px;padding:0 8px;border-radius:10px;'
        f'background:{box_bg};display:flex;align-items:center;justify-content:center;'
        f'color:white;font-size:14px;font-weight:800;'
        f'box-shadow:3px 3px 8px rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.08);">'
        f'{v}</div>'
        for v in values
    )


def _node_card(label, header_color, boxes_html):
    return (
        f'<div style="background:rgba(15,23,42,0.92);border:1px solid {header_color}55;'
        f'border-radius:14px;padding:8px 14px;margin:4px;min-width:80px;'
        f'box-shadow:0 4px 18px rgba(0,0,0,0.45);">'
        f'<div style="color:{header_color};font-size:9px;font-weight:700;'
        f'letter-spacing:1.5px;margin-bottom:5px;text-align:center;">{label}</div>'
        f'<div style="display:flex;gap:4px;flex-wrap:wrap;justify-content:center;">'
        f'{boxes_html}</div></div>'
    )


# ─────────────────────────────────────────────────────────────────
#  SPLIT PHASE RENDERER
#  Pre-order traversal → parent gets lower ID than children
#  Layout: parent above, children below
# ─────────────────────────────────────────────────────────────────

def render_split_tree_html(node, step_counter, reveal_up_to):
    """Returns (html, next_step_counter)."""
    if node is None:
        return "", step_counter

    my_id        = step_counter
    step_counter += 1
    is_base      = node["left"] is None
    visible      = my_id <= reveal_up_to

    if is_base:
        header_color = "#10B981"
        label        = "BASE"
        box_bg       = "linear-gradient(135deg,#10B981,#059669)"
        values       = node["arr"]
    else:
        header_color = "#A78BFA"
        label        = "SPLIT"
        box_bg       = "linear-gradient(145deg,#1E293B,#0F172A)"
        values       = node["arr"]

    opacity    = "1"              if visible else "0"
    ty         = "translateY(0)"  if visible else "translateY(-18px)"
    transition = f"opacity 0.4s ease {(my_id % 6)*0.06:.2f}s, transform 0.4s ease"

    card = _node_card(label, header_color, _boxes_html(values, box_bg))

    html = (
        f'<div style="display:flex;flex-direction:column;align-items:center;'
        f'opacity:{opacity};transform:{ty};transition:{transition};">'
        f'{card}'
    )

    if not is_base:
        left_html,  step_counter = render_split_tree_html(node["left"],  step_counter, reveal_up_to)
        right_html, step_counter = render_split_tree_html(node["right"], step_counter, reveal_up_to)
        html += (
            f'<div style="display:flex;gap:10px;align-items:flex-start;'
            f'justify-content:center;margin-top:2px;">'
            f'{left_html}{right_html}</div>'
        )

    html += "</div>"
    return html, step_counter


# ─────────────────────────────────────────────────────────────────
#  MERGE PHASE RENDERER  (inverted / diamond bottom half)
#  Post-order traversal → leaves get lower IDs, root gets highest ID
#  Layout: children above, merged result below  → forms lower half of diamond
# ─────────────────────────────────────────────────────────────────

def render_merge_inverted_html(node, step_counter, reveal_up_to):
    """Post-order IDs; children rendered above their parent node."""
    if node is None:
        return "", step_counter

    is_base = node["left"] is None

    if is_base:
        # Leaf node — assign ID now (post-order for leaf is same as pre-order)
        my_id        = step_counter
        step_counter += 1
        visible      = my_id <= reveal_up_to
        opacity      = "1"             if visible else "0"
        ty           = "translateY(0)" if visible else "translateY(18px)"
        transition   = f"opacity 0.4s ease {(my_id % 6)*0.06:.2f}s, transform 0.4s ease"

        card = _node_card("BASE", "#10B981", _boxes_html(node["sorted"],
                          "linear-gradient(135deg,#10B981,#059669)"))
        html = (
            f'<div style="display:flex;flex-direction:column;align-items:center;'
            f'opacity:{opacity};transform:{ty};transition:{transition};">'
            f'{card}</div>'
        )
        return html, step_counter

    # Internal node — traverse children first (post-order)
    left_html,  step_counter = render_merge_inverted_html(node["left"],  step_counter, reveal_up_to)
    right_html, step_counter = render_merge_inverted_html(node["right"], step_counter, reveal_up_to)

    my_id        = step_counter          # Parent gets ID after both children
    step_counter += 1
    visible      = my_id <= reveal_up_to
    opacity      = "1"             if visible else "0"
    ty           = "translateY(0)" if visible else "translateY(18px)"
    transition   = f"opacity 0.4s ease {(my_id % 6)*0.06:.2f}s, transform 0.4s ease"

    card = _node_card(
        "MERGED", "#38BDF8",
        _boxes_html(node["sorted"], "linear-gradient(135deg,#F59E0B,#D97706)")
    )

    # Children row on TOP, merged card BELOW
    html = (
        f'<div style="display:flex;flex-direction:column;align-items:center;">'
        f'<div style="display:flex;gap:10px;align-items:flex-end;justify-content:center;margin-bottom:2px;">'
        f'{left_html}{right_html}</div>'
        f'<div style="opacity:{opacity};transform:{ty};transition:{transition};">'
        f'{card}</div></div>'
    )
    return html, step_counter


# ─────────────────────────────────────────────────────────────────
#  JAVASCRIPT-ANIMATED SELF-CONTAINED HTML PAGE
# ─────────────────────────────────────────────────────────────────

def build_animated_merge_html(arr, speed_seconds):
    """
    Returns a complete HTML document that plays the full merge-sort
    animation client-side.  Call once with components.html(); Streamlit
    never re-renders during playback so scroll position is preserved.
    """
    tree     = build_merge_tree(arr)
    total    = count_nodes(tree)
    delay_ms = int(speed_seconds * 1000)

    # --- Pre-render all split frames (reveal_up_to: -1 → total) ---
    split_frames = []
    for rev in range(-1, total + 1):
        html, _ = render_split_tree_html(tree, 0, rev)
        split_frames.append(html)

    # --- Pre-render all merge frames (reveal_up_to: -1 → total) ---
    merge_frames = []
    for rev in range(-1, total + 1):
        html, _ = render_merge_inverted_html(tree, 0, rev)
        merge_frames.append(html)

    # --- Final sorted boxes ---
    sorted_arr   = sorted(arr)
    sorted_boxes = "".join(
        f'<div style="min-width:48px;height:48px;padding:0 10px;border-radius:12px;'
        f'background:linear-gradient(135deg,#10B981,#059669);'
        f'display:flex;align-items:center;justify-content:center;'
        f'color:white;font-size:18px;font-weight:800;'
        f'box-shadow:0 4px 14px rgba(16,185,129,0.4);">{v}</div>'
        for v in sorted_arr
    )

    # Escape frames for JS template literals
    def to_js_array(frames):
        escaped = [f.replace("\\", "\\\\").replace("`", "\\`") for f in frames]
        return "[" + ",".join(f"`{e}`" for e in escaped) + "]"

    split_js = to_js_array(split_frames)
    merge_js = to_js_array(merge_frames)

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 8px;
    background: transparent;
    font-family: 'Segoe UI', sans-serif;
    color: white;
  }}
  .phase-label {{
    font-size: 11px; font-weight: 800; letter-spacing: 2px;
    padding: 5px 16px; border-radius: 999px;
    display: inline-block; margin-bottom: 10px;
  }}
  #status-bar {{
    background: rgba(15,23,42,0.85);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 11px 18px; margin-bottom: 10px;
    transition: border-color 0.4s;
  }}
  #final-box {{
    display: none;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 14px; padding: 16px; text-align: center; margin-top: 10px;
  }}
  .divider {{
    width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, #334155, transparent);
    margin: 10px 0;
  }}
</style>
</head>
<body>

<!-- Status bar -->
<div id="status-bar">
  <span id="phase-tag"  style="font-size:10px;font-weight:700;letter-spacing:1px;color:#A78BFA;">PHASE</span>
  <span id="phase-name" style="color:#F8FAFC;font-weight:700;margin-left:10px;">Splitting</span>
  <span id="phase-info" style="color:#475569;font-size:12px;margin-left:8px;"></span>
</div>

<div style="display:flex;flex-direction:column;align-items:center;">

  <!-- ── SPLIT: root at top, leaves grow downward ── -->
  <div style="width:100%;display:flex;flex-direction:column;align-items:center;">
    <span class="phase-label"
          style="background:rgba(167,139,250,0.12);color:#A78BFA;border:1px solid #A78BFA44;">
      ▼ SPLIT PHASE
    </span>
    <div id="split-area"></div>
  </div>

  <div class="divider"></div>

  <!-- ── MERGE: base elements at top, merged root grows downward ── -->
  <div style="width:100%;display:flex;flex-direction:column;align-items:center;">
    <span class="phase-label"
          style="background:rgba(56,189,248,0.12);color:#38BDF8;border:1px solid #38BDF844;">
      ▲ MERGE PHASE
    </span>
    <div id="merge-area"></div>
  </div>

</div>

<!-- Final sorted result (shown when done) -->
<div id="final-box">
  <div style="color:#10B981;font-size:10px;font-weight:700;letter-spacing:2px;margin-bottom:12px;">
    ✅ FINAL SORTED ARRAY
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;">
    {sorted_boxes}
  </div>
</div>

<script>
(function() {{
  var splitFrames = {split_js};
  var mergeFrames = {merge_js};
  var delay    = {delay_ms};
  var total    = {total};

  var splitArea  = document.getElementById('split-area');
  var mergeArea  = document.getElementById('merge-area');
  var statusBar  = document.getElementById('status-bar');
  var phaseTag   = document.getElementById('phase-tag');
  var phaseName  = document.getElementById('phase-name');
  var phaseInfo  = document.getElementById('phase-info');
  var finalBox   = document.getElementById('final-box');

  // Index 0 in our arrays corresponds to reveal_up_to = -1 (nothing shown)
  // Index k corresponds to reveal_up_to = k-1
  var OFFSET = 1;   // splitFrames[OFFSET + k] = frame where k nodes revealed

  var phase = 'split';
  var frame = 0;      // 0 = nothing revealed yet

  // Show initial empty state
  splitArea.innerHTML = splitFrames[0];
  mergeArea.innerHTML = mergeFrames[0];

  function tick() {{
    if (phase === 'split') {{
      splitArea.innerHTML = splitFrames[OFFSET + frame];
      phaseTag.style.color     = '#A78BFA';
      phaseTag.textContent     = 'PHASE';
      phaseName.textContent    = 'Splitting';
      phaseInfo.textContent    = '— node ' + frame + ' / ' + total;
      statusBar.style.borderColor = 'rgba(167,139,250,0.4)';

      frame++;
      if (frame <= total) {{
        setTimeout(tick, delay);
      }} else {{
        // Pause then start merge
        phase = 'merge';
        frame = 0;
        setTimeout(tick, delay * 1.5);
      }}

    }} else {{
      mergeArea.innerHTML = mergeFrames[OFFSET + frame];
      phaseTag.style.color     = '#38BDF8';
      phaseTag.textContent     = 'PHASE';
      phaseName.textContent    = 'Merging';
      phaseInfo.textContent    = '— step ' + frame + ' / ' + total;
      statusBar.style.borderColor = 'rgba(56,189,248,0.4)';

      frame++;
      if (frame <= total) {{
        setTimeout(tick, delay);
      }} else {{
        phaseTag.style.color     = '#10B981';
        phaseTag.textContent     = '✅';
        phaseName.textContent    = 'Sort Complete!';
        phaseInfo.textContent    = 'Array is fully sorted.';
        statusBar.style.borderColor = 'rgba(16,185,129,0.4)';
        finalBox.style.display   = 'block';
      }}
    }}
  }}

  setTimeout(tick, 400);
}})();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────
#  STEP GENERATOR  (kept for future use / testing)
# ─────────────────────────────────────────────────────────────────

def merge_sort_steps(arr, level=0):
    if len(arr) <= 1:
        yield {
            "type": "base", "level": level, "array": arr.copy(),
            "left": None, "right": None, "merged": None,
            "message": f"Reached single element {arr}"
        }
        return arr

    mid   = len(arr) // 2
    left  = arr[:mid]
    right = arr[mid:]

    yield {
        "type": "split", "level": level, "array": arr.copy(),
        "left": left.copy(), "right": right.copy(), "merged": None,
        "message": f"Splitting {arr} into {left} and {right}"
    }

    left_sorted  = yield from merge_sort_steps(left,  level + 1)
    right_sorted = yield from merge_sort_steps(right, level + 1)

    merged = []
    i = j  = 0
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] < right_sorted[j]:
            merged.append(left_sorted[i]); i += 1
        else:
            merged.append(right_sorted[j]); j += 1
    merged.extend(left_sorted[i:])
    merged.extend(right_sorted[j:])

    yield {
        "type": "merge", "level": level, "array": arr.copy(),
        "left": left_sorted.copy(), "right": right_sorted.copy(),
        "merged": merged.copy(),
        "message": f"Merging {left_sorted} and {right_sorted} → {merged}"
    }
    return merged