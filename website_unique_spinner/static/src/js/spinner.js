(function () {
    "use strict";

    var OVERLAY_ID = "uws-overlay";
    var DISPLAY_MS = 2000; // <-- change this to control how long the initial spinner shows (ms)

    function getOverlay() {
        return document.getElementById(OVERLAY_ID);
    }

    function hideOverlay() {
        var el = getOverlay();
        if (el) {
            el.classList.add("uws-hidden");
        }
    }

    function showOverlay(transition) {
        var el = getOverlay();
        if (el) {
            el.classList.remove("uws-hidden");
            el.classList.toggle("uws-transition", !!transition);
        }
    }

    setTimeout(hideOverlay, DISPLAY_MS);

    window.addEventListener("pageshow", function (ev) {
        if (ev.persisted) {
            hideOverlay();
        }
    });

    function isInternalNavigableLink(link) {
        if (!link || !link.href) return false;
        if (link.target && link.target !== "" && link.target !== "_self") return false;
        if (link.hasAttribute("download")) return false;
        if (link.dataset && (link.dataset.bsToggle || link.dataset.toggle)) return false;

        var href = link.getAttribute("href") || "";
        if (!href || href.charAt(0) === "#") return false;
        if (href.indexOf("mailto:") === 0 || href.indexOf("tel:") === 0 || href.indexOf("javascript:") === 0) {
            return false;
        }

        try {
            var url = new URL(link.href, window.location.href);
            if (url.origin !== window.location.origin) return false;
            // Same-page anchor jump: don't show a spinner for that.
            if (url.pathname === window.location.pathname && url.hash) return false;
        } catch (e) {
            return false;
        }

        return true;
    }

    document.addEventListener("click", function (ev) {
        if (ev.defaultPrevented || ev.button !== 0) return;
        if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;

        var link = ev.target.closest ? ev.target.closest("a") : null;
        if (isInternalNavigableLink(link)) {
            showOverlay(true);
        }
    });

    document.addEventListener("submit", function (ev) {
        var form = ev.target;
        if (form && !form.classList.contains("uws-no-spinner")) {
            showOverlay(true);
        }
    });
})();
