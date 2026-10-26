=== MedCare Testimonials ===
Requires at least: 6.2
Requires PHP: 7.4
Requires Plugins: advanced-custom-fields
Stable tag: 1.0.0
License: GPLv2 or later

Lightweight replacement for the homepage testimonials section (Elementor template 388878).
Content lives in the "Testimonials" post type; the section is rendered by the [mc_testimonials]
shortcode with inline CSS (no extra stylesheet request) and one small footer script that reuses
Elementor's bundled Swiper 8 (handle "swiper").

== Usage ==

Place a Shortcode widget containing [mc_testimonials] where the section should appear.
Shows the first 5 testimonials by default. Options: [mc_testimonials limit="8"] and
[mc_testimonials more_url="https://example.com/testimonial/"] (default: the page with slug "testimonial").

== Editing testimonials ==

* Add: Testimonials > Add New. Title = person's name. Fill Quote and Photo (required), plus Headline,
  Role, Organization, optional company logo and the button ("Read More" links to the Testimonials page, or a "Watch Story" video).
* Edit: change any field and Update. Both carousels update together.
* Reorder: set "Order" in the Page Attributes box (lower = earlier). The list screen shows the order.
* Hide: switch to Draft or move to Trash.
* Photo alt text comes from the Media Library; if empty, the person's name is used.

After editing, WP Rocket's cache is cleared automatically when WP Rocket is active. If another page
cache or CDN is in front of the site, purge it after editing testimonials (or hook
`mc_testimonials_flush_cache`).

== Rollback ==

1. Remove the [mc_testimonials] Shortcode widget from the page (the old section is untouched).
2. Deactivate the plugin. Testimonial posts and their fields stay in the database; delete them from
   Testimonials if no longer needed.

== Filters ==

* mc_testimonials_heading - section heading text.
* mc_testimonials_bg_url  - decorative background circle URL.
* mc_testimonials_flush_cache (action) - runs after a testimonial is saved, trashed, restored or deleted.
