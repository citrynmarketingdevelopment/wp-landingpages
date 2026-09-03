# SJO GitPress Integration

Status: prepared locally. Nothing in WordPress has been changed or published.

## Rendering model

The shared `header.html` and `footer.html` fragments require GitPress Managed mode. Apply the following settings to the existing pages only when deployment is approved:

```txt
render_mode: gitpress_managed
render_position: replace
full_page_canvas: true
full_width_content: false
```

Do not enable the managed shell while a page is still using the Divi theme shell. Mixing the two modes will duplicate the header and footer.

## Global shell shortcodes

Header:

```text
[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="sjo/header.html" format="html"]
```

Footer:

```text
[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="sjo/footer.html" format="html"]
```

## Existing pages

| Page | Existing ID | Route | Body shortcode |
| --- | ---: | --- | --- |
| Home | 12 | `/` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="sjo/home.html" format="html"]` |
| Services | 96 | `/services/` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="sjo/services.html" format="html"]` |
| Contact Us | 71 | `/contact-us/` | `[divi_github_content owner="citrynmarketingdevelopment" repo="wp-landingpages" branch="main" path="sjo/contact.html" format="html"]` |

Convert these pages in place after backing them up. Do not create replacement pages or change their public routes.

## Managed header behavior

The production header exposes the required GitPress hooks:

- `#siteHeader`
- `#hamburger`
- `#sheetScrim`
- `#mobileSheet`
- `.mobile-sheet`
- `[data-nav]`
- `body.menu-open`
- `.site-header.scrolled`

The GitPress Managed canvas or an approved shared asset must bind the hamburger, scrim, Escape key, active-link, scrolled-header, breakpoint cleanup, and drawer-focus behavior. Critical JavaScript is intentionally not embedded in the sanitized header fragment. The standalone previews provide a local-only behavior binder.

Confirm those behaviors against the exact hooks above before publishing. Without the managed binder, desktop navigation remains usable, but the mobile drawer and Home scrolled-header state will not be production-ready.

## Contact and pending assets

- Contact uses `[fluentform id="3"]`.
- The preview substitutes a non-submitting form facsimile.
- The approved public email is `info@sanjoaquinoperators.com`.
- The Privacy Policy link remains unpublished pending an approved policy and URL.
- The header and footer wordmarks are temporary assets pending an approved client logo package.
- Home retains the current affiliation logos pending the client&rsquo;s replacement logo package. The global footer keeps text fallbacks so the same logos are not repeated in every page shell.
- Home&rsquo;s Quick Access section uses `home-field-team.webp` as a temporary project image. Replace that asset when the client-supplied project photo arrives; the edge-grading treatment is already applied in the page CSS.
