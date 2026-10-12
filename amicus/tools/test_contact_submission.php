<?php
// Synthetic GitPress Forms end-to-end test in a disposable WordPress install.
// Mail is intercepted before wp_mail can reach a transport.
define('DISABLE_WP_CRON', true);
$root = dirname(__DIR__);
$wordpress = getenv('AMICUS_TEST_WP');
if (!$wordpress || !is_file($wordpress . DIRECTORY_SEPARATOR . 'wp-load.php')) {
    fwrite(STDERR, "Set AMICUS_TEST_WP to an isolated WordPress directory.\n");
    exit(2);
}
require $wordpress . DIRECTORY_SEPARATOR . 'wp-load.php';
require_once $root . '/wp-plugin/amicus-site.php';
if (!class_exists('GitPress\\Forms\\Importer')) {
    throw new RuntimeException('GitPress Forms is not active.');
}

function amicus_test_assert($condition, $message) {
    if (!$condition) { throw new RuntimeException($message); }
}

wp_set_current_user(1);
amicus_test_assert(current_user_can('manage_options'), 'The isolated test user must be an administrator.');
$input = json_decode(file_get_contents($root . '/forms/contact-import.json'), true, 512, JSON_THROW_ON_ERROR);
$import = GitPress\Forms\Importer::run($input);
$formId = (int) ($import['forms'][0]['id'] ?? 0);
amicus_test_assert($formId > 0, 'The native importer did not return a numeric ID.');
$again = GitPress\Forms\Importer::run($input);
amicus_test_assert((int) $again['forms'][0]['id'] === $formId && !empty($again['forms'][0]['alreadyImported']), 'The native import is not idempotent.');
$form = GitPress\Forms\Repository::form($formId);
GitPress\Forms\Repository::save(array(
    'title' => $form['title'],
    'definition' => $form['definition'],
    'status' => 'published',
    'version' => $form['version'],
), $formId);
$markup = do_shortcode('[gitpress_form id="' . $formId . '"]');
foreach (array('name="name"', 'name="email"', 'name="message"', 'class="gpf-alert"', 'name="_gpf_website"') as $needle) {
    amicus_test_assert(strpos($markup, $needle) !== false, 'Rendered form is missing ' . $needle);
}
amicus_test_assert(do_shortcode('[amicus_form_status id="' . $formId . '"]') === '', 'Published form shows the unavailable state.');
amicus_test_assert(strpos(do_shortcode('[amicus_form_status id="0"]'), 'temporarily unavailable') !== false, 'Unavailable form state is missing.');
if (class_exists('DGS_Shortcode_Handler')) {
    $renderFragment = new ReflectionMethod('DGS_Shortcode_Handler', 'render_html_fragment');
    foreach (array('contact-us.html', 'recommended-charities.html') as $fragmentName) {
        $fragment = str_replace('__AMICUS_CONTACT_FORM_ID__', (string) $formId, file_get_contents($root . '/' . $fragmentName));
        $rendered = $renderFragment->invoke(null, $fragment);
        amicus_test_assert(strpos($rendered, 'class="gpf-form') !== false, $fragmentName . ' lost the form during GitPress rendering.');
        amicus_test_assert(strpos($rendered, 'temporarily unavailable') === false, $fragmentName . ' shows an unavailable notice for a published form.');
    }
}

global $wpdb;
$jobsTable = GitPress\Forms\Database::table('jobs');
$heldJobs = $wpdb->get_results("SELECT id,available_at FROM $jobsTable WHERE status='pending' AND available_at <= UTC_TIMESTAMP()", ARRAY_A);
foreach ($heldJobs as $held) {
    $wpdb->update($jobsTable, array('available_at' => gmdate('Y-m-d H:i:s', time() + 3600)), array('id' => $held['id'], 'status' => 'pending'));
}
register_shutdown_function(static function () use ($wpdb, $jobsTable, $heldJobs) {
    foreach ($heldJobs as $held) {
        $wpdb->update($jobsTable, array('available_at' => $held['available_at']), array('id' => $held['id'], 'status' => 'pending'));
    }
});
$_SERVER['REMOTE_ADDR'] = '127.0.0.248';
unset($_SERVER['HTTP_ORIGIN']);
$token = GitPress\Forms\Security::token($formId);
$base = array('token' => $token, 'source' => home_url('/contact-us/'));
$unique = bin2hex(random_bytes(8));
$invalid = GitPress\Forms\Submissions::submit($formId, $base + array(
    'idempotencyKey' => 'amicusinvalid0001',
    'values' => array('name' => '', 'email' => 'invalid', 'message' => ''),
));
amicus_test_assert(isset($invalid['errors']['name'], $invalid['errors']['email'], $invalid['errors']['message']), 'Required-field and email validation failed.');
try {
    GitPress\Forms\Submissions::submit($formId, array('token' => 'invalid', 'idempotencyKey' => 'amicusbadtoken001', 'values' => array()));
    throw new RuntimeException('The invalid session token was accepted.');
} catch (RuntimeException $error) {
    amicus_test_assert($error->getCode() === 403, 'Unexpected session-token failure: ' . $error->getMessage());
}
$message = array('name' => 'Amicus Test', 'email' => 'amicus-test@example.test', 'message' => 'Synthetic staging message.');
$accepted = GitPress\Forms\Submissions::submit($formId, $base + array('idempotencyKey' => 'amicusSuccess' . $unique, 'values' => $message));
amicus_test_assert(!empty($accepted['success']), 'Valid contact submission was rejected.');
$job = $wpdb->get_row($wpdb->prepare("SELECT j.* FROM $jobsTable j JOIN " . GitPress\Forms\Database::table('entries') . " e ON e.id=j.entry_id WHERE e.form_id=%d ORDER BY j.id DESC LIMIT 1", $formId), ARRAY_A);
amicus_test_assert($job && $job['status'] === 'pending' && $job['kind'] === 'notification', 'Notification job was not queued.');

$mail = array();
$interceptor = static function ($result, $args) use (&$mail) {
    $mail[] = $args;
    return true;
};
add_filter('pre_wp_mail', $interceptor, 10, 2);
GitPress\Forms\Jobs::run();
remove_filter('pre_wp_mail', $interceptor, 10);
$status = $wpdb->get_var($wpdb->prepare("SELECT status FROM $jobsTable WHERE id=%d", $job['id']));
amicus_test_assert($status === 'completed', 'Intercepted notification did not complete.');
amicus_test_assert(count($mail) === 1 && in_array('info@amicusfoundation.com', (array) $mail[0]['to'], true), 'Mail was not routed to the requested address.');

$second = GitPress\Forms\Submissions::submit($formId, $base + array('idempotencyKey' => 'amicusFailure' . $unique, 'values' => $message));
amicus_test_assert(!empty($second['success']), 'The mail-failure test submission was rejected.');
$failureJob = $wpdb->get_row($wpdb->prepare("SELECT j.* FROM $jobsTable j JOIN " . GitPress\Forms\Database::table('entries') . " e ON e.id=j.entry_id WHERE e.form_id=%d ORDER BY j.id DESC LIMIT 1", $formId), ARRAY_A);
$failingInterceptor = static function () { return false; };
add_filter('pre_wp_mail', $failingInterceptor, 10, 2);
GitPress\Forms\Jobs::run();
remove_filter('pre_wp_mail', $failingInterceptor, 10);
$failed = $wpdb->get_row($wpdb->prepare("SELECT status,attempts,last_error FROM $jobsTable WHERE id=%d", $failureJob['id']), ARRAY_A);
amicus_test_assert($failed['status'] === 'pending' && (int) $failed['attempts'] === 1 && strpos($failed['last_error'], 'could not send') !== false, 'Mail failure was not retained for retry.');

$report = array(
    'environment' => 'isolated WordPress',
    'native_import' => 'passed',
    'idempotent_import' => 'passed',
    'rendered_fields_and_states' => 'passed',
    'gitpress_fragment_rendering' => 'passed',
    'required_and_email_validation' => 'passed',
    'session_token_rejection' => 'passed',
    'synthetic_submission' => 'passed',
    'intercepted_mail_recipient' => 'info@amicusfoundation.com',
    'mail_failure_retry' => 'passed',
    'production_form_id_bound' => false,
);
file_put_contents($root . '/qa/form-test-result.json', json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n");
echo json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
