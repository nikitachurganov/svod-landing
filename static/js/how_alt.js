(function () {
    "use strict";

    var section = document.querySelector(".how-alt");
    if (!section) return;

    var innerEl = section.querySelector(".how-alt__inner");
    var headerEl = section.querySelector(".how-alt-header");
    var cardsWrap = section.querySelector(".how-alt__cards");
    var cards = Array.from(section.querySelectorAll(".how-alt__card"));
    var cardCount = cards.length;

    var ticking = false;
    var movingCards = cardCount > 1 ? cards.slice(1) : [];
    var segmentCount = movingCards.length;

    function getGapPx() {
        if (!innerEl) return 160;
        var g = window.getComputedStyle(innerEl).rowGap || window.getComputedStyle(innerEl).gap;
        var n = parseFloat(g);
        return isNaN(n) ? 160 : n;
    }

    function applyInitialState() {
        if (cardsWrap) cardsWrap.style.transform = "translateY(0)";
        if (segmentCount === 0) return;
        cards[0].style.transform = "translateY(0)";
        cards[0].style.zIndex = "1";
        for (var i = 0; i < movingCards.length; i++) {
            movingCards[i].style.transform = "translateY(100vh)";
            movingCards[i].style.zIndex = String(2 + i);
        }
    }

    function onScroll() {
        if (ticking) return;

        ticking = true;
        requestAnimationFrame(function () {
            ticking = false;

            var rect = section.getBoundingClientRect();
            var sectionHeight = section.offsetHeight;
            var viewportHeight = window.innerHeight;
            var scrolled = -rect.top;
            var scrollable = sectionHeight - viewportHeight;

            if (scrollable <= 0) return;

            var progress = Math.max(0, Math.min(1, scrolled / scrollable));

            if (cardsWrap && headerEl) {
                var liftMax = headerEl.offsetHeight + getGapPx();
                cardsWrap.style.transform = "translateY(" + -liftMax * progress + "px)";
            }

            if (segmentCount === 0) return;

            var segmentSize = 1 / segmentCount;

            for (var i = 0; i < segmentCount; i++) {
                var segStart = i * segmentSize;
                var segEnd = segStart + segmentSize;
                var yVh;
                if (progress >= segEnd) {
                    yVh = 0;
                } else if (progress < segStart) {
                    yVh = 100;
                } else {
                    var cardProgress = (progress - segStart) / segmentSize;
                    yVh = (1 - cardProgress) * 100;
                }
                movingCards[i].style.transform = "translateY(" + yVh + "vh)";
            }
        });
    }

    function handleResize() {
        applyInitialState();
        onScroll();
    }

    applyInitialState();
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", handleResize, { passive: true });
})();
