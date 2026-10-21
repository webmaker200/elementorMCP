# Coffee Fix DXB – dynamic single blog template

A PHP version of https://medcaredemo.online/practice/coffee-single-blog/ that fills itself in from every published post.

## Files

| File | Put it in your theme (child theme recommended) |
|---|---|
| `single.php` | `your-theme/single.php` |
| `inc/coffee-single-blog.php` | `your-theme/inc/coffee-single-blog.php` |
| `assets/css/coffee-single-blog.css` | `your-theme/assets/css/coffee-single-blog.css` |

Add this line to the theme's `functions.php`:

```php
require_once get_stylesheet_directory() . '/inc/coffee-single-blog.php';
```

The CSS and the Plus Jakarta Sans font load only on single posts.

## Where each part comes from

| On the page | Comes from |
|---|---|
| Breadcrumb | Home → Blog page (Settings → Reading → Posts page) → primary category |
| Category pill | Primary category (Yoast / Rank Math primary, otherwise the first category) |
| "6 min read" | Word count ÷ 200. To set it yourself, add a custom field `cfb_reading_time` (e.g. `6`) |
| Published date | Post date |
| H1 | Post title |
| Lead paragraph | The post's **Excerpt**. If it's empty, the first ~32 words of the post are used |
| Author row | Author display name + author bio (Users → Profile → Biographical Info). With no bio, the tagline from settings is shown |
| Banner | **Featured image**, cropped to the same 21:8 box (16:10 on mobile). With no featured image, the original thermometer placeholder is shown |
| Article body | Post content |
| "In this article" | Built from every **H2** in the post; each H2 gets an anchor id automatically. A leading "1. " is removed from the link text |
| Tags | Post tags, linked to their tag archives. The row is hidden when there are no tags |
| Share | WhatsApp / Facebook / LinkedIn links for the current post |
| Related articles | 3 posts from the same category, topped up with the latest posts. Each card uses the post's featured image, category, reading time, title and excerpt |
| Sidebar card, contact band, phone, WhatsApp | Fixed brand text in `cfb_settings()` in `inc/coffee-single-blog.php`. Edit it there once |

## How to write a post so it matches the design

Use the normal block editor:

- **Paragraph**: body text.
- **Heading (H2)**: section titles. Each one shows up in "In this article".
- **List (bulleted)**: shows as the green check list.
- **List (numbered)**: shows as the numbered steps. Start each item with **bold text** for the step title, then a line break (Shift+Enter) and the description.
- **Quote**: shows as the dark "Technician tip" box. Put the label (e.g. `Technician tip`) in the quote's citation field; it appears above the text.
- **Image**: full width with rounded corners.

## Layout notes

- The page width matches the live page: full-width coloured sections, with content in a 1240px centred container (32px side padding, 24px on tablet, 16px on mobile).
- The article and sidebar are sized with `width`, not `flex-basis`. The article is 68% of the row minus the gap, capped at 760px; the sidebar is 32%. At 1440px wide that gives 760px + 396.8px, the same as the live page.
- Breakpoints are the same as Elementor's: laptop ≤1366px, tablet ≤1024px (the sidebar moves under the article and "In this article" is hidden), mobile ≤767px.
- All class names start with `cfb-`, so they won't clash with Elementor or theme styles.
