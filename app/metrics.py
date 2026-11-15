try:
    from prometheus_client import (
        CONTENT_TYPE_LATEST,
        Counter,
        Histogram,
        generate_latest,
    )

    REQUESTS_TOTAL = Counter(
        "hotel_requests_total",
        "Total HTTP requests received by the service",
        ["method", "endpoint", "status_code"],
    )

    BOOKING_CONFLICTS_TOTAL = Counter(
        "hotel_booking_conflicts_total",
        "Total reservation booking conflicts encountered (409 Conflict)",
    )

    BOOKINGS_CONFIRMED_TOTAL = Counter(
        "hotel_bookings_confirmed_total",
        "Total reservations successfully confirmed (201 Created)",
    )

    REQUEST_LATENCY = Histogram(
        "hotel_request_duration_seconds",
        "HTTP request duration in seconds",
        ["endpoint"],
    )

    def get_latest_metrics() -> tuple[bytes, str]:
        return generate_latest(), CONTENT_TYPE_LATEST

except ImportError:
    # Graceful fallback if prometheus_client is not yet imported
    REQUESTS_TOTAL = None
    BOOKING_CONFLICTS_TOTAL = None
    BOOKINGS_CONFIRMED_TOTAL = None
    REQUEST_LATENCY = None

    def get_latest_metrics() -> tuple[bytes, str]:
        content = (
            "# HELP hotel_requests_total Total HTTP requests\n"
            "# TYPE hotel_requests_total counter\n"
            "hotel_requests_total 0\n"
        )
        return content.encode("utf-8"), "text/plain; version=0.0.4; charset=utf-8"
