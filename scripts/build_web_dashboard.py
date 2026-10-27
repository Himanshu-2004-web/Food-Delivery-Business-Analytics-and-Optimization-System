"""
Script to build standalone, ultra-polished, animated dashboard.html
Zero dependencies, zero Streamlit, works out of the box with double-click.
Font sizes increased for high readability during presentations and viva voce.
"""

import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'cleaned_food_orders.csv')
OUTPUT_HTML = os.path.join(BASE_DIR, 'dashboard.html')

df = pd.read_csv(DATA_FILE)

# Extract records as JSON array (replacing NaN with None/null)
records = df.where(pd.notnull(df), None).to_dict(orient='records')
orders_json = json.dumps(records)

html_content = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Food Delivery Business Analytics & Optimization System</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    }},
                    colors: {{
                        brand: {{
                            50: '#EEF2FF',
                            100: '#E0E7FF',
                            500: '#6366F1',
                            600: '#4F46E5',
                            700: '#4338CA',
                            900: '#1E1B4B',
                        }}
                    }}
                }}
            }}
        }}
    </script>

    <style>
        body {{
            font-size: 15px;
        }}
        .glass-nav {{
            background: rgba(15, 23, 42, 0.90);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .glass-card {{
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 28px -4px rgba(0, 0, 0, 0.08);
            border-color: #CBD5E1;
        }}
        .tab-btn {{
            position: relative;
            transition: all 0.25s ease-in-out;
        }}
        .tab-btn.active {{
            color: #FFFFFF;
            background: rgba(99, 102, 241, 0.28);
            border-color: #818CF8;
        }}
        .tab-btn.active::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 15%;
            right: 15%;
            height: 2.5px;
            background: #818CF8;
            border-radius: 9999px;
            box-shadow: 0 0 14px #818CF8;
        }}
        .fade-in {{
            animation: fadeIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: #F1F5F9;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #CBD5E1;
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #94A3B8;
        }}
    </style>
</head>
<body class="bg-[#F8FAFC] text-slate-800 antialiased selection:bg-indigo-500 selection:text-white min-h-screen flex flex-col">

    <!-- Top Sticky Glassmorphism Navigation Bar -->
    <header class="glass-nav sticky top-0 z-50 text-white shadow-lg shadow-slate-900/10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-20">
                
                <!-- Logo & Brand Info -->
                <div class="flex items-center space-x-3.5">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-amber-400 flex items-center justify-center shadow-lg shadow-indigo-500/25">
                        <span class="text-2xl">🍔</span>
                    </div>
                    <div>
                        <div class="flex items-center space-x-2.5">
                            <span class="font-extrabold text-lg sm:text-xl tracking-tight text-white">FoodFlow Analytics</span>
                            <span class="bg-indigo-500/25 text-indigo-300 border border-indigo-400/40 text-xs font-semibold px-2.5 py-0.5 rounded-full uppercase tracking-wider">Enterprise UI</span>
                        </div>
                        <p class="text-xs sm:text-sm text-slate-300 hidden sm:block">Food Delivery Performance & Optimization System</p>
                    </div>
                </div>

                <!-- Smooth 4-Tab Navigation -->
                <nav class="flex items-center space-x-1.5 sm:space-x-2 bg-slate-900/70 p-1.5 rounded-xl border border-slate-700/60">
                    <button onclick="switchTab('executive')" id="tab-btn-executive" class="tab-btn active px-4 py-2 rounded-lg text-sm sm:text-base font-semibold text-slate-200 hover:text-white transition flex items-center space-x-2">
                        <span class="text-base">📊</span>
                        <span class="hidden md:inline">Executive Dashboard</span>
                        <span class="md:hidden">Overview</span>
                    </button>
                    <button onclick="switchTab('diagnostic')" id="tab-btn-diagnostic" class="tab-btn px-4 py-2 rounded-lg text-sm sm:text-base font-semibold text-slate-300 hover:text-white transition flex items-center space-x-2">
                        <span class="text-base">🔍</span>
                        <span class="hidden md:inline">Diagnostic Analytics</span>
                        <span class="md:hidden">Diagnostics</span>
                    </button>
                    <button onclick="switchTab('predictive')" id="tab-btn-predictive" class="tab-btn px-4 py-2 rounded-lg text-sm sm:text-base font-semibold text-slate-300 hover:text-white transition flex items-center space-x-2">
                        <span class="text-base">📈</span>
                        <span class="hidden md:inline">Predictive Forecast</span>
                        <span class="md:hidden">Forecast</span>
                    </button>
                    <button onclick="switchTab('prescriptive')" id="tab-btn-prescriptive" class="tab-btn px-4 py-2 rounded-lg text-sm sm:text-base font-semibold text-slate-300 hover:text-white transition flex items-center space-x-2">
                        <span class="text-base">🎯</span>
                        <span class="hidden md:inline">Prescriptive Strategy</span>
                        <span class="md:hidden">Strategy</span>
                    </button>
                </nav>

                <!-- Status Indicator -->
                <div class="hidden lg:flex items-center space-x-2.5 text-sm text-slate-300 bg-slate-800/90 px-3.5 py-2 rounded-xl border border-slate-700">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="font-mono text-emerald-300 font-semibold" id="live-dataset-size">2,000 Orders</span>
                </div>

            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1 space-y-8">

        <!-- ========================================================================= -->
        <!-- PREMIUM ANALYTICS CONTROL BAR (FILTERS) -->
        <!-- ========================================================================= -->
        <section class="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-sm relative overflow-hidden">
            <div class="absolute -right-16 -top-16 w-56 h-56 bg-indigo-50 rounded-full blur-2xl pointer-events-none"></div>

            <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-5">
                
                <!-- Filter Title & Active Count Badge -->
                <div class="flex items-center space-x-3.5">
                    <div class="w-10 h-10 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 font-bold text-lg">
                        ⚡
                    </div>
                    <div>
                        <h2 class="text-base sm:text-lg font-bold text-slate-900 tracking-tight flex items-center space-x-2.5">
                            <span>Interactive Analytics Controls</span>
                            <span id="filtered-badge" class="bg-indigo-100 text-indigo-800 text-xs sm:text-sm font-semibold px-3 py-1 rounded-full transition">Showing 2,000 orders</span>
                        </h2>
                        <p class="text-xs sm:text-sm text-slate-500 mt-0.5">Live multi-dimensional filters with instant reactive computation</p>
                    </div>
                </div>

                <!-- Controls Layout: City, Cuisine, Status, Reset -->
                <div class="flex flex-wrap items-center gap-4">
                    
                    <!-- City Dropdown -->
                    <div class="relative">
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">City</label>
                        <select id="filter-city" onchange="applyFilters()" class="text-sm font-medium bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none text-slate-800 cursor-pointer hover:bg-slate-100 transition shadow-sm">
                            <option value="ALL">All Cities (5 Hubs)</option>
                            <option value="Bangalore">Bangalore</option>
                            <option value="Mumbai">Mumbai</option>
                            <option value="Delhi NCR">Delhi NCR</option>
                            <option value="Hyderabad">Hyderabad</option>
                            <option value="Pune">Pune</option>
                        </select>
                    </div>

                    <!-- Cuisine Dropdown -->
                    <div class="relative">
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Cuisine Category</label>
                        <select id="filter-cuisine" onchange="applyFilters()" class="text-sm font-medium bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none text-slate-800 cursor-pointer hover:bg-slate-100 transition shadow-sm">
                            <option value="ALL">All Cuisines (7 Types)</option>
                            <option value="North Indian">North Indian</option>
                            <option value="Biryani">Biryani</option>
                            <option value="Fast Food">Fast Food</option>
                            <option value="South Indian">South Indian</option>
                            <option value="Desserts">Desserts</option>
                            <option value="Chinese">Chinese</option>
                            <option value="Italian">Italian</option>
                        </select>
                    </div>

                    <!-- Order Status -->
                    <div class="relative">
                        <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5">Order Status</label>
                        <select id="filter-status" onchange="applyFilters()" class="text-sm font-medium bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none text-slate-800 cursor-pointer hover:bg-slate-100 transition shadow-sm">
                            <option value="ALL">All Statuses</option>
                            <option value="Delivered">Delivered Only</option>
                            <option value="Cancelled">Cancelled Only</option>
                            <option value="Returned">Returned Only</option>
                        </select>
                    </div>

                    <!-- Reset Button -->
                    <div class="pt-5">
                        <button onclick="resetFilters()" class="px-4 py-2 text-sm font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition flex items-center space-x-2 border border-slate-200 shadow-sm active:scale-95">
                            <span>🔄</span>
                            <span>Reset Filters</span>
                        </button>
                    </div>

                </div>

            </div>
        </section>

        <!-- ========================================================================= -->
        <!-- TAB 1: EXECUTIVE DASHBOARD (DESCRIPTIVE ANALYTICS) -->
        <!-- ========================================================================= -->
        <div id="tab-content-executive" class="tab-pane fade-in space-y-8">
            
            <!-- 6 KPI Summary Cards -->
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                
                <!-- KPI 1 -->
                <div class="glass-card p-5 rounded-2xl relative overflow-hidden">
                    <div class="flex items-center justify-between text-slate-500 text-sm mb-1.5">
                        <span class="font-bold uppercase tracking-wider text-xs">Total Orders</span>
                        <span class="text-base">📦</span>
                    </div>
                    <p id="kpi-orders" class="text-3xl font-extrabold text-slate-900 tracking-tight">2,000</p>
                    <p class="text-xs sm:text-sm text-slate-500 mt-1 font-medium">Orders Analyzed</p>
                </div>

                <!-- KPI 2 -->
                <div class="glass-card p-5 rounded-2xl relative overflow-hidden">
                    <div class="flex items-center justify-between text-slate-500 text-sm mb-1.5">
                        <span class="font-bold uppercase tracking-wider text-xs">Delivered Orders</span>
                        <span class="text-base">✅</span>
                    </div>
                    <p id="kpi-delivered" class="text-3xl font-extrabold text-emerald-600 tracking-tight">1,881</p>
                    <p id="kpi-fulfillment-rate" class="text-xs sm:text-sm font-semibold text-emerald-600 mt-1">94.05% Fulfilled</p>
                </div>

                <!-- KPI 3 -->
                <div class="glass-card p-5 rounded-2xl relative overflow-hidden">
                    <div class="flex items-center justify-between text-slate-500 text-sm mb-1.5">
                        <span class="font-bold uppercase tracking-wider text-xs">Cancellation Rate</span>
                        <span class="text-base">⚠️</span>
                    </div>
                    <p id="kpi-cancellation" class="text-3xl font-extrabold text-rose-500 tracking-tight">4.90%</p>
                    <p id="kpi-cancelled-count" class="text-xs sm:text-sm text-slate-500 mt-1 font-medium">98 Cancelled</p>
                </div>

                <!-- KPI 4 -->
                <div class="glass-card p-5 rounded-2xl relative overflow-hidden">
                    <div class="flex items-center justify-between text-slate-500 text-sm mb-1.5">
                        <span class="font-bold uppercase tracking-wider text-xs">Gross Sales (GMV)</span>
                        <span class="text-base">💳</span>
                    </div>
                    <p id="kpi-gmv" class="text-3xl font-extrabold text-slate-900 tracking-tight">₹12.41 L</p>
                    <p class="text-xs sm:text-sm text-slate-500 mt-1 font-medium">Gross Customer Spend</p>
                </div>

                <!-- KPI 5 -->
                <div class="glass-card p-5 rounded-2xl relative overflow-hidden border-indigo-200 bg-indigo-50/25">
                    <div class="flex items-center justify-between text-indigo-500 text-sm mb-1.5">
                        <span class="font-bold uppercase tracking-wider text-xs text-indigo-900">Platform Revenue</span>
                        <span class="text-base">💰</span>
                    </div>
                    <p id="kpi-revenue" class="text-3xl font-extrabold text-indigo-600 tracking-tight">₹2.59 L</p>
                    <p id="kpi-take-rate" class="text-xs sm:text-sm font-semibold text-indigo-600 mt-1">Take Rate: 20.90%</p>
                </div>

                <!-- KPI 6 -->
                <div class="glass-card p-5 rounded-2xl relative overflow-hidden">
                    <div class="flex items-center justify-between text-slate-500 text-sm mb-1.5">
                        <span class="font-bold uppercase tracking-wider text-xs">Avg Delivery Time</span>
                        <span class="text-base">⏱️</span>
                    </div>
                    <p id="kpi-avg-time" class="text-3xl font-extrabold text-amber-600 tracking-tight">35.2m</p>
                    <p id="kpi-rating" class="text-xs sm:text-sm font-bold text-slate-700 mt-1">Rating: 3.65 / 5.0★</p>
                </div>

            </div>

            <!-- Descriptive Charts Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                
                <!-- Monthly Trend Chart -->
                <div class="glass-card p-6 rounded-2xl">
                    <div class="flex items-center justify-between mb-5">
                        <div>
                            <h3 class="text-base sm:text-lg font-bold text-slate-900">Monthly Orders & Platform Revenue Trend</h3>
                            <p class="text-xs sm:text-sm text-slate-500 mt-0.5">Dual-axis time series tracking seasonal volume and revenue growth</p>
                        </div>
                        <span class="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded-lg uppercase">FY 2025</span>
                    </div>
                    <div class="h-72 sm:h-80">
                        <canvas id="chart-monthly-trend"></canvas>
                    </div>
                </div>

                <!-- City Revenue Benchmark -->
                <div class="glass-card p-6 rounded-2xl">
                    <div class="flex items-center justify-between mb-5">
                        <div>
                            <h3 class="text-base sm:text-lg font-bold text-slate-900">City Performance & Market Share</h3>
                            <p class="text-xs sm:text-sm text-slate-500 mt-0.5">Net platform revenue generated across 5 primary operating hubs</p>
                        </div>
                        <span class="px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-bold rounded-lg uppercase">Top Metros</span>
                    </div>
                    <div class="h-72 sm:h-80">
                        <canvas id="chart-city-perf"></canvas>
                    </div>
                </div>

            </div>

            <!-- Cuisine Breakdown Grid -->
            <div class="glass-card p-6 rounded-2xl">
                <div class="flex items-center justify-between mb-5">
                    <div>
                        <h3 class="text-base sm:text-lg font-bold text-slate-900">Cuisine Category Performance & Average Order Value (AOV)</h3>
                        <p class="text-xs sm:text-sm text-slate-500 mt-0.5">Gross revenue share and order value density across culinary categories</p>
                    </div>
                </div>
                <div class="h-64 sm:h-72">
                    <canvas id="chart-cuisine-perf"></canvas>
                </div>
            </div>

        </div>

        <!-- ========================================================================= -->
        <!-- TAB 2: DIAGNOSTIC ANALYTICS -->
        <!-- ========================================================================= -->
        <div id="tab-content-diagnostic" class="tab-pane hidden fade-in space-y-8">
            
            <div class="bg-indigo-950 text-white p-6 sm:p-7 rounded-2xl relative overflow-hidden shadow-sm border border-indigo-900">
                <div class="relative z-10 max-w-3xl">
                    <span class="bg-indigo-800 text-indigo-200 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Root-Cause Analysis</span>
                    <h3 class="text-xl sm:text-2xl font-bold mt-2.5">Diagnostic Analytics: Investigating Delivery Friction & Dissatisfaction</h3>
                    <p class="text-sm sm:text-base text-indigo-200 mt-1.5 leading-relaxed">
                        Evaluates underlying drivers of late deliveries, customer rating collapse, and cancellation friction without falsely assuming correlation represents sole causation.
                    </p>
                </div>
                <div class="absolute right-0 bottom-0 text-8xl opacity-10 font-bold select-none">DIAGNOSTIC</div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                
                <!-- Diagnostic 1: Speed vs Rating -->
                <div class="glass-card p-6 rounded-2xl">
                    <div class="flex items-center justify-between mb-2">
                        <h4 class="text-base sm:text-lg font-bold text-slate-900">1. Delivery Speed Bracket vs Customer Rating</h4>
                        <span class="text-sm font-mono bg-rose-50 text-rose-600 font-bold px-2.5 py-1 rounded border border-rose-200">r = -0.424</span>
                    </div>
                    <p class="text-sm text-slate-600 mb-5 leading-relaxed">
                        Clear degradation pattern: Orders exceeding 45 minutes experience a massive jump in 1-2 star reviews (54.8% dissatisfied vs 9.7% for &lt; 30m deliveries).
                    </p>
                    <div class="h-72">
                        <canvas id="chart-diag-speed"></canvas>
                    </div>
                </div>

                <!-- Diagnostic 2: Distance vs Outcome -->
                <div class="glass-card p-6 rounded-2xl">
                    <div class="flex items-center justify-between mb-2">
                        <h4 class="text-base sm:text-lg font-bold text-slate-900">2. Delivery Distance vs Transit Time & Rating</h4>
                        <span class="text-sm font-mono bg-amber-50 text-amber-600 font-bold px-2.5 py-1 rounded border border-amber-200">10 km Barrier</span>
                    </div>
                    <p class="text-sm text-slate-600 mb-5 leading-relaxed">
                        Deliveries beyond 10 km take an average of 60.6 mins and collapse average customer satisfaction to 2.08 stars.
                    </p>
                    <div class="h-72">
                        <canvas id="chart-diag-distance"></canvas>
                    </div>
                </div>

            </div>

            <!-- Diagnostic 3: Hourly Congestion Breakdown -->
            <div class="glass-card p-6 rounded-2xl">
                <div class="flex items-center justify-between mb-5">
                    <div>
                        <h4 class="text-base sm:text-lg font-bold text-slate-900">3. Peak Congestion Window Analysis</h4>
                        <p class="text-sm text-slate-500 mt-0.5">Late delivery percentage by time-of-day operational windows</p>
                    </div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
                    
                    <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
                        <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Breakfast / Morning</p>
                        <p class="text-2xl font-bold text-slate-800 mt-1.5">32.6m avg</p>
                        <p class="text-sm text-emerald-600 font-semibold mt-1">7.4% late rate</p>
                    </div>

                    <div class="p-4 rounded-xl bg-amber-50 border border-amber-200">
                        <p class="text-xs font-bold text-amber-800 uppercase tracking-wider">Lunch Peak (12-2 PM)</p>
                        <p class="text-2xl font-bold text-amber-950 mt-1.5">37.0m avg</p>
                        <p class="text-sm text-amber-800 font-bold mt-1">15.5% late rate ⚠️</p>
                    </div>

                    <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
                        <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Evening Snacks</p>
                        <p class="text-2xl font-bold text-slate-800 mt-1.5">32.5m avg</p>
                        <p class="text-sm text-emerald-600 font-semibold mt-1">3.6% late rate</p>
                    </div>

                    <div class="p-4 rounded-xl bg-rose-50 border border-rose-200">
                        <p class="text-xs font-bold text-rose-800 uppercase tracking-wider">Dinner Peak (7-9 PM)</p>
                        <p class="text-2xl font-bold text-rose-950 mt-1.5">36.9m avg</p>
                        <p class="text-sm text-rose-800 font-bold mt-1">16.1% late rate 🚨</p>
                    </div>

                    <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
                        <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Late Night / Off-Peak</p>
                        <p class="text-2xl font-bold text-slate-800 mt-1.5">33.4m avg</p>
                        <p class="text-sm text-emerald-600 font-semibold mt-1">6.5% late rate</p>
                    </div>

                </div>
            </div>

        </div>

        <!-- ========================================================================= -->
        <!-- TAB 3: PREDICTIVE ANALYTICS -->
        <!-- ========================================================================= -->
        <div id="tab-content-predictive" class="tab-pane hidden fade-in space-y-8">
            
            <div class="bg-gradient-to-r from-blue-950 via-indigo-950 to-slate-900 text-white p-6 sm:p-7 rounded-2xl relative overflow-hidden shadow-sm border border-blue-900">
                <div class="relative z-10 max-w-3xl">
                    <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Demand Forecasting</span>
                    <h3 class="text-xl sm:text-2xl font-bold mt-2.5">Predictive Analytics: 3-Month Moving Average Demand Forecast</h3>
                    <p class="text-sm sm:text-base text-blue-200 mt-1.5 leading-relaxed">
                        University syllabus baseline moving average demand model for operational capacity planning and driver fleet scheduling.
                    </p>
                </div>
            </div>

            <!-- Forecast KPI Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
                
                <div class="glass-card p-6 rounded-2xl border-indigo-200 bg-indigo-50/20">
                    <span class="text-xs font-bold text-indigo-700 uppercase tracking-wider">Baseline Model</span>
                    <p class="text-2xl font-extrabold text-slate-900 mt-2">3-Month Moving Average</p>
                    <p class="text-sm text-slate-500 mt-1">Window k = 3 historical periods</p>
                </div>

                <div class="glass-card p-6 rounded-2xl border-emerald-200 bg-emerald-50/20">
                    <span class="text-xs font-bold text-emerald-700 uppercase tracking-wider">Model Accuracy</span>
                    <p class="text-2xl font-extrabold text-emerald-700 mt-2">MAPE: 8.36%</p>
                    <p class="text-sm text-emerald-600 mt-1 font-medium">MAE: 12.89 orders (Industry standard &lt; 10%)</p>
                </div>

                <div class="glass-card p-6 rounded-2xl border-amber-200 bg-amber-50/20">
                    <span class="text-xs font-bold text-amber-700 uppercase tracking-wider">Next Period Projection</span>
                    <p class="text-2xl font-extrabold text-amber-700 mt-2">174.3 Orders</p>
                    <p class="text-sm text-slate-500 mt-1">Target fleet capacity for Month 13</p>
                </div>

            </div>

            <!-- Forecast Comparison Chart -->
            <div class="glass-card p-6 rounded-2xl">
                <div class="flex items-center justify-between mb-5">
                    <div>
                        <h4 class="text-base sm:text-lg font-bold text-slate-900">Actual Monthly Demand vs Moving Average Forecast</h4>
                        <p class="text-sm text-slate-500 mt-0.5">Evaluation across 12 monthly operational periods (2025)</p>
                    </div>
                </div>
                <div class="h-80 sm:h-96">
                    <canvas id="chart-predictive"></canvas>
                </div>
            </div>

        </div>

        <!-- ========================================================================= -->
        <!-- TAB 4: PRESCRIPTIVE STRATEGY RECOMMENDATIONS -->
        <!-- ========================================================================= -->
        <div id="tab-content-prescriptive" class="tab-pane hidden fade-in space-y-8">
            
            <div class="bg-gradient-to-r from-emerald-950 via-teal-950 to-slate-900 text-white p-6 sm:p-7 rounded-2xl relative overflow-hidden shadow-sm border border-emerald-900">
                <div class="relative z-10 max-w-3xl">
                    <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Decision Support System</span>
                    <h3 class="text-xl sm:text-2xl font-bold mt-2.5">Prescriptive Analytics: Evidence-Based Business Actions</h3>
                    <p class="text-sm sm:text-base text-emerald-200 mt-1.5 leading-relaxed">
                        Data-driven operational interventions to eliminate delivery latency, protect platform commission margins, and reduce customer churn.
                    </p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                
                <!-- Rule 1 -->
                <div class="glass-card p-6 rounded-2xl border-t-4 border-t-indigo-600 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center space-x-2.5 text-indigo-700 font-bold text-base mb-3">
                            <span class="text-lg">⚡</span> <span>1. Dynamic Fleet Surge</span>
                        </div>
                        <div class="space-y-3 text-sm">
                            <div class="p-3 bg-slate-50 rounded-xl text-slate-700 leading-relaxed border border-slate-100">
                                <span class="font-bold text-slate-900">Trigger:</span> Dinner peak (19:00 - 21:30) experiences a 16.1% late delivery rate in Bangalore & Mumbai.
                            </div>
                            <div class="p-3 bg-indigo-50 rounded-xl text-indigo-950 font-medium leading-relaxed border border-indigo-100">
                                <span class="font-bold text-indigo-950">Action:</span> Deploy a 20%-25% delivery rider surge bonus to increase active driver density during evening peak hours.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Rule 2 -->
                <div class="glass-card p-6 rounded-2xl border-t-4 border-t-amber-500 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center space-x-2.5 text-amber-700 font-bold text-base mb-3">
                            <span class="text-lg">📍</span> <span>2. Distance Radius Throttling</span>
                        </div>
                        <div class="space-y-3 text-sm">
                            <div class="p-3 bg-slate-50 rounded-xl text-slate-700 leading-relaxed border border-slate-100">
                                <span class="font-bold text-slate-900">Trigger:</span> Deliveries &gt; 10 km take 60.6 mins on average and crash customer ratings to 2.08 stars.
                            </div>
                            <div class="p-3 bg-amber-50 rounded-xl text-amber-950 font-medium leading-relaxed border border-amber-100">
                                <span class="font-bold text-amber-950">Action:</span> Throttle standard delivery radius to 8 km during monsoons and peak traffic; charge ₹15/km surcharge for long routes.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Rule 3 -->
                <div class="glass-card p-6 rounded-2xl border-t-4 border-t-rose-500 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center space-x-2.5 text-rose-700 font-bold text-base mb-3">
                            <span class="text-lg">🍳</span> <span>3. Kitchen Prep SLA</span>
                        </div>
                        <div class="space-y-3 text-sm">
                            <div class="p-3 bg-slate-50 rounded-xl text-slate-700 leading-relaxed border border-slate-100">
                                <span class="font-bold text-slate-900">Trigger:</span> Over 50% of delay time at high-volume Biryani & Italian partners originates from kitchen prep delays.
                            </div>
                            <div class="p-3 bg-rose-50 rounded-xl text-rose-950 font-medium leading-relaxed border border-rose-100">
                                <span class="font-bold text-rose-950">Action:</span> Enforce an 18-minute kitchen preparation SLA; mandate 14-day quality reviews for kitchens with &lt; 3.8 stars.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Rule 4 -->
                <div class="glass-card p-6 rounded-2xl border-t-4 border-t-emerald-600 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center space-x-2.5 text-emerald-700 font-bold text-base mb-3">
                            <span class="text-lg">💰</span> <span>4. Subsidy Margin Protection</span>
                        </div>
                        <div class="space-y-3 text-sm">
                            <div class="p-3 bg-slate-50 rounded-xl text-slate-700 leading-relaxed border border-slate-100">
                                <span class="font-bold text-slate-900">Trigger:</span> Free delivery subsidies on low-ticket orders (&lt; ₹300) wipe out over 40% of platform commission.
                            </div>
                            <div class="p-3 bg-emerald-50 rounded-xl text-emerald-950 font-medium leading-relaxed border border-emerald-100">
                                <span class="font-bold text-emerald-950">Action:</span> Restrict free delivery subsidies to basket sizes exceeding a minimum order value of ₹550.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Rule 5 -->
                <div class="glass-card p-6 rounded-2xl border-t-4 border-t-purple-600 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center space-x-2.5 text-purple-700 font-bold text-base mb-3">
                            <span class="text-lg">🎁</span> <span>5. Automated Compensation</span>
                        </div>
                        <div class="space-y-3 text-sm">
                            <div class="p-3 bg-slate-50 rounded-xl text-slate-700 leading-relaxed border border-slate-100">
                                <span class="font-bold text-slate-900">Trigger:</span> Exactly 55 orders breached the statistical IQR Upper Bound (55.9 mins), triggering severe churn.
                            </div>
                            <div class="p-3 bg-purple-50 rounded-xl text-purple-950 font-medium leading-relaxed border border-purple-100">
                                <span class="font-bold text-purple-950">Action:</span> Program an automated ₹75 platform wallet credit trigger whenever an order exceeds 56 mins.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Rule 6 -->
                <div class="glass-card p-6 rounded-2xl border-t-4 border-t-blue-600 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center space-x-2.5 text-blue-700 font-bold text-base mb-3">
                            <span class="text-lg">🚀</span> <span>6. Proactive Scheduling</span>
                        </div>
                        <div class="space-y-3 text-sm">
                            <div class="p-3 bg-slate-50 rounded-xl text-slate-700 leading-relaxed border border-slate-100">
                                <span class="font-bold text-slate-900">Trigger:</span> Forecast indicates 174 orders/month with an 8.36% MAPE error margin.
                            </div>
                            <div class="p-3 bg-blue-50 rounded-xl text-blue-950 font-medium leading-relaxed border border-blue-100">
                                <span class="font-bold text-blue-950">Action:</span> Proactively contract 30 delivery partners during holiday and festival periods to eliminate supply deficit.
                            </div>
                        </div>
                    </div>
                </div>

            </div>

        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-slate-900 text-slate-400 text-sm py-8 mt-16 border-t border-slate-800">
        <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
            <div>
                <p class="font-semibold text-slate-200 text-base">Food Delivery Business Analytics and Optimization System</p>
                <p class="text-xs text-slate-500 mt-1">University Mini Project Assessment | Clean Pure Frontend Architecture</p>
            </div>
            <div class="text-xs text-slate-400 font-medium">
                <span>Excel &bull; Python &bull; Interactive Dashboard</span>
            </div>
        </div>
    </footer>

    <!-- ========================================================================= -->
    <!-- JAVASCRIPT: DATA & INTERACTIVE REACTIVE LOGIC -->
    <!-- ========================================================================= -->
    <script>
        // Raw dataset embedded directly
        const rawOrders = {orders_json};

        let currentFilteredOrders = [...rawOrders];
        let chartMonthlyTrend, chartCityPerf, chartCuisinePerf, chartDiagSpeed, chartDiagDistance, chartPredictive;

        // Initialize application on load
        window.addEventListener('DOMContentLoaded', () => {{
            calculateAndRenderKPIs(currentFilteredOrders);
            initCharts();
        }});

        // Smooth Tab Switching
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById(`tab-btn-${{tabId}}`);
            if (activeBtn) activeBtn.classList.add('active');

            document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.add('hidden'));
            const targetPane = document.getElementById(`tab-content-${{tabId}}`);
            if (targetPane) {{
                targetPane.classList.remove('hidden');
                targetPane.classList.remove('fade-in');
                void targetPane.offsetWidth;
                targetPane.classList.add('fade-in');
            }}
        }}

        // Reactive Filter Engine
        function applyFilters() {{
            const city = document.getElementById('filter-city').value;
            const cuisine = document.getElementById('filter-cuisine').value;
            const status = document.getElementById('filter-status').value;

            currentFilteredOrders = rawOrders.filter(row => {{
                const matchCity = (city === 'ALL' || row.city === city);
                const matchCuisine = (cuisine === 'ALL' || row.cuisine_category === cuisine);
                const matchStatus = (status === 'ALL' || row.order_status === status);
                return matchCity && matchCuisine && matchStatus;
            }});

            document.getElementById('filtered-badge').textContent = `Showing ${{currentFilteredOrders.length.toLocaleString()}} orders`;
            calculateAndRenderKPIs(currentFilteredOrders);
            updateCharts(currentFilteredOrders);
        }}

        function resetFilters() {{
            document.getElementById('filter-city').value = 'ALL';
            document.getElementById('filter-cuisine').value = 'ALL';
            document.getElementById('filter-status').value = 'ALL';
            applyFilters();
        }}

        // Calculate and update KPI values
        function calculateAndRenderKPIs(orders) {{
            const total = orders.length;
            const delivered = orders.filter(o => o.order_status === 'Delivered');
            const cancelled = orders.filter(o => o.order_status === 'Cancelled');
            const cancelRate = total > 0 ? ((cancelled.length / total) * 100).toFixed(2) : '0.00';
            const fulfillRate = total > 0 ? ((delivered.length / total) * 100).toFixed(1) : '0.0';

            const gmv = orders.reduce((sum, o) => sum + (o.order_value || 0), 0);
            const revenue = orders.reduce((sum, o) => sum + (o.platform_revenue || 0), 0);
            const takeRate = gmv > 0 ? ((revenue / gmv) * 100).toFixed(2) : '0.00';

            const validTimes = delivered.map(o => o.delivery_time_mins).filter(t => t != null);
            const avgTime = validTimes.length > 0 ? (validTimes.reduce((a, b) => a + b, 0) / validTimes.length).toFixed(1) : '0.0';

            const validRatings = delivered.map(o => o.customer_rating).filter(r => r != null);
            const avgRating = validRatings.length > 0 ? (validRatings.reduce((a, b) => a + b, 0) / validRatings.length).toFixed(2) : '0.00';

            document.getElementById('kpi-orders').textContent = total.toLocaleString();
            document.getElementById('kpi-delivered').textContent = delivered.length.toLocaleString();
            document.getElementById('kpi-fulfillment-rate').textContent = `${{fulfillRate}}% Fulfilled`;
            document.getElementById('kpi-cancellation').textContent = `${{cancelRate}}%`;
            document.getElementById('kpi-cancelled-count').textContent = `${{cancelled.length}} Cancelled`;
            document.getElementById('kpi-gmv').textContent = `₹${{(gmv / 100000).toFixed(2)}} L`;
            document.getElementById('kpi-revenue').textContent = `₹${{(revenue / 100000).toFixed(2)}} L`;
            document.getElementById('kpi-take-rate').textContent = `Take Rate: ${{takeRate}}%`;
            document.getElementById('kpi-avg-time').textContent = `${{avgTime}}m`;
            document.getElementById('kpi-rating').textContent = `Rating: ${{avgRating}} / 5.0★`;
        }}

        // Initialize all charts with enhanced fonts
        function initCharts() {{
            Chart.defaults.font.family = '"Plus Jakarta Sans", sans-serif';
            Chart.defaults.color = '#475569';
            Chart.defaults.font.size = 13;

            // 1. Monthly Trend
            const ctxMonthly = document.getElementById('chart-monthly-trend').getContext('2d');
            chartMonthlyTrend = new Chart(ctxMonthly, {{
                type: 'bar',
                data: getMonthlyData(currentFilteredOrders),
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ title: {{ display: true, text: 'Orders', font: {{ size: 14, weight: 'bold' }} }}, grid: {{ color: '#F1F5F9' }} }},
                        y1: {{ position: 'right', grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'Revenue (₹)', font: {{ size: 14, weight: 'bold' }} }} }}
                    }}
                }}
            }});

            // 2. City Performance
            const ctxCity = document.getElementById('chart-city-perf').getContext('2d');
            chartCityPerf = new Chart(ctxCity, {{
                type: 'bar',
                data: getCityData(currentFilteredOrders),
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{ x: {{ grid: {{ color: '#F1F5F9' }}, title: {{ display: true, text: 'Platform Revenue (INR)', font: {{ size: 14, weight: 'bold' }} }} }} }}
                }}
            }});

            // 3. Cuisine Performance
            const ctxCuisine = document.getElementById('chart-cuisine-perf').getContext('2d');
            chartCuisinePerf = new Chart(ctxCuisine, {{
                type: 'bar',
                data: getCuisineData(currentFilteredOrders),
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ title: {{ display: true, text: 'Revenue (₹)', font: {{ size: 14, weight: 'bold' }} }}, grid: {{ color: '#F1F5F9' }} }}
                    }}
                }}
            }});

            // 4. Diagnostic Speed
            const ctxSpeed = document.getElementById('chart-diag-speed').getContext('2d');
            chartDiagSpeed = new Chart(ctxSpeed, {{
                type: 'bar',
                data: {{
                    labels: ['Fast (<= 30m)', 'Moderate (31-45m)', 'Delayed (> 45m)'],
                    datasets: [
                        {{ label: 'Avg Rating (Stars)', data: [4.02, 3.70, 2.41], backgroundColor: '#10B981', yAxisID: 'y' }},
                        {{ label: 'Dissatisfaction Rate (%)', data: [9.7, 16.7, 54.8], backgroundColor: '#F43F5E', yAxisID: 'y1' }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ min: 0, max: 5, title: {{ display: true, text: 'Rating (Stars)', font: {{ size: 14, weight: 'bold' }} }} }},
                        y1: {{ position: 'right', min: 0, max: 100, grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: '% Unhappy Customers', font: {{ size: 14, weight: 'bold' }} }} }}
                    }}
                }}
            }});

            // 5. Diagnostic Distance
            const ctxDist = document.getElementById('chart-diag-distance').getContext('2d');
            chartDiagDistance = new Chart(ctxDist, {{
                type: 'bar',
                data: {{
                    labels: ['<= 3 km', '3 - 7 km', '7 - 10 km', '> 10 km'],
                    datasets: [
                        {{ label: 'Avg Delivery Time (mins)', data: [28.5, 36.0, 47.6, 60.6], backgroundColor: '#F59E0B', yAxisID: 'y' }},
                        {{ label: 'Customer Rating (Stars)', data: [3.97, 3.64, 2.85, 2.08], type: 'line', borderColor: '#4F46E5', backgroundColor: '#4F46E5', yAxisID: 'y1', tension: 0.2 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ title: {{ display: true, text: 'Delivery Time (mins)', font: {{ size: 14, weight: 'bold' }} }} }},
                        y1: {{ position: 'right', min: 0, max: 5, grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'Rating (Stars)', font: {{ size: 14, weight: 'bold' }} }} }}
                    }}
                }}
            }});

            // 6. Predictive Forecast
            const ctxPred = document.getElementById('chart-predictive').getContext('2d');
            chartPredictive = new Chart(ctxPred, {{
                type: 'line',
                data: {{
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan 2026 (Forecast)'],
                    datasets: [
                        {{
                            label: 'Actual Orders',
                            data: [157, 163, 180, 167, 166, 165, 174, 176, 129, 169, 176, 178, null],
                            borderColor: '#1E3A8A',
                            backgroundColor: '#1E3A8A',
                            borderWidth: 3,
                            tension: 0.2
                        }},
                        {{
                            label: '3-Month MA Forecast',
                            data: [null, null, null, 166.7, 170.0, 171.0, 166.0, 168.3, 171.7, 159.7, 158.0, 158.0, 174.3],
                            borderColor: '#E11D48',
                            borderDash: [6, 6],
                            backgroundColor: '#E11D48',
                            borderWidth: 2.5,
                            tension: 0.2
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ title: {{ display: true, text: 'Order Demand', font: {{ size: 14, weight: 'bold' }} }}, grid: {{ color: '#F1F5F9' }} }}
                    }}
                }}
            }});
        }}

        // Data processing helpers for charts
        function getMonthlyData(orders) {{
            const months = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12'];
            const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            const orderCounts = months.map(m => orders.filter(o => o.order_date.startsWith(m)).length);
            const revenues = months.map(m => orders.filter(o => o.order_date.startsWith(m)).reduce((s, o) => s + (o.platform_revenue || 0), 0));

            return {{
                labels: labels,
                datasets: [
                    {{ label: 'Orders Placed', data: orderCounts, backgroundColor: '#6366F1', borderRadius: 6, yAxisID: 'y' }},
                    {{ label: 'Revenue (₹)', data: revenues, type: 'line', borderColor: '#F59E0B', backgroundColor: '#F59E0B', tension: 0.3, yAxisID: 'y1' }}
                ]
            }};
        }}

        function getCityData(orders) {{
            const cities = ['Bangalore', 'Mumbai', 'Delhi NCR', 'Hyderabad', 'Pune'];
            const revenues = cities.map(c => orders.filter(o => o.city === c).reduce((s, o) => s + (o.platform_revenue || 0), 0));

            return {{
                labels: cities,
                datasets: [{{
                    data: revenues,
                    backgroundColor: ['#4F46E5', '#6366F1', '#818CF8', '#A5B4FC', '#C7D2FE'],
                    borderRadius: 6
                }}]
            }};
        }}

        function getCuisineData(orders) {{
            const cuisines = ['North Indian', 'Biryani', 'Fast Food', 'South Indian', 'Desserts', 'Chinese', 'Italian'];
            const revenues = cuisines.map(c => orders.filter(o => o.cuisine_category === c).reduce((s, o) => s + (o.platform_revenue || 0), 0));

            return {{
                labels: cuisines,
                datasets: [{{
                    label: 'Gross Revenue (₹)',
                    data: revenues,
                    backgroundColor: '#10B981',
                    borderRadius: 6
                }}]
            }};
        }}

        function updateCharts(orders) {{
            if (!chartMonthlyTrend) return;
            const mData = getMonthlyData(orders);
            chartMonthlyTrend.data.labels = mData.labels;
            chartMonthlyTrend.data.datasets = mData.datasets;
            chartMonthlyTrend.update();

            const cData = getCityData(orders);
            chartCityPerf.data.datasets[0].data = cData.datasets[0].data;
            chartCityPerf.update();

            const csData = getCuisineData(orders);
            chartCuisinePerf.data.datasets[0].data = csData.datasets[0].data;
            chartCuisinePerf.update();
        }}
    </script>
</body>
</html>
"""

with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"High-readability Dashboard built successfully: {OUTPUT_HTML}")
