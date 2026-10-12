<?php
// Verify the actual GitPress HTML sanitizer and shortcode sequence in isolated WP.
$root = dirname(__DIR__);
$wordpress = getenv('AMICUS_TEST_WP');
if (!$wordpress || !is_file($wordpress . DIRECTORY_SEPARATOR . 'wp-load.php')) {
    fwrite(STDERR, "Set AMICUS_TEST_WP to an isolated WordPress directory.\n");
    exit(2);
}
require $wordpress . DIRECTORY_SEPARATOR . 'wp-load.php';
require_once $root . '/wp-plugin/amicus-site.php';
if (!class_exists('DGS_Shortcode_Handler')) {
    fwrite(STDERR, "GitPress is not active in the test installation.\n");
    exit(2);
}
$method = new ReflectionMethod('DGS_Shortcode_Handler', 'render_html_fragment');
$html = $method->invoke(null, file_get_contents($root . '/header.html'));
$checks = array(
    'header ID' => strpos($html, 'id="siteHeader"') !== false,
    'hamburger ID' => strpos($html, 'id="hamburger"') !== false,
    'mobile sheet ID' => strpos($html, 'id="mobileSheet"') !== false,
    'header navigation' => strpos($html, 'amicus-desktop-nav') !== false,
);
$home = $method->invoke(null, file_get_contents($root . '/home.html'));
$checks['page content'] = strpos($home, 'Grants That Make a Difference') !== false;
$checks['native accordion'] = strpos($home, 'amicus-toggle') !== false;
$jotform = $method->invoke(null, '[amicus_jotform id="230195983314055"]');
$checks['Jotform embed'] = strpos($jotform, 'form.jotform.com/jsform/230195983314055') !== false;
$youtube = $method->invoke(null, '[amicus_youtube id="YHHtyO33FMA"]');
$checks['YouTube embed'] = strpos($youtube, 'youtube.com/embed/YHHtyO33FMA') !== false;
$unavailable = $method->invoke(null, '[amicus_form_status id="0"]');
$checks['unavailable contact state'] = strpos($unavailable, 'temporarily unavailable') !== false;
$checks['script sanitization'] = strpos($method->invoke(null, '<script>alert(1)</script>'), 'alert(1)') === false;
$routes = json_decode(file_get_contents($root . '/routes.json'), true, 512, JSON_THROW_ON_ERROR);
$renderedRoutes = 0;
foreach (array_merge($routes['pages'], $routes['archives']) as $record) {
    $rendered = $method->invoke(null, file_get_contents($root . '/' . $record['file']));
    if (strpos($rendered, 'amicus-page') === false || strpos($rendered, 'id="siteHeader"') !== false) {
        $checks['render ' . $record['file']] = false;
    }
    $renderedRoutes++;
}
$checks['all route fragments rendered'] = $renderedRoutes === 17;
foreach ($checks as $name => $ok) {
    echo ($ok ? 'PASS ' : 'FAIL ') . $name . "\n";
}
if (in_array(false, $checks, true)) { exit(1); }
