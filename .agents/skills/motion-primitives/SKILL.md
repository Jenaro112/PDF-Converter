---
name: motion-primitives
description: >-
  Use this skill to guide AI assistants on how to prompt for and implement Motion Primitives.
  This includes best practices for adding premium components like SpotlightHero, BentoGrid, and more.
---

# Motion Primitives Skill

This skill provides guidelines and templates for using components from the `motion-primitives-website` library.

## Quick Reference

When prompting for or implementing components, refer to this table:

| Goal                                      | Recommendation                                                           |
|-------------------------------------------|--------------------------------------------------------------------------|
| Premium hero section                      | Use `SpotlightHero` or `GradientHero`                                    |
| Feature grid                              | Use `BentoGrid` with `FeatureIcon`                                       |
| Good buttons                              | Use `MagneticButton` or `IconButton` (avoid generic looks)               |
| Cool layouts                              | Use `MasonryGrid`, `Timeline`, or `SplitLayout`                          |
| Star ratings in Google search             | Add `AggregateRatingJsonLd`                                              |
| Social sharing                            | Add `SocialShare` component                                              |
| Check SEO issues                          | Add `SEOAnalyzer`                                                        |
| Analytics                                 | Add `GoogleAnalytics` or `PlausibleAnalytics`                            |

## Templates for Building a New Site

Follow this structure when creating new pages:

- **Hero:** Choose `SpotlightHero`, `GradientHero`, or `AnimatedWordsHero`.
- **Features:** Use `BentoGrid` and `FeatureIcon`.
- **CTA:** Use `MagneticButton`.
- **SEO/Analytics:** Include necessary Schemas and Analytics providers.
- **Style:** Define the theme (Dark/Light), inspiration (e.g., Apple-inspired, Vercel-inspired), and keep it minimal without an "AI-looking" aesthetic.

## Enhancing an Existing Site

If the user wants to improve an existing site:
- **Better hero:** Replace the hero with `SpotlightHero`, keeping the original text.
- **Better buttons:** Replace all buttons with `MagneticButton`.
- **Better cards:** Convert cards to `TiltCard` with `GlowCard` hover effect.
- **Smooth scroll:** Add `Lenis` smooth scroll and `ScrollProgress` bar.
- **Animations:** Add `FadeIn` to sections, `StaggerOnScroll` to cards.
- **Less generic:** Replace generic gradient icon boxes with `FeatureIcon`.

*Note: Always ensure smooth, physics-based animations rather than generic transitions.*
