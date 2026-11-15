INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hotel Room Availability & Reservation Service - DevOps Console</title>
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-card: #111827;
            --bg-card-hover: #1f2937;
            --border-color: #374151;
            --text-primary: #f3f4f6;
            --text-muted: #9ca3af;
            --accent-cyan: #06b6d4;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-amber: #f59e0b;
            --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.5;
            padding: 24px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
            margin-bottom: 28px;
        }

        .header-title h1 {
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: -0.025em;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .header-title p {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 4px;
        }

        .badge-bar {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        .badge {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-family: var(--font-mono);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }

        .dot-green { background-color: var(--accent-green); box-shadow: 0 0 8px var(--accent-green); }
        .dot-red { background-color: var(--accent-red); box-shadow: 0 0 8px var(--accent-red); }
        .dot-amber { background-color: var(--accent-amber); box-shadow: 0 0 8px var(--accent-amber); }

        .grid-2 {
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
            margin-bottom: 28px;
        }

        @media (min-width: 900px) {
            .grid-2 {
                grid-template-columns: 1fr 1fr;
            }
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }

        .card h2 {
            font-size: 1.15rem;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .form-group {
            margin-bottom: 14px;
        }

        label {
            display: block;
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 6px;
        }

        input, select {
            width: 100%;
            padding: 9px 12px;
            background: #0f172a;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: #fff;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input:focus, select:focus {
            border-color: var(--accent-cyan);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 9px 18px;
            border-radius: 6px;
            font-size: 0.88rem;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: opacity 0.2s, background-color 0.2s;
        }

        .btn-primary {
            background: var(--accent-cyan);
            color: #042f2e;
        }

        .btn-primary:hover {
            opacity: 0.9;
        }

        .btn-outline {
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        .btn-outline:hover {
            background: var(--bg-card-hover);
        }

        .btn-sm {
            padding: 4px 10px;
            font-size: 0.78rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin-top: 10px;
        }

        th, td {
            text-align: left;
            padding: 10px 12px;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            color: var(--text-muted);
            font-weight: 600;
            background: #0f172a;
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }

        .alert {
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 16px;
            font-size: 0.88rem;
            display: none;
        }

        .alert-success {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid var(--accent-green);
            color: #34d399;
        }

        .alert-danger {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid var(--accent-red);
            color: #f87171;
        }

        .devops-links {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid var(--border-color);
        }

        .devops-link {
            color: var(--accent-cyan);
            text-decoration: none;
            font-size: 0.85rem;
            font-family: var(--font-mono);
            padding: 6px 12px;
            background: #111827;
            border: 1px solid var(--border-color);
            border-radius: 4px;
        }

        .devops-link:hover {
            border-color: var(--accent-cyan);
        }

        .pill-type {
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 999px;
            font-family: var(--font-mono);
            background: #1e293b;
            border: 1px solid #475569;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-title">
                <h1>🏨 Hotel Booking Service <span style="font-size: 0.8rem; font-weight: normal; color: var(--accent-cyan); font-family: var(--font-mono);">v1.0.0</span></h1>
                <p>PostgreSQL 16 &bull; Concurrency-Controlled GiST Reservations &bull; FastAPI</p>
            </div>
            <div class="badge-bar">
                <div class="badge" id="badge-health">
                    <span class="dot dot-amber" id="dot-health"></span>
                    <span>Liveness: <strong id="val-health">CHECKING</strong></span>
                </div>
                <div class="badge" id="badge-ready">
                    <span class="dot dot-amber" id="dot-ready"></span>
                    <span>Readiness: <strong id="val-ready">CONNECTING</strong></span>
                </div>
            </div>
        </header>

        <div class="grid-2">
            <!-- Availability Checker -->
            <div class="card">
                <h2>
                    <span>🔍 Room Availability Finder</span>
                    <button class="btn btn-outline btn-sm" onclick="checkAvailability()">Search</button>
                </h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div class="form-group">
                        <label for="search-checkin">Check-in Date</label>
                        <input type="date" id="search-checkin" value="2026-12-01">
                    </div>
                    <div class="form-group">
                        <label for="search-checkout">Check-out Date</label>
                        <input type="date" id="search-checkout" value="2026-12-05">
                    </div>
                </div>
                <div class="form-group">
                    <label for="search-type">Room Type Filter</label>
                    <select id="search-type">
                        <option value="">All Types (STANDARD, DELUXE, SUITE)</option>
                        <option value="STANDARD">STANDARD</option>
                        <option value="DELUXE">DELUXE</option>
                        <option value="SUITE">SUITE</option>
                    </select>
                </div>
                <div style="margin-top: 10px; max-height: 280px; overflow-y: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>Room</th>
                                <th>Type</th>
                                <th>Price/Night</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="availability-tbody">
                            <tr><td colspan="4" style="text-align: center; color: var(--text-muted);">Click Search to query available rooms</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Booking Form -->
            <div class="card">
                <h2>
                    <span>⚡ Quick Reservation Booking</span>
                    <span style="font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono);">SELECT FOR UPDATE</span>
                </h2>

                <div id="booking-alert-success" class="alert alert-success"></div>
                <div id="booking-alert-danger" class="alert alert-danger"></div>

                <form id="booking-form" onsubmit="event.preventDefault(); submitBooking();">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="form-group">
                            <label for="book-room-id">Target Room ID</label>
                            <input type="number" id="book-room-id" placeholder="e.g. 1" required min="1">
                        </div>
                        <div class="form-group">
                            <label for="book-guest">Guest Name</label>
                            <input type="text" id="book-guest" placeholder="e.g. Sarah Connor" required value="Sarah Connor">
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="form-group">
                            <label for="book-checkin">Check-in Date</label>
                            <input type="date" id="book-checkin" value="2026-12-01" required>
                        </div>
                        <div class="form-group">
                            <label for="book-checkout">Check-out Date</label>
                            <input type="date" id="book-checkout" value="2026-12-05" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 10px;">
                        🔒 Confirm Reservation (Pessimistic + GiST Guarded)
                    </button>
                </form>
            </div>
        </div>

        <!-- Recent Reservations Table -->
        <div class="card">
            <h2>
                <span>📋 Live Confirmed Reservations</span>
                <button class="btn btn-outline btn-sm" onclick="loadReservations()">↻ Refresh</button>
            </h2>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Reference</th>
                            <th>Room ID</th>
                            <th>Guest Name</th>
                            <th>Check-in</th>
                            <th>Check-out</th>
                            <th>Status</th>
                            <th>Created At</th>
                        </tr>
                    </thead>
                    <tbody id="reservations-tbody">
                        <tr><td colspan="7" style="text-align: center; color: var(--text-muted);">Loading reservations...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- DevOps Navigation Bar -->
        <div class="devops-links">
            <span style="color: var(--text-muted); font-size: 0.85rem; align-self: center;">DevOps Endpoints:</span>
            <a class="devops-link" href="/health" target="_blank">/health (Liveness)</a>
            <a class="devops-link" href="/ready" target="_blank">/ready (Readiness)</a>
            <a class="devops-link" href="/metrics" target="_blank">/metrics (Prometheus)</a>
            <a class="devops-link" href="/rooms" target="_blank">/rooms</a>
            <a class="devops-link" href="/reservations" target="_blank">/reservations</a>
            <a class="devops-link" href="/docs" target="_blank">Swagger OpenAPI UI</a>
            <a class="devops-link" href="/redoc" target="_blank">ReDoc</a>
        </div>
    </div>

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
                } else {
                    dot.className = 'dot dot-red';
                    val.innerText = 'FAIL';
                }
            } catch (e) {
                document.getElementById('dot-health').className = 'dot dot-red';
                document.getElementById('val-health').innerText = 'DOWN';
            }

            // Readiness
            try {
                const res = await fetch('/ready');
                const data = await res.json();
                const dot = document.getElementById('dot-ready');
                const val = document.getElementById('val-ready');
                if (res.ok && data.status === 'ready') {
                    dot.className = 'dot dot-green';
                    val.innerText = 'READY (DB CONNECTED)';
                } else {
                    dot.className = 'dot dot-red';
                    val.innerText = 'UNAVAILABLE';
                }
            } catch (e) {
                document.getElementById('dot-ready').className = 'dot dot-red';
                document.getElementById('val-ready').innerText = 'DISCONNECTED';
            }
        }

        async function checkAvailability() {
            const checkIn = document.getElementById('search-checkin').value;
            const checkOut = document.getElementById('search-checkout').value;
            const type = document.getElementById('search-type').value;

            const tbody = document.getElementById('availability-tbody');
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">Searching...</td></tr>';

            let url = `/rooms/availability?check_in=${checkIn}&check_out=${checkOut}`;
            if (type) url += `&room_type=${type}`;

            try {
                const res = await fetch(url);
                const rooms = await res.json();
                if (!res.ok) {
                    tbody.innerHTML = `<tr><td colspan="4" style="color: var(--accent-red);">${rooms.detail || 'Error querying availability'}</td></tr>`;
                    return;
                }
                if (rooms.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">No rooms available for selected criteria.</td></tr>';
                    return;
                }
                tbody.innerHTML = rooms.map(r => `
                    <tr>
                        <td><strong>#${r.room_number}</strong></td>
                        <td><span class="pill-type">${r.room_type}</span></td>
                        <td>$${parseFloat(r.price_per_night).toFixed(2)}</td>
                        <td>
                            <button class="btn btn-outline btn-sm" onclick="selectRoomForBooking(${r.id}, '${checkIn}', '${checkOut}')">Select</button>
                        </td>
                    </tr>
                `).join('');
            } catch (e) {
                tbody.innerHTML = `<tr><td colspan="4" style="color: var(--accent-red);">Network error</td></tr>`;
            }
        }

        function selectRoomForBooking(id, checkIn, checkOut) {
            document.getElementById('book-room-id').value = id;
            document.getElementById('book-checkin').value = checkIn;
            document.getElementById('book-checkout').value = checkOut;
            window.scrollTo({ top: 100, behavior: 'smooth' });
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
                    successAlert.innerHTML = `✅ <strong>201 Created:</strong> Reservation confirmed! Booking Reference: <code>${data.booking_reference}</code> for ${data.guest_name}`;
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
                    tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted);">No reservations found.</td></tr>';
                    return;
                }
                tbody.innerHTML = items.map(r => `
                    <tr>
                        <td><code style="color: var(--accent-cyan); font-weight: bold;">${r.booking_reference}</code></td>
                        <td>#${r.room_id}</td>
                        <td>${r.guest_name}</td>
                        <td>${r.check_in}</td>
                        <td>${r.check_out}</td>
                        <td><span style="color: var(--accent-green); font-weight: bold;">${r.status}</span></td>
                        <td style="font-size: 0.78rem; color: var(--text-muted);">${new Date(r.created_at).toLocaleString()}</td>
                    </tr>
                `).join('');
            } catch (e) {
                tbody.innerHTML = '<tr><td colspan="7" style="color: var(--accent-red);">Failed to load reservations.</td></tr>';
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
