<?php
/**
 * Plugin Name: WCC Home Interactions
 * Description: Loads the West Coast Construction homepage controls after GitPress renders the sanitized page.
 * Version: 1.0.2
 * Requires PHP: 7.4
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action(
	'wp_enqueue_scripts',
	static function () {
		if ( ! is_front_page() ) {
			return;
		}

		wp_enqueue_script(
			'wcc-home-interactions',
			'https://cdn.jsdelivr.net/gh/citrynmarketingdevelopment/wp-landingpages@d98aa25/wcc/assets/js/wcc.js',
			array(),
			'd98aa25',
			true
		);
	}
);
