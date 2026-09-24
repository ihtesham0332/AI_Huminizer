# 19. FRONTEND DESIGN

The frontend will be built with Next.js 14, React, and Tailwind CSS. The UX principle is: "Hide the complex agents behind a simple, intuitive interface."

## 1. Dashboard (The Control Center)
*   **Stats Panel:** Words Processed, Credits Remaining, Average Quality Score.
*   **Recent Documents:** List of past jobs with quick-download links (DOCX/PDF).
*   **Profile Selector:** A dropdown to select which "Writing DNA" to apply to the next job.

## 2. Workspace (The Main Editor)
*   **Split View:** Left side = Original Text. Right side = Humanized Text.
*   **Diff Viewer:** Additions are highlighted in green, removals in red. Protected facts are highlighted in blue.
*   **Action Bar:** 
    *   Mode Selector: Fast, Balanced, Deep.
    *   "Humanize" Button.

## 3. Explainability Panel (The "Why")
When a user clicks on a changed sentence in the Diff Viewer, a sidebar opens showing:
*   *Reason:* "Reduced excessive passive voice."
*   *Facts Preserved:* `["15%", "2026"]`
*   *Quality Metrics:* Semantic Match (98%).

## 4. Usage Estimator (Pre-Flight Check)
Before processing a large document, a modal appears:
> **Document Analysis Complete**
> - Words: 12,050
> - Sentences requiring rewrite: 450 (32%)
> - Estimated Cost (Balanced Mode): 1,200 Credits
> [Confirm and Process] | [Cancel]
