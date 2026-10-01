# WCC homepage interactions

GitPress sanitizes scripts and iframes in GitHub HTML fragments. Install
`wcc-home-interactions.zip` as a WordPress plugin on wccgrp.com to load the
homepage script through WordPress. The script enables the review controls and
adds the Instagram profile iframe after GitPress finishes sanitizing the page.

The plugin runs only on the WordPress front page. It pins the script to the
verified `d98aa25` commit so jsDelivr cannot serve an older `@main` copy.
After activating it, clear the WordPress page cache and check that the live
homepage contains the `native-video-gallery-2026-10-01-v6` marker.
