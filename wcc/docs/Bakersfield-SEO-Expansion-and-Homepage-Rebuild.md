# West Coast Construction Group

## Bakersfield SEO Landing Page Expansion and Homepage Rebuild

## 1. Project summary

Rebuild the West Coast Construction Group homepage and create 18 Bakersfield-focused service landing pages organized under the existing residential, commercial, and emergency service silos.

The new pages must:

- Match the established West Coast Construction Group brand.
- Use the existing website as a visual and content reference without copying the current Divi-generated markup.
- Be built with reusable components and structured page data.
- Target specific Bakersfield construction searches without keyword stuffing.
- Contain unique, useful content for each service.
- Strengthen the relationship between the homepage, parent service pages, and individual service pages.
- Improve metadata, heading hierarchy, internal linking, accessibility, structured data, image optimization, and conversion paths.
- Preserve or improve the current responsive experience.
- Be ready for deployment, sitemap submission, Search Console inspection, and future expansion.

The final site architecture will contain:

- 1 rebuilt homepage.
- 3 existing parent service pages updated as service hubs.
- 18 new service landing pages.
- Shared components for service pages, FAQs, calls to action, trust signals, related services, breadcrumbs, and structured data.

## 2. Primary project goals

### Search goals

1.  Increase relevance for Bakersfield service-specific construction searches.
2.  Establish a clear topical hierarchy around residential, commercial, and emergency construction.
3.  prevent the parent pages and child pages from competing for the same search intent.
4.  Give every important page at least one crawlable contextual internal link.
5.  Create materially unique pages rather than duplicating the same Bakersfield copy across multiple URLs.
6.  Improve the website’s ability to earn useful title links, snippets, sitelinks, and local-business understanding.

### Conversion goals

1.  Make it immediately clear what service the visitor has reached.
2.  Show the phone number and primary call to action above the fold.
3.  Distinguish normal estimates from emergency calls.
4.  Reinforce licensing, insurance, service area, communication, project management, and craftsmanship.
5.  Provide answers to the questions a prospective customer asks before contacting a contractor.
6.  Make contact actions easy on desktop and mobile.

## 3. Existing-site audit and required corrections

Use the supplied homepage, residential, commercial, and emergency HTML files as references for:

- Current brand direction.
- Existing colors, typography, imagery, and visual personality.
- Current company positioning.
- Phone number and license presentation.
- Existing service descriptions.
- Current calls to action.
- Existing reviews and trust statements.

Do not copy the exported WordPress or Divi markup into the new build.

Correct the following during implementation:

- Use exactly one visible H1 per page.
- Correct “sorrounding” to “surrounding.”
- Correct the homepage commercial-services button so it links to `/services/commercial/`.
- Replace testimonial text currently marked as H2 elements with semantic testimonial markup such as `blockquote`, `p`, and `cite`.
- Replace generic keyword headings such as “tenant improvements Bakersfield CA” with natural, readable headings.
- Fix “Get a Estimate” to “Get an Estimate.”
- Add a unique emergency parent-page meta description.
- Add descriptive alt text to meaningful images.
- Give decorative images an intentionally empty alt attribute.
- Replace the favicon currently used as the homepage social-sharing image with a properly sized branded homepage image.
- Remove inconsistent footer paths and capitalization such as `/Residential/`.
- Ensure all calls to action have functioning `href` destinations.
- Preserve existing analytics and Search Console tracking during the migration.
- Ensure no WordPress admin-bar or editor markup appears in production output.

## 4. URL architecture

### Homepage

`/`

### Residential parent

`/services/residential/`

### Residential child pages

- `/services/residential/custom-home-building/`
- `/services/residential/adu-garage-conversions/`
- `/services/residential/home-additions-expansions/`
- `/services/residential/remodeling-home-renovations/`
- `/services/residential/roofing-roof-leak-repair/`
- `/services/residential/outdoor-living-patios-patio-covers-pergolas-pool-areas/`

### Commercial parent

`/services/commercial/`

### Commercial child pages

- `/services/commercial/commercial-gc-project-management/`
- `/services/commercial/tenant-improvements-build-outs/`
- `/services/commercial/commercial-remodeling-renovations/`
- `/services/commercial/new-commercial-construction/`
- `/services/commercial/concrete-asphalt-parking-lots-flatwork/`
- `/services/commercial/facility-maintenance-on-call-repairs/`

### Emergency parent

Change the emergency parent URL to:

`/services/emergency/`

Create a permanent 301 redirect:

`/services/emergency-services/` → `/services/emergency/`

### Emergency child pages

- `/services/emergency/emergency-water-damage-response/`
- `/services/emergency/emergency-roof-leaks/`
- `/services/emergency/storm-damage-emergency-repairs/`
- `/services/emergency/emergency-property-damage-repairs/`
- `/services/emergency/ceiling-collapse-drywall-failure-emergency-repairs/`
- `/services/emergency/emergency-structural-stabilization/`

Do not launch the emergency child pages beneath `/services/emergency/` while leaving the parent at `/services/emergency-services/`.

## 5. Shared service-page template

Create one reusable service landing-page system that accepts unique content and metadata for each page.

The template must support the following structure.

### Breadcrumb navigation

Example:

Home → Residential Services → Custom Home Building

Requirements:

- Use a semantic `nav` element.
- Add `aria-label="Breadcrumb"`.
- Link every level except the current page.
- Include matching `BreadcrumbList` JSON-LD.

### Hero section

Include:

- Service category eyebrow.
- One unique H1.
- A short service-specific value statement.
- An approximately 80–130-word introduction.
- Primary call-to-action button.
- Secondary phone or emergency-call action.
- Relevant project or service image.
- License or trust line where appropriate.

### Trust strip

Possible verified items:

- CSLB license number.
- Licensed and insured.
- Bakersfield and Kern County service.
- Residential and commercial experience.
- 24/7 phone availability on emergency pages only.
- Financing availability only when currently offered and accurately disclosed.

### Service overview

Use an H2 that naturally describes the specific service.

Explain:

- What the service is.
- Who normally needs it.
- Common project goals.
- The role West Coast Construction Group performs.
- What the visitor should expect next.

### Service scope

Use one H2 followed by several H3 subsections.

Each H3 should describe a real component of the service. Use H4 only when an H3 requires legitimate nested detail.

Do not use H4 or H5 merely to make text look smaller.

### Problems, needs, or signs section

Use an H2 appropriate to the search intent, such as:

- Signs your roof may need repair.
- When a garage conversion may make sense.
- When to call for emergency structural help.
- Common reasons businesses renovate occupied spaces.

This section should help visitors recognize whether the service applies to their situation.

### Project process

Use one H2 and four to six H3 steps.

Possible steps:

1.  Initial call or consultation.
2.  Site review.
3.  Scope and estimate.
4.  Planning, permits, or scheduling.
5.  Construction or stabilization.
6.  Inspection, punch list, and closeout.

Change the process where needed so it accurately reflects the service. Emergency pages should use an emergency-response process rather than the standard estimate process.

### Bakersfield relevance

Include one useful local section rather than repeatedly inserting “Bakersfield” into every paragraph.

Possible topics, when factually verified:

- Bakersfield and Kern County service coverage.
- Local permitting coordination.
- Heat, rain, roof exposure, or property conditions relevant to the service.
- Scheduling around operating businesses.
- Local project examples.
- Local residential styles or property needs.

Do not create filler neighborhood lists or unsupported local claims.

### Why choose West Coast Construction Group

Use an H2 with concise supporting points such as:

- Defined scopes.
- Clear communication.
- Organized timelines.
- Trade coordination.
- Clean job sites.
- Quality-control and punch-list process.
- Residential and commercial capabilities.
- Emergency stabilization and follow-up repair coordination.

Only include claims that can be verified.

### Related services

Include three to five contextual internal links.

Every related-service card must contain:

- Descriptive title.
- One or two explanatory sentences.
- Crawlable anchor element with an `href`.
- Anchor text that clearly identifies the destination.

### Frequently asked questions

Use:

- H2: Frequently asked questions.
- H3 for each question.
- A direct answer immediately following each H3.
- Five to seven unique questions per service page.
- Approximately 40–100 words per answer when the subject warrants it.
- Accordion behavior may be used, but the complete question and answer must remain accessible in the rendered DOM.

Do not use H5 for top-level FAQ questions.

FAQs are primarily for users, long-tail relevance, and conversion. Do not rely on FAQ rich-result eligibility.

### Final call to action

Include:

- Service-specific H2.
- Brief closing statement.
- Main contact button.
- Click-to-call telephone link.
- Emergency wording only on emergency pages.

## 6. Heading hierarchy

Use heading elements for document structure, not styling.

### Required hierarchy

- H1: One page title only.
- H2: Major page sections.
- H3: Subsections under the relevant H2.
- H4: Detail nested beneath a specific H3.
- H5: Use only when another legitimate level of detail exists beneath an H4.

Do not force every page to contain H1 through H5.

Do not:

- Add multiple H1 elements.
- Skip from H2 directly to H5.
- Mark testimonials as headings.
- use headings only to insert keywords.
- Repeat the same heading with minor keyword changes.
- use all-lowercase keyword phrases as visible headings.

## 7. Content and keyword requirements

### Page uniqueness

Each page must contain its own:

- Introduction.
- Service explanation.
- Scope subsections.
- Customer problems or use cases.
- Process language.
- Local section.
- FAQs.
- closing call to action.
- Metadata.
- Social-sharing description.
- Image alt text.

The only copy that may repeat exactly is limited global content such as:

- License information.
- Short trust-strip labels.
- Header and footer navigation.
- Basic phone CTA wording.
- Legal disclaimers.

### Recommended content ranges

These are editorial targets, not padding requirements:

- Homepage: approximately 1,200–1,800 useful words.
- Parent service hubs: approximately 800–1,200 useful words each.
- Standard service landing pages: approximately 850–1,300 useful words.
- Emergency pages: approximately 700–1,050 useful words.

Stop when the page fully answers the search intent. Do not inflate word count.

### Keyword placement

Use the primary phrase naturally in:

- SEO title.
- H1.
- Opening paragraph.
- One relevant H2 or H3 when natural.
- Meta description.
- One image alt attribute when the image genuinely represents the subject.
- At least one internal-link anchor pointing to the page.

Use related terms naturally throughout the copy.

Do not add a visible keyword list or stuff geographic phrases into every heading.

### Cannibalization rules

- Parent pages target broad category intent.
- Child pages target specific service intent.
- The residential roofing page targets planned residential roofing and normal roof-leak repair.
- The emergency roof page targets active and urgent roof leaks.
- The commercial general-contracting page targets oversight and project management.
- The new commercial construction page targets ground-up construction.
- The tenant-improvement page targets leased-space build-outs.
- The commercial-remodeling page targets changes to existing commercial properties.
- The water-damage page targets water intrusion and initial construction response.
- The general property-damage page targets broader urgent physical damage.
- The structural-stabilization page targets suspected structural instability and temporary stabilization.

## 8. Homepage rebuild

### Recommended metadata

**SEO title:**  
General Contractor Bakersfield, CA \| West Coast Construction

**Meta description:**  
West Coast Construction Group provides residential, commercial, roofing, remodeling, and 24/7 emergency construction services in Bakersfield and Kern County.

**H1:**  
General Contractor in Bakersfield, CA

### Homepage structure

1.  Header with primary navigation and prominent estimate button.

2.  Hero with one H1, positioning statement, project imagery, estimate CTA, and phone CTA.

3.  Trust strip with license, insurance, service area, and emergency availability.

4.  Three primary service-silo cards:

    - Residential construction.
    - Commercial construction.
    - 24/7 emergency repairs.

5.  Featured residential services with links to all six residential pages.

6.  Featured commercial services with links to all six commercial pages.

7.  High-visibility emergency-response banner linking to the emergency parent and phone number.

8.  Why choose West Coast Construction Group.

9.  Project process.

10. Selected project gallery or case studies using real company work.

11. Bakersfield and Kern County service-area section.

12. Financing section only if the financing program remains current.

13. Customer testimonials using semantic testimonial markup.

14. General-contractor FAQs.

15. Final estimate CTA.

16. Complete footer with consistent canonical links.

### Homepage design requirements

- Do not recreate the existing page as a direct visual clone.
- Preserve recognizable brand elements while improving spacing, hierarchy, readability, and conversion flow.
- Feature real project imagery where available.
- Use a custom Open Graph image rather than the favicon.
- Ensure the three main service paths are visible without excessive scrolling.
- Create a sticky mobile call or estimate action that does not obstruct content.

## 9. Parent service-page updates

The residential, commercial, and emergency pages remain broad service hubs.

Each parent page must:

- Retain its broad category focus.
- Introduce the category without trying to rank for every child-page phrase.
- Display six linked service cards.
- Give each service card 50–100 words of genuinely helpful descriptive copy.
- Link to each child page with a descriptive anchor.
- Link back to the homepage.
- Include a related-services section connecting to the other two parent categories.
- Use one H1.
- Use H2 for the FAQ section and H3 for each question.
- Receive refreshed metadata, social metadata, image alt text, and structured data.
- Avoid duplicating complete child-page content.

### Residential parent target

**Primary intent:** residential contractor and residential construction services in Bakersfield.

### Commercial parent target

**Primary intent:** commercial contractor and commercial construction services in Bakersfield.

### Emergency parent target

**Primary intent:** 24-hour or emergency construction contractor in Bakersfield.

# 10. Page-specific SEO specifications

## Residential service pages

### 10.1 Custom home building

**URL:**  
`/services/residential/custom-home-building/`

**SEO title:**  
Custom Home Builder Bakersfield, CA \| West Coast Construction

**Meta description:**  
Plan and build a custom home in Bakersfield with organized project management, clear communication, permitting coordination, and quality construction.

**H1:**  
Custom Home Building in Bakersfield, CA

**Primary keyword:**  
custom home builder Bakersfield CA

**Related terms:**  
custom home construction, new home construction, ground-up home construction, residential general contractor, custom house contractor, Kern County custom homes, construction project management

**Suggested FAQ themes:**

- The custom-home process.
- Typical project phases.
- Permits and inspections.
- Working with plans, architects, or designers.
- Lot and site preparation.
- Estimate and scheduling process.

### 10.2 ADU construction and garage conversions

**URL:**  
`/services/residential/adu-garage-conversions/`

**SEO title:**  
ADU Builder Bakersfield, CA \| West Coast Construction

**Meta description:**  
Build an ADU or convert a garage in Bakersfield with a licensed contractor managing planning, permits, construction, inspections, and final closeout.

**H1:**  
ADU Construction & Garage Conversions in Bakersfield, CA

**Primary keyword:**  
ADU contractor Bakersfield CA

**Related terms:**  
ADU builder, accessory dwelling unit, garage conversion contractor, granny flat construction, detached ADU, attached ADU, residential conversion, ADU permits

**Suggested FAQ themes:**

- Attached versus detached ADUs.
- Garage-conversion feasibility.
- Permit requirements.
- Utility connections.
- ADU project timelines.
- Existing-garage limitations.
- Starting an estimate.

### 10.3 Home additions and expansions

**URL:**  
`/services/residential/home-additions-expansions/`

**SEO title:**  
Home Additions Bakersfield, CA \| West Coast Construction

**Meta description:**  
Expand your Bakersfield home with a room addition, bedroom, bathroom, garage, or living-area expansion planned for a seamless, durable result.

**H1:**  
Home Additions & Expansions in Bakersfield, CA

**Primary keyword:**  
home additions Bakersfield CA

**Related terms:**  
room addition contractor, home expansion, bedroom addition, bathroom addition, living-room addition, garage addition, residential addition contractor

**Suggested FAQ themes:**

- Common types of additions.
- Matching an addition to the existing home.
- Permit and inspection needs.
- Living in the home during construction.
- Addition timelines.
- Foundation, roof, and utility coordination.

### 10.4 Home remodeling and renovations

**URL:**  
`/services/residential/remodeling-home-renovations/`

**SEO title:**  
Home Remodeling Bakersfield, CA \| West Coast Construction

**Meta description:**  
Remodel your Bakersfield home with organized kitchen, bathroom, interior, and whole-home renovation services from a licensed general contractor.

**H1:**  
Home Remodeling & Renovations in Bakersfield, CA

**Primary keyword:**  
home remodeling Bakersfield CA

**Related terms:**  
home renovation contractor, kitchen remodeling, bathroom remodeling, whole-home renovation, interior remodeling, residential general contractor

**Suggested FAQ themes:**

- Kitchen, bathroom, and whole-home remodeling.
- Whether permits are required.
- Remodeling an occupied home.
- Project phasing.
- Selecting or supplying materials.
- Estimate and timeline expectations.

### 10.5 Residential roofing and roof-leak repair

**URL:**  
`/services/residential/roofing-roof-leak-repair/`

**SEO title:**  
Roof Repair Bakersfield, CA \| West Coast Construction

**Meta description:**  
Get roofing and roof leak repair in Bakersfield for damaged, aging, or leaking residential roofs, with clear assessment and repair planning.

**H1:**  
Residential Roofing & Roof Leak Repair in Bakersfield, CA

**Primary keyword:**  
roof repair Bakersfield CA

**Related terms:**  
residential roofing contractor, roof leak repair, damaged roof repair, leaking roof, roof inspection, roof maintenance, roofing repairs

**Suggested FAQ themes:**

- Common roof-leak signs.
- Repair versus replacement considerations.
- How roof leaks are assessed.
- Temporary versus permanent repairs.
- What to do after discovering a leak.
- Difference between standard and emergency service.

### 10.6 Outdoor living, patios, and patio covers

**URL:**  
`/services/residential/outdoor-living-patios-patio-covers-pergolas-pool-areas/`

**SEO title:**  
Outdoor Living Bakersfield, CA \| West Coast Construction

**Meta description:**  
Create a functional Bakersfield outdoor living space with patios, patio covers, pergolas, pool-area improvements, and custom exterior construction.

**H1:**  
Outdoor Living, Patios & Patio Covers in Bakersfield, CA

**Primary keyword:**  
outdoor living contractor Bakersfield CA

**Related terms:**  
patio contractor, patio cover builder, pergola contractor, outdoor living construction, pool-area improvements, backyard renovation, exterior construction

**Suggested FAQ themes:**

- Patio-cover and pergola options.
- Permit requirements.
- Material selection.
- Integrating existing pool areas.
- Outdoor-living project timelines.
- Combining multiple exterior improvements.

## Commercial service pages

### 10.7 Commercial general contracting and project management

**URL:**  
`/services/commercial/commercial-gc-project-management/`

**SEO title:**  
Commercial GC Bakersfield, CA \| West Coast Construction

**Meta description:**  
West Coast Construction provides commercial general contracting and project management in Bakersfield with coordinated trades, schedules, and closeout.

**H1:**  
Commercial General Contracting & Project Management in Bakersfield, CA

**Primary keyword:**  
commercial general contractor Bakersfield CA

**Related terms:**  
commercial GC, construction project management, preconstruction planning, subcontractor coordination, commercial construction management, project scheduling

**Suggested FAQ themes:**

- Role of a commercial general contractor.
- Preconstruction and scope development.
- Trade coordination.
- Schedule management.
- Occupied-site planning.
- Inspections and project closeout.

### 10.8 Tenant improvements and build-outs

**URL:**  
`/services/commercial/tenant-improvements-build-outs/`

**SEO title:**  
Tenant Improvements Bakersfield, CA \| West Coast Construction

**Meta description:**  
Plan and complete tenant improvements and commercial build-outs in Bakersfield with phased scheduling, trade coordination, and clear project oversight.

**H1:**  
Tenant Improvements & Build-Outs in Bakersfield, CA

**Primary keyword:**  
tenant improvements Bakersfield CA

**Related terms:**  
commercial build-out, office build-out, retail build-out, leasehold improvements, tenant renovation contractor, commercial interior construction

**Suggested FAQ themes:**

- Tenant-improvement scope.
- Landlord and tenant coordination.
- Plans and permits.
- Working in an occupied building.
- Phased construction.
- Office and retail build-outs.
- Project closeout.

### 10.9 Commercial remodeling and renovations

**URL:**  
`/services/commercial/commercial-remodeling-renovations/`

**SEO title:**  
Commercial Remodeling Bakersfield, CA \| West Coast Construction

**Meta description:**  
Renovate offices, retail spaces, and commercial properties in Bakersfield with structured planning, coordinated construction, and minimal disruption.

**H1:**  
Commercial Remodeling & Renovations in Bakersfield, CA

**Primary keyword:**  
commercial remodeling Bakersfield CA

**Related terms:**  
commercial renovation contractor, office renovation, retail renovation, business remodeling, occupied-space renovation, commercial interior remodel

**Suggested FAQ themes:**

- Types of commercial spaces renovated.
- Operating during construction.
- Phased work.
- Permit and inspection coordination.
- Exterior versus interior renovation.
- Project scheduling and estimates.

### 10.10 New commercial construction

**URL:**  
`/services/commercial/new-commercial-construction/`

**SEO title:**  
Commercial Construction Bakersfield, CA \| West Coast Construction

**Meta description:**  
Build a new commercial property in Bakersfield with general contracting, project coordination, schedule management, inspections, and quality closeout.

**H1:**  
New Commercial Construction in Bakersfield, CA

**Primary keyword:**  
commercial construction Bakersfield CA

**Related terms:**  
new commercial building, ground-up commercial construction, commercial builder, commercial general contractor, preconstruction, building construction management

**Suggested FAQ themes:**

- Ground-up commercial project phases.
- Preconstruction services.
- Design-team coordination.
- Permits and inspections.
- Project schedules.
- Trade management.
- Final closeout and punch list.

### 10.11 Commercial concrete, asphalt, and parking lots

**URL:**  
`/services/commercial/concrete-asphalt-parking-lots-flatwork/`

**SEO title:**  
Commercial Concrete Bakersfield, CA \| West Coast Construction

**Meta description:**  
Improve commercial properties in Bakersfield with concrete flatwork, asphalt repairs, parking-lot improvements, walkways, pads, and exterior surfaces.

**H1:**  
Commercial Concrete, Asphalt & Parking Lot Work in Bakersfield, CA

**Primary keyword:**  
commercial concrete contractor Bakersfield CA

**Related terms:**  
concrete flatwork, asphalt repair, commercial parking lot repair, concrete pads, sidewalks, walkways, curbs, exterior property improvements

**Suggested FAQ themes:**

- Types of flatwork completed.
- Asphalt repair versus replacement.
- Working around active businesses.
- Phased parking-lot access.
- Drainage and surface planning.
- Concrete curing and project access.

Only include paving, striping, drainage, or related capabilities that the company actually provides or manages.

### 10.12 Facility maintenance and on-call repairs

**URL:**  
`/services/commercial/facility-maintenance-on-call-repairs/`

**SEO title:**  
Facility Maintenance Bakersfield, CA \| West Coast Construction

**Meta description:**  
Keep your Bakersfield commercial property operating with on-call facility maintenance, construction repairs, exterior work, and coordinated service.

**H1:**  
Commercial Facility Maintenance & On-Call Repairs in Bakersfield, CA

**Primary keyword:**  
commercial facility maintenance Bakersfield CA

**Related terms:**  
commercial property maintenance, on-call contractor, building repairs, facility repair services, property-manager contractor, commercial maintenance services

**Suggested FAQ themes:**

- Types of repairs handled.
- One-time versus ongoing work.
- Scheduling around operations.
- Service for property managers.
- Documentation and repair scopes.
- Emergency versus non-emergency calls.

## Emergency service pages

### 10.13 Emergency water-damage response

**URL:**  
`/services/emergency/emergency-water-damage-response/`

**SEO title:**  
Water Damage Response Bakersfield, CA \| West Coast Construction

**Meta description:**  
Call for 24/7 construction response to water intrusion and property damage in Bakersfield, including assessment, containment, stabilization, and repairs.

**H1:**  
24/7 Emergency Water Damage Response in Bakersfield, CA

**Primary keyword:**  
emergency water damage response Bakersfield CA

**Related terms:**  
water intrusion response, emergency water damage repair, property stabilization, ceiling water damage, wall water damage, construction damage response

**Suggested FAQ themes:**

- Immediate steps after discovering water.
- When to leave the affected area.
- Initial assessment and containment.
- Temporary stabilization.
- Damage documentation.
- Transition from emergency response to permanent repair.

Do not claim mold remediation, water extraction, plumbing repair, or insurance-adjusting services unless verified.

### 10.14 Emergency roof leaks

**URL:**  
`/services/emergency/emergency-roof-leaks/`

**SEO title:**  
Emergency Roof Repair Bakersfield, CA \| West Coast Construction

**Meta description:**  
Get 24/7 help for an active roof leak in Bakersfield with rapid assessment, temporary protection, damage control, and a plan for permanent repairs.

**H1:**  
24/7 Emergency Roof Leak Repair in Bakersfield, CA

**Primary keyword:**  
emergency roof repair Bakersfield CA

**Related terms:**  
emergency roof leak, active roof leak, temporary roof repair, leaking ceiling, storm roof leak, urgent roofing contractor

**Suggested FAQ themes:**

- What to do during an active leak.
- Temporary protection options.
- Response during ongoing weather.
- Interior damage caused by leaks.
- Temporary versus permanent roof repair.
- Difference between emergency and scheduled roof service.

### 10.15 Storm-damage emergency repairs

**URL:**  
`/services/emergency/storm-damage-emergency-repairs/`

**SEO title:**  
Storm Damage Repair Bakersfield, CA \| West Coast Construction

**Meta description:**  
Call for 24/7 storm damage repair in Bakersfield for roof, exterior, water-intrusion, and property damage requiring immediate stabilization.

**H1:**  
24/7 Storm Damage & Emergency Repairs in Bakersfield, CA

**Primary keyword:**  
storm damage repair Bakersfield CA

**Related terms:**  
wind damage repair, rain damage, emergency exterior repair, storm roof damage, property stabilization, board-up service

**Suggested FAQ themes:**

- Types of storm damage handled.
- Immediate safety steps.
- Temporary stabilization.
- Board-up availability when verified.
- Damage documentation.
- Permanent repair planning.

### 10.16 Emergency property-damage repairs

**URL:**  
`/services/emergency/emergency-property-damage-repairs/`

**SEO title:**  
Property Damage Repair Bakersfield, CA \| West Coast Construction

**Meta description:**  
Get 24/7 construction help for urgent residential or commercial property damage in Bakersfield, from site assessment and stabilization to repair planning.

**H1:**  
24/7 Emergency Property Damage Repairs in Bakersfield, CA

**Primary keyword:**  
emergency property damage repair Bakersfield CA

**Related terms:**  
urgent property repair, residential property damage, commercial property damage, impact damage, board-up, construction emergency contractor

**Suggested FAQ themes:**

- What qualifies as emergency property damage.
- Residential and commercial response.
- Board-up and temporary containment.
- Damage documentation.
- Safety and access restrictions.
- Permanent reconstruction process.

### 10.17 Ceiling collapse and drywall failure

**URL:**  
`/services/emergency/ceiling-collapse-drywall-failure-emergency-repairs/`

**SEO title:**  
Ceiling Collapse Repair Bakersfield, CA \| West Coast Construction

**Meta description:**  
Call for urgent help with a ceiling collapse or drywall failure in Bakersfield, including safety assessment, containment, stabilization, and repairs.

**H1:**  
Ceiling Collapse & Drywall Failure Emergency Repair in Bakersfield, CA

**Primary keyword:**  
ceiling collapse repair Bakersfield CA

**Related terms:**  
emergency drywall repair, sagging ceiling, water-damaged ceiling, collapsed drywall, ceiling failure, urgent ceiling repair

**Suggested FAQ themes:**

- Warning signs before a ceiling collapses.
- Whether to leave the room.
- Water and electrical safety.
- Temporary containment.
- Determining the cause.
- Permanent ceiling and drywall repairs.

Avoid diagnosing structural or electrical conditions without an inspection.

### 10.18 Emergency structural stabilization

**URL:**  
`/services/emergency/emergency-structural-stabilization/`

**SEO title:**  
Structural Stabilization Bakersfield, CA \| West Coast Construction

**Meta description:**  
Get 24/7 help for suspected structural damage in Bakersfield with site assessment, temporary stabilization, damage documentation, and repair planning.

**H1:**  
24/7 Emergency Structural Stabilization in Bakersfield, CA

**Primary keyword:**  
emergency structural stabilization Bakersfield CA

**Related terms:**  
structural damage response, temporary shoring, unstable wall, impact damage, emergency building stabilization, structural repair contractor

**Suggested FAQ themes:**

- Signs of possible structural instability.
- When occupants should leave.
- Temporary stabilization and shoring.
- Engineer involvement.
- Damage from impact, storms, or failure.
- Transitioning to permanent structural repair.

Do not represent West Coast Construction Group as a structural engineering firm unless that service is independently licensed and verified.

## 11. Internal-linking architecture

### Homepage links

The homepage must link to:

- All three parent service pages.
- At least three priority residential child pages.
- At least three priority commercial child pages.
- The emergency parent page.
- At least two priority emergency child pages.
- Contact page.
- About page.
- Project gallery or case studies when available.

### Parent-page links

Each parent page must link to all six children in its category.

### Child-page links

Every child page must link to:

- Its parent service page.
- Contact page.
- Homepage through breadcrumbs.
- Two to four relevant sibling services.
- One related service from another silo when contextually useful.

Examples:

- ADU page → home additions and remodeling.
- Standard roof-repair page → emergency roof-leak page.
- Tenant-improvements page → commercial remodeling and commercial GC.
- Storm-damage page → emergency roof leaks and structural stabilization.

### Anchor-text rules

Use descriptive anchor text such as:

- Bakersfield ADU construction.
- Commercial tenant improvements.
- Emergency roof-leak repair.
- Home additions and expansions.

Avoid relying on:

- Click here.
- Learn more.
- This page.
- Services.

Generic button labels may be visually displayed when necessary, but include descriptive surrounding context and accessible labels.

## 12. Metadata requirements

Every page must contain:

- Unique `<title>`.
- Unique meta description.
- Self-referencing canonical URL.
- `index, follow` robots directive in production.
- Unique Open Graph title.
- Unique Open Graph description.
- Correct Open Graph URL.
- Relevant Open Graph image.
- Twitter large-image metadata.
- Consistent site name.
- Correct language declaration.

Do not reuse one meta description across multiple pages.

Do not automatically append excessively long keyword phrases to every title.

Staging and preview deployments must remain `noindex` until production launch.

## 13. Structured data

### Homepage and sitewide business entity

Create a consistent schema graph containing:

- `WebSite`.
- `GeneralContractor` as the most specific applicable local-business entity.
- Business name.
- Alternate brand name if used.
- Canonical website URL.
- Logo.
- Telephone.
- Verified public address or valid service-area configuration.
- Bakersfield and Kern County area served.
- License identifier when correctly represented.
- Social-profile URLs.
- Opening hours or emergency availability only when accurate.
- Links between the business entity and website.

Use one stable `@id` for the business entity across the site.

### Page-level schema

Add where appropriate:

- `WebPage`.
- `BreadcrumbList`.
- `Service` describing the visible page service and referencing the business as provider.

Do not add structured data for services, claims, reviews, prices, ratings, or availability that are not visible and verified on the page.

Do not implement `FAQPage` solely for a Google FAQ rich result.

Validate the final schema with:

- Google Rich Results Test for Google-supported features.
- Schema Markup Validator for general Schema.org syntax.

## 14. Image SEO and media requirements

For every content image:

- Use real project photography whenever possible.
- Create descriptive filenames before upload.
- Supply concise, accurate alt text.
- Add width and height attributes to reduce layout shift.
- Use responsive `srcset` or the framework’s image component.
- Serve WebP or AVIF where supported.
- Lazy-load below-the-fold images.
- Do not lazy-load the main hero image when it would delay the largest visible content.
- Add captions when the image documents a real Bakersfield-area project.
- Avoid reusing the same hero image on many service pages.
- Avoid stock photos that falsely imply completed company work.

Create a branded Open Graph image system with appropriate images for:

- Homepage.
- Residential category.
- Commercial category.
- Emergency category.
- Individual pages where suitable imagery is available.

## 15. Accessibility and mobile requirements

- Use semantic landmarks: `header`, `nav`, `main`, `section`, `aside`, and `footer`.
- Maintain a logical keyboard-navigation order.
- Give buttons and links visible focus states.
- Meet accessible text contrast.
- Use descriptive form labels.
- Keep accordion controls keyboard accessible.
- Use `aria-expanded` and `aria-controls` for custom accordions.
- Ensure tap targets are comfortably sized.
- Use click-to-call links on mobile.
- Prevent sticky mobile controls from covering page content.
- Respect reduced-motion preferences.
- Provide useful error and confirmation states for forms.

## 16. Technical implementation requirements

Create reusable components rather than 18 independent hard-coded page layouts.

Recommended component structure:

- `SiteHeader`
- `Breadcrumbs`
- `ServiceHero`
- `TrustBar`
- `ServiceOverview`
- `ServiceScopeGrid`
- `ProblemSignsSection`
- `ProcessSteps`
- `LocalServiceSection`
- `WhyChooseUs`
- `RelatedServices`
- `FaqAccordion`
- `ServiceCta`
- `Testimonials`
- `ProjectGallery`
- `SiteFooter`
- `SeoMetadata`
- `StructuredData`

Store service-specific page information in a structured data file or content collection.

Each page record should support fields such as:

- Slug.
- Parent category.
- SEO title.
- Meta description.
- H1.
- Hero introduction.
- Primary keyword.
- Related terms.
- Scope subsections.
- Problem or need sections.
- Process steps.
- Local content.
- FAQs.
- Related-page IDs.
- Hero image.
- Open Graph image.
- Image alt text.
- CTA type.
- Structured-data service name.

Page content must be server-rendered or statically generated and available in the initial HTML.

Create or update:

- XML sitemap.
- Robots configuration.
- Redirect configuration.
- Canonical generation.
- 404 handling.
- Metadata generation.
- Analytics integration.
- Search Console verification.
- Form tracking.
- Click-to-call tracking.
- Estimate-button tracking.

## 17. GitPress/Broseph workflow

This scope assumes GitPress is used for the primary implementation pass and Broseph is used for structured review, SEO validation, and revision. Reverse the labels if the actual tool responsibilities differ.

### Phase 1: Repository and design audit

GitPress must:

1.  Inspect the current repository and framework.
2.  Identify shared header, footer, typography, color, button, form, and layout systems.
3.  Locate analytics, metadata, sitemap, robots, and redirect implementations.
4.  Identify where current parent pages are generated.
5.  Document existing reusable components before adding new ones.
6.  Confirm the production route structure.
7.  Record any facts that need client verification.

Deliverable:

- Short repository audit.
- Component reuse plan.
- Route plan.
- Migration-risk list.
- List of business facts requiring verification.

Do not begin by generating 18 disconnected pages.

### Phase 2: Shared system and homepage

GitPress must:

1.  Build the reusable service landing-page template.
2.  Build metadata and schema helpers.
3.  Rebuild the homepage.
4.  Create service-card and related-service components.
5.  Correct navigation and footer URLs.
6.  Create the emergency-parent redirect.
7.  Add responsive and accessibility behavior.
8.  Preserve tracking.

Deliverable:

- Homepage implementation.
- Shared component library.
- One sample page configuration.
- Responsive screenshots.
- Successful production build.

### Phase 3: Pilot service pages

Build one page from each silo first:

- Custom home building.
- Tenant improvements.
- Emergency roof leaks.

Broseph must review the three pilot pages for:

- Search-intent differentiation.
- Page uniqueness.
- Heading hierarchy.
- Keyword use.
- Local relevance.
- FAQ quality.
- Internal links.
- Conversion flow.
- Mobile experience.
- Metadata.
- Structured data.
- Unsupported claims.

Resolve the pilot-page review before scaling the template to the remaining pages.

### Phase 4: Residential batch

Implement:

- All six residential service pages.
- Residential parent-page service cards.
- Residential contextual internal links.
- Residential metadata and schema.
- Image and alt-text assignments.

Deliverable:

- Separate residential pull request.
- Page inventory.
- Build results.
- Responsive screenshots for representative pages.
- SEO QA checklist.

### Phase 5: Commercial batch

Implement:

- All six commercial service pages.
- Commercial parent-page service cards.
- Commercial contextual internal links.
- Commercial metadata and schema.
- Image and alt-text assignments.

Deliverable:

- Separate commercial pull request.
- Page inventory.
- Build results.
- Responsive screenshots.
- SEO QA checklist.

### Phase 6: Emergency batch

Implement:

- New `/services/emergency/` parent.
- All six emergency service pages.
- 301 redirect from `/services/emergency-services/`.
- Emergency calls to action.
- Click-to-call behavior.
- Emergency metadata and schema.
- Emergency-related internal links.

Deliverable:

- Separate emergency pull request.
- Redirect test.
- Page inventory.
- Build results.
- Responsive screenshots.
- SEO QA checklist.

### Phase 7: Broseph final review

Broseph must perform a sitewide review for:

- Duplicate introductions.
- Duplicate FAQ questions and answers.
- Keyword cannibalization.
- Multiple H1 elements.
- Skipped heading levels.
- Missing metadata.
- Broken internal links.
- Orphan pages.
- Incorrect canonicals.
- Incorrect redirects.
- Missing alt text.
- Generic link text.
- Unsupported business claims.
- Missing schema fields.
- Schema that does not match visible content.
- Mobile layout problems.
- Form or telephone-link failures.

Broseph should return findings grouped as:

- Blocking.
- High priority.
- Medium priority.
- Optional enhancement.

GitPress then implements the blocking and high-priority corrections.

### Phase 8: Final launch verification

Before merging:

1.  Run the production build.
2.  Run linting and type checking.
3.  Crawl all 22 affected URLs.
4.  Confirm a 200 response for every intended page.
5.  Confirm the old emergency URL returns one 301 to the new parent.
6.  Confirm there are no redirect chains.
7.  Validate canonical tags.
8.  Validate metadata.
9.  Validate structured data.
10. Confirm staging `noindex` is removed only on production.
11. Test desktop and mobile forms.
12. Test click-to-call links.
13. Test navigation and breadcrumbs.
14. Confirm sitemap inclusion.
15. Confirm analytics events.
16. Submit or resubmit the sitemap.
17. Request indexing for the homepage, parent pages, and highest-priority child pages.

## 18. Acceptance criteria

The project is complete only when all of the following are true.

### Page inventory

- Homepage rebuilt.
- Three parent service hubs updated.
- Eighteen child service pages published.
- All specified routes are correct.
- Emergency parent redirect works.

### Content

- Every child page is materially unique.
- Every page satisfies its specific search intent.
- No page contains filler neighborhood or city lists.
- No page invents project experience, response times, warranties, insurance services, engineering services, or trade capabilities.
- Every page includes useful FAQs.
- Every page includes Bakersfield relevance without excessive repetition.

### On-page SEO

- Exactly one H1 per page.
- Logical H2-H5 hierarchy.
- Unique SEO title.
- Unique meta description.
- Self-referencing canonical.
- Correct Open Graph information.
- Descriptive image alt text.
- Descriptive internal-link anchors.
- No orphan service pages.
- No broken internal links.
- No accidental `noindex` directives in production.

### Structured data

- Valid sitewide business entity.
- Valid WebPage and BreadcrumbList data.
- Service data matches visible content.
- No unsupported or misleading review, rating, FAQ, or business data.
- No critical validator errors.

### User experience

- Responsive on common desktop, tablet, and mobile widths.
- Phone and estimate actions work.
- Emergency pages prioritize the telephone action.
- Forms include success and error feedback.
- FAQ accordions are accessible.
- No layout shift caused by missing image dimensions.
- No sticky element blocks important content.

### Engineering

- Production build passes.
- Lint and type checks pass.
- Shared components are used.
- Metadata is data-driven.
- Page content is server-rendered or statically generated.
- Sitemap includes all new canonical URLs.
- Redirect rules are committed.
- No WordPress export or admin markup is included.
- No console errors appear during normal page use.

## 19. Information that must be verified before final publication

Do not guess these details:

- Exact public business name.
- Whether the preferred displayed brand is “West Coast Construction,” “West Coast Construction Group,” or “West Coast Construction GRP.”
- Current phone number.
- License number and approved license wording.
- Insurance wording.
- Public address or whether the company is service-area only.
- Current service areas.
- Whether San Luis Obispo County should remain prominent.
- Actual 24/7 staffing and response availability.
- Services self-performed versus subcontracted or coordinated.
- Roofing capabilities.
- Asphalt and paving capabilities.
- Board-up capabilities.
- Water extraction or mitigation capabilities.
- Mold-remediation capabilities.
- Structural-shoring capabilities.
- Structural-engineering relationships.
- Insurance-claim documentation or coordination.
- Financing program and required disclosures.
- Warranties.
- Project photographs and permissions.
- Customer testimonials and permissions.

Use visible placeholders in draft content until these items are confirmed.

## 20. Out of scope unless separately approved

- Separate city landing pages for every Kern County community.
- Blog-post production.
- Ongoing monthly SEO.
- Backlink outreach.
- Google Business Profile management.
- Paid-search campaigns.
- New photography or video production.
- Full customer portal or estimate system.
- Online emergency dispatch.
- Insurance adjusting.
- Translation into additional languages.
- Unverified review or aggregate-rating schema.

## 21. Final definition of done

The implementation is done when West Coast Construction Group has a rebuilt, conversion-focused homepage and a crawlable Bakersfield service architecture consisting of three parent service hubs and 18 substantially unique child pages.

Visitors and search engines must be able to understand:

- What each page is about.
- How that service differs from adjacent services.
- Where the company operates.
- Why the company is relevant to the project.
- What the next step is.
- How to contact the company.
- Which related service page may help next.

The completed work must be technically valid, accessible, responsive, internally connected, free of unsupported claims, and ready for production indexing.
