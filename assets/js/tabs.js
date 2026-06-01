// Progressive enhancement only: the first tab/panel is already active server-side,
// so the dashboard works with JavaScript disabled. This just switches tabs.
(function () {
  "use strict";
  var buttons = Array.prototype.slice.call(document.querySelectorAll(".tab-button"));
  var panels = Array.prototype.slice.call(document.querySelectorAll(".tab-panel"));
  if (!buttons.length) return;

  function activate(slug) {
    buttons.forEach(function (b) {
      var on = b.getAttribute("data-tab") === slug;
      b.classList.toggle("active", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    panels.forEach(function (p) {
      var on = p.id === "panel-" + slug;
      p.classList.toggle("active", on);
      if (on) { p.removeAttribute("hidden"); } else { p.setAttribute("hidden", ""); }
    });
  }

  buttons.forEach(function (b) {
    b.addEventListener("click", function () { activate(b.getAttribute("data-tab")); });
  });
})();
