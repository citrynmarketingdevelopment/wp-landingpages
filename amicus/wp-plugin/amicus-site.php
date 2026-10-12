<?php
/**
 * Plugin Name: Amicus GitPress Site
 * Description: Assets and native WordPress integrations for the Amicus Foundation GitPress migration.
 * Version: 1.0.0
 * Requires PHP: 7.4
 */

if (!defined('ABSPATH')) { exit; }

const AMICUS_GITPRESS_OWNER = 'citrynmarketingdevelopment';
const AMICUS_GITPRESS_REPO = 'wp-landingpages';
const AMICUS_GITPRESS_BRANCH = 'main';

function amicus_gitpress_short_code($path) {
    return sprintf(
        '[divi_github_content owner="%s" repo="%s" branch="%s" path="amicus/%s" format="html"]',
        AMICUS_GITPRESS_OWNER,
        AMICUS_GITPRESS_REPO,
        AMICUS_GITPRESS_BRANCH,
        $path
    );
}

function amicus_gitpress_route_slug() {
    if (is_front_page()) { return 'home'; }
    if (is_singular('project') && get_post_field('post_name', get_queried_object_id()) === 'test') {
        return 'project-test';
    }
    if (is_post_type_archive('project')) { return 'project-archive'; }
    if (is_author()) {
        $author = get_queried_object();
        return $author && isset($author->user_nicename) && $author->user_nicename === 'amicus' ? 'author-amicus' : '';
    }
    if (!is_page()) { return ''; }
    $slug = get_post_field('post_name', get_queried_object_id());
    $known = array(
        'zakouma', 'ww2-memorial', 'contact-us', 'dolly-parton-imagination',
        'warriors-quiet-waters', 'montana-wild-sheep-foundation',
        'returning-charities-application', 'bakersfield-pregnancy-center',
        'independence-through-grace', 'recommended-charities', 'grant-forms',
        'new-charities-application', 'montana-classrooms',
    );
    return in_array($slug, $known, true) ? $slug : '';
}

function amicus_gitpress_asset($type, $name) {
    $relative = 'assets/' . $type . '/' . $name;
    $path = plugin_dir_path(__FILE__) . $relative;
    if (!file_exists($path)) { return null; }
    return array(plugin_dir_url(__FILE__) . $relative, (string) filemtime($path));
}

add_action('wp_enqueue_scripts', function () {
    $slug = amicus_gitpress_route_slug();
    if (!$slug) { return; }
    $source = amicus_gitpress_asset('css', $slug . '.css');
    if ($source) {
        wp_enqueue_style('amicus-source', $source[0], array(), $source[1]);
    }
    $site = amicus_gitpress_asset('css', 'site.css');
    if ($site) {
        wp_enqueue_style('amicus-site', $site[0], $source ? array('amicus-source') : array(), $site[1]);
    }
    $script = amicus_gitpress_asset('js', 'site.js');
    if ($script) {
        wp_enqueue_script('amicus-site', $script[0], array(), $script[1], true);
    }
    wp_enqueue_style('amicus-font-open-sans', 'https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800&subset=latin,latin-ext&display=swap', array(), null);
    wp_enqueue_style('amicus-font-builder', 'https://fonts.googleapis.com/css?family=Plus+Jakarta+Sans:200,300,regular,500,600,700,800,200italic,300italic,italic,500italic,600italic,700italic,800italic|Poppins:100,100italic,200,200italic,regular,italic,500,500italic,600,600italic,700,700italic,800,800italic,900,900italic|Roboto:100,100italic,300,300italic,regular,italic,500italic,700,700italic,900,900italic|Inter:100,200,300,regular,500,600,700,800,900|Roboto+Condensed:300,300italic,regular,italic,700,700italic|Manrope:200,300,regular,500,600,700,800|Oswald:200,300,regular,500,600,700|Lora:regular,500,600,700,italic,500italic,600italic,700italic|Urbanist:100,200,300,regular,500,600,700,800,900,100italic,200italic,300italic,italic,500italic,600italic,700italic,800italic,900italic|DM+Sans:regular,italic,500,500italic,700,700italic&subset=latin,latin-ext&display=swap', array(), null);
});

add_filter('dgs_allowed_inner_shortcodes', function ($shortcodes) {
    $shortcodes[] = 'amicus_jotform';
    $shortcodes[] = 'amicus_comments';
    $shortcodes[] = 'amicus_youtube';
    $shortcodes[] = 'amicus_form_status';
    $shortcodes[] = 'amicus_project_archive';
    $shortcodes[] = 'amicus_author_archive';
    return array_values(array_unique($shortcodes));
});

add_shortcode('amicus_form_status', function ($atts) {
    $atts = shortcode_atts(array('id' => 0), $atts, 'amicus_form_status');
    $id = absint($atts['id']);
    $form = $id && class_exists('GitPress\\Forms\\Repository')
        ? GitPress\Forms\Repository::form($id)
        : null;
    if ($form && $form['status'] === 'published') { return ''; }
    return '<p class="amicus-form-unavailable" role="status">The contact form is temporarily unavailable. Please email <a href="mailto:info@amicusfoundation.com">info@amicusfoundation.com</a>.</p>';
});

add_shortcode('amicus_jotform', function ($atts) {
    $atts = shortcode_atts(array('id' => ''), $atts, 'amicus_jotform');
    $id = (string) $atts['id'];
    if (!in_array($id, array('230195983314055', '250696793084167'), true)) {
        return '<p class="amicus-form-unavailable">This application is unavailable. Please contact info@amicusfoundation.com.</p>';
    }
    return '<script src="https://form.jotform.com/jsform/' . esc_attr($id) . '"></script>';
});

add_shortcode('amicus_youtube', function ($atts) {
    $atts = shortcode_atts(array('id' => ''), $atts, 'amicus_youtube');
    $id = (string) $atts['id'];
    if (!in_array($id, array('p-blKuphgOM', 'YHHtyO33FMA'), true)) { return ''; }
    return '<iframe title="Amicus Foundation video" src="https://www.youtube.com/embed/' . esc_attr($id) . '" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>';
});

add_shortcode('amicus_comments', function () {
    if (!is_singular('project')) { return ''; }
    ob_start();
    comments_template();
    return ob_get_clean();
});

add_shortcode('amicus_project_archive', function () {
    $projects = new WP_Query(array('post_type' => 'project', 'post_status' => 'publish', 'posts_per_page' => 20));
    ob_start();
    if ($projects->have_posts()) {
        echo '<div class="amicus-archive-list">';
        while ($projects->have_posts()) {
            $projects->the_post();
            echo '<article class="amicus-project-card"><a href="' . esc_url(get_permalink()) . '">';
            if (has_post_thumbnail()) { the_post_thumbnail('medium', array('loading' => 'lazy')); }
            echo '<h2>' . esc_html(get_the_title()) . '</h2></a></article>';
        }
        echo '</div>';
    } else {
        echo '<p>No Results Found</p>';
    }
    wp_reset_postdata();
    get_search_form();
    return ob_get_clean();
});

add_shortcode('amicus_author_archive', function () {
    ob_start();
    if (have_posts()) {
        echo '<div class="amicus-archive-list">';
        while (have_posts()) {
            the_post();
            echo '<article class="amicus-project-card"><a href="' . esc_url(get_permalink()) . '"><h2>' . esc_html(get_the_title()) . '</h2></a></article>';
        }
        echo '</div>';
        rewind_posts();
    } else {
        echo '<h1>No Results Found</h1>';
    }
    get_search_form();
    return ob_get_clean();
});

add_filter('template_include', function ($template) {
    $slug = amicus_gitpress_route_slug();
    if ($slug === 'project-archive' || $slug === 'author-amicus') {
        return plugin_dir_path(__FILE__) . 'archive-template.php';
    }
    return $template;
}, 99);

add_filter('body_class', function ($classes) {
    $slug = amicus_gitpress_route_slug();
    if ($slug) {
        $classes[] = 'et_pb_pagebuilder_layout';
        $classes[] = 'et_pb_button_helper_class';
        $classes[] = 'et-db';
    }
    if ($slug === 'project-archive' || $slug === 'author-amicus') {
        $classes[] = 'dgs-gitpress-managed';
    }
    return $classes;
});

add_action('template_redirect', function () {
    $path = parse_url($_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH);
    if ($path === '/layout_tag/light/' || $path === '/layout_tag/light') {
        wp_safe_redirect(home_url('/'), 301);
        exit;
    }
}, 1);
