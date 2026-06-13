/* SITE OVERRIDE of Congo v2.14.0 js/appearance.js (added 20260613).
   Only change vs theme: the two pre-paint setThemeColor() calls (in the initial
   appearance block and the auto-appearance block) are removed. Those call
   window.getComputedStyle(), which forces a synchronous style recalc before the
   render-blocking CSS bundle has loaded, causing Firefox to paint a flash of
   unstyled content on CDN-served pages. The class is still set synchronously
   (cheap, no reflow), and setThemeColor() still runs at DOMContentLoaded below,
   so the <meta name=theme-color> is still updated. The static meta theme-color
   already holds the correct value before JS runs, so nothing is lost visually.
   Re-sync if Congo is upgraded past v2.14.0. */
const sitePreference = document.documentElement.getAttribute("data-default-appearance");
const userPreference = localStorage.getItem("appearance");

function getCSSValue(varName) {
  var cssValue = window.getComputedStyle(document.documentElement).getPropertyValue(varName);
  return "rgb(" + cssValue.replace(/\s+/g, "") + ")";
}

function setThemeColor() {
  var metaThemeColor = document.querySelector("meta[name=theme-color]");
  document.documentElement.classList.contains("dark")
    ? metaThemeColor.setAttribute("content", getCSSValue("--color-neutral-800"))
    : metaThemeColor.setAttribute("content", getCSSValue("--color-neutral"));
  return true;
}

if ((sitePreference === "dark" && userPreference === null) || userPreference === "dark") {
  document.documentElement.classList.add("dark");
}

if (document.documentElement.getAttribute("data-auto-appearance") === "true") {
  if (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches &&
    userPreference !== "light"
  ) {
    document.documentElement.classList.add("dark");
  }
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (event) => {
    if (event.matches) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    setThemeColor();
  });
}

function add_to_top_elem() {
  var body = document.body;
  var html = document.documentElement;

  const height =
    Math.max(
      body.scrollHeight,
      body.offsetHeight,
      html.clientHeight,
      html.scrollHeight,
      html.offsetHeight
    ) - 150;

  const elem = document.getElementById("to-top");
  if (elem === null || elem === undefined) {
    return;
  }

  elem.hidden = height < window.innerHeight;
}

window.addEventListener("DOMContentLoaded", (event) => {
  add_to_top_elem();
  setThemeColor();
  var switchers = document.querySelectorAll("[id^='appearance-switcher']");
  switchers.forEach((switcher) => {
    switcher.addEventListener("click", () => {
      document.documentElement.classList.toggle("dark");
      setThemeColor();
      localStorage.setItem(
        "appearance",
        document.documentElement.classList.contains("dark") ? "dark" : "light"
      );
    });
    switcher.addEventListener("contextmenu", (event) => {
      event.preventDefault();
      localStorage.removeItem("appearance");
    });
  });
});
