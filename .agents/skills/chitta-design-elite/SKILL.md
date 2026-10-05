---
name: chitta-design-elite
description: >-
  Use this skill when designing or implementing web pages to enforce the $10K quality bar,
  ensuring Elite UI/UX engineering constraints, Framer Motion integration, and strict quality gates.
---

# Chitta Design Elite Starter Skill

This skill enforces the baseline infrastructure, design principles, and quality gates from the `chitta-design-elite-starter` framework.

## Core Stack & Tooling

Always adhere to the following stack choices:
- **Framework:** Next.js App Router (RSC by default)
- **Language:** Strict TypeScript
- **Styling:** Tailwind v4 (CSS-first config, `@theme` blocks, OKLch tokens)
- **Motion:** Framer Motion (`motion/react`) - *Mandatory on every interactive component.*
- **Components:** shadcn/ui, Aceternity UI, Magic UI
- **Fonts:** Geist + Inter via `next/font`
- **Utilities:** `clsx` + `tailwind-merge` (`cn()` helper required for all conditional classes)

## Quality Gates ($10K Bar)

Every artifact must pass these constraints before being considered complete:
- **Lighthouse:** 100/100/100/100 (Performance, Accessibility, Best Practices, SEO)
- **Accessibility:** 0 axe-core violations, WCAG 2.2 AA minimum (AAA where feasible)
- **Web Vitals:** CLS = 0, LCP < 1.0s, TBT < 50ms
- **Performance:** Initial JS bundle < 100KB gzip, Animation 60fps under 4x CPU throttle
- **Zero custom CSS files:** All styling must be through Tailwind v4 and the `@theme` token system
- **Consistency:** Use `cn()` for all dynamic classes

## Elite UI/UX Engineer Constraints

- **Animation First:** Never use a standard `<div>` where a `<motion.div>` should be utilized for interaction or entrance.
- **Typography:** Strictly use Geist or Inter.
- **Component Fetching:** Prioritize existing implementations in shadcn, Aceternity, or Magic UI before writing custom UI code.
- **Visual Audit:** Always ensure responsive padding, proper contrast, and distinct hover/active states are implemented.

## Advanced Tooling Integration

When appropriate, integrate advanced tooling for premium effects:
- **3D/WebGL:** `@react-three/fiber`, `three`
- **Smooth scroll:** `lenis`
- **Pre-rendered animations:** `lottie-react`, `@rive-app/react-canvas`
- **Premium Primitives:** `vaul`, `embla-carousel-react`, `@floating-ui/react`

*Note: Override visual tokens per project by editing the `@theme` block in `app/globals.css`. That is the primary branding surface.*
