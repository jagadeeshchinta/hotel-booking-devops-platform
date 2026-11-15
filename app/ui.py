INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Algions Luxury Stays &bull; Bespoke Suites & Private Sanctuaries</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        serif: ['"Playfair Display"', 'Georgia', 'serif'],
                        sans: ['"Inter"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
                        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace']
                    }
                }
            }
        }
    </script>

    <style>
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #0c1524;
            background-image:
                linear-gradient(to bottom, rgba(10, 18, 30, 0.45), rgba(10, 18, 30, 0.65)),
                url('https://images.unsplash.com/photo-1540541338287-41700207dee6?auto=format&fit=crop&w=2560&q=85');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
        }

        /* Apple-style Ultra-translucent Frosted Glass */
        .glass-panel {
            background: rgba(15, 23, 42, 0.32);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.20);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }

        .glass-panel-subtle {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .glass-input {
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.22);
            color: #ffffff;
            transition: all 0.2s ease;
        }
        .glass-input:focus {
            background: rgba(255, 255, 255, 0.16);
            border-color: rgba(255, 255, 255, 0.50);
            outline: none;
            box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.15);
        }
        .glass-input::placeholder {
            color: rgba(255, 255, 255, 0.45);
        }

        input[type="date"]::-webkit-calendar-picker-indicator {
            filter: invert(1);
            opacity: 0.85;
            cursor: pointer;
        }

        /* Sleek Status Indicator Dots */
        .dot {
            width: 7px;
            height: 7px;
            border-radius: 9999px;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .dot-green {
            background-color: #34d399;
            box-shadow: 0 0 10px #34d399;
        }
        .dot-red {
            background-color: #f87171;
            box-shadow: 0 0 10px #f87171;
        }
        .dot-amber {
            background-color: #fbbf24;
            box-shadow: 0 0 10px #fbbf24;
        }

        /* Custom Scrollbar */
        .custom-scrollbar::-webkit-scrollbar {
            width: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 9999px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.25);
            border-radius: 9999px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.45);
        }
    </style>
</head>
<body class="text-white min-h-screen flex flex-col justify-between selection:bg-white/30 selection:text-white">

    <!-- Hero Navbar: Apple-style Minimal Glass Header -->
    <header class="border-b border-white/15 glass-panel sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 sm:px-8 h-20 flex items-center justify-between">
            <div class="flex items-center space-x-3.5">
                <div class="w-10 h-10 rounded-2xl bg-white/15 border border-white/30 backdrop-blur-md flex items-center justify-center text-white text-lg font-serif shadow-lg">
                    ⚜
                </div>
                <div>
                    <span class="font-serif text-2xl font-medium tracking-tight text-white block leading-none">
                        Algions Luxury Stays
                    </span>
                    <span class="text-[10px] text-gray-300 uppercase tracking-widest font-light mt-1 block">
                        Bespoke Suites &bull; High-Concurrency Engine
                    </span>
                </div>
            </div>

            <!-- Sleek Minimalist Health & Telemetry Badges -->
            <div class="flex items-center gap-3">
                <div id="badge-health" class="px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 flex items-center gap-2 shadow-sm">
                    <span class="dot dot-amber" id="dot-health"></span>
                    <span class="text-[11px] font-light tracking-wide text-gray-200">Liveness: <strong id="val-health" class="text-amber-300 font-medium">CHECKING</strong></span>
                </div>
                <div id="badge-ready" class="px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 flex items-center gap-2 shadow-sm">
                    <span class="dot dot-amber" id="dot-ready"></span>
                    <span class="text-[11px] font-light tracking-wide text-gray-200">Readiness: <strong id="val-ready" class="text-amber-300 font-medium">CONNECTING</strong></span>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Booking Experience -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full flex-grow space-y-10">

        <!-- Hero Headline -->
        <div class="text-center max-w-2xl mx-auto space-y-3 pt-2">
            <h1 class="font-serif text-3xl sm:text-5xl text-white font-normal tracking-tight drop-shadow-md">
                Reserve Your Private Sanctuary
            </h1>
            <p class="text-gray-200 text-sm sm:text-base font-light leading-relaxed">
                Experience world-class hospitality guarded by real-time pessimistic locking and PostgreSQL GiST exclusion integrity. Zero double bookings guaranteed.
            </p>
        </div>

        <!-- Split Grid: Availability Finder (Left) & Instant Reservation (Right) -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

            <!-- Panel 1: Availability Search & Room Selection (7 cols) -->
            <div class="lg:col-span-7 glass-panel rounded-3xl p-8 sm:p-10 space-y-7">
                <div class="flex items-center justify-between border-b border-white/15 pb-5">
                    <div>
                        <h2 class="font-serif text-2xl font-normal text-white flex items-center gap-2.5">
                            <span>🔍</span> Find Available Suites
                        </h2>
                        <p class="text-xs text-gray-200 font-light mt-1">Filter luxury accommodations by stay duration and tier</p>
                    </div>
                    <button onclick="checkAvailability()" class="px-5 py-2.5 bg-white/20 hover:bg-white/30 text-white border border-white/30 transition-all rounded-full text-xs font-medium uppercase tracking-wider shadow-sm active:scale-95">
                        Check Dates
                    </button>
                </div>

                <!-- Search Controls -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div class="space-y-2">
                        <label for="search-checkin" class="block text-xs font-light uppercase tracking-wider text-gray-200">Check-in Date</label>
                        <input type="date" id="search-checkin" value="2026-12-01"
                               class="w-full glass-input rounded-2xl px-4 py-3 text-sm">
                    </div>
                    <div class="space-y-2">
                        <label for="search-checkout" class="block text-xs font-light uppercase tracking-wider text-gray-200">Check-out Date</label>
                        <input type="date" id="search-checkout" value="2026-12-05"
                               class="w-full glass-input rounded-2xl px-4 py-3 text-sm">
                    </div>
                </div>

                <div class="space-y-2">
                    <label for="search-type" class="block text-xs font-light uppercase tracking-wider text-gray-200">Suite Tier Category</label>
                    <select id="search-type"
                            class="w-full glass-input rounded-2xl px-4 py-3 text-sm cursor-pointer">
                        <option value="" class="bg-slate-900 text-white">All Tiers (STANDARD, DELUXE, SUITE)</option>
                        <option value="STANDARD" class="bg-slate-900 text-white">STANDARD &bull; Cozy Comfort & Urban Elegance</option>
                        <option value="DELUXE" class="bg-slate-900 text-white">DELUXE &bull; Panoramic Vista & Executive Lounge</option>
                        <option value="SUITE" class="bg-slate-900 text-white">SUITE &bull; Presidential Penthouse & Private Balcony</option>
                    </select>
                </div>

                <!-- Available Rooms Cards Container -->
                <div>
                    <h3 class="text-xs uppercase tracking-wider text-gray-300 font-medium mb-4">Available Accommodations</h3>
                    <div id="availability-tbody" class="grid grid-cols-1 sm:grid-cols-2 gap-4 max-h-[400px] overflow-y-auto pr-1.5 custom-scrollbar">
                        <!-- Populated dynamically by checkAvailability() -->
                    </div>
                </div>
            </div>

            <!-- Panel 2: Quick Booking Form (5 cols) -->
            <div class="lg:col-span-5 glass-panel rounded-3xl p-8 sm:p-10 space-y-7 flex flex-col justify-between" id="booking-card">
                <div>
                    <div class="flex items-center justify-between border-b border-white/15 pb-5 mb-6">
                        <div>
                            <h2 class="font-serif text-2xl font-normal text-white flex items-center gap-2.5">
                                <span>⚡</span> Confirm Reservation
                            </h2>
                            <p class="text-xs text-gray-200 font-light mt-1">Instant booking with PostgreSQL GiST exclusion lock</p>
                        </div>
                        <span class="text-[10px] font-mono text-white bg-white/15 border border-white/25 px-2.5 py-1 rounded-full">
                            SELECT FOR UPDATE
                        </span>
                    </div>

                    <!-- Instant Alerts -->
                    <div id="booking-alert-success" class="hidden mb-5 p-4 rounded-2xl bg-emerald-950/60 border border-emerald-400/40 text-emerald-200 text-sm shadow-xl leading-relaxed backdrop-blur-md"></div>
                    <div id="booking-alert-danger" class="hidden mb-5 p-4 rounded-2xl bg-rose-950/60 border border-rose-400/40 text-rose-200 text-sm shadow-xl leading-relaxed backdrop-blur-md"></div>

                    <form id="booking-form" onsubmit="event.preventDefault(); submitBooking();" class="space-y-4">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="space-y-2">
                                <label for="book-room-id" class="block text-xs font-light uppercase tracking-wider text-gray-200">Room ID</label>
                                <input type="number" id="book-room-id" placeholder="e.g. 1" required min="1"
                                       class="w-full glass-input rounded-2xl px-4 py-3 text-sm font-mono">
                            </div>
                            <div class="space-y-2">
                                <label for="book-guest" class="block text-xs font-light uppercase tracking-wider text-gray-200">Guest Name</label>
                                <input type="text" id="book-guest" placeholder="e.g. Sarah Connor" required value="Sarah Connor"
                                       class="w-full glass-input rounded-2xl px-4 py-3 text-sm">
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="space-y-2">
                                <label for="book-checkin" class="block text-xs font-light uppercase tracking-wider text-gray-200">Check-in Date</label>
                                <input type="date" id="book-checkin" value="2026-12-01" required
                                       class="w-full glass-input rounded-2xl px-4 py-3 text-sm">
                            </div>
                            <div class="space-y-2">
                                <label for="book-checkout" class="block text-xs font-light uppercase tracking-wider text-gray-200">Check-out Date</label>
                                <input type="date" id="book-checkout" value="2026-12-05" required
                                       class="w-full glass-input rounded-2xl px-4 py-3 text-sm">
                            </div>
                        </div>

                        <button type="submit"
                                class="w-full py-3.5 px-6 rounded-full font-medium text-white bg-white/20 hover:bg-white/30 border border-white/35 backdrop-blur-md shadow-xl active:scale-[0.98] transition-all duration-300 text-sm flex items-center justify-center gap-2 mt-4 cursor-pointer">
                            <span>🔒</span> Complete Booking Reservation
                        </button>
                    </form>
                </div>

                <div class="p-4 rounded-2xl bg-white/5 border border-white/10 text-xs text-gray-200 space-y-1.5 mt-4">
                    <div class="flex items-center gap-2 text-white font-medium">
                        <span>🛡️</span> Concurrency Guard Active
                    </div>
                    <p class="font-light leading-relaxed text-gray-300">Transactions serialize via row-level locks and validate non-overlapping date spans before committing to PostgreSQL storage.</p>
                </div>
            </div>
        </div>

        <!-- Confirmed Bookings Table -->
        <div class="glass-panel rounded-3xl p-8 sm:p-10 space-y-5">
            <div class="flex items-center justify-between border-b border-white/15 pb-5">
                <div>
                    <h2 class="font-serif text-2xl font-normal text-white flex items-center gap-2.5">
                        <span>📋</span> Live Confirmed Reservations
                    </h2>
                    <p class="text-xs text-gray-200 font-light mt-1">Real-time ledger of active bookings in database</p>
                </div>
                <button onclick="loadReservations()" class="px-4 py-2 bg-white/15 hover:bg-white/25 text-white rounded-full text-xs font-medium border border-white/25 transition-all shadow-sm active:scale-95">
                    ↻ Refresh Table
                </button>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs border-collapse">
                    <thead>
                        <tr class="border-b border-white/15 text-gray-300 font-medium tracking-wider uppercase text-[10px]">
                            <th class="py-3.5 px-4">Booking Ref</th>
                            <th class="py-3.5 px-4">Room</th>
                            <th class="py-3.5 px-4">Guest</th>
                            <th class="py-3.5 px-4">Check-In</th>
                            <th class="py-3.5 px-4">Check-Out</th>
                            <th class="py-3.5 px-4">Status</th>
                            <th class="py-3.5 px-4">Created (UTC)</th>
                        </tr>
                    </thead>
                    <tbody id="reservations-tbody" class="divide-y divide-white/10 font-normal">
                        <tr><td colspan="7" class="py-8 text-center text-gray-300 font-light">Loading reservations...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- DevOps Navigation Bar -->
        <div class="flex flex-wrap items-center justify-center gap-3 pt-6 border-t border-white/15 text-xs">
            <span class="text-gray-300 font-light">Direct API Endpoints:</span>
            <a href="/health" target="_blank" class="px-3.5 py-1.5 rounded-full bg-white/10 hover:bg-white/20 text-gray-200 hover:text-white border border-white/20 transition-all">/health</a>
            <a href="/ready" target="_blank" class="px-3.5 py-1.5 rounded-full bg-white/10 hover:bg-white/20 text-gray-200 hover:text-white border border-white/20 transition-all">/ready</a>
            <a href="/metrics" target="_blank" class="px-3.5 py-1.5 rounded-full bg-white/10 hover:bg-white/20 text-gray-200 hover:text-white border border-white/20 transition-all">/metrics</a>
            <a href="/rooms" target="_blank" class="px-3.5 py-1.5 rounded-full bg-white/10 hover:bg-white/20 text-gray-200 hover:text-white border border-white/20 transition-all">/rooms</a>
            <a href="/reservations" target="_blank" class="px-3.5 py-1.5 rounded-full bg-white/10 hover:bg-white/20 text-gray-200 hover:text-white border border-white/20 transition-all">/reservations</a>
            <a href="/docs" target="_blank" class="px-4 py-1.5 rounded-full bg-white/20 hover:bg-white/30 text-white font-medium border border-white/30 transition-all">Swagger UI</a>
            <a href="/redoc" target="_blank" class="px-3.5 py-1.5 rounded-full bg-white/10 hover:bg-white/20 text-gray-200 hover:text-white border border-white/20 transition-all">ReDoc</a>
        </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-white/15 py-6 text-center text-xs text-gray-300 glass-panel mt-12 font-light">
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
                    val.className = 'text-emerald-300 font-medium';
                } else {
                    dot.className = 'dot dot-red';
                    val.innerText = 'FAIL';
                    val.className = 'text-rose-300 font-medium';
                }
            } catch (e) {
                document.getElementById('dot-health').className = 'dot dot-red';
                const val = document.getElementById('val-health');
                val.innerText = 'DOWN';
                val.className = 'text-rose-300 font-medium';
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
                    val.className = 'text-emerald-300 font-medium';
                } else {
                    dot.className = 'dot dot-red';
                    val.innerText = 'UNAVAILABLE';
                    val.className = 'text-rose-300 font-medium';
                }
            } catch (e) {
                document.getElementById('dot-ready').className = 'dot dot-red';
                const val = document.getElementById('val-ready');
                val.innerText = 'DISCONNECTED';
                val.className = 'text-rose-300 font-medium';
            }
        }

        async function checkAvailability() {
            const checkIn = document.getElementById('search-checkin').value;
            const checkOut = document.getElementById('search-checkout').value;
            const type = document.getElementById('search-type').value;

            const tbody = document.getElementById('availability-tbody');
            tbody.innerHTML = '<div class="col-span-full text-center py-8 text-white/80 animate-pulse text-sm">Searching available suites...</div>';

            let url = `/rooms/availability?check_in=${checkIn}&check_out=${checkOut}`;
            if (type) url += `&room_type=${type}`;

            try {
                const res = await fetch(url);
                const rooms = await res.json();
                if (!res.ok) {
                    tbody.innerHTML = `<div class="col-span-full text-center py-6 text-rose-300 text-sm">${rooms.detail || 'Error querying availability'}</div>`;
                    return;
                }
                if (rooms.length === 0) {
                    tbody.innerHTML = '<div class="col-span-full text-center py-8 text-gray-300 italic text-sm">No suites available for the selected dates and tier.</div>';
                    return;
                }

                tbody.innerHTML = rooms.map(r => {
                    let badgeColor = 'bg-white/15 text-white border-white/25';
                    let perks = 'Ocean Breeze &bull; King Bed &bull; High-Speed Wi-Fi';
                    if (r.room_type === 'SUITE') {
                        badgeColor = 'bg-amber-400/20 text-amber-200 border-amber-300/30';
                        perks = 'Private Plunge Pool &bull; Penthouse Terrace &bull; Butler Service';
                    } else if (r.room_type === 'DELUXE') {
                        badgeColor = 'bg-cyan-400/20 text-cyan-200 border-cyan-300/30';
                        perks = 'Panoramic Sea Vista &bull; Executive Balcony &bull; Rain Shower';
                    }

                    return `
                    <div class="group relative bg-white/10 hover:bg-white/15 border border-white/20 hover:border-white/40 rounded-2xl p-5 backdrop-blur-md transition-all duration-300 shadow-xl flex flex-col justify-between">
                        <div>
                            <div class="flex items-start justify-between gap-2 mb-2">
                                <span class="text-[11px] tracking-wider uppercase font-semibold px-2.5 py-0.5 rounded-full border ${badgeColor}">
                                    ${r.room_type}
                                </span>
                                <div class="text-right">
                                    <span class="text-xl font-serif font-semibold text-white">$${parseFloat(r.price_per_night).toFixed(2)}</span>
                                    <span class="text-[10px] text-gray-300 block -mt-1">/ night</span>
                                </div>
                            </div>
                            <h4 class="text-lg font-serif font-medium text-white">Suite #${r.room_number}</h4>
                            <p class="text-xs text-gray-200 mt-1 mb-4 leading-relaxed">${perks}</p>
                        </div>
                        <button onclick="selectRoomForBooking(${r.id}, '${checkIn}', '${checkOut}')"
                                class="w-full py-2.5 px-4 text-xs font-medium tracking-wide uppercase text-white bg-white/20 hover:bg-white/30 border border-white/30 rounded-full transition-all duration-200 shadow-sm active:scale-[0.98] cursor-pointer">
                            Select Suite &rarr;
                        </button>
                    </div>
                    `;
                }).join('');
            } catch (e) {
                tbody.innerHTML = '<div class="col-span-full text-center py-6 text-rose-300 text-sm">Network communication error</div>';
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
                    successAlert.innerHTML = `✨ <strong>201 Created:</strong> Reservation confirmed for <strong>${data.guest_name}</strong>! Reference Code: <code class="font-mono text-white bg-white/20 px-2.5 py-1 rounded-full font-semibold border border-white/30">${data.booking_reference}</code>`;
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
                    tbody.innerHTML = '<tr><td colspan="7" class="py-8 text-center text-gray-300 font-light">No reservations currently recorded.</td></tr>';
                    return;
                }
                tbody.innerHTML = items.map(r => `
                    <tr class="hover:bg-white/[0.04] transition-colors">
                        <td class="py-3.5 px-4 font-mono font-medium text-white"><span class="px-2.5 py-1 rounded-full bg-white/10 border border-white/20">${r.booking_reference}</span></td>
                        <td class="py-3.5 px-4 text-gray-200">Room #${r.room_id}</td>
                        <td class="py-3.5 px-4 font-medium text-white">${r.guest_name}</td>
                        <td class="py-3.5 px-4 text-gray-200">${r.check_in}</td>
                        <td class="py-3.5 px-4 text-gray-200">${r.check_out}</td>
                        <td class="py-3.5 px-4">
                            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-400/20 text-emerald-300 border border-emerald-400/30">
                                ${r.status}
                            </span>
                        </td>
                        <td class="py-3.5 px-4 text-gray-300 font-mono text-[11px]">${new Date(r.created_at).toLocaleString()}</td>
                    </tr>
                `).join('');
            } catch (e) {
                tbody.innerHTML = '<tr><td colspan="7" class="py-8 text-center text-rose-300">Failed to load reservations ledger.</td></tr>';
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
