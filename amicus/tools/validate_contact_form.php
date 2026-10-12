<?php
// Run against an isolated WordPress test installation. This only calls import
// preview: it does not save a form or send a message.
$root = dirname(__DIR__);
$wordpress = getenv('AMICUS_TEST_WP');
if (!$wordpress || !is_file($wordpress . DIRECTORY_SEPARATOR . 'wp-load.php')) {
    fwrite(STDERR, "Set AMICUS_TEST_WP to an isolated WordPress directory.\n");
    exit(2);
}
require $wordpress . DIRECTORY_SEPARATOR . 'wp-load.php';
if (!class_exists('GitPress\\Forms\\Importer')) {
    fwrite(STDERR, "GitPress Forms is not active in the test installation.\n");
    exit(2);
}
$input = json_decode(file_get_contents($root . '/forms/contact-import.json'), true, 512, JSON_THROW_ON_ERROR);
$preview = GitPress\Forms\Importer::preview($input);
if (count($preview['forms']) !== 1) {
    throw new RuntimeException('Expected one contact form in import preview.');
}
$form = $preview['forms'][0]['definition'];
$fields = $form['fields'];
if (array_column($fields, 'name') !== array('name', 'email', 'message')) {
    throw new RuntimeException('Contact fields differ from the source form.');
}
if (count(array_filter($fields, static function ($field) { return $field['required']; })) !== 3) {
    throw new RuntimeException('All three contact fields must be required.');
}
if (($form['settings']['notifications'][0]['to'] ?? '') !== 'info@amicusfoundation.com') {
    throw new RuntimeException('Notification recipient mismatch.');
}
echo "GitPress Forms import preview validated: 3 required fields, contact notification, schema version 1.\n";
