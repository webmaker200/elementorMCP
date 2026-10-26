<?php
/**
 * Plugin Name:       MedCare Testimonials
 * Description:       Lightweight, CPT-driven testimonials section. Use the [mc_testimonials] shortcode.
 * Version:           1.0.0
 * Requires at least: 6.2
 * Requires PHP:      7.4
 * Requires Plugins:  advanced-custom-fields
 * Author:            MedCare MSO
 * License:           GPL-2.0-or-later
 * Text Domain:       medcare-testimonials
 *
 * @package MedCare_Testimonials
 */

defined( 'ABSPATH' ) || exit;

define( 'MC_TST_VERSION', '1.0.0' );
define( 'MC_TST_FILE', __FILE__ );
define( 'MC_TST_DIR', plugin_dir_path( __FILE__ ) );
define( 'MC_TST_URL', plugin_dir_url( __FILE__ ) );

require_once MC_TST_DIR . 'includes/post-type.php';
require_once MC_TST_DIR . 'includes/fields.php';
require_once MC_TST_DIR . 'includes/render.php';
require_once MC_TST_DIR . 'includes/cache.php';
require_once MC_TST_DIR . 'includes/admin.php';
require_once MC_TST_DIR . 'includes/settings.php';
require_once MC_TST_DIR . 'includes/seed.php';

register_activation_hook( __FILE__, 'mc_tst_activate' );

/**
 * Activation: register the post type, then import the initial testimonials once.
 */
function mc_tst_activate() {
	mc_tst_register_post_type();
	mc_tst_seed();
}
