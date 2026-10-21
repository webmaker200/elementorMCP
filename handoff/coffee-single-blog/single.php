<?php
/**
 * Single blog post – Coffee Fix DXB design.
 *
 * Needs inc/coffee-single-blog.php (loaded from functions.php) and
 * assets/css/coffee-single-blog.css.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

while ( have_posts() ) :
	the_post();

	$cfb      = cfb_settings();
	$post_id  = get_the_ID();
	$category = cfb_primary_category( $post_id );
	$minutes  = cfb_reading_time( $post_id );
	$blog_url = cfb_blog_url();
	$author   = get_the_author_meta( 'display_name' );
	$author   = $author ? $author : get_bloginfo( 'name' );
	$bio      = get_the_author_meta( 'description' );
	$tags     = get_the_tags();
	$share    = rawurlencode( get_permalink() );
	$content  = cfb_prepare_content( apply_filters( 'the_content', get_the_content() ) );
	$related  = cfb_related_posts( $post_id, (int) $cfb['related_count'] );
	$card_icons = array( 'tint', 'search', 'wrench' );
	?>

<main id="content" <?php post_class( 'cfb-single' ); ?>>

	<!-- Hero -->
	<section class="cfb-section cfb-hero">
		<div class="cfb-container">
			<div class="cfb-hero__inner">

				<nav class="cfb-crumbs" aria-label="Breadcrumb">
					<a class="cfb-crumbs__link" href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a>
					<span class="cfb-crumbs__sep" aria-hidden="true">/</span>
					<a class="cfb-crumbs__link" href="<?php echo esc_url( $blog_url ); ?>">Blog</a>
					<?php if ( $category ) : ?>
						<span class="cfb-crumbs__sep" aria-hidden="true">/</span>
						<span class="cfb-crumbs__current" aria-current="page"><?php echo esc_html( $category->name ); ?></span>
					<?php endif; ?>
				</nav>

				<div class="cfb-meta">
					<?php if ( $category ) : ?>
						<span class="cfb-meta__cat"><?php echo esc_html( $category->name ); ?></span>
					<?php endif; ?>
					<span class="cfb-meta__item"><?php echo esc_html( $minutes ); ?> min read</span>
					<span class="cfb-meta__item" aria-hidden="true">&middot;</span>
					<span class="cfb-meta__item">Published <time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>"><?php echo esc_html( get_the_date( 'j F Y' ) ); ?></time></span>
				</div>

				<h1 class="cfb-title"><?php the_title(); ?></h1>

				<?php $lead = cfb_lead( $post_id ); ?>
				<?php if ( $lead ) : ?>
					<p class="cfb-lead"><?php echo wp_kses_post( $lead ); ?></p>
				<?php endif; ?>

				<div class="cfb-author">
					<div class="cfb-author__icon"><?php echo cfb_icon( 'wrench' ); // phpcs:ignore WordPress.Security.EscapeOutput ?></div>
					<div class="cfb-author__text">
						<p class="cfb-author__name"><?php echo esc_html( $author ); ?></p>
						<p class="cfb-author__role"><?php echo esc_html( $bio ? wp_strip_all_tags( $bio ) : $cfb['author_tagline'] ); ?></p>
					</div>
				</div>

			</div>
		</div>
	</section>

	<!-- Banner + article -->
	<section class="cfb-section cfb-body">
		<div class="cfb-container">

			<div class="cfb-banner<?php echo has_post_thumbnail() ? ' has-image' : ''; ?>">
				<?php
				if ( has_post_thumbnail() ) {
					the_post_thumbnail(
						'full',
						array(
							'class'         => 'cfb-banner__img',
							'loading'       => 'eager',
							'fetchpriority' => 'high',
							'sizes'         => '(max-width: 1304px) 100vw, 1240px',
						)
					);
				} else {
					echo '<div class="cfb-banner__icon">' . cfb_icon( 'thermometer' ) . '</div>'; // phpcs:ignore WordPress.Security.EscapeOutput
				}
				?>
			</div>

			<div class="cfb-layout">

				<article class="cfb-article">
					<div class="cfb-content">
						<?php echo $content['html']; // phpcs:ignore WordPress.Security.EscapeOutput -- filtered by the_content. ?>
					</div>

					<?php
					wp_link_pages(
						array(
							'before' => '<nav class="cfb-pages">',
							'after'  => '</nav>',
						)
					);
					?>

					<div class="cfb-article__foot">
						<?php if ( $tags ) : ?>
							<div class="cfb-chips">
								<p class="cfb-chips__label">Tags</p>
								<?php foreach ( $tags as $tag ) : ?>
									<a class="cfb-chip" href="<?php echo esc_url( get_tag_link( $tag ) ); ?>"><?php echo esc_html( $tag->name ); ?></a>
								<?php endforeach; ?>
							</div>
						<?php endif; ?>

						<div class="cfb-chips">
							<p class="cfb-chips__label">Share</p>
							<a class="cfb-chip" href="<?php echo esc_url( 'https://wa.me/?text=' . rawurlencode( get_the_title() . ' ' ) . $share ); ?>" target="_blank" rel="noopener">WhatsApp</a>
							<a class="cfb-chip" href="<?php echo esc_url( 'https://www.facebook.com/sharer/sharer.php?u=' . $share ); ?>" target="_blank" rel="noopener">Facebook</a>
							<a class="cfb-chip" href="<?php echo esc_url( 'https://www.linkedin.com/sharing/share-offsite/?url=' . $share ); ?>" target="_blank" rel="noopener">LinkedIn</a>
						</div>
					</div>
				</article>

				<aside class="cfb-aside">
					<?php if ( $content['toc'] ) : ?>
						<nav class="cfb-toc" aria-label="In this article">
							<p class="cfb-toc__title">In this article</p>
							<?php foreach ( $content['toc'] as $item ) : ?>
								<a class="cfb-toc__link" href="#<?php echo esc_attr( $item['id'] ); ?>"><?php echo esc_html( $item['label'] ); ?></a>
							<?php endforeach; ?>
						</nav>
					<?php endif; ?>

					<div class="cfb-help">
						<p class="cfb-eyebrow cfb-help__eyebrow"><?php echo esc_html( $cfb['side_eyebrow'] ); ?></p>
						<h3 class="cfb-help__title"><?php echo esc_html( $cfb['side_title'] ); ?></h3>
						<p class="cfb-help__text"><?php echo esc_html( $cfb['side_text'] ); ?></p>
						<a class="cfb-btn cfb-btn--light" href="<?php echo esc_url( $cfb['whatsapp_url'] ); ?>" target="_blank" rel="noopener"><?php echo esc_html( $cfb['side_whatsapp'] ); ?></a>
						<a class="cfb-btn cfb-btn--ghost-light" href="<?php echo esc_url( 'tel:' . $cfb['phone'] ); ?>">Call <?php echo esc_html( $cfb['phone_label'] ); ?></a>
					</div>
				</aside>

			</div>
		</div>
	</section>

	<?php if ( $related ) : ?>
		<!-- Related articles -->
		<section class="cfb-section cfb-related">
			<div class="cfb-container">
				<div class="cfb-related__head">
					<div class="cfb-related__intro">
						<p class="cfb-eyebrow"><?php echo esc_html( $cfb['related_eyebrow'] ); ?></p>
						<h2 class="cfb-h2"><?php echo esc_html( $cfb['related_title'] ); ?></h2>
					</div>
					<a class="cfb-textlink" href="<?php echo esc_url( $blog_url ); ?>"><?php echo wp_kses_post( $cfb['related_all'] ); ?></a>
				</div>

				<div class="cfb-grid">
					<?php foreach ( $related as $i => $rel ) : ?>
						<?php
						$rel_cat  = cfb_primary_category( $rel->ID );
						$rel_link = get_permalink( $rel );
						?>
						<article class="cfb-card">
							<a class="cfb-card__media" href="<?php echo esc_url( $rel_link ); ?>" tabindex="-1" aria-hidden="true">
								<?php
								if ( has_post_thumbnail( $rel ) ) {
									echo get_the_post_thumbnail(
										$rel,
										'medium_large',
										array(
											'class'   => 'cfb-card__img',
											'loading' => 'lazy',
											'sizes'   => '(max-width: 767px) 100vw, (max-width: 1024px) 50vw, 400px',
										)
									);
								} else {
									echo '<span class="cfb-card__icon">' . cfb_icon( $card_icons[ $i % 3 ] ) . '</span>'; // phpcs:ignore WordPress.Security.EscapeOutput
								}
								?>
							</a>
							<div class="cfb-card__body">
								<div class="cfb-card__meta">
									<?php if ( $rel_cat ) : ?>
										<span class="cfb-card__cat"><?php echo esc_html( $rel_cat->name ); ?></span>
									<?php endif; ?>
									<span class="cfb-card__time"><?php echo esc_html( cfb_reading_time( $rel->ID ) ); ?> min read</span>
								</div>
								<h3 class="cfb-card__title"><a href="<?php echo esc_url( $rel_link ); ?>"><?php echo esc_html( get_the_title( $rel ) ); ?></a></h3>
								<p class="cfb-card__text"><?php echo esc_html( wp_strip_all_tags( has_excerpt( $rel ) ? get_the_excerpt( $rel ) : wp_trim_words( strip_shortcodes( $rel->post_content ), 18, '&hellip;' ) ) ); ?></p>
								<a class="cfb-textlink" href="<?php echo esc_url( $rel_link ); ?>">Read article &rarr;</a>
							</div>
						</article>
					<?php endforeach; ?>
				</div>
			</div>
		</section>
	<?php endif; ?>

	<!-- Contact band -->
	<section class="cfb-section cfb-contact">
		<div class="cfb-container">
			<div class="cfb-contact__box">
				<div class="cfb-contact__text">
					<p class="cfb-eyebrow cfb-contact__eyebrow"><?php echo esc_html( $cfb['contact_eyebrow'] ); ?></p>
					<h2 class="cfb-h2"><?php echo esc_html( $cfb['contact_title'] ); ?></h2>
					<p class="cfb-contact__lead"><?php echo esc_html( $cfb['contact_text'] ); ?></p>
				</div>
				<div class="cfb-contact__actions">
					<a class="cfb-btn cfb-btn--primary" href="<?php echo esc_url( $cfb['whatsapp_url'] ); ?>" target="_blank" rel="noopener"><?php echo esc_html( $cfb['contact_whatsapp'] ); ?></a>
					<a class="cfb-btn cfb-btn--outline" href="<?php echo esc_url( 'tel:' . $cfb['phone'] ); ?>">Call <?php echo esc_html( $cfb['phone_label'] ); ?></a>
				</div>
			</div>
		</div>
	</section>

</main>

	<?php
endwhile;

get_footer();
