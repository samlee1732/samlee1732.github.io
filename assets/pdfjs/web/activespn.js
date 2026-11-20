/* Publication reader profiles for the bundled PDF.js 6.5.438. */
(() => {
  const params = new URLSearchParams(window.location.search);
  const profile = params.get("profile");
  const files = {
    activespn: "activespn.pdf", activespn2: "activespn2-author.pdf",
    "active-surface": "active-surface.pdf", "flip-and-flap": "flip-and-flap.pdf",
    adap: "adap.pdf", "stable-quadrotor": "stable-quadrotor.pdf",
    "parameter-adaptive-control": "parameter-adaptive-control.pdf",
    "oral-care": "oral-care.pdf",
  };
  if (!Object.hasOwn(files, profile)) return;
  const file = new URL(params.get("file") || "", document.baseURI);
  if (!file.pathname.endsWith(`/${files[profile]}`)) return;

  document.documentElement.classList.add("activespn-reader");
  document.documentElement.dataset.readerProfile = profile;
  const stylesheet = document.createElement("link");
  stylesheet.rel = "stylesheet";
  stylesheet.href = "activespn.css?v=20261120-publication-readers";
  document.head.append(stylesheet);

  const desktop = window.matchMedia("(min-width: 720px)");
  const OUTLINE = 2;
  const NONE = 0;

  // Preserve embedded outlines (including ADAP's). Other profiles use measured
  // headings or the PDF's native named section destinations. XYZ coordinates
  // use a bottom origin. The source PDFs are never rewritten.
  const pageHeight = {
    activespn2: 793.701, adap: 793.701,
    "stable-quadrotor": 800.05, "parameter-adaptive-control": 782.929,
    "oral-care": 807.9,
  }[profile] || 792;
  const section = (title, page, top, items = []) => ({
    title, dest: [page - 1, { name: "XYZ" }, null, pageHeight - top + 8, null],
    bold: false, italic: false, color: new Uint8ClampedArray(3),
    count: items.length ? -items.length : 0, items,
  });
  const linkedSection = (title, dest, items = []) => ({
    title, dest, bold: false, italic: false, color: new Uint8ClampedArray(3),
    count: items.length ? -items.length : 0, items,
  });
  const outlines = {
    "stable-quadrotor": [
      section("Abstract", 1, 339.43),
      section("1. Introduction", 1, 463.84),
      section("2. System Model", 2, 426.98),
      section("3. Flight Trajectory Control Design", 3, 619.91, [
        section("3.1. Trajectory Differentiation", 4, 275.41),
        section("3.2. Attitude Control Design", 4, 691.61),
        section("3.3. Position Control Design", 5, 435.70),
      ]),
      section("4. Simulation Results and Analysis", 6, 198.80),
      // The supplied PDF's sec5 named destination incorrectly targets page 7.
      section("5. Conclusions", 10, 73.11),
      section("Data Availability", 10, 277.15),
      section("Conflicts of Interest", 10, 332.25),
      section("Acknowledgments", 10, 387.36),
      section("References", 10, 476.82),
    ],
    "parameter-adaptive-control": [
      section("Abstract", 1, 283.92),
      section("I. Introduction", 1, 473.20),
      section("II. Model", 2, 590.95, [
        section("A. Notation", 2, 686.97),
        section("B. System Dynamics", 3, 333.46),
      ]),
      section("III. Control Design", 3, 542.49, [
        section("A. Attitude Control", 3, 626.35),
        section("B. Position Control", 4, 602.93),
      ]),
      section("IV. Numerical Simulations and Results", 7, 66.32, [
        section("A. Trajectory 1: Point-to-Point Control", 7, 572.92),
        section("B. Trajectory 2: Tracking Control", 8, 517.27),
        section("C. Performance Measures", 8, 582.87),
      ]),
      section("V. Conclusion", 9, 176.30),
      section("References", 9, 477.56),
    ],
    "oral-care": [
      section("Abstract", 1, 453.11),
      section("Introduction", 2, 138.59),
      section("Experimental", 3, 652.96, [
        section("Sensor Design and Fabrication", 3, 668.06),
        section("VBDeformP for Force and Torque Inference", 5, 359.35),
      ]),
      section("Results and Discussion", 7, 657.18, [
        section("Brushing Regions Classification Performance", 7, 672.28),
        section("F/T Perception in Quasi-static and Dynamic Scenarios", 11, 430.68),
      ]),
      section("Conclusions", 16, 579.06),
      section("Declarations", 17, 295.52, [
        section("Authors' Contributions", 17, 310.62),
        section("Availability of Data and Materials", 17, 604.99),
        section("Financial Support and Sponsorship", 17, 658.45),
        section("Conflicts of Interest", 18, 71.91),
        section("Ethical Approval and Consent to Participate", 18, 110.95),
        section("Consent for Publication", 18, 190.30),
        section("Copyright", 18, 229.34),
      ]),
      section("References", 18, 268.94),
    ],
    "active-surface": [
      section("Abstract", 1, 162.54),
      section("I. Introduction", 1, 339.00),
      section("II. Gripper Design", 1, 657.85, [
        section("A. Passive Soft Polyhedral Finger Design", 1, 672.62),
        section("B. Active Surface Design", 2, 623.49),
      ]),
      section("III. Analysis", 2, 429.75, [
        section("A. Finger-Active Surface Interaction", 2, 660.59),
        section("B. Passive Finger Compliance: Stiffness Distribution", 3, 467.11),
        section("C. Comparison with 2D FinRay Finger", 3, 490.10),
        section("D. Pinch & Lift Phase in Simplified Model", 3, 695.27),
      ]),
      section("IV. Results and Discussions", 4, 587.15),
      section("V. Conclusion", 6, 54.23),
      section("References", 6, 395.85),
    ],
    "flip-and-flap": [
      section("Abstract", 1, 164.28),
      section("I. Introduction", 1, 378.57),
      section("II. Experimental Platform", 2, 199.27, [
        section("A. Specifications of Flying Platform", 2, 261.61),
        section("B. Extended Leg", 2, 389.80),
      ]),
      section("III. Model", 3, 551.73, [
        section("A. Flip Phase: Impact and Upward-Flip in Simplified Model", 3, 453.96),
        section("B. Flap Phase: Controlled Downward Swing in Simplified Model", 4, 331.56),
        section("C. Multilink Dynamics Mode", 4, 325.71),
      ]),
      section("IV. Simulation", 5, 295.08, [
        section("A. Flip Phase: Impact and Upward-Flip in Simplified Model", 5, 312.90),
        section("B. Flap Phase: Controlled Downward Swing in Simplified Model", 5, 303.66),
        section("C. Flip-and-Flap Dynamics Simulation in Multi-Links Model", 5, 630.90),
      ]),
      section("V. Experimental Validation", 6, 609.11),
      section("VI. Conclusion", 8, 295.88),
      section("References", 8, 575.49),
    ],
    activespn: [
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
          if (!outlineCount && outline) {
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
