/* ActiveSPN-only reader configuration for the bundled PDF.js 6.5.438. */
(() => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("profile") !== "activespn") return;
  const file = new URL(params.get("file") || "", document.baseURI);
  if (!file.pathname.endsWith("/activespn.pdf")) return;

  document.documentElement.classList.add("activespn-reader");
  const stylesheet = document.createElement("link");
  stylesheet.rel = "stylesheet";
  stylesheet.href = "activespn.css";
  document.head.append(stylesheet);

  const desktop = window.matchMedia("(min-width: 720px)");
  const OUTLINE = 2;
  const NONE = 0;

  // The published PDF has no embedded outline. Heading positions are measured
  // from its top edge in points (page height: 792 pt). XYZ uses a bottom origin.
  // Keep a small margin above each heading, without changing the user's zoom.
  const section = (title, page, top, items = []) => ({
    title, dest: [page - 1, { name: "XYZ" }, null, 792 - top + 8, null],
    bold: false, italic: false, color: new Uint8ClampedArray(3),
    count: items.length ? -items.length : 0, items,
  });
  const outline = [
    section("Abstract", 1, 164.11),
    section("I. Introduction", 1, 426.21),
    section("II. ActiveSPN for In-Finger Manipulation With Omni-Directional Adaptation", 2, 430.78),
    section("III. In-Finger Pose Estimation for Objects", 3, 657.93, [
      section("1. Encoder-Decoder Architecture", 3, 674.74),
      section("2. Pose Estimation", 4, 333.56),
      section("3. Data Collection Platform & Data Transformation in SE(3)", 4, 626.92),
    ]),
    section("IV. Experiment and Results", 5, 496.53, [
      section("A. Evaluation of Gripper Design on Grasping Success Rate", 5, 512.23),
      section("B. In-Finger Manipulation of YCB Objects", 5, 657.81),
      section("C. Evaluation of In-Finger Object Pose Estimation", 6, 669.76),
      section("D. Closed-Loop In-Finger Manipulation", 7, 514.34),
    ]),
    section("V. Concluding Remarks", 7, 669.88),
    section("References", 8, 387.88),
  ];

  let eventDocument = document;
  try { eventDocument = window.parent.document; } catch { /* Standalone reader. */ }
  const configure = event => {
    if (event.detail?.source !== window) return;
    eventDocument.removeEventListener("webviewerloaded", configure);
    const app = window.PDFViewerApplication;
    const options = window.PDFViewerApplicationOptions;
    options.set("defaultZoomValue", "auto");
    options.set("sidebarViewOnLoad", desktop.matches ? OUTLINE : NONE);
    options.set("viewerCssTheme", 1);
    options.set("viewOnLoad", 1);
    options.set("ignoreDestinationZoom", true);
    options.set("annotationEditorMode", 0);
    options.set("enableNewAltTextWhenAddingImage", false);

    app.initializedPromise.then(() => {
      let outlineInstalled = false;
      app.eventBus.on("outlineloaded", ({ outlineCount }) => {
        if (outlineInstalled) return;
        outlineInstalled = true;
        // Wait until the native empty-outline handler has finished. A genuine
        // outline in a future PDF takes precedence over this page navigation.
        queueMicrotask(() => {
          if (!outlineCount) {
            app.pdfOutlineViewer.render({ outline, pdfDocument: app.pdfDocument });
          }
          app.viewsManager.switchView(OUTLINE, desktop.matches);
        });
      });
      desktop.addEventListener("change", () => {
        if (!outlineInstalled) return;
        app.viewsManager.switchView(desktop.matches ? OUTLINE : NONE, desktop.matches);
      });
    });
  };
  eventDocument.addEventListener("webviewerloaded", configure);
})();
