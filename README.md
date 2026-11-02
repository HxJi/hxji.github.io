# hxji.github.io

Source for [Houxiang Ji's academic homepage](https://hxji.github.io), built with Jekyll and
adapted from the [academic-homepage](https://github.com/luost26/academic-homepage) template.

## Structure

- `_data/profile.yml` – name, positions, bio, education, experience, links.
- `_data/navigation.yml` – navbar entries.
- `_data/authors.yml` – author display names and bolding for publication lists.
- `_publications/<year>/` – one Markdown file per paper (front matter only).
- `_news/` – one Markdown file per news item.
- `research.html` – research overview page (hand-written HTML).
- `_layouts/`, `_includes/` – page templates and widgets.
- `assets/` – CSS, JS, images and PDFs.

## Adding content

**Publication:** create `_publications/<year>/<year>-<slug>.md` with `title`, `date`,
`selected`, `pub`, `pub_date`, `authors`, optional `links` and `pub_last`, and the four
`artifact_*` / `results_reproduced` flags set explicitly (omitting a flag shows its badge).

**News:** create `_news/<slug>.md` with `title` (HTML allowed), `date`, `show_homepage`
and optional `highlight: true`.

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

## Deployment

GitHub Pages builds the `master` branch directly; pushing to `master` publishes the site.
