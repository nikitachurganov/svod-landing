(function () {
    var el = document.getElementById('phone');
    if (!el) return;

    var MASK = '+7 (___) ___ - __ - __';
    var SLOTS = [];
    for (var i = 0; i < MASK.length; i++) {
        if (MASK[i] === '_') SLOTS.push(i);
    }
    var FIRST = SLOTS[0];
    var active = false;
    var digits = [];

    function render() {
        var out = MASK.split('');
        for (var i = 0; i < SLOTS.length; i++) {
            out[SLOTS[i]] = i < digits.length ? digits[i] : '_';
        }
        return out.join('');
    }

    function paint(slotIdx) {
        el.value = render();
        var pos;
        if (slotIdx >= digits.length && digits.length < SLOTS.length) {
            pos = SLOTS[digits.length];
        } else if (slotIdx < SLOTS.length) {
            pos = SLOTS[slotIdx];
        } else {
            pos = el.value.length;
        }
        pos = Math.max(FIRST, pos);
        el.setSelectionRange(pos, pos);
    }

    function slotAt(caret) {
        for (var i = 0; i < SLOTS.length; i++) {
            if (SLOTS[i] >= caret) return i;
        }
        return SLOTS.length;
    }

    function cleanPasted(raw) {
        var d = (raw || '').replace(/\D/g, '');
        if (d.length >= 11 && (d[0] === '7' || d[0] === '8')) return d.slice(1, 11);
        if (d.length >= 10 && d[0] === '9') return d.slice(0, 10);
        return d;
    }

    function activate() {
        if (active) return;
        active = true;
        paint(0);
    }

    function deactivate() {
        active = false;
        if (digits.length === 0) {
            el.value = '';
        }
    }

    var biHandled = false;

    el.addEventListener('beforeinput', function (e) {
        e.preventDefault();
        biHandled = true;
        activate();

        var s = Math.min(el.selectionStart || 0, el.value.length);
        var end = Math.min(el.selectionEnd || 0, el.value.length);
        var sS = slotAt(s);
        var sE = slotAt(end);
        var t = e.inputType;

        if (t === 'insertText' || t === 'insertFromPaste' || t === 'insertFromDrop' || t === 'insertReplacementText') {
            var data = e.data;
            if (!data && e.dataTransfer) data = e.dataTransfer.getData('text/plain');
            var add = cleanPasted(data).split('');
            if (!add.length) return;
            if (s !== end) digits.splice(sS, sE - sS);
            var room = SLOTS.length - digits.length;
            var chunk = add.slice(0, room);
            for (var i = 0; i < chunk.length; i++) {
                digits.splice(sS + i, 0, chunk[i]);
            }
            paint(sS + chunk.length);
            return;
        }

        if (t === 'deleteContentBackward' || t === 'deleteWordBackward' || t === 'deleteSoftLineBackward' || t === 'deleteHardLineBackward') {
            if (s !== end) {
                digits.splice(sS, sE - sS);
                paint(sS);
            } else if (sS > 0) {
                digits.splice(sS - 1, 1);
                paint(sS - 1);
            } else {
                paint(0);
            }
            return;
        }

        if (t === 'deleteContentForward' || t === 'deleteWordForward' || t === 'deleteByCut') {
            if (s !== end) {
                digits.splice(sS, sE - sS);
            } else if (sS < digits.length) {
                digits.splice(sS, 1);
            }
            paint(sS);
            return;
        }

        paint(slotAt(s));
    });

    el.addEventListener('input', function () {
        if (biHandled) {
            biHandled = false;
            return;
        }
        activate();
        var d = el.value.replace(/\D/g, '');
        if (d.length >= 11 && (d[0] === '7' || d[0] === '8')) {
            d = d.slice(1);
        } else if (d.length >= 1 && d[0] === '7') {
            d = d.slice(1);
        }
        digits = d.slice(0, SLOTS.length).split('');
        paint(digits.length);
    });

    el.addEventListener('click', function () {
        if (!active) return;
        var p = el.selectionStart || 0;
        if (p < FIRST) el.setSelectionRange(FIRST, FIRST);
    });

    el.addEventListener('focus', function () {
        activate();
    });

    el.addEventListener('blur', function () {
        deactivate();
    });

    el.addEventListener('keydown', function (e) {
        if (e.key === 'Home' && !e.shiftKey) {
            e.preventDefault();
            el.setSelectionRange(FIRST, FIRST);
        }
        if (e.key === 'ArrowLeft' && !e.shiftKey) {
            var p = el.selectionStart || 0;
            if (p <= FIRST) {
                e.preventDefault();
                el.setSelectionRange(FIRST, FIRST);
            }
        }
    });

    function resetField() {
        digits = [];
        active = false;
        el.value = '';
    }
    window.resetContactPhoneField = resetField;

    el.setAttribute('type', 'tel');
    el.setAttribute('inputmode', 'numeric');
    el.setAttribute('autocomplete', 'tel');
    el.setAttribute('maxlength', String(MASK.length));
    el.value = '';
})();
