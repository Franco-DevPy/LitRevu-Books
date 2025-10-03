// Gestion des messages flash (auto disparition + fermeture manuelle)
(function () {
  function fadeAndRemove(el) {
    if (!el) return;
    el.classList.add("fade-out");
    setTimeout(function () {
      if (el && el.parentNode) el.parentNode.removeChild(el);
    }, 500);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var messages = document.querySelectorAll(".messages .message");
    messages.forEach(function (msg) {
      var timeout = parseInt(msg.getAttribute("data-timeout"), 10);
      if (!isNaN(timeout) && timeout > 0) {
        setTimeout(function () {
          fadeAndRemove(msg);
        }, timeout);
      }
      var closeBtn = msg.querySelector(".message-close");
      if (closeBtn) {
        closeBtn.addEventListener("click", function () {
          fadeAndRemove(msg);
        });
      }
    });
  });
})();
