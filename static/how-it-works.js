(function () {
    var root = document.querySelector('.how-it-works');
    if (!root) return;

    var grid = root.querySelector('.how-it-works__grid');
    var list = root.querySelector('.how-it-works__steps');
    var steps = Array.from(root.querySelectorAll('.how-it-works__step'));
    var DURATION_MS = 20000;
    var activeIndex = 0;
    var timerId = null;

    function clearTimer() {
        if (timerId !== null) {
            clearTimeout(timerId);
            timerId = null;
        }
    }

    function prefersReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    function restartBarAnimation(bar) {
        bar.classList.remove('how-it-works__step-progress-bar--animating');
        void bar.offsetWidth;
        if (!prefersReducedMotion()) {
            bar.classList.add('how-it-works__step-progress-bar--animating');
        }
    }

    function scheduleAdvance() {
        clearTimer();
        timerId = setTimeout(function () {
            timerId = null;
            var next = (activeIndex + 1) % steps.length;
            activate(next);
        }, DURATION_MS);
    }

    function applyVisualState(index, skipBarRestart) {
        steps.forEach(function (li, i) {
            var on = i === index;
            li.classList.toggle('how-it-works__step--active', on);
            var btn = li.querySelector('.how-it-works__step-row');
            var panel = li.querySelector('.how-it-works__step-details');
            var bar = li.querySelector('.how-it-works__step-progress-bar');
            btn.setAttribute('aria-expanded', String(on));
            if (on) {
                panel.removeAttribute('aria-hidden');
                if (!skipBarRestart) {
                    restartBarAnimation(bar);
                }
            } else {
                panel.setAttribute('aria-hidden', 'true');
                bar.classList.remove('how-it-works__step-progress-bar--animating');
            }
        });
    }

    function activate(index) {
        activeIndex = index;
        applyVisualState(index, false);
        scheduleAdvance();
    }

    function restartCurrent() {
        var bar = steps[activeIndex].querySelector('.how-it-works__step-progress-bar');
        restartBarAnimation(bar);
        scheduleAdvance();
    }

    function isTwoColumnLayout() {
        return window.matchMedia('(min-width: 900.02px)').matches;
    }

    function measureMaxListHeight() {
        if (!grid || !list || steps.length === 0) return;

        if (!isTwoColumnLayout()) {
            grid.style.minHeight = '';
            return;
        }

        var saved = activeIndex;
        clearTimer();
        root.classList.add('how-it-works--measuring');

        var maxH = 0;
        for (var i = 0; i < steps.length; i++) {
            activeIndex = i;
            applyVisualState(i, true);
            void list.offsetHeight;
            var h = list.getBoundingClientRect().height;
            if (h > maxH) {
                maxH = Math.ceil(h);
            }
        }

        root.classList.remove('how-it-works--measuring');
        if (maxH > 0) {
            grid.style.minHeight = maxH + 'px';
        }

        activate(saved);
    }

    function debounce(fn, ms) {
        var t = null;
        return function () {
            clearTimeout(t);
            var args = arguments;
            t = setTimeout(function () {
                fn.apply(null, args);
            }, ms);
        };
    }

    steps.forEach(function (li, i) {
        li.querySelector('.how-it-works__step-row').addEventListener('click', function () {
            if (i === activeIndex) {
                restartCurrent();
            } else {
                activate(i);
            }
        });
    });

    activate(0);

    function runMeasure() {
        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(measureMaxListHeight);
        } else {
            measureMaxListHeight();
        }
    }

    requestAnimationFrame(function () {
        requestAnimationFrame(runMeasure);
    });

    window.addEventListener('resize', debounce(runMeasure, 150));
})();
