# Graph Report - wcc  (2026-07-29)

## Corpus Check
- 53 files · ~397,838 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 123 nodes · 290 edges · 10 communities (9 shown, 1 thin omitted)
- Extraction: 96% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Site Architecture
- Residential Services
- Service Page Previews
- Homepage Components
- Page Builders and Schema
- Generation Pipeline
- Emergency Stabilization
- Call to Action System
- Preview Assets

## God Nodes (most connected - your core abstractions)
1. `Bakersfield SEO Expansion and Homepage Rebuild Specification` - 23 edges
2. `build_home()` - 18 edges
3. `e()` - 17 edges
4. `build_parent()` - 17 edges
5. `build_service()` - 16 edges
6. `General Contractor in Bakersfield Homepage` - 15 edges
7. `General Contractor in Bakersfield, CA` - 13 edges
8. `Commercial Construction Services Hub` - 10 edges
9. `24/7 Emergency Construction Contractor in Bakersfield, CA` - 9 edges
10. `Commercial Construction Services Preview` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Commercial Construction Services Preview` --semantically_similar_to--> `Commercial Construction Services Hub`  [INFERRED] [semantically similar]
  _preview/9-commercial-hub.html → services/commercial.html
- `WordPress Redirect Configuration` --references--> `Bakersfield SEO Expansion and Homepage Rebuild Specification`  [AMBIGUOUS]
  redirects.md → docs/Bakersfield-SEO-Expansion-and-Homepage-Rebuild.md
- `Legacy General Contractor Homepage` --semantically_similar_to--> `General Contractor in Bakersfield Homepage`  [INFERRED] [semantically similar]
  old-pages/home-page-old.html → home.html
- `Legacy Emergency Contractor Page` --semantically_similar_to--> `24/7 Emergency Construction Services Hub`  [INFERRED] [semantically similar]
  old-pages/24 Hour Emergency Contractor Bakersfield CA _ Roof & Repairs.html → services/emergency.html
- `Legacy Commercial Contractor Page` --semantically_similar_to--> `Commercial Construction Services Hub`  [INFERRED] [semantically similar]
  old-pages/Commercial Contractor Bakersfield CA _ Tenant Improvements.html → services/commercial.html

## Import Cycles
- None detected.

## Communities (10 total, 1 thin omitted)

### Community 0 - "Site Architecture"
Cohesion: 0.23
Nodes (27): Outdoor Living, Patios and Patio Covers Preview, Commercial Construction Services Preview, Accessibility and Mobile Requirements, Reusable Service Page System Avoids Disconnected Page Implementations, Parent and Child Search Intent Separation Prevents Cannibalization, Homepage, Parent Hub, and Child Service Architecture, Bakersfield SEO Expansion and Homepage Rebuild Specification, WordPress Fragment Migration Without Exported Divi Markup (+19 more)

### Community 1 - "Residential Services"
Cohesion: 0.12
Nodes (24): Emergency Water Damage Response Page, Emergency Water Damage Response, Water Damage Response Process, ADU Construction and Garage Conversions, ADU Project Process, ADU and Garage Conversions Page, Custom Home Building, Custom Home Building Process (+16 more)

### Community 2 - "Service Page Previews"
Cohesion: 0.29
Nodes (20): Commercial General Contracting & Project Management in Bakersfield, CA, Tenant Improvements & Build-Outs in Bakersfield, CA, Commercial Remodeling & Renovations in Bakersfield, CA, New Commercial Construction in Bakersfield, CA, Commercial Concrete, Asphalt & Parking Lot Work in Bakersfield, CA, Commercial Facility Maintenance & On-Call Repairs in Bakersfield, CA, 24/7 Emergency Construction Contractor in Bakersfield, CA, 24/7 Emergency Water Damage Response in Bakersfield, CA (+12 more)

### Community 3 - "Homepage Components"
Cohesion: 0.23
Nodes (14): arrow_link(), arrowish(), before_after_section(), build_home(), e(), icon(), instagram_section(), Dark band. Featured bracketed player plus a playlist rail that swaps the (+6 more)

### Community 4 - "Page Builders and Schema"
Cohesion: 0.29
Nodes (12): build_parent(), build_service(), business_node(), crumbs(), emergency_band(), faq_block(), ldjson(), Escape copy, then turn [[page-id|anchor text]] tokens into contextual        int (+4 more)

### Community 5 - "Generation Pipeline"
Cohesion: 0.43
Nodes (5): assemble(), main(), preview_wrap(), sticky_bar(), write()

### Community 7 - "Emergency Stabilization"
Cohesion: 0.33
Nodes (6): Emergency Structural Stabilization Page, Structural Response Process, Emergency Structural Stabilization, Storm Damage Emergency Repairs Page, Storm Damage and Emergency Repairs, Storm Response Process

### Community 8 - "Call to Action System"
Cohesion: 0.50
Nodes (5): call_btn(), cta_buttons(), final_cta(), hero_dark(), phone_btn()

## Ambiguous Edges - Review These
- `Bakersfield SEO Expansion and Homepage Rebuild Specification` → `WordPress Redirect Configuration`  [AMBIGUOUS]
  redirects.md · relation: references

## Knowledge Gaps
- **17 isolated node(s):** `Accessibility and Mobile Requirements`, `Emergency Structural Stabilization`, `Structural Response Process`, `Water Damage Response Process`, `Storm Damage and Emergency Repairs` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Bakersfield SEO Expansion and Homepage Rebuild Specification` and `WordPress Redirect Configuration`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Emergency Water Damage Response Page` connect `Residential Services` to `Emergency Stabilization`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **What connects `Escape copy, then turn [[page-id|anchor text]] tokens into contextual        int`, `items: list of (name, url|None). Last item = current page (url None).`, `Dark band. Featured bracketed player plus a playlist rail that swaps the` to the rest of the system?**
  _25 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Residential Services` be split into smaller, more focused modules?**
  _Cohesion score 0.11956521739130435 - nodes in this community are weakly interconnected._