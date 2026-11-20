/* ActiveSPN paper readers for the bundled PDF.js 6.5.438. */
(() => {
  const params = new URLSearchParams(window.location.search);
  const profile = params.get("profile");
  const files = { activespn: "activespn.pdf", activespn2: "activespn2.pdf" };
  if (!Object.hasOwn(files, profile)) return;
  const file = new URL(params.get("file") || "", document.baseURI);
  if (!file.pathname.endsWith(`/${files[profile]}`)) return;

  document.documentElement.classList.add("activespn-reader");
  const stylesheet = document.createElement("link");
  stylesheet.rel = "stylesheet";
  stylesheet.href = "activespn.css";
  document.head.append(stylesheet);

  const desktop = window.matchMedia("(min-width: 720px)");
  const OUTLINE = 2;
  const NONE = 0;

  // Neither supplied PDF has an embedded outline. Heading positions are measured
  // from its top edge in points. XYZ uses a bottom origin. ActiveSPN2 is an image
  // PDF: its headings were checked against the rendered article-in-press pages.
  // Keep a small margin above each heading, without changing the user's zoom.
  const pageHeight = profile === "activespn2" ? 841.92004 : 792;
  const section = (title, page, top, items = []) => ({
    title, dest: [page - 1, { name: "XYZ" }, null, pageHeight - top + 8, null],
    bold: false, italic: false, color: new Uint8ClampedArray(3),
    count: items.length ? -items.length : 0, items,
  });
  const outlines = { activespn: [
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
  ], activespn2: [
    section("Abstract", 1, 289.96),
    section("1. Introduction", 1, 474.55),
    section("2. ActiveSPN2 as soft active surfaces", 3, 405.16, [
      section("2.1. Specifications of ActiveSPN2 module", 3, 499.42),
      section("2.2. Dynamics of ActiveSPN2 module", 4, 645.38),
      section("2.3. Dynamics of ActiveSPN2 gripper", 5, 235.64),
    ]),
    section("3. Multi-modal VBDormP architecture", 5, 569.45, [
      section("3.1. In-finger deformation tracking", 5, 644.07),
      section("3.2. Multi-modal generative architecture", 5, 687.93),
      section("3.3. Data collection platform", 7, 517.09),
    ]),
    section("4. Experiments and results", 8, 491.56, [
      section("4.1. System characterization and performance", 8, 513.16, [
        section("4.1.1. Quantification of adaptive kinesthesia under external loading", 8, 611.35),
        section("4.1.2. Bending angle and gripping force", 9, 383.56),
        section("4.1.3. Gripper structural reliability and object handling performance", 9, 89.67),
        section("4.1.4. In-finger manipulation and object reorientation", 9, 610.04),
      ]),
      section("4.2. Validation of the multi-modal perception framework", 10, 514.47, [
        section("4.2.1. Competitive grasping with human interaction", 10, 601.53),
        section("4.2.2. Experimental validation of force estimation", 10, 317.45),
        section("4.2.3. Peg-in task demonstrations in confined spaces", 11, 439.20),
      ]),
      section("4.3. Demonstration of in-finger dexterity and robustness", 11, 594.98),
    ]),
    section("5. Conclusion", 12, 410.40),
    section("CRediT authorship contribution statement", 12, 89.67),
    section("Declaration of competing interest", 12, 182.62),
    section("Acknowledgments", 12, 244.15),
    section("Appendix A. Supplementary data", 12, 326.62),
    section("References", 12, 377.67),
  ] };
  const outline = outlines[profile];

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
