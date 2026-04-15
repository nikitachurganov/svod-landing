(function () {
    var topBar = document.querySelector(".site-top");
    if (!topBar) return;

    var lastY = window.scrollY;
    var threshold = 14;
    var topZone = 40;
    var ticking = false;
    var locked = false;

    function setTopHidden(hidden) {
        if (locked) return;
        topBar.classList.toggle("site-top--hidden", hidden);
        topBar.classList.toggle("site-top--visible", !hidden);
    }

    window.lockSiteTopVisible = function () {
        locked = true;
        topBar.classList.remove("site-top--hidden");
        topBar.classList.add("site-top--visible");
    };

    window.unlockSiteTop = function () {
        locked = false;
        lastY = window.scrollY;
    };

    function onScrollFrame() {
        ticking = false;
        var y = window.scrollY;
        var delta = y - lastY;

        if (y <= topZone) {
            setTopHidden(false);
        } else if (delta > threshold) {
            setTopHidden(true);
        } else if (delta < -threshold) {
            setTopHidden(false);
        }

        lastY = y;
    }

    function onScroll() {
        if (!ticking) {
            window.requestAnimationFrame(onScrollFrame);
            ticking = true;
        }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    lastY = window.scrollY;

    var logo = document.querySelector(".site-header__logo");
    if (logo) {
        logo.addEventListener("click", function (e) {
            var path = window.location.pathname.replace(/\/$/, "") || "/";
            if (path !== "/") return;

            e.preventDefault();
            var instant = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
            window.scrollTo({
                top: 0,
                behavior: instant ? "auto" : "smooth",
            });
        });
    }
})();
