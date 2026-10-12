<?php
if (!defined('ABSPATH')) { exit; }
$slug = amicus_gitpress_route_slug();
$body = $slug === 'project-archive' ? 'project-archive.html' : 'author-amicus.html';
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <?php wp_head(); ?>
</head>
<body <?php body_class(array('dgs-gitpress-managed')); ?>>
<?php wp_body_open(); ?>
<div class="dgs-managed-page">
  <header class="dgs-managed-header"><?php echo do_shortcode((string) get_option('dgs_managed_header_shortcode', '')); ?></header>
  <main class="dgs-managed-main" id="main"><?php echo do_shortcode(amicus_gitpress_short_code($body)); ?></main>
  <footer class="dgs-managed-footer"><?php echo do_shortcode((string) get_option('dgs_managed_footer_shortcode', '')); ?></footer>
</div>
<?php wp_footer(); ?>
</body>
</html>
