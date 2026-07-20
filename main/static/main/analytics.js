(function () {
    // Generate UUID function
    function generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    // Get or create visitor UUID
    let visitorUuid = localStorage.getItem('cte_visitor_uuid');
    if (!visitorUuid) {
        visitorUuid = generateUUID();
        localStorage.setItem('cte_visitor_uuid', visitorUuid);
    }

    // Detect device type (Mobile / Tablet / Desktop)
    function detectDevice() {
        const ua = navigator.userAgent;
        if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
            return 'Tablet';
        }
        if (/Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) {
            return 'Mobile';
        }
        return 'Desktop';
    }

    // Detect phone/tablet brand (Infinix, Samsung, Apple, Tecno, Itel, etc.)
    function detectBrand() {
        const ua = navigator.userAgent;
        // African / popular global brands
        if (/Infinix/i.test(ua))          return 'Infinix';
        if (/TECNO/i.test(ua))            return 'Tecno';
        if (/itel/i.test(ua))             return 'Itel';
        if (/Oukitel/i.test(ua))          return 'Oukitel';
        if (/Itel/i.test(ua))             return 'Itel';
        // Global brands
        if (/iPhone|iPad|iPod/i.test(ua)) return 'Apple';
        if (/Samsung/i.test(ua))          return 'Samsung';
        if (/Huawei|HUAWEI/i.test(ua))   return 'Huawei';
        if (/Xiaomi|Redmi|POCO/i.test(ua)) return 'Xiaomi';
        if (/OnePlus/i.test(ua))          return 'OnePlus';
        if (/Oppo|OPPO/i.test(ua))       return 'Oppo';
        if (/Vivo|vivo/i.test(ua))        return 'Vivo';
        if (/Realme/i.test(ua))           return 'Realme';
        if (/Nokia/i.test(ua))            return 'Nokia';
        if (/Motorola|moto/i.test(ua))    return 'Motorola';
        if (/LG/i.test(ua))              return 'LG';
        if (/Sony/i.test(ua))            return 'Sony';
        if (/HTC/i.test(ua))             return 'HTC';
        if (/BlackBerry|BB10/i.test(ua)) return 'BlackBerry';
        if (/Windows Phone/i.test(ua))   return 'Windows Phone';
        // Fallback to device type
        const dtype = detectDevice();
        return dtype === 'Desktop' ? 'Desktop/PC' : 'Unknown Mobile';
    }

    function detectBrowser() {
        const ua = navigator.userAgent;
        if (ua.includes("Chrome") && !ua.includes("Chromium") && !ua.includes("Edg")) return "Chrome";
        if (ua.includes("Safari") && !ua.includes("Chrome")) return "Safari";
        if (ua.includes("Firefox")) return "Firefox";
        if (ua.includes("Edg")) return "Edge";
        if (ua.includes("OPR") || ua.includes("Opera")) return "Opera";
        return "Unknown";
    }

    // Capture referrer safely
    const referrer = document.referrer || '';
    const path = window.location.pathname;
    
    // Blog post identifier from body attribute
    const blogPostId = document.body.getAttribute('data-post-id') || null;

    let pageViewId = null;
    let secondsSpent = 0;
    let maxScrollDepth = 0;
    let timerInterval = null;

    // Track scroll depth
    function getScrollPercent() {
        const h = document.documentElement;
        const b = document.body;
        const st = 'scrollTop';
        const sh = 'scrollHeight';
        return Math.round((h[st] || b[st]) / ((h[sh] || b[sh]) - h.clientHeight) * 100) || 0;
    }

    window.addEventListener('scroll', () => {
        const currentScroll = getScrollPercent();
        if (currentScroll > maxScrollDepth) {
            maxScrollDepth = Math.min(currentScroll, 100);
        }
    });

    // Send tracking request after location is determined
    function initTracking(locationData = {}) {
        const payload = {
            visitor_uuid: visitorUuid,
            path: path,
            referrer: referrer,
            blog_post_id: blogPostId,
            device_type: detectDevice(),
            device_brand: detectBrand(),
            browser: detectBrowser(),
            country: locationData.country_name || 'Unknown',
            region: locationData.region || 'Unknown',
            city: locationData.city || 'Unknown'
        };

        fetch('/analytics/track-pageview/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                pageViewId = data.page_view_id;
                // Start heartbeat timer
                startHeartbeat();
            }
        })
        .catch(err => console.error('Analytics pageview track failed', err));
    }

    function sendHeartbeat(isBeacon = false) {
        if (!pageViewId) return;

        const payload = JSON.stringify({
            page_view_id: pageViewId,
            duration_seconds: secondsSpent,
            scroll_depth: maxScrollDepth
        });

        if (isBeacon && navigator.sendBeacon) {
            navigator.sendBeacon('/analytics/track-heartbeat/', payload);
        } else {
            fetch('/analytics/track-heartbeat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: payload,
                keepalive: true
            }).catch(() => {});
        }
    }

    function startHeartbeat() {
        timerInterval = setInterval(() => {
            secondsSpent += 10;
            sendHeartbeat();
        }, 10000);
    }

    // Flush last heartbeat on page exit
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
            sendHeartbeat(true);
        }
    });

    // Location Lookup Client-Side
    fetch('https://ipapi.co/json/')
        .then(res => {
            if (!res.ok) throw new Error();
            return res.json();
        })
        .then(data => initTracking(data))
        .catch(() => {
            // Fallback lookup if ipapi.co is blocked or rate-limited
            fetch('https://ip-api.com/json/')
                .then(res => res.json())
                .then(data => {
                    initTracking({
                        country_name: data.country,
                        region: data.regionName,
                        city: data.city
                    });
                })
                .catch(() => initTracking()); // Track with empty location if both fail
        });
})();
