/* ActiveSPN paper readers for the bundled PDF.js 6.5.438. */
(() => {
  const params = new URLSearchParams(window.location.search);
  const profile = params.get("profile");
  const files = { activespn: "activespn.pdf", activespn2: "activespn2-author.pdf" };
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

  // Neither supplied PDF has an embedded outline. ActiveSPN uses measured
  // headings; the 14-page ActiveSPN2 author PDF supplies native named section
  // destinations. XYZ uses a bottom origin. Do not rewrite either PDF.
  const pageHeight = profile === "activespn2" ? 793.701 : 792;
  const section = (title, page, top, items = []) => ({
    title, dest: [page - 1, { name: "XYZ" }, null, pageHeight - top + 8, null],
    bold: false, italic: false, color: new Uint8ClampedArray(3),
    count: items.length ? -items.length : 0, items,
  });
  const linkedSection = (title, dest, items = []) => ({
    title, dest, bold: false, italic: false, color: new Uint8ClampedArray(3),
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
    section("Abstract", 1, 164.53),
    linkedSection("1. Introduction", "section.1"),
    linkedSection("2. ActiveSPN2 as Soft Active Surfaces", "section.2", [
      linkedSection("2.1. Specifications of ActiveSPN2 Module", "subsection.2.1"),
      linkedSection("2.2. Dynamics of ActiveSPN2 Module", "subsection.2.2"),
      linkedSection("2.3. Dynamics of ActiveSPN2 Gripper", "subsection.2.3"),
    ]),
    linkedSection("3. Multi-Modal VBDormP Architecture", "section.3", [
      linkedSection("3.1. In-finger Deformation Tracking", "subsection.3.1"),
      linkedSection("3.2. Multi-Modal Generative Architecture", "subsection.3.2"),
      linkedSection("3.3. Data Collection Platform", "subsection.3.3"),
    ]),
    linkedSection("4. Experiments and Results", "section.4", [
      linkedSection("4.1. System Characterization and Performance", "subsection.4.1", [
        linkedSection("4.1.1. Quantification of Adaptive Kinesthesia Under External Loading", "subsubsection.4.1.1"),
        linkedSection("4.1.2. Bending Angle and Gripping Force", "subsubsection.4.1.2"),
        linkedSection("4.1.3. Gripper Structural Reliability and Object Handling Performance", "subsubsection.4.1.3"),
        linkedSection("4.1.4. In-Finger Manipulation and Object Reorientation", "subsubsection.4.1.4"),
      ]),
      linkedSection("4.2. Validation of the Multi-Modal Perception Framework", "subsection.4.2", [
        linkedSection("4.2.1. Competitive Grasping with Human Interaction", "subsubsection.4.2.1"),
        linkedSection("4.2.2. Experimental Validation of Force Estimation", "subsubsection.4.2.2"),
        linkedSection("4.2.3. Peg-in Task Demonstrations in Confined Spaces", "subsubsection.4.2.3"),
      ]),
      linkedSection("4.3. Demonstration of In-Finger Dexterity and Robustness", "subsection.4.3"),
    ]),
    linkedSection("5. Conclusion", "section.5"),
    linkedSection("References", "section*.1"),
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
