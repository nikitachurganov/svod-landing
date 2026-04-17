(function () {
    var root = document.querySelector(".pricing");
    if (!root) return;

    var cards = root.querySelectorAll(".js-pricing-card");
    var options = root.querySelectorAll(".pricing__toggle-option");

    function setActiveClasses() {
        options.forEach(function (opt) {
            var input = opt.querySelector('input[name="pricing-period"]');
            opt.classList.toggle("pricing__toggle-option--active", !!(input && input.checked));
        });
    }

    function updatePrices(period) {
        var isYear = period === "year";
        cards.forEach(function (card) {
            var el = card.querySelector(".js-pricing-price-value");
            if (!el) return;
            var val = isYear ? card.getAttribute("data-price-year") : card.getAttribute("data-price-month");
            el.classList.add("pricing__card-price-value--fade");
            window.setTimeout(function () {
                el.textContent = val || "—";
                el.classList.remove("pricing__card-price-value--fade");
            }, 120);
        });
        setActiveClasses();
    }

    root.querySelectorAll('input[name="pricing-period"]').forEach(function (radio) {
        radio.addEventListener("change", function () {
            if (radio.checked) updatePrices(radio.value);
        });
    });

    setActiveClasses();
})();
