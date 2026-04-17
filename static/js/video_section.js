/**
 * Показывает кастомную заглушку, пока демо-видео недоступно;
 * при успешной загрузке плавно показывает <video>.
 */
(function () {
    var frame = document.querySelector(".video-section__frame");
    var video = frame && frame.querySelector(".video-section__media");
    if (!frame || !video) return;

    function markReady() {
        frame.classList.remove("video-section__frame--error");
        frame.classList.add("video-section__frame--ready");
    }

    function markError() {
        frame.classList.remove("video-section__frame--ready");
        frame.classList.add("video-section__frame--error");
    }

    video.addEventListener(
        "loadeddata",
        function () {
            markReady();
        },
        { once: true }
    );

    video.addEventListener("error", function () {
        markError();
    });

    if (video.error) {
        markError();
        return;
    }

    if (video.readyState >= 2) {
        markReady();
    }
})();
