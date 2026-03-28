# Design System Strategy: The Precision Monolith

## 1. Overview & Creative North Star
**The Creative North Star: "Precision Utility"**
This design system moves beyond simple minimalism to embrace a high-fidelity, editorial aesthetic inspired by technical rigor and architectural clarity. By combining the airy, intentional whitespace of Vercel with the dense, functional density of Linear, we create an interface that feels like a professional instrument.

We break the "template" look through **Hyper-Definition**. While most systems rely on shadows to create depth, this system uses razor-thin 0.5px borders and distinct tonal shifts between surfaces. It is a "Monolith" because it feels carved from a single source—interconnected, structural, and uncompromisingly sharp.

---

## 2. Color Palette & Surface Architecture
Our palette is rooted in a "Warm White" foundation (`#F8F8F6`), providing a more sophisticated, gallery-like feel than pure clinical white.

### Core Accent Colors
*   **Primary (Action):** `#378ADD` – Used for active states and critical path actions.
*   **Semantic Accents:** 
    *   `#E24B4A` (Error/High Priority): For potholes and critical infrastructure failures.
    *   `#BA7517` (Tertiary/Medium): For cracks and preventative maintenance.
    *   `#639922` (Secondary/Low): For stable, healthy environments.

### The "No-Line" Rule
Prohibit the use of 1px solid borders for sectioning the layout. Instead, define structural boundaries through background shifts. A sidebar should be defined by `surface-container-low`, while the main stage remains `surface`. This creates an "Organic Brutalist" structure where the architecture is defined by volume, not lines.

### Surface Hierarchy & Nesting
Treat the UI as a series of nested layers.
*   **Base Layer:** `surface` (#F8F8F6) for the main application background.
*   **The Container:** `surface-container-lowest` (#FFFFFF) for cards and primary content areas.
*   **The Inset:** Use `surface-container` (#EEEEEC) for nested elements like code blocks or secondary metadata feeds.

### The "Ghost Border" Implementation
To achieve the "Razor Edge" look requested, all card borders must use the `outline-variant` token at **0.5px thickness**. If the rendering engine struggles with sub-pixel borders, use a 1px border with the opacity reduced to 20% to mimic the visual weight of a 0.5px line.

---

## 3. Typography: Editorial Authority
We utilize **Inter** not as a default sans-serif, but as a typographic grid. By utilizing extreme weight contrasts, we create an editorial hierarchy.

*   **Display & Headlines:** Use `display-md` (2.75rem) with negative letter-spacing (-0.02em) for "Big Number" dashboard stats. This conveys authority.
*   **Titles:** `title-sm` (1rem) should be Medium or Semi-Bold (weight 500/600) to act as a clear anchor for card content.
*   **Labels:** Use `label-sm` (0.6875rem) in ALL CAPS with +0.05em tracking for metadata. This provides a "Technical Blueprint" feel.

---

## 4. Elevation & Depth: Tonal Layering
In the absence of heavy shadows, depth is achieved through **Tonal Layering** and **Environmental Occlusion**.

*   **The Layering Principle:** To "lift" an element, do not add a shadow. Instead, place a `surface-container-lowest` (White) card on top of a `surface` (#F8F8F6) background. The 0.5px border provides the necessary definition.
*   **Micro-Shadowing:** When a floating element (like a Popover) is required, use a "Ghost Shadow": `0px 4px 20px rgba(26, 28, 27, 0.04)`. It should feel like a soft glow of light being blocked, rather than a dark smudge.
*   **Glassmorphism:** For top navigation bars or floating action buttons, use `surface` at 80% opacity with a `blur(12px)` backdrop. This keeps the user grounded in the "Monolith" while providing a sense of sophisticated translucency.

---

## 5. Components

### Cards
*   **Background:** `surface-container-lowest` (#FFFFFF).
*   **Border:** 0.5px `outline-variant`.
*   **Radius:** `xl` (12px)
*   **Content:** No dividers. Use `spacing-6` (1.3rem) to separate header from body.

### Buttons
*   **Primary:** `primary` (#005ea4) background with `on-primary` (#FFFFFF) text. Radius: `lg` (8px).
*   **Secondary:** Ghost style. 0.5px `outline-variant` border. No background.
*   **States:** On hover, shift background to `primary_container`. Transitions should be `150ms ease-out`.

### Badges & Pills (Priority Indicators)
*   **Radius:** `full` (20px).
*   **High Priority:** Background `tertiary_container`, Text `on_tertiary_container`.
*   **Visual Soul:** Use a small 4px solid circle (the "Status Dot") next to the text for immediate pattern recognition.

### Input Fields
*   **Style:** Minimalist. No background color (transparent).
*   **Border:** Bottom-only 1px `outline-variant` or a full 0.5px ghost border. 
*   **Focus State:** Border color shifts to `primary` (#005ea4) with a subtle 2px outer "glow" using the primary color at 10% opacity.

### Additional Component: The "Data Striated" List
Instead of using dividers between list items, use alternating backgrounds or simply `spacing-2` (0.4rem) gaps. This keeps the "Precision" look without cluttering the UI with horizontal lines.

---

## 6. Layout & Do's and Don'ts

*   **DO:** Use the Spacing Scale religiously. The difference between `spacing-3` and `spacing-4` is the difference between "cluttered" and "professional."
*   **DO:** Use "Optical Centering." Buttons with icons should have slightly more padding on the icon side to feel balanced.
*   **DON'T:** Use solid black (#000000). Always use `on-surface` (#1A1C1B) for text to maintain the "Editorial" softness.
*   **DON'T:** Use standard 1px borders for inner elements. If a divider is essential, use a `surface-variant` color shift rather than a line.
*   **DO:** Prioritize legibility. Ensure that the `#639922` (Green) used for "Normal" priority meets AA contrast standards against the `#F8F8F6` background.
