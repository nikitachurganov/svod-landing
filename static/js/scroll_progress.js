(function () {
    var root = document.getElementById("scrollProgress");
    var fill = document.getElementById("scrollProgressFill");
    if (!root || !fill) return;

    function clamp(n, min, max) {
        return Math.min(Math.max(n, min), max);
    }

    function update() {
        var el = document.documentElement;
        var scrollTop = window.scrollY || el.scrollTop || 0;
        var viewH = window.innerHeight || el.clientHeight || 0;
        var totalH = el.scrollHeight || 0;
        var maxScroll = totalH - viewH;
        var ratio = maxScroll <= 0 ? 1 : clamp(scrollTop / maxScroll, 0, 1);
        var pct = Math.round(ratio * 100);

        fill.style.width = pct + "%";
        root.setAttribute("aria-valuenow", String(pct));
    }

    var ticking = false;
    function onScrollOrResize() {
        if (!ticking) {
            window.requestAnimationFrame(function () {
                ticking = false;
                update();
            });
            ticking = true;
        }
    }

    window.addEventListener("scroll", onScrollOrResize, { passive: true });
    window.addEventListener("resize", onScrollOrResize);
    if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(update).catch(update);
    }
    update();
})();
