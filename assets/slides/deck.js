// Lecture decks: show one slide at a time. Without this script the slides
// simply stack, so everything stays readable.
(function () {
  var slides = Array.prototype.slice.call(document.querySelectorAll(".slide"));
  if (!slides.length) {
    return;
  }
  document.documentElement.classList.add("js");

  // Shrink a code block whose longest line is too wide, down to 75%. The
  // ratio holds at any stage size, so it also suits the printed slides.
  function fitCode() {
    Array.prototype.forEach.call(document.querySelectorAll(".slide pre"), function (pre) {
      pre.style.removeProperty("--fit");
      var style = getComputedStyle(pre);
      var pad = parseFloat(style.paddingLeft) + parseFloat(style.paddingRight);
      var ratio = (pre.clientWidth - pad) / (pre.scrollWidth - pad);
      if (ratio < 1) {
        pre.style.setProperty("--fit", Math.max(0.75, Math.floor(ratio * 98) / 100));
      }
    });
  }
  fitCode();
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(fitCode);
  }

  var counter = document.querySelector('[data-deck="current"]');
  var bar = document.querySelector(".deck-progress span");
  var current = 0;

  function fromHash() {
    var n = parseInt(location.hash.replace("#slide-", "").replace("#", ""), 10);
    return isNaN(n) ? 0 : Math.min(Math.max(n - 1, 0), slides.length - 1);
  }

  function show(index) {
    current = Math.min(Math.max(index, 0), slides.length - 1);
    slides.forEach(function (slide, i) {
      var on = i === current;
      slide.classList.toggle("is-current", on);
      slide.setAttribute("aria-hidden", on ? "false" : "true");
    });
    if (counter) {
      counter.textContent = current + 1;
    }
    if (bar) {
      bar.style.width = ((current + 1) / slides.length) * 100 + "%";
    }
    var hash = "#" + (current + 1);
    if (location.hash !== hash) {
      history.replaceState(null, "", hash);
    }
  }

  function fullscreen() {
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen();
    }
  }

  document.addEventListener("keydown", function (event) {
    if (event.altKey || event.ctrlKey || event.metaKey) {
      return;
    }
    switch (event.key) {
      case "ArrowRight":
      case "ArrowDown":
      case "PageDown":
      case "Enter":
        show(current + 1);
        break;
      case " ":
        show(event.shiftKey ? current - 1 : current + 1);
        break;
      case "ArrowLeft":
      case "ArrowUp":
      case "PageUp":
      case "Backspace":
        show(current - 1);
        break;
      case "Home":
        show(0);
        break;
      case "End":
        show(slides.length - 1);
        break;
      case "f":
      case "F":
        fullscreen();
        break;
      default:
        return;
    }
    event.preventDefault();
  });

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-deck]");
    if (!button) {
      return;
    }
    var action = button.getAttribute("data-deck");
    if (action === "prev") {
      show(current - 1);
    } else if (action === "next") {
      show(current + 1);
    } else if (action === "fullscreen") {
      fullscreen();
    }
  });

  var touchX = null;
  document.addEventListener("touchstart", function (event) {
    touchX = event.touches[0].clientX;
  }, { passive: true });
  document.addEventListener("touchend", function (event) {
    if (touchX === null) {
      return;
    }
    var dx = event.changedTouches[0].clientX - touchX;
    touchX = null;
    if (Math.abs(dx) > 50) {
      show(dx < 0 ? current + 1 : current - 1);
    }
  });

  window.addEventListener("hashchange", function () {
    show(fromHash());
  });

  show(fromHash());
})();
