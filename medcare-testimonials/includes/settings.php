<?php
/**
 * Testimonials > Settings: how many testimonials to show and where "Read More" goes.
 *
 * @package MedCare_Testimonials
 */

defined( 'ABSPATH' ) || exit;

add_action( 'admin_menu', 'mc_tst_settings_menu' );
add_action( 'admin_init', 'mc_tst_settings_register' );
add_action( 'update_option_mc_tst_settings', 'mc_tst_flush' );

/**
 * Read one setting.
 *
 * @param string $key count|more_url.
 * @return int|string
 */
function mc_tst_setting( $key ) {
	$saved    = get_option( 'mc_tst_settings', array() );
	$settings = wp_parse_args(
		is_array( $saved ) ? $saved : array(),
		array(
			'count'    => 5,
			'more_url' => '',
		)
	);
	return 'count' === $key ? max( 1, (int) $settings['count'] ) : (string) $settings[ $key ];
}

/**
 * "Read More" URL: the saved setting, else the page with slug "testimonial".
 *
 * @return string
 */
function mc_tst_more_url() {
	$url = mc_tst_setting( 'more_url' );
	if ( '' === $url ) {
		$page = get_page_by_path( 'testimonial' );
		$url  = $page ? get_permalink( $page ) : home_url( '/testimonial/' );
	}
	return (string) apply_filters( 'mc_testimonials_more_url', $url );
}

/**
 * Submenu under Testimonials.
 */
function mc_tst_settings_menu() {
	add_submenu_page(
		'edit.php?post_type=mc_testimonial',
		__( 'Testimonials Settings', 'medcare-testimonials' ),
		__( 'Settings', 'medcare-testimonials' ),
		'manage_options',
		'mc-tst-settings',
		'mc_tst_settings_page'
	);
}

/**
 * Register the option and its fields.
 */
function mc_tst_settings_register() {
	register_setting(
		'mc_tst_settings',
		'mc_tst_settings',
		array(
			'type'              => 'array',
			'sanitize_callback' => 'mc_tst_settings_sanitize',
			'default'           => array(
				'count'    => 5,
				'more_url' => '',
			),
		)
	);
	add_settings_section( 'mc_tst_main', '', '__return_false', 'mc-tst-settings' );
	add_settings_field( 'mc_tst_count', __( 'Testimonials to show', 'medcare-testimonials' ), 'mc_tst_field_count', 'mc-tst-settings', 'mc_tst_main', array( 'label_for' => 'mc_tst_count' ) );
	add_settings_field( 'mc_tst_more_url', __( '"Read More" link', 'medcare-testimonials' ), 'mc_tst_field_more_url', 'mc-tst-settings', 'mc_tst_main', array( 'label_for' => 'mc_tst_more_url' ) );
}

/**
 * Sanitize.
 *
 * @param mixed $input Raw input.
 * @return array
 */
function mc_tst_settings_sanitize( $input ) {
	$input = is_array( $input ) ? $input : array();
	return array(
		'count'    => min( 50, max( 1, absint( $input['count'] ?? 5 ) ) ),
		'more_url' => esc_url_raw( trim( (string) ( $input['more_url'] ?? '' ) ) ),
	);
}

/**
 * Count field.
 */
function mc_tst_field_count() {
	printf(
		'<input type="number" id="mc_tst_count" name="mc_tst_settings[count]" value="%1$d" min="1" max="50" class="small-text"> <p class="description">%2$s</p>',
		(int) mc_tst_setting( 'count' ),
		esc_html__( 'The first N published testimonials, in Order (Page Attributes) order. Default 5.', 'medcare-testimonials' )
	);
}

/**
 * Read More URL field.
 */
function mc_tst_field_more_url() {
	printf(
		'<input type="url" id="mc_tst_more_url" name="mc_tst_settings[more_url]" value="%1$s" class="regular-text" placeholder="%2$s"> <p class="description">%3$s</p>',
		esc_attr( mc_tst_setting( 'more_url' ) ),
		esc_attr( home_url( '/testimonial/' ) ),
		esc_html__( 'Leave empty to use the Testimonials page (slug "testimonial").', 'medcare-testimonials' )
	);
}

/**
 * Page output.
 */
function mc_tst_settings_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	?>
	<div class="wrap">
		<h1><?php esc_html_e( 'Testimonials Settings', 'medcare-testimonials' ); ?></h1>
		<form action="options.php" method="post">
			<?php
			settings_fields( 'mc_tst_settings' );
			do_settings_sections( 'mc-tst-settings' );
			submit_button();
			?>
		</form>
	</div>
	<?php
}
