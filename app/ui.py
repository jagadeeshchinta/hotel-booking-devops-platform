INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Algions Luxury Stays &bull; Bespoke Suites & Private Sanctuaries</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        serif: ['"Playfair Display"', 'Georgia', 'serif'],
                        sans: ['"Inter"', 'sans-serif'],
                        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace']
                    },
                    colors: {
                        gold: {
                            300: '#fde68a',
                            400: '#fbbf24',
                            500: '#f59e0b',
                            600: '#d97706'
                        }
                    }
                }
            }
        }
    </script>

    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #030712;
            background-image:
                radial-gradient(at 0% 0%, rgba(245, 158, 11, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
                linear-gradient(to bottom, rgba(3, 7, 18, 0.88), rgba(3, 7, 18, 0.94)),
                url('https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=2400&q=85');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .glass-panel {
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.45);
        }

        .glass-panel-subtle {
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .dot {
            width: 8px;
            height: 8px;
            border-radius: 9999px;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .dot-green {
            background-color: #10b981;
            box-shadow: 0 0 10px #10b981;
        }
        .dot-red {
            background-color: #f43f5e;
            box-shadow: 0 0 10px #f43f5e;
        }
        .dot-amber {
            background-color: #f59e0b;
            box-shadow: 0 0 10px #f59e0b;
        }

        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.3);
            border-radius: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(245, 158, 11, 0.25);
            border-radius: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: rgba(245, 158, 11, 0.5);
        }
    </style>
</head>
<body class="text-slate-100 min-h-screen flex flex-col justify-between selection:bg-amber-500 selection:text-slate-950">

    <!-- Top Navigation / Hero Header -->
    <header class="border-b border-white/10 glass-panel sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-600 to-amber-300 flex items-center justify-center text-slate-950 text-xl font-bold shadow-lg shadow-amber-500/20">
                    ⚜
                </div>
                <div>
                    <span class="font-serif text-2xl font-bold tracking-tight bg-gradient-to-r from-amber-200 via-amber-400 to-amber-100 bg-clip-text text-transparent">
                        Algions Luxury Stays
                    </span>
                    <span class="hidden sm:block text-[11px] text-amber-200/60 uppercase tracking-widest font-medium">
                        Bespoke Suites &bull; High-Concurrency Engine
                    </span>
                </div>
            </div>

            <!-- Live Probes & DevOps Telemetry Badges -->
            <div class="flex items-center gap-3">
                <div id="badge-health" class="px-3.5 py-1.5 rounded-full glass-panel-subtle flex items-center gap-2 border border-white/10">
                    <span class="dot dot-amber" id="dot-health"></span>
                    <span class="text-xs font-mono text-slate-300">Liveness: <strong id="val-health" class="text-amber-400">CHECKING</strong></span>
                </div>
                <div id="badge-ready" class="px-3.5 py-1.5 rounded-full glass-panel-subtle flex items-center gap-2 border border-white/10">
                    <span class="dot dot-amber" id="dot-ready"></span>
                    <span class="text-xs font-mono text-slate-300">Readiness: <strong id="val-ready" class="text-amber-400">CONNECTING</strong></span>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Booking Experience -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-grow space-y-8">

        <!-- Hero Sub-headline -->
        <div class="text-center max-w-2xl mx-auto space-y-2 pt-2">
            <h1 class="font-serif text-3xl sm:text-4xl text-white font-medium tracking-tight">
                Reserve Your Private Sanctuary
            </h1>
            <p class="text-slate-400 text-sm leading-relaxed">
                Experience world-class hospitality guarded by real-time pessimistic locking and PostgreSQL GiST exclusion integrity. Zero double bookings guaranteed.
            </p>
        </div>

        <!-- Split Grid: Availability Finder (Left) & Instant Reservation (Right) -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

            <!-- Panel 1: Availability Search & Room Selection (7 cols) -->
            <div class="lg:col-span-7 glass-panel rounded-2xl p-6 sm:p-7 space-y-6">
                <div class="flex items-center justify-between border-b border-white/10 pb-4">
                    <div>
                        <h2 class="font-serif text-xl font-semibold text-white flex items-center gap-2">
                            <span>🔍</span> Find Available Suites
                        </h2>
                        <p class="text-xs text-slate-400 mt-0.5">Filter luxury accommodations by stay duration and tier</p>
                    </div>
                    <button onclick="checkAvailability()" class="px-4 py-2 bg-amber-500/10 hover:bg-amber-500 text-amber-300 hover:text-slate-950 border border-amber-400/40 hover:border-amber-400 rounded-xl text-xs font-semibold uppercase tracking-wider transition-all duration-200">
                        Check Dates
                    </button>
                </div>

                <!-- Search Controls -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div class="space-y-1.5">
                        <label for="search-checkin" class="block text-xs font-medium text-slate-300">Check-in Date</label>
                        <input type="date" id="search-checkin" value="2026-12-01"
                               class="w-full bg-slate-950/70 border border-slate-700/80 focus:border-amber-400 focus:ring-1 focus:ring-amber-400/50 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 outline-none transition-all">
                    </div>
                    <div class="space-y-1.5">
                        <label for="search-checkout" class="block text-xs font-medium text-slate-300">Check-out Date</label>
                        <input type="date" id="search-checkout" value="2026-12-05"
                               class="w-full bg-slate-950/70 border border-slate-700/80 focus:border-amber-400 focus:ring-1 focus:ring-amber-400/50 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 outline-none transition-all">
                    </div>
                </div>

                <div class="space-y-1.5">
                    <label for="search-type" class="block text-xs font-medium text-slate-300">Suite Tier Category</label>
                    <select id="search-type"
                            class="w-full bg-slate-950/70 border border-slate-700/80 focus:border-amber-400 focus:ring-1 focus:ring-amber-400/50 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 outline-none transition-all">
                        <option value="">All Tiers (STANDARD, DELUXE, SUITE)</option>
                        <option value="STANDARD">STANDARD &bull; Cozy Comfort & Urban Elegance</option>
                        <option value="DELUXE">DELUXE &bull; Panoramic Vista & Executive Lounge</option>
                        <option value="SUITE">SUITE &bull; Presidential Penthouse & Private Balcony</option>
                    </select>
                </div>

                <!-- Available Rooms Cards Container -->
                <div>
                    <h3 class="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-3">Available Accommodations</h3>
                    <div id="availability-tbody" class="grid grid-cols-1 sm:grid-cols-2 gap-4 max-h-[380px] overflow-y-auto pr-1 custom-scrollbar">
                        <!-- Populated dynamically by checkAvailability() -->
                    </div>
                </div>
            </div>

            <!-- Panel 2: Quick Booking Form (5 cols) -->
            <div class="lg:col-span-5 glass-panel rounded-2xl p-6 sm:p-7 space-y-6 flex flex-col justify-between" id="booking-card">
                <div>
                    <div class="flex items-center justify-between border-b border-white/10 pb-4 mb-5">
                        <div>
                            <h2 class="font-serif text-xl font-semibold text-white flex items-center gap-2">
                                <span>⚡</span> Confirm Reservation
                            </h2>
                            <p class="text-xs text-slate-400 mt-0.5">Instant booking with PostgreSQL GiST exclusion lock</p>
                        </div>
                        <span class="text-[10px] font-mono text-amber-300 bg-amber-500/10 border border-amber-400/30 px-2 py-0.5 rounded-full">
                            SELECT FOR UPDATE
                        </span>
                    </div>

                    <!-- Instant Alerts -->
                    <div id="booking-alert-success" class="hidden mb-4 p-4 rounded-xl bg-emerald-950/80 border border-emerald-500/50 text-emerald-300 text-sm shadow-lg leading-relaxed"></div>
                    <div id="booking-alert-danger" class="hidden mb-4 p-4 rounded-xl bg-rose-950/80 border border-rose-500/50 text-rose-300 text-sm shadow-lg leading-relaxed"></div>

                    <form id="booking-form" onsubmit="event.preventDefault(); submitBooking();" class="space-y-4">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="space-y-1.5">
                                <label for="book-room-id" class="block text-xs font-medium text-slate-300">Room ID</label>
                                <input type="number" id="book-room-id" placeholder="e.g. 1" required min="1"
                                       class="w-full bg-slate-950/70 border border-slate-700/80 focus:border-amber-400 focus:ring-1 focus:ring-amber-400/50 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 outline-none font-mono">
                            </div>
                            <div class="space-y-1.5">
                                <label for="book-guest" class="block text-xs font-medium text-slate-300">Guest Name</label>
                                <input type="text" id="book-guest" placeholder="e.g. Sarah Connor" required value="Sarah Connor"
                                       class="w-full bg-slate-950/70 border border-slate-700/80 focus:border-amber-400 focus:ring-1 focus:ring-amber-400/50 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 outline-none">
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="space-y-1.5">
                                <label for="book-checkin" class="block text-xs font-medium text-slate-300">Check-in Date</label>
                                <input type="date" id="book-checkin" value="2026-12-01" required
                                       class="w-full bg-slate-950/70 border border-slate-700/80 focus:border-amber-400 focus:ring-1 focus:ring-amber-400/50 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 outline-none">
                            </div>
                            <div class="space-y-1.5">
                                <label for="book-checkout" class="block text-xs font-medium text-slate-300">Check-out Date</label>
                                <input type="date" id="book-checkout" value="2026-12-05" required
                                       class="w-full bg-slate-950/70 border border-slate-700/80 focus:border-amber-400 focus:ring-1 focus:ring-amber-400/50 rounded-xl px-3.5 py-2.5 text-sm text-slate-100 outline-none">
                            </div>
                        </div>

                        <button type="submit"
                                class="w-full py-3.5 px-6 rounded-xl font-semibold text-slate-950 bg-gradient-to-r from-amber-400 via-amber-300 to-amber-500 hover:from-amber-300 hover:to-amber-400 shadow-lg shadow-amber-500/20 active:scale-[0.99] transition-all duration-200 text-sm flex items-center justify-center gap-2 mt-2">
                            <span>🔒</span> Complete Booking Reservation
                        </button>
                    </form>
                </div>

                <div class="p-3.5 rounded-xl bg-slate-950/50 border border-white/5 text-[11px] text-slate-400 space-y-1">
                    <div class="flex items-center gap-1.5 text-amber-300/80 font-medium">
                        <span>🛡️</span> Concurrency Guard Active
                    </div>
                    <p>Transactions serialize via row-level locks and validate non-overlapping date spans before committing to PostgreSQL storage.</p>
                </div>
            </div>
        </div>

        <!-- Confirmed Bookings Table -->
        <div class="glass-panel rounded-2xl p-6 sm:p-7 space-y-4">
            <div class="flex items-center justify-between border-b border-white/10 pb-4">
                <div>
                    <h2 class="font-serif text-xl font-semibold text-white flex items-center gap-2">
                        <span>📋</span> Live Confirmed Reservations
                    </h2>
                    <p class="text-xs text-slate-400 mt-0.5">Real-time ledger of active bookings in database</p>
                </div>
                <button onclick="loadReservations()" class="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium border border-white/10 transition-colors">
                    ↻ Refresh Table
                </button>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs border-collapse">
                    <thead>
                        <tr class="border-b border-white/10 text-slate-400 font-semibold tracking-wider uppercase text-[10px]">
                            <th class="py-3 px-4">Booking Ref</th>
                            <th class="py-3 px-4">Room</th>
                            <th class="py-3 px-4">Guest</th>
                            <th class="py-3 px-4">Check-In</th>
                            <th class="py-3 px-4">Check-Out</th>
                            <th class="py-3 px-4">Status</th>
                            <th class="py-3 px-4">Created (UTC)</th>
                        </tr>
                    </thead>
                    <tbody id="reservations-tbody" class="divide-y divide-white/5 font-normal">
                        <tr><td colspan="7" class="py-6 text-center text-slate-500">Loading reservations...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- DevOps Navigation Bar -->
        <div class="flex flex-wrap items-center justify-center gap-3 pt-4 border-t border-white/10 text-xs">
            <span class="text-slate-500 font-medium">Direct API Endpoints:</span>
            <a href="/health" target="_blank" class="px-3 py-1.5 rounded-lg glass-panel-subtle text-amber-300 hover:text-white transition-colors">/health</a>
            <a href="/ready" target="_blank" class="px-3 py-1.5 rounded-lg glass-panel-subtle text-amber-300 hover:text-white transition-colors">/ready</a>
            <a href="/metrics" target="_blank" class="px-3 py-1.5 rounded-lg glass-panel-subtle text-amber-300 hover:text-white transition-colors">/metrics</a>
            <a href="/rooms" target="_blank" class="px-3 py-1.5 rounded-lg glass-panel-subtle text-amber-300 hover:text-white transition-colors">/rooms</a>
            <a href="/reservations" target="_blank" class="px-3 py-1.5 rounded-lg glass-panel-subtle text-amber-300 hover:text-white transition-colors">/reservations</a>
            <a href="/docs" target="_blank" class="px-3 py-1.5 rounded-lg bg-amber-500/10 text-amber-300 hover:bg-amber-500 hover:text-slate-950 font-semibold border border-amber-400/30 transition-all">Swagger UI</a>
            <a href="/redoc" target="_blank" class="px-3 py-1.5 rounded-lg glass-panel-subtle text-slate-300 hover:text-white transition-colors">ReDoc</a>
        </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-white/10 py-6 text-center text-xs text-slate-500 glass-panel mt-12">
        <p>&copy; 2026 Algions Luxury Stays &bull; Production DevOps Architecture by Jagadeesh Chinta</p>
    </footer>

    <!-- JavaScript Handlers (Zero change to API contracts or Element IDs) -->
    <script>
        async function fetchProbes() {
            // Liveness
            try {
                const res = await fetch('/health');
                const data = await res.json();
                const dot = document.getElementById('dot-health');
                const val = document.getElementById('val-health');
                if (res.ok && data.status === 'healthy') {
                    dot.className = 'dot dot-green';
                    val.innerText = 'HEALTHY';
                    val.className = 'text-emerald-400 font-bold';
                } else {
                    dot.className = 'dot dot-red';
                    val.innerText = 'FAIL';
                    val.className = 'text-rose-400 font-bold';
                }
            } catch (e) {
                document.getElementById('dot-health').className = 'dot dot-red';
                const val = document.getElementById('val-health');
                val.innerText = 'DOWN';
                val.className = 'text-rose-400 font-bold';
            }

            // Readiness
            try {
                const res = await fetch('/ready');
                const data = await res.json();
                const dot = document.getElementById('dot-ready');
                const val = document.getElementById('val-ready');
                if (res.ok && data.status === 'ready') {
                    dot.className = 'dot dot-green';
                    val.innerText = 'READY';
                    val.className = 'text-emerald-400 font-bold';
                } else {
                    dot.className = 'dot dot-red';
                    val.innerText = 'UNAVAILABLE';
                    val.className = 'text-rose-400 font-bold';
                }
            } catch (e) {
                document.getElementById('dot-ready').className = 'dot dot-red';
                const val = document.getElementById('val-ready');
                val.innerText = 'DISCONNECTED';
                val.className = 'text-rose-400 font-bold';
            }
        }

        async function checkAvailability() {
            const checkIn = document.getElementById('search-checkin').value;
            const checkOut = document.getElementById('search-checkout').value;
            const type = document.getElementById('search-type').value;

            const tbody = document.getElementById('availability-tbody');
            tbody.innerHTML = '<div class="col-span-full text-center py-8 text-amber-300 animate-pulse text-sm">Searching available suites...</div>';

            let url = `/rooms/availability?check_in=${checkIn}&check_out=${checkOut}`;
            if (type) url += `&room_type=${type}`;

            try {
                const res = await fetch(url);
                const rooms = await res.json();
                if (!res.ok) {
                    tbody.innerHTML = `<div class="col-span-full text-center py-6 text-rose-400 text-sm">${rooms.detail || 'Error querying availability'}</div>`;
                    return;
                }
                if (rooms.length === 0) {
                    tbody.innerHTML = '<div class="col-span-full text-center py-8 text-slate-400 italic text-sm">No suites available for the selected dates and tier.</div>';
                    return;
                }

                tbody.innerHTML = rooms.map(r => {
                    let badgeColor = 'bg-amber-500/10 text-amber-300 border-amber-400/30';
                    let perks = '✨ King Bed &bull; City View &bull; High-Speed Wi-Fi';
                    if (r.room_type === 'SUITE') {
                        badgeColor = 'bg-purple-500/10 text-purple-300 border-purple-400/30';
                        perks = '👑 Penthouse Terrace &bull; Personal Butler &bull; Spa Tub';
                    } else if (r.room_type === 'DELUXE') {
                        badgeColor = 'bg-indigo-500/10 text-indigo-300 border-indigo-400/30';
                        perks = '🍸 Ocean View &bull; Executive Lounge &bull; Mini Bar';
                    }

                    return `
                    <div class="group relative bg-slate-900/60 hover:bg-slate-800/80 border border-white/10 hover:border-amber-400/50 rounded-xl p-4 transition-all duration-300 shadow-md flex flex-col justify-between">
                        <div>
                            <div class="flex items-start justify-between gap-2 mb-2">
                                <span class="text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 rounded-full border ${badgeColor}">
                                    ${r.room_type}
                                </span>
                                <div class="text-right">
                                    <span class="text-lg font-serif font-bold text-amber-400">$${parseFloat(r.price_per_night).toFixed(2)}</span>
                                    <span class="text-[10px] text-slate-400 block -mt-1">/ night</span>
                                </div>
                            </div>
                            <h4 class="text-base font-serif font-semibold text-white">Suite #${r.room_number}</h4>
                            <p class="text-[11px] text-slate-400 mt-1 mb-3">${perks}</p>
                        </div>
                        <button onclick="selectRoomForBooking(${r.id}, '${checkIn}', '${checkOut}')"
                                class="w-full py-2 px-3 text-xs font-semibold uppercase tracking-wider text-amber-300 bg-amber-500/10 hover:bg-amber-500 hover:text-slate-950 border border-amber-400/30 hover:border-amber-400 rounded-lg transition-all duration-200">
                            Select Suite &rarr;
                        </button>
                    </div>
                    `;
                }).join('');
            } catch (e) {
                tbody.innerHTML = '<div class="col-span-full text-center py-6 text-rose-400 text-sm">Network communication error</div>';
            }
        }

        function selectRoomForBooking(id, checkIn, checkOut) {
            document.getElementById('book-room-id').value = id;
            document.getElementById('book-checkin').value = checkIn;
            document.getElementById('book-checkout').value = checkOut;
            const target = document.getElementById('booking-card');
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }

        async function submitBooking() {
            const successAlert = document.getElementById('booking-alert-success');
            const dangerAlert = document.getElementById('booking-alert-danger');
            successAlert.style.display = 'none';
            dangerAlert.style.display = 'none';

            const payload = {
                room_id: parseInt(document.getElementById('book-room-id').value, 10),
                guest_name: document.getElementById('book-guest').value,
                check_in: document.getElementById('book-checkin').value,
                check_out: document.getElementById('book-checkout').value
            };

            try {
                const res = await fetch('/reservations', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (res.status === 201) {
                    successAlert.innerHTML = `✨ <strong>201 Created:</strong> Reservation confirmed for <strong>${data.guest_name}</strong>! Reference Code: <code class="font-mono text-amber-300 bg-amber-500/20 px-2 py-0.5 rounded font-bold">${data.booking_reference}</code>`;
                    successAlert.style.display = 'block';
                    loadReservations();
                    checkAvailability();
                } else if (res.status === 409) {
                    dangerAlert.innerHTML = `⚠️ <strong>409 Conflict:</strong> ${data.detail || 'Room is already booked for overlapping dates.'}`;
                    dangerAlert.style.display = 'block';
                } else {
                    dangerAlert.innerHTML = `❌ <strong>Error (${res.status}):</strong> ${data.detail || 'Reservation request failed.'}`;
                    dangerAlert.style.display = 'block';
                }
            } catch (e) {
                dangerAlert.innerHTML = `❌ Network error while creating reservation.`;
                dangerAlert.style.display = 'block';
            }
        }

        async function loadReservations() {
            const tbody = document.getElementById('reservations-tbody');
            try {
                const res = await fetch('/reservations');
                const items = await res.json();
                if (items.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="7" class="py-6 text-center text-slate-500">No reservations currently recorded.</td></tr>';
                    return;
                }
                tbody.innerHTML = items.map(r => `
                    <tr class="hover:bg-white/[0.02] transition-colors">
                        <td class="py-3 px-4 font-mono font-bold text-amber-400">${r.booking_reference}</td>
                        <td class="py-3 px-4 text-slate-300">Room #${r.room_id}</td>
                        <td class="py-3 px-4 font-medium text-white">${r.guest_name}</td>
                        <td class="py-3 px-4 text-slate-300">${r.check_in}</td>
                        <td class="py-3 px-4 text-slate-300">${r.check_out}</td>
                        <td class="py-3 px-4">
                            <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                                ${r.status}
                            </span>
                        </td>
                        <td class="py-3 px-4 text-slate-500 font-mono text-[11px]">${new Date(r.created_at).toLocaleString()}</td>
                    </tr>
                `).join('');
            } catch (e) {
                tbody.innerHTML = '<tr><td colspan="7" class="py-6 text-center text-rose-400">Failed to load reservations ledger.</td></tr>';
            }
        }

        // Initialize probes and data
        fetchProbes();
        checkAvailability();
        loadReservations();
        setInterval(fetchProbes, 5000);
    </script>
</body>
</html>
"""
