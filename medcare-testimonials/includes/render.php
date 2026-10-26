<?php
/**
 * [mc_testimonials] shortcode and front-end assets.
 *
 * @package MedCare_Testimonials
 */

defined( 'ABSPATH' ) || exit;

add_shortcode( 'mc_testimonials', 'mc_tst_shortcode' );
add_action( 'wp_enqueue_scripts', 'mc_tst_register_assets' );

/**
 * Register the script. It is only enqueued when the shortcode renders with 2+ items.
 * The handle "swiper" is registered by Elementor (lib/swiper/v8, Swiper 8.4.5).
 */
function mc_tst_register_assets() {
	$deps = wp_script_is( 'swiper', 'registered' ) ? array( 'swiper' ) : array();
	wp_register_script(
		'mc-testimonials',
		MC_TST_URL . 'assets/mc-testimonials.js',
		$deps,
		MC_TST_VERSION,
		array(
			'in_footer' => true,
			'strategy'  => 'defer',
		)
	);
}

/**
 * Query published testimonials. One query feeds both tracks so photos and quotes stay paired.
 *
 * @param int $limit Max items; 0 = all.
 * @return array[]
 */
function mc_tst_get_items( $limit = 0 ) {
	$query = new WP_Query(
		array(
			'post_type'              => 'mc_testimonial',
			'post_status'            => 'publish',
			'posts_per_page'         => $limit > 0 ? $limit : -1, // phpcs:ignore WordPress.WP.PostsPerPage.posts_per_page_posts_per_page -- small, admin-curated list.
			'orderby'                => array(
				'menu_order' => 'ASC',
				'date'       => 'DESC',
			),
			'no_found_rows'          => true,
			'ignore_sticky_posts'    => true,
			'update_post_term_cache' => false,
		)
	);

	$items = array();
	foreach ( $query->posts as $post ) {
		$quote = (string) get_post_meta( $post->ID, 'mc_quote', true );
		$image = (int) get_post_meta( $post->ID, 'mc_image', true );
		if ( '' === trim( $quote ) || ! $image ) {
			continue; // Both are required; skip incomplete drafts that were published early.
		}
		$items[] = array(
			'name'      => get_the_title( $post ),
			'headline'  => (string) get_post_meta( $post->ID, 'mc_headline', true ),
			'quote'     => $quote,
			'role'      => (string) get_post_meta( $post->ID, 'mc_role', true ),
			'org'       => (string) get_post_meta( $post->ID, 'mc_organization', true ),
			'image'     => $image,
			'logo'      => (int) get_post_meta( $post->ID, 'mc_logo', true ),
			'cta_type'  => (string) get_post_meta( $post->ID, 'mc_cta_type', true ),
			'cta_label' => (string) get_post_meta( $post->ID, 'mc_cta_label', true ),
			'video_url' => (string) get_post_meta( $post->ID, 'mc_video_url', true ),
		);
	}
	return $items;
}

/**
 * URL of the Testimonials page used by every "Read More" button.
 *
 * @return string
 */
function mc_tst_more_url() {
	$page = get_page_by_path( 'testimonial' );
	$url  = $page ? get_permalink( $page ) : home_url( '/testimonial/' );
	return (string) apply_filters( 'mc_testimonials_more_url', $url );
}

/**
 * Button for a testimonial: "Read More" (Testimonials page) or "Watch Story" (Elementor video lightbox).
 *
 * @param array  $item     Testimonial.
 * @param string $more_url Testimonials page URL.
 * @return array{0:string,1:string} [href, label] or empty strings.
 */
function mc_tst_cta( $item, $more_url ) {
	$type = '' !== $item['cta_type'] ? $item['cta_type'] : 'more';
	if ( 'video' === $type && '' !== $item['video_url'] ) {
		$url = $item['video_url'];
		if ( preg_match( '~(youtube\.com|youtu\.be)~i', $url ) ) {
			$video_type = 'youtube';
		} elseif ( preg_match( '~vimeo\.com~i', $url ) ) {
			$video_type = 'vimeo';
		} else {
			$video_type = 'hosted';
		}
		$settings = array(
			'type'      => 'video',
			'videoType' => $video_type,
			'url'       => $url,
		);
		$href     = '#elementor-action:action=lightbox&settings=' . base64_encode( wp_json_encode( $settings ) ); // phpcs:ignore WordPress.PHP.DiscouragedPHPFunctions.obfuscation_base64_encode
		return array( $href, '' !== $item['cta_label'] ? $item['cta_label'] : __( 'Watch Story', 'medcare-testimonials' ) );
	}
	if ( 'none' !== $type && '' !== $more_url ) {
		return array( $more_url, '' !== $item['cta_label'] ? $item['cta_label'] : __( 'Read More', 'medcare-testimonials' ) );
	}
	return array( '', '' );
}

/**
 * Inline CSS, printed once per page.
 *
 * @return string
 */
function mc_tst_css() {
	$css = file_get_contents( MC_TST_DIR . 'assets/mc-testimonials.css' ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents
	$css = preg_replace( '~/\*.*?\*/~s', '', (string) $css );
	$css = preg_replace( '~\s+~', ' ', $css );
	$css = str_replace( array( ' {', '{ ', ' }', '; ', ': ', ', ', ' > ', ';}' ), array( '{', '{', '}', ';', ':', ',', '>', '}' ), $css );
	return trim( $css );
}

/**
 * Shortcode callback.
 *
 * @param array|string $atts Attributes.
 * @return string
 */
function mc_tst_shortcode( $atts ) {
	static $instance  = 0;
	static $css_done  = false;

	$atts  = shortcode_atts(
		array(
			'limit'    => 5,
			'more_url' => '',
		),
		$atts,
		'mc_testimonials'
	);
	$items = mc_tst_get_items( absint( $atts['limit'] ) );
	$count = count( $items );
	if ( 0 === $count ) {
		return '';
	}

	++$instance;
	$uid     = 'mc-tst-' . $instance;
	$heading = apply_filters( 'mc_testimonials_heading', __( 'What Our Clients Say About Working With Us', 'medcare-testimonials' ) );
	$uploads = wp_get_upload_dir();
	$bg_url  = apply_filters( 'mc_testimonials_bg_url', $uploads['baseurl'] . '/2024/03/testimonial-bg-circle.svg' );
	$multi   = $count > 1;
	$more    = '' !== $atts['more_url'] ? $atts['more_url'] : mc_tst_more_url();

	if ( $multi ) {
		wp_enqueue_script( 'mc-testimonials' );
	}

	ob_start();

	if ( ! $css_done ) {
		$css_done = true;
		echo '<style id="mc-testimonials-css">' . mc_tst_css() . '</style>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- static CSS from the plugin.
	}
	?>
<section class="mc-tst<?php echo $multi ? '' : ' mc-tst--single'; ?>" id="<?php echo esc_attr( $uid ); ?>" aria-labelledby="<?php echo esc_attr( $uid ); ?>-title" style="--mc-tst-bg:url('<?php echo esc_url( $bg_url ); ?>')" data-count="<?php echo esc_attr( $count ); ?>">
	<h3 class="mc-tst__title" id="<?php echo esc_attr( $uid ); ?>-title"><?php echo esc_html( $heading ); ?></h3>
	<div class="mc-tst__body">
		<div class="mc-tst__media" dir="rtl" aria-hidden="true">
			<div class="mc-tst__track">
			<?php
			foreach ( $items as $i => $item ) :
				$alt = trim( (string) get_post_meta( $item['image'], '_wp_attachment_image_alt', true ) );
				?>
				<div class="mc-tst__slide mc-tst__photo<?php echo 0 === $i ? ' is-active' : ''; ?>" data-index="<?php echo esc_attr( $i ); ?>">
					<?php
					echo wp_get_attachment_image( // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes attributes.
						$item['image'],
						'full',
						false,
						array(
							'class'    => 'mc-tst__img',
							'alt'      => '' !== $alt ? $alt : $item['name'],
							'loading'  => 'lazy',
							'decoding' => 'async',
							'sizes'    => '(max-width: 767px) 197px, (max-width: 1024px) 156px, 292px',
						)
					);
					?>
				</div>
			<?php endforeach; ?>
			</div>
		</div>
		<div class="mc-tst__quotes">
			<div class="mc-tst__track">
			<?php
			foreach ( $items as $i => $item ) :
				list( $href, $label ) = mc_tst_cta( $item, $more );
				$meta                 = implode( ', ', array_filter( array( trim( $item['role'] ), trim( $item['org'] ) ), 'strlen' ) );
				?>
				<figure class="mc-tst__slide mc-tst__card" data-index="<?php echo esc_attr( $i ); ?>">
					<svg class="mc-tst__mark" viewBox="0 0 61 52" aria-hidden="true" focusable="false"><use href="#<?php echo esc_attr( $uid ); ?>-mark"/></svg>
					<?php if ( '' !== $item['headline'] ) : ?>
						<p class="mc-tst__headline"><?php echo esc_html( $item['headline'] ); ?></p>
					<?php endif; ?>
					<blockquote class="mc-tst__quote"><p><?php echo esc_html( $item['quote'] ); ?></p></blockquote>
					<figcaption class="mc-tst__cap">
						<span class="mc-tst__name"><?php echo esc_html( $item['name'] ); ?></span>
						<?php if ( '' !== $meta ) : ?>
							<span class="mc-tst__role"><?php echo esc_html( $meta ); ?></span>
						<?php endif; ?>
						<?php if ( '' !== $href ) : ?>
							<a class="mc-tst__cta" href="<?php echo 0 === strpos( $href, '#' ) ? esc_attr( $href ) : esc_url( $href ); ?>"><?php echo esc_html( $label ); ?><span class="mc-tst__sr"> <?php echo esc_html( sprintf( /* translators: %s: person's name */ __( 'from %s', 'medcare-testimonials' ), $item['name'] ) ); ?></span></a>
						<?php endif; ?>
						<?php
						if ( $item['logo'] ) {
							echo wp_get_attachment_image( // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- core escapes attributes.
								$item['logo'],
								'full',
								false,
								array(
									'class'    => 'mc-tst__logo',
									'loading'  => 'lazy',
									'decoding' => 'async',
								)
							);
						}
						?>
					</figcaption>
				</figure>
			<?php endforeach; ?>
			</div>
		</div>
		<?php if ( $multi ) : ?>
		<div class="mc-tst__nav">
			<div class="mc-tst__dots" role="group" aria-label="<?php esc_attr_e( 'Choose a testimonial', 'medcare-testimonials' ); ?>">
				<?php for ( $i = 0; $i < $count; $i++ ) : ?>
					<button type="button" class="mc-tst__dot" data-index="<?php echo esc_attr( $i ); ?>" aria-label="<?php echo esc_attr( sprintf( /* translators: 1: number, 2: total */ __( 'Show testimonial %1$d of %2$d', 'medcare-testimonials' ), $i + 1, $count ) ); ?>"<?php echo 0 === $i ? ' aria-current="true"' : ''; ?>></button>
				<?php endfor; ?>
			</div>
			<div class="mc-tst__arrows">
				<button type="button" class="mc-tst__arrow mc-tst__prev" aria-label="<?php esc_attr_e( 'Previous testimonial', 'medcare-testimonials' ); ?>"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M15 4 7 12l8 8"/></svg></button>
				<button type="button" class="mc-tst__arrow mc-tst__next" aria-label="<?php esc_attr_e( 'Next testimonial', 'medcare-testimonials' ); ?>"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="m9 4 8 8-8 8"/></svg></button>
			</div>
		</div>
		<?php endif; ?>
	</div>
	<svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute"><symbol id="<?php echo esc_attr( $uid ); ?>-mark" viewBox="0 0 61 52"><path d="M61 18.12c0 4.75-1.02 9.21-3.05 13.38-2.03 4.17-4.79 7.98-8.28 11.44-3.63 3.6-7.77 6.62-12.42 9.06l-3.92-4.96c3.63-2.88 6.75-6.04 9.37-9.5 2.61-3.3 3.92-6.69 3.92-10.14 0-2.01-.36-3.38-1.09-4.1-.73-.72-1.67-1.44-2.83-2.16-1.6-.86-3.05-2.09-4.36-3.67-1.31-1.58-1.96-3.74-1.96-6.47 0-3.02 1.02-5.61 3.05-7.77C41.47 1.08 44.08 0 47.28 0c3.77 0 7.04 1.51 9.8 4.53C59.69 7.55 61 12.08 61 18.12Zm-33.33 0c0 4.75-1.02 9.21-3.05 13.38-2.03 4.17-4.79 7.98-8.28 11.44-3.63 3.6-7.77 6.62-12.42 9.06L0 47.04c3.63-2.88 6.75-6.04 9.37-9.5 2.61-3.3 3.92-6.69 3.92-10.14 0-2.01-.36-3.38-1.09-4.1-.73-.72-1.67-1.44-2.83-2.16-1.6-.86-3.05-2.09-4.36-3.67C3.7 15.89 3.05 13.74 3.05 11c0-3.02 1.02-5.61 3.05-7.77C8.13 1.08 10.75 0 13.94 0c3.78 0 7.05 1.51 9.81 4.53 2.61 3.02 3.92 7.55 3.92 13.59Z"/></symbol></svg>
</section>
	<?php
	return (string) ob_get_clean();
}
