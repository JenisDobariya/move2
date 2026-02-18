<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Event Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@2.0.1/dist/chartjs-plugin-zoom.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8/hammer.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link
        href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap"
        rel="stylesheet">

    <style>
        :root {
            --bg: #050a14;
            --surface: #0d1626;
            --surface2: #111e35;
            --border: #1c2e4a;
            --accent: #00d4ff;
            --accent2: #7c3aed;
            --accent3: #10b981;
            --danger: #ef4444;
            --text: #e2eaf8;
            --text-muted: #8aafd4;
            --glow: 0 0 20px rgba(0, 212, 255, 0.25);
            --glow2: 0 0 20px rgba(124, 58, 237, 0.25);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'Syne', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Animated grid background */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
            z-index: 0;
        }

        /* Floating orbs */
        body::after {
            content: '';
            position: fixed;
            top: -200px;
            right: -200px;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(124, 58, 237, 0.08) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }

        .orb {
            position: fixed;
            bottom: -150px;
            left: -150px;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(0, 212, 255, 0.06) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }

        /* NAVBAR */
        nav {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(5, 10, 20, 0.85);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
            padding: 0 2rem;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .nav-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 800;
            font-size: 1.1rem;
            letter-spacing: 0.05em;
        }

        .nav-brand .dot {
            width: 10px;
            height: 10px;
            background: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {

            0%,
            100% {
                opacity: 1;
                transform: scale(1);
            }

            50% {
                opacity: 0.5;
                transform: scale(0.8);
            }
        }

        .nav-actions {
            display: flex;
            gap: 10px;
        }

        .btn {
            padding: 8px 18px;
            border-radius: 6px;
            font-family: 'Space Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            cursor: pointer;
            border: none;
            text-decoration: none;
            transition: all 0.2s;
        }

        .btn-primary {
            background: var(--accent);
            color: #000;
        }

        .btn-primary:hover {
            box-shadow: var(--glow);
            transform: translateY(-1px);
        }

        .btn-danger {
            background: transparent;
            color: var(--danger);
            border: 1px solid var(--danger);
        }

        .btn-danger:hover {
            background: var(--danger);
            color: #fff;
        }

        /* MAIN */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }

        /* HEADER */
        .page-header {
            margin-bottom: 2rem;
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .welcome-text {
            font-size: 2rem;
            font-weight: 800;
        }

        .welcome-text span {
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .live-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 6px 14px;
            border-radius: 100px;
            font-family: 'Space Mono', monospace;
            font-size: 0.7rem;
            color: var(--accent3);
            letter-spacing: 0.1em;
        }

        .live-dot {
            width: 7px;
            height: 7px;
            background: var(--accent3);
            border-radius: 50%;
            animation: pulse 1.5s infinite;
            box-shadow: 0 0 6px var(--accent3);
        }

        /* EVENT SELECTOR */
        .event-selector {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1.5rem;
            flex-wrap: wrap;
        }

        .selector-label {
            font-family: 'Space Mono', monospace;
            font-size: 0.7rem;
            color: var(--text-muted);
            letter-spacing: 0.12em;
            text-transform: uppercase;
            white-space: nowrap;
        }

        select#eventFilter {
            flex: 1;
            min-width: 200px;
            background: var(--surface2);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 10px 14px;
            border-radius: 8px;
            font-family: 'Syne', sans-serif;
            font-size: 0.9rem;
            outline: none;
            cursor: pointer;
            transition: border-color 0.2s;
        }

        select#eventFilter:focus {
            border-color: var(--accent);
        }

        /* META INFO STRIP */
        .meta-strip {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .meta-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem 1.2rem;
            position: relative;
            overflow: hidden;
            transition: border-color 0.3s, transform 0.2s;
        }

        .meta-card:hover {
            border-color: var(--accent);
            transform: translateY(-2px);
            box-shadow: var(--glow);
        }

        .meta-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 3px;
            height: 100%;
            background: linear-gradient(180deg, var(--accent), var(--accent2));
        }

        .meta-label {
            font-family: 'Space Mono', monospace;
            font-size: 0.65rem;
            color: var(--text-muted);
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }

        .meta-value {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text);
        }

        /* KPI CARDS */
        .kpi-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .kpi-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.3rem 1.5rem;
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
        }

        .kpi-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }

        .kpi-card::after {
            content: '';
            position: absolute;
            bottom: 0;
            right: 0;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            opacity: 0.08;
        }

        .kpi-card:nth-child(1)::after {
            background: var(--accent);
        }

        .kpi-card:nth-child(2)::after {
            background: var(--accent2);
        }

        .kpi-card:nth-child(3)::after {
            background: var(--accent3);
        }

        .kpi-label {
            font-family: 'Space Mono', monospace;
            font-size: 0.65rem;
            color: var(--text-muted);
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .kpi-value {
            font-size: 2.4rem;
            font-weight: 800;
            line-height: 1;
        }

        .kpi-card:nth-child(1) .kpi-value {
            color: var(--accent);
        }

        .kpi-card:nth-child(2) .kpi-value {
            color: var(--accent2);
        }

        .kpi-card:nth-child(3) .kpi-value {
            color: var(--accent3);
        }

        /* CHARTS GRID */
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .chart-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            transition: border-color 0.3s;
        }

        .chart-card:hover {
            border-color: rgba(0, 212, 255, 0.3);
        }

        .chart-header {
            padding: 1rem 1.3rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .chart-title {
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.03em;
        }

        .chart-tag {
            font-family: 'Space Mono', monospace;
            font-size: 0.6rem;
            color: var(--accent);
            background: rgba(0, 212, 255, 0.08);
            border: 1px solid rgba(0, 212, 255, 0.2);
            padding: 3px 8px;
            border-radius: 4px;
            letter-spacing: 0.08em;
        }

        .chart-body {
            padding: 1.2rem;
        }

        /* ZOOM CONTROLS */
        .zoom-controls {
            display: flex;
            gap: 6px;
        }

        .zoom-btn {
            width: 28px;
            height: 28px;
            background: var(--surface2);
            border: 1px solid var(--border);
            color: var(--text);
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }

        .zoom-btn:hover {
            background: var(--accent);
            color: #000;
            border-color: var(--accent);
        }

        /* LINE CHART FULL WIDTH */
        .line-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 2rem;
        }

        .line-card .chart-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .hint-text {
            font-family: 'Space Mono', monospace;
            font-size: 0.6rem;
            color: var(--text-muted);
            letter-spacing: 0.08em;
        }

        /* SCROLL WRAPPER */
        .scroll-wrapper {
            position: relative;
            overflow: hidden;
        }

        .chart-scroll-container {
            overflow-x: auto;
            overflow-y: hidden;
            scroll-behavior: smooth;
            padding: 1.2rem;
            padding-bottom: 0;
            cursor: grab;
        }

        .chart-scroll-container:active {
            cursor: grabbing;
        }

        .chart-scroll-container::-webkit-scrollbar {
            height: 6px;
        }

        .chart-scroll-container::-webkit-scrollbar-track {
            background: var(--surface2);
            border-radius: 10px;
        }

        .chart-scroll-container::-webkit-scrollbar-thumb {
            background: var(--accent);
            border-radius: 10px;
            opacity: 0.5;
        }

        #chartArea {
            height: 350px;
            min-width: 100%;
        }

        /* Scroll fade edges */
        .scroll-wrapper::before,
        .scroll-wrapper::after {
            content: '';
            position: absolute;
            top: 0;
            bottom: 0;
            width: 40px;
            z-index: 10;
            pointer-events: none;
        }

        .scroll-wrapper::before {
            left: 0;
            background: linear-gradient(90deg, var(--surface), transparent);
        }

        .scroll-wrapper::after {
            right: 0;
            background: linear-gradient(-90deg, var(--surface), transparent);
        }

        /* Scroll bottom bar */
        .scroll-bar {
            padding: 0.8rem 1.2rem 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .scroll-nav {
            display: flex;
            gap: 8px;
        }

        .scroll-nav button {
            background: var(--surface2);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 6px 14px;
            border-radius: 6px;
            font-family: 'Space Mono', monospace;
            font-size: 0.7rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .scroll-nav button:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        /* Emotion top list */
        .emotion-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .emotion-row {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .emotion-name {
            font-size: 0.8rem;
            min-width: 80px;
            text-transform: capitalize;
            color: var(--text);
        }

        .emotion-bar-wrap {
            flex: 1;
            height: 8px;
            background: var(--surface2);
            border-radius: 10px;
            overflow: hidden;
        }

        .emotion-bar-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.8s ease;
        }

        .emotion-count {
            font-family: 'Space Mono', monospace;
            font-size: 0.7rem;
            color: var(--text-muted);
            min-width: 30px;
            text-align: right;
        }

        /* RESPONSIVE */
        @media (max-width: 900px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }

            .meta-strip {
                grid-template-columns: repeat(2, 1fr);
            }

            .kpi-row {
                grid-template-columns: 1fr;
            }
        }

        /* FADE IN ANIMATION */
        @keyframes fadeUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .chart-card,
        .kpi-card,
        .meta-card,
        .line-card,
        .event-selector {
            animation: fadeUp 0.5s ease both;
        }
    </style>
</head>

<body>

    <div class="orb"></div>

    <nav>
        <div class="nav-brand">
            <div class="dot"></div>
            EVENT ANALYTICS PRO
        </div>
        <div class="nav-actions">
            <a href="/add-event" class="btn btn-primary">+ NEW EVENT</a>
            <a href="/logout" class="btn btn-danger">LOGOUT</a>
        </div>
    </nav>

    <div class="container">

        <div class="page-header">
            <div class="welcome-text">Welcome, <span id="userDisplay">{{ user }}</span></div>
            <div class="live-badge">
                <div class="live-dot"></div>
                LIVE · AUTO-REFRESH 5s
            </div>
        </div>

        <!-- Event Selector -->
        <div class="event-selector">
            <span class="selector-label">Active Event</span>
            <select id="eventFilter"></select>
        </div>

        <!-- Meta Strip -->
        <div class="meta-strip">
            <div class="meta-card">
                <div class="meta-label">Date</div>
                <div class="meta-value" id="eventDate">—</div>
            </div>
            <div class="meta-card">
                <div class="meta-label">Time Range</div>
                <div class="meta-value" id="eventTimeRange">—</div>
            </div>
            <div class="meta-card">
                <div class="meta-label">License Key</div>
                <div class="meta-value" id="eventLicKey" style="font-family:'Space Mono',monospace;font-size:0.75rem;">—
                </div>
            </div>
            <div class="meta-card">
                <div class="meta-label">Handler</div>
                <div class="meta-value" id="eventHandler">—</div>
            </div>
        </div>

        <!-- KPI Row -->
        <div class="kpi-row">
            <div class="kpi-card">
                <div class="kpi-label">Total Entries</div>
                <div class="kpi-value" id="kpiTotal">0</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Emotion Types</div>
                <div class="kpi-value" id="kpiEmotions">0</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Top Emotion</div>
                <div class="kpi-value" id="kpiTop" style="font-size:1.4rem;">—</div>
            </div>
        </div>

        <!-- Bar + Pie -->
        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-header">
                    <span class="chart-title">Emotion Distribution</span>
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span class="chart-tag">BAR</span>
                        <div class="zoom-controls">
                            <button class="zoom-btn" onclick="zoomChart(barChart,'in')">+</button>
                            <button class="zoom-btn" onclick="zoomChart(barChart,'out')">−</button>
                            <button class="zoom-btn" onclick="resetChart(barChart)" title="Reset">⟳</button>
                        </div>
                    </div>
                </div>
                <div class="chart-body">
                    <canvas id="barChart" height="220"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <div class="chart-header">
                    <span class="chart-title">Emotion Breakdown</span>
                    <span class="chart-tag">PIE</span>
                </div>
                <div class="chart-body">
                    <div style="display:flex;gap:1.5rem;align-items:flex-start;">
                        <div style="flex:1;max-width:200px;">
                            <canvas id="pieChart"></canvas>
                        </div>
                        <div class="emotion-list" id="emotionList" style="flex:1;margin-top:8px;"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Line Chart -->
        <div class="line-card">
            <div class="chart-header">
                <div>
                    <span class="chart-title">Emotion Frequency Trends</span>
                    <div class="hint-text" style="margin-top:4px;">SCROLL → drag · ZOOM → pinch / wheel · RESET →
                        double-click</div>
                </div>
                <div style="display:flex;align-items:center;gap:10px;">
                    <span class="chart-tag">TIMELINE</span>
                    <div class="zoom-controls">
                        <button class="zoom-btn" onclick="zoomChart(lineChart,'in')">+</button>
                        <button class="zoom-btn" onclick="zoomChart(lineChart,'out')">−</button>
                        <button class="zoom-btn" onclick="resetChart(lineChart)">⟳</button>
                    </div>
                </div>
            </div>
            <div class="scroll-wrapper">
                <div class="chart-scroll-container" id="scrollContainer">
                    <div id="chartArea">
                        <canvas id="lineChart"></canvas>
                    </div>
                </div>
            </div>
            <div class="scroll-bar">
                <div class="scroll-nav">
                    <button onclick="scrollChart(-300)">← PREV</button>
                    <button onclick="scrollChart(300)">NEXT →</button>
                    <button onclick="scrollToEnd()">END ↦</button>
                </div>
                <div class="hint-text">DRAG TO SCROLL</div>
            </div>
        </div>

    </div>

    <script>
        let barChart, pieChart, lineChart;
        let eventMap = {};
        let currentDataLength = 0;

        const PALETTE = [
            '#00d4ff', '#7c3aed', '#10b981', '#f59e0b',
            '#ef4444', '#ec4899', '#14b8a6', '#a78bfa'
        ];

        /* ---- Drag-to-scroll ---- */
        const scrollContainer = document.getElementById('scrollContainer');
        let isDragging = false, startX, scrollLeft;

        scrollContainer.addEventListener('mousedown', e => {
            isDragging = true;
            startX = e.pageX - scrollContainer.offsetLeft;
            scrollLeft = scrollContainer.scrollLeft;
        });
        scrollContainer.addEventListener('mouseleave', () => isDragging = false);
        scrollContainer.addEventListener('mouseup', () => isDragging = false);
        scrollContainer.addEventListener('mousemove', e => {
            if (!isDragging) return;
            e.preventDefault();
            const x = e.pageX - scrollContainer.offsetLeft;
            scrollContainer.scrollLeft = scrollLeft - (x - startX) * 1.5;
        });

        /* ---- Scroll helpers ---- */
        function scrollChart(px) {
            scrollContainer.scrollBy({ left: px, behavior: 'smooth' });
        }
        function scrollToEnd() {
            scrollContainer.scrollTo({ left: scrollContainer.scrollWidth, behavior: 'smooth' });
        }

        /* ---- Zoom helpers ---- */
        function zoomChart(chart, dir) {
            if (!chart) return;
            if (dir === 'in') chart.zoom(1.3);
            else chart.zoom(0.7);
        }
        function resetChart(chart) {
            if (!chart) return;
            chart.resetZoom();
        }

        /* ---- Fetch ---- */
        async function fetchData() {
            const res = await fetch('/api/data');
            return await res.json();
        }

        /* ---- Analytics ---- */
        function getAnalytics(eventData) {
            const emotionCount = {};
            const timeGroups = {};
            if (!eventData?.data) return { emotionCount, timeGroups, total: 0 };

            const entries = Object.values(eventData.data)
                .filter(e => e.time_stamp && e.emotion)
                .map(e => {
                    let ts = Number(e.time_stamp);
                    if (!ts || isNaN(ts)) return null;
                    if (ts < 10000000000) ts *= 1000;
                    return { emotion: e.emotion.toLowerCase(), timestamp: ts };
                })
                .filter(Boolean)
                .sort((a, b) => a.timestamp - b.timestamp);

            entries.forEach(entry => {
                emotionCount[entry.emotion] = (emotionCount[entry.emotion] || 0) + 1;
                if (!timeGroups[entry.timestamp]) timeGroups[entry.timestamp] = {};
                timeGroups[entry.timestamp][entry.emotion] =
                    (timeGroups[entry.timestamp][entry.emotion] || 0) + 1;
            });

            return { emotionCount, timeGroups, total: entries.length };
        }

        /* ---- Chart init ---- */
        function initCharts(labels, values, timeGroups) {
            const barCtx = document.getElementById('barChart');
            const pieCtx = document.getElementById('pieChart');
            const lineCtx = document.getElementById('lineChart');

            barChart = new Chart(barCtx, {
                type: 'bar',
                data: {
                    labels,
                    datasets: [{
                        label: 'Occurrences',
                        data: values,
                        backgroundColor: PALETTE.slice(0, labels.length),
                        borderRadius: 6,
                        borderSkipped: false
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        zoom: {
                            zoom: {
                                wheel: { enabled: true },
                                pinch: { enabled: true },
                                mode: 'xy'
                            },
                            pan: { enabled: true, mode: 'xy' }
                        }
                    },
                    scales: {
                        x: {
                            grid: { color: 'rgba(255,255,255,0.06)' },
                            ticks: { color: '#c8d8f0', font: { family: 'Space Mono', size: 10 } }
                        },
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255,255,255,0.06)' },
                            ticks: { color: '#c8d8f0', font: { family: 'Space Mono', size: 10 }, stepSize: 1 }
                        }
                    }
                }
            });

            pieChart = new Chart(pieCtx, {
                type: 'doughnut',
                data: {
                    labels,
                    datasets: [{
                        data: values,
                        backgroundColor: PALETTE.slice(0, labels.length),
                        borderWidth: 2,
                        borderColor: '#0d1626',
                        hoverOffset: 8
                    }]
                },
                options: {
                    responsive: true,
                    cutout: '70%',
                    plugins: {
                        legend: { display: false }
                    }
                }
            });

            createLineChart(timeGroups);
        }

        function createLineChart(timeGroups) {
            const lineCtx = document.getElementById('lineChart');
            const timeKeys = Object.keys(timeGroups);

            const formattedLabels = timeKeys.map(t =>
                new Date(Number(t)).toLocaleTimeString([], {
                    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
                })
            );

            const emotions = [...new Set(
                Object.values(timeGroups).flatMap(obj => Object.keys(obj))
            )];

            const width = Math.max(
                scrollContainer.clientWidth,
                Math.min(timeKeys.length * 45, 5000)
            );
            document.getElementById('chartArea').style.width = width + 'px';

            lineChart = new Chart(lineCtx, {
                type: 'line',
                data: {
                    labels: formattedLabels,
                    datasets: emotions.map((emo, i) => ({
                        label: emo.charAt(0).toUpperCase() + emo.slice(1),
                        data: timeKeys.map(t => timeGroups[t][emo] || 0),
                        borderColor: PALETTE[i % PALETTE.length],
                        backgroundColor: PALETTE[i % PALETTE.length] + '18',
                        tension: 0.4,
                        pointRadius: 4,
                        pointHoverRadius: 7,
                        fill: true,
                        borderWidth: 2
                    }))
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: '#e2eaf8',
                                font: { family: 'Space Mono', size: 10 },
                                boxWidth: 12,
                                padding: 16
                            }
                        },
                        zoom: {
                            zoom: {
                                wheel: { enabled: true },
                                pinch: { enabled: true },
                                mode: 'x'
                            },
                            pan: { enabled: true, mode: 'x' }
                        }
                    },
                    scales: {
                        x: {
                            grid: { color: 'rgba(255,255,255,0.06)' },
                            ticks: { color: '#c8d8f0', font: { family: 'Space Mono', size: 10 }, maxRotation: 45 }
                        },
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255,255,255,0.06)' },
                            ticks: { color: '#c8d8f0', font: { family: 'Space Mono', size: 11 }, stepSize: 1 }
                        }
                    }
                }
            });

            scrollContainer.scrollTo({ left: scrollContainer.scrollWidth, behavior: 'smooth' });
        }

        /* ---- Update charts ---- */
        function updateCharts(labels, values, timeGroups) {
            barChart.data.labels = labels;
            barChart.data.datasets[0].data = values;
            barChart.data.datasets[0].backgroundColor = PALETTE.slice(0, labels.length);
            barChart.update('none');

            pieChart.data.labels = labels;
            pieChart.data.datasets[0].data = values;
            pieChart.data.datasets[0].backgroundColor = PALETTE.slice(0, labels.length);
            pieChart.update('none');

            lineChart.destroy();
            createLineChart(timeGroups);
        }

        /* ---- Emotion List (sidebar) ---- */
        function renderEmotionList(emotionCount) {
            const list = document.getElementById('emotionList');
            const max = Math.max(...Object.values(emotionCount));
            list.innerHTML = '';
            Object.entries(emotionCount)
                .sort(([, a], [, b]) => b - a)
                .forEach(([emo, count], i) => {
                    const pct = Math.round((count / max) * 100);
                    list.innerHTML += `
                    <div class="emotion-row">
                        <span class="emotion-name">${emo}</span>
                        <div class="emotion-bar-wrap">
                            <div class="emotion-bar-fill" style="width:${pct}%;background:${PALETTE[i % PALETTE.length]}"></div>
                        </div>
                        <span class="emotion-count">${count}</span>
                    </div>`;
                });
        }

        /* ---- Load dashboard ---- */
        async function loadDashboard() {
            const firebaseData = await fetchData();
            const events = firebaseData.Events || {};
            eventMap = events;

            const filter = document.getElementById('eventFilter');
            const prev = filter.value;
            filter.innerHTML = '';
            Object.entries(eventMap).forEach(([key, ev]) => {
                const opt = document.createElement('option');
                opt.value = key;
                opt.text = ev.event_name || key;
                filter.appendChild(opt);
            });
            filter.value = prev || Object.keys(eventMap)[0];
            if (filter.value) updateDashboardForEvent(filter.value);
        }

        /* ---- Update event view ---- */
        function updateDashboardForEvent(licKey) {
            const event = eventMap[licKey];
            if (!event) return;

            document.getElementById('eventDate').innerText = event.event_date || '—';
            // document.getElementById('eventTimeRange').innerText =
            //     (event.start_time || '??') + ' → ' + (event.end_time || '??');

            // 2. Update Time Range (Start - End)
            const start = event.event_start_time_ || "??:??";
            const end = event.event_end_time_to || "??:??";
            document.getElementById("eventTimeRange").innerText = `${start} to ${end}`;

            document.getElementById('eventLicKey').innerText = licKey;
            document.getElementById('eventHandler').innerText = event.handling_person_name || '—';

            const { emotionCount, timeGroups, total } = getAnalytics(event);

            // KPIs
            document.getElementById('kpiTotal').innerText = total;
            const labels = Object.keys(emotionCount);
            document.getElementById('kpiEmotions').innerText = labels.length;
            const topEmo = labels.sort((a, b) => emotionCount[b] - emotionCount[a])[0] || '—';
            document.getElementById('kpiTop').innerText = topEmo.charAt(0).toUpperCase() + topEmo.slice(1);

            const values = labels.map(l => emotionCount[l]);
            renderEmotionList(emotionCount);

            if (total === currentDataLength) return;
            currentDataLength = total;

            if (!barChart) initCharts(labels, values, timeGroups);
            else updateCharts(labels, values, timeGroups);
        }

        document.getElementById('eventFilter').addEventListener('change',
            e => updateDashboardForEvent(e.target.value));

        loadDashboard();
        setInterval(loadDashboard, 5000);
    </script>
</body>

</html> 