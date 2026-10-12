"""Create reviewable, backup-first Broseph conversion payloads (no network writes)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
routes = json.loads((ROOT / "routes.json").read_text(encoding="utf-8"))
conversions = []
for public_path, page in routes["pages"].items():
    if public_path.startswith("/project/"):
        continue  # Broseph v1 conversion accepts post_type=page only.
    seo = page["seo"]
    if not (seo.get("source_post_id") and seo.get("source_slug")):
        raise SystemExit(f"Missing public WordPress identity for {public_path}")
    conversions.append({
        "path": public_path,
        "source_page_id": int(seo["source_post_id"]),
        "endpoint": f"/wp-json/broseph/v1/pages/{seo['source_post_id']}/convert-to-gitpress",
        "payload": {
            "shortcode": page["shortcode"],
            "render_mode": "gitpress_managed",
            "render_position": "replace",
            "full_width_content": False,
            "full_page_canvas": True,
            "backup_first": True,
            "clear_existing_content": True,
            "disable_divi_builder": True,
            "expected_slug": seo["source_slug"],
            "expected_status": seo["source_status"],
        },
        "seo_snapshot": {
            "title": seo["title"],
            "description": seo["description"],
            "canonical": seo["canonical"],
            "og_image": seo["og_image"],
        },
        "source_parent_id": seo["source_parent_id"],
    })
(ROOT / "deployment.json").write_text(json.dumps({
    "conversion_endpoint_note": "These payloads are for review and staging use. Confirm page identity and plugin capabilities before posting.",
    "global_header_shortcode": routes["managed_header_shortcode"],
    "global_footer_shortcode": routes["managed_footer_shortcode"],
    "page_conversions": conversions,
    "project_test": {
        "source_post_id": routes["pages"]["/project/test/"]["seo"]["source_post_id"],
        "shortcode": routes["pages"]["/project/test/"]["shortcode"],
        "instruction": "Set the GitPress page-level shortcode/render mode on the existing project CPT post; Broseph v1 only converts pages.",
    },
    "archive_routes": routes["archives"],
    "redirects": routes["redirects"],
}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Prepared {len(conversions)} backup-first page conversion payloads")
