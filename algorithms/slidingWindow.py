import json


def max_sum_subarray_visual(arr, k):
    if k > len(arr) or k <= 0:
        yield arr, [], "Invalid window size", 0, 0, []
        return

    current_sum = sum(arr[:k])
    max_sum = current_sum
    max_window = arr[:k]
    max_indices = list(range(k))

    yield arr, list(range(k)), f"Initial Window: {arr[:k]}", current_sum, max_sum, max_indices

    for i in range(k, len(arr)):
        out_idx = i - k
        in_idx  = i

        current_sum = current_sum - arr[out_idx] + arr[in_idx]
        current_indices = list(range(out_idx + 1, i + 1))
        current_window  = arr[out_idx + 1 : i + 1]

        if current_sum > max_sum:
            max_sum    = current_sum
            max_window = current_window
            max_indices = current_indices.copy()

        yield arr, current_indices, f"Window: {current_window}", current_sum, max_sum, max_indices

    yield arr, max_indices, f"Best Window Found: {max_window}", current_sum, max_sum, max_indices


# ─────────────────────────────────────────────────────────────────
#  SELF-CONTAINED JS-ANIMATED HTML  (no Streamlit rerenders)
# ─────────────────────────────────────────────────────────────────

def build_animated_sliding_window_html(arr, k, speed_seconds):
    """
    Pre-computes every animation step and returns a single HTML page
    driven entirely by JavaScript timers.  Streamlit renders this once
    and the browser handles all animation — scroll position is never reset.
    """
    steps = []
    for arr_s, highlight, status, current_sum, max_sum, best_indices in max_sum_subarray_visual(arr, k):
        steps.append({
            "arr":         list(arr_s),
            "highlight":   list(highlight),
            "best":        list(best_indices),
            "status":      status,
            "current_sum": current_sum,
            "max_sum":     max_sum,
        })

    steps_json = json.dumps(steps)
    delay_ms   = int(speed_seconds * 1000)
    total      = len(steps)

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 10px;
    background: transparent;
    font-family: 'Segoe UI', sans-serif;
    color: white;
  }}
  .box {{
    width: 62px; height: 62px;
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 800;
    transition: background 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
  }}
  #boxes-row {{
    display: flex; gap: 10px; flex-wrap: wrap;
    justify-content: center; padding: 12px 0;
  }}
  #info-panel {{
    background: rgba(15,23,42,0.85);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 18px 22px;
    margin-top: 10px;
  }}
  .metric-label {{
    color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 1px;
  }}
  .metric-value {{
    font-size: 1.4rem; font-weight: 900; margin-top: 3px;
  }}
  #progress-bar-track {{
    background: rgba(255,255,255,0.05);
    border-radius: 999px; height: 6px; overflow: hidden;
    margin-top: 14px;
  }}
  #progress-bar-fill {{
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #F59E0B, #10B981);
    transition: width 0.3s ease;
  }}
  #step-label {{
    color: #475569; font-size: 11px;
    margin-top: 5px; text-align: right;
  }}
  #done-banner {{
    display: none;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 18px;
    padding: 18px 22px; margin-top: 10px; text-align: center;
  }}
</style>
</head>
<body>

<div id="boxes-row"></div>

<div id="info-panel">
  <div style="display:flex;gap:28px;flex-wrap:wrap;margin-bottom:4px;">
    <div>
      <div class="metric-label">WINDOW</div>
      <div id="metric-window" class="metric-value" style="color:#F59E0B;font-size:1rem;">—</div>
    </div>
    <div>
      <div class="metric-label">CURRENT SUM</div>
      <div id="metric-current" class="metric-value" style="color:#F8FAFC;">—</div>
    </div>
    <div>
      <div class="metric-label">MAX SUM</div>
      <div id="metric-max" class="metric-value" style="color:#10B981;">—</div>
    </div>
  </div>
  <div id="progress-bar-track">
    <div id="progress-bar-fill" style="width:0%"></div>
  </div>
  <div id="step-label">Step 0 of {total}</div>
</div>

<div id="done-banner">
  <div style="color:#10B981;font-weight:800;font-size:1rem;margin-bottom:6px;">
    ✅ Done! Maximum sum subarray found.
  </div>
  <div id="done-detail" style="color:#94A3B8;font-size:0.95rem;"></div>
</div>

<script>
(function() {{
  var steps     = {steps_json};
  var delay     = {delay_ms};
  var total     = {total};
  var stepIndex = 0;

  var boxesRow   = document.getElementById('boxes-row');
  var winEl      = document.getElementById('metric-window');
  var curEl      = document.getElementById('metric-current');
  var maxEl      = document.getElementById('metric-max');
  var barFill    = document.getElementById('progress-bar-fill');
  var stepLabel  = document.getElementById('step-label');
  var doneBanner = document.getElementById('done-banner');
  var doneDetail = document.getElementById('done-detail');
  var infoPanel  = document.getElementById('info-panel');

  function buildBoxes(arr, highlight, best) {{
    var h  = new Set(highlight);
    var b  = new Set(best);
    var html = '';
    for (var i = 0; i < arr.length; i++) {{
      var bg, shadow, transform, border;
      if (b.has(i)) {{
        bg        = 'linear-gradient(135deg,#10B981,#059669)';
        shadow    = '0 0 14px rgba(16,185,129,0.55)';
        transform = 'scale(1.12)';
        border    = '2px solid #10B98188';
      }} else if (h.has(i)) {{
        bg        = 'linear-gradient(135deg,#F59E0B,#D97706)';
        shadow    = '0 0 14px rgba(245,158,11,0.55)';
        transform = 'scale(1.08)';
        border    = '2px solid #F59E0B88';
      }} else {{
        bg        = 'linear-gradient(145deg,#1E293B,#0F172A)';
        shadow    = 'none';
        transform = 'scale(1)';
        border    = '1px solid rgba(255,255,255,0.07)';
      }}
      html += '<div class="box" style="background:'+bg+';box-shadow:'+shadow+
              ';transform:'+transform+';border:'+border+'">'+arr[i]+'</div>';
    }}
    boxesRow.innerHTML = html;
  }}

  function tick() {{
    if (stepIndex >= steps.length) {{
      // Animation complete
      var last = steps[steps.length - 1];
      infoPanel.style.display = 'none';
      doneBanner.style.display = 'block';
      doneDetail.innerHTML =
        'Best window indices: ' + JSON.stringify(last.best) +
        ' &nbsp;|&nbsp; Max sum: <b style="color:#10B981">' + last.max_sum + '</b>';
      buildBoxes(last.arr, last.best, last.best);
      return;
    }}

    var s = steps[stepIndex];
    buildBoxes(s.arr, s.highlight, s.best);

    winEl.textContent = s.status;
    curEl.textContent = s.current_sum;
    maxEl.textContent = s.max_sum;

    var pct = Math.round(((stepIndex + 1) / total) * 100);
    barFill.style.width = pct + '%';
    stepLabel.textContent = 'Step ' + (stepIndex + 1) + ' of ' + total;

    stepIndex++;
    setTimeout(tick, delay);
  }}

  // Kick off
  setTimeout(tick, 200);
}})();
</script>
</body>
</html>"""