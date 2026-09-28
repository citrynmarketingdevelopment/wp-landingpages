# Capacity Constraint Assessment — editable Divi layout

Import **[../capacity-constraint-assessment.divi.json](../capacity-constraint-assessment.divi.json)**.

This rebuilds `alpha-nova/capacity-constraint-assessment.html` as a Divi 4 page layout using the format of the supplied Aerospace case-study export. All 14 content sections are separate Divi Sections, with native Rows, Columns, and modules. A fifteenth utility section contains the portable CSS. The original HTML and sample JSON are unchanged.

## Import into a page

1. Open a new or draft WordPress page and enable the Divi Builder.
2. Open the builder's **Portability** dialog (the import/export arrows), then **Import**.
3. Choose `capacity-constraint-assessment.divi.json` and import the layout. On a new page, replace the initial empty content; on an existing page, use the dialog's backup option before replacing content.
4. Switch to **Wireframe View** to see the numbered sections and named modules. Save the draft and check it in Divi's desktop, tablet, and phone views.

Use the **page builder's** portability dialog. This file has `context: "et_builder"`, matching the supplied export; it is not a Divi Library collection or a Theme Builder template export. See [Elegant Themes' import instructions](https://help.elegantthemes.com/en/articles/8626073-importing-exporting-divi-builder-layouts-library-collections).

This is page body content. The site's existing header/footer or page template controls the surrounding page. If the current page uses a GitPress shortcode to render the old HTML, replace that body content with this imported layout and ensure GitPress is not configured to replace the page output afterward.

## What you can edit

| Element | Divi representation |
| --- | --- |
| Each of the 14 original sections | Separate, named Section |
| Headings, paragraphs, checklists, card icons/numbers | 95 Text modules |
| Client logos and testimonial artwork | 15 Image modules |
| CTA links | 2 Button modules |
| FAQ questions and answers | 11 independent Toggle modules |
| Shared decorative and responsive styles | 1 Code module in `00 \| Shared layout styles (keep)` |
| LeadConnector form and its embed script | 1 Code module in `14 \| Request your assessment` |

There are 31 Rows and 57 Columns. Cards use native Columns containing individual Text modules. Move the Column to move a whole card, or move an individual module to rearrange its content. FAQs use independent Toggles so multiple answers can stay open, as in the original page.

Open Text modules to edit the copy and lists, Image modules to replace images, and Button modules to change labels or destinations. Headings are Text modules containing `h1`, `h2`, or `h3`; use their corresponding Heading Text controls in the Design tab. Standard typography, colors, alignment, padding, and margins are stored in the native module settings.

Keep the `00` styles section when using the layout. It has zero padding and no visible content on the published page; find it in Wireframe View. Its CSS uses the `anca-` namespace and does not apply global `body`, `:root`, heading, or link overrides. The code provides gear artwork, card decoration, accent spans, list markers, and responsive adjustments. Preserve the custom CSS classes when editing. If you copy a section to another page, copy the shared CSS module too. [Elegant Themes documents this portable Code-module technique](https://www.elegantthemes.com/blog/divi-resources/how-to-export-a-divi-page-layout-that-has-custom-code).

The testimonial images already contain their text. You can replace the image in Divi, but editing text inside the image requires editing the source artwork. The form's fields and submission routing are managed in LeadConnector; the Code module retains the original form ID, iframe attributes, and embed script.

## Architecture and format

The reference export uses six top-level keys:

```json
{
  "context": "et_builder",
  "data": { "1": "[et_pb_section ...]...[/et_pb_section]" },
  "presets": {},
  "global_colors": [],
  "images": {},
  "thumbnails": []
}
```

`data` maps an export content key to one shortcode string. The supplied export uses `21192`; the new layout uses `1` as its export key, not as a destination page ID. The hierarchy inside that string is:

```text
et_pb_section
  et_pb_row
    et_pb_column
      et_pb_text / et_pb_image / et_pb_button / et_pb_toggle / et_pb_code
```

The new modules use `_builder_version="4.27.4"`, as in the most recent modules in the supplied file. Each element has an `admin_label`. The existing `assessment`, `deliverables`, `faq`, and `request-assessment` anchors remain on their Divi Sections.

The sample includes unrelated global colors and an embedded base64 aerospace photo. This layout uses explicit local colors and references the page's 15 existing WordPress-hosted images instead, with their original paths and alt text. All image URLs were checked to return HTTP 200 over HTTPS; the export upgrades the source's HTTP image links to HTTPS. The empty `images` map means these existing images are referenced, not copied into a new site's Media Library. No sample presets or global color definitions are imported.

## Preview and verification

Open **[the local preview](../preview/capacity-constraint-assessment.divi.preview.html)** in a browser.

The preview simulates Divi's HTML wrappers and module styles. It does **not** run WordPress or Divi. Its FAQ interactions use native HTML details elements for inspection; the JSON contains actual Divi Toggle modules. Final import compatibility and the site's theme/preset interactions still need to be checked in Divi. The form can take a few seconds to load from LeadConnector.

Completed checks:

- Valid UTF-8 JSON, matching the reference envelope and a lossless JSON round trip.
- Balanced shortcode tags and valid Section → Row → Column → Module nesting.
- Every original heading, paragraph, list item, FAQ question, image path, and image alt text retained.
- Unique anchor IDs, working CTA fragment destinations, original iframe attributes, and exactly one form embed script.
- Local preview checked at 1440px, 820px, and 390px; no horizontal overflow and all 15 images loaded.
- LeadConnector form loaded; no form was submitted.

No import into a live WordPress/Divi installation has been performed. The file targets the Divi 4 format of the supplied export; Divi 5 conversion has not been tested.

## Rebuild from the HTML

```powershell
python alpha-nova/divi/build_capacity_layout.py
```

The build uses only Python's standard library. It reads the original HTML and `capacity-constraint-assessment.css`, then generates the JSON, `capacity-constraint-assessment.shortcodes.txt` for inspection, and the local preview. It validates the content and structure before writing the output. The source's section order is mapped explicitly; if sections are added or rearranged in the HTML, update the mapping in the build script.

Edits made in Divi are not synchronized back to the source HTML. Export the edited page from Divi if you want to preserve builder changes; rerunning this script regenerates the files from the repository source.
