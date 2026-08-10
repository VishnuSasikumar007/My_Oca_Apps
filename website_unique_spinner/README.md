# Website Unique Loading Spinner (Odoo 19)

A lightweight Odoo 19 module that adds a distinctive animated triple-ring **orbit spinner** to Odoo website pages.

## Features

* Full-screen preloader shown while the page and its assets load.
* Smooth fade-out once the page is ready.
* Optional transition spinner for internal website navigation.
* Shows the transition spinner when visitors click internal links or submit supported forms.
* Automatic **6-second fallback timeout** to prevent the spinner from getting stuck.
* Respects `prefers-reduced-motion` for accessibility.
* Pure CSS animation with no GIF or PNG images.
* No external JavaScript libraries.
* Lightweight vanilla JavaScript.
* Fully customizable through CSS variables.
* Works only on Odoo website/frontend pages.
* Does not affect the Odoo backend.

## Installation

1. Copy the `website_unique_spinner` folder into your Odoo 19 custom addons directory.

2. Restart the Odoo server.

3. Go to:

   **Apps → Update Apps List**

4. Remove the default **Apps** filter if required.

5. Search for:

   **Website Unique Loading Spinner**

6. Click **Install**.

7. Visit any Odoo website page. The spinner will appear automatically while the page is loading.

## Module Structure

```text
website_unique_spinner/
├── __init__.py
├── __manifest__.py
├── README.md
│
├── static/
│   └── src/
│       └── css/
│           └── spinner.css
│       └── js/
│           └── spinner.js
│
└── views/
    └── templates.xml
```

## Customize Colors and Size

All spinner visuals are controlled through CSS variables defined in:

```text
static/src/css/spinner.css
```

Default variables:

```css
:root {
    --uws-bg: #ffffff;
    --uws-color-1: #7c3aed;
    --uws-color-2: #06b6d4;
    --uws-color-3: #f43f5e;
    --uws-core: #111827;
    --uws-size: 88px;
}
```

### Available Variables

| Variable        | Description                    |
| --------------- | ------------------------------ |
| `--uws-bg`      | Full-screen loading background |
| `--uws-color-1` | Outer ring color               |
| `--uws-color-2` | Middle ring color              |
| `--uws-color-3` | Inner ring color               |
| `--uws-core`    | Center dot color               |
| `--uws-size`    | Overall spinner size           |

You can override these variables from another frontend asset to match your website's branding without modifying the original module.

## Disable the Transition Spinner for a Specific Form

Add the `uws-no-spinner` class to any form that should not trigger the transition spinner.

```xml
<form class="uws-no-spinner" ...>
```

For example:

```xml
<form class="uws-no-spinner"
      action="/shop"
      method="get">

    <!-- Form content -->

</form>
```

The initial page-loading spinner will still work.

## Accessibility

The module respects the user's `prefers-reduced-motion` system preference.

When reduced motion is enabled, unnecessary animations are reduced or disabled to provide a more accessible browsing experience.

## Fallback Protection

The JavaScript includes a **6-second fallback timeout**.

If a page resource or third-party resource prevents the normal loading event from completing, the spinner is automatically hidden after the timeout.

This prevents the loading screen from remaining visible indefinitely.

## Performance

The module is designed to be lightweight:

* Pure CSS animations.
* Vanilla JavaScript.
* No third-party JavaScript dependencies.
* No GIF or PNG assets.
* No external API calls.
* No backend modifications.
* Frontend assets only.

## Frontend Only

The module uses Odoo's:

```text
web.assets_frontend
```

It does not affect the Odoo backend interface.

## Technical Information

**Odoo Version:** Odoo 19.0

**Dependency:** `website`

**License:** LGPL-3

## Author

**Vishnu Sasikumar**

Odoo Software Engineer / Developer

## License

This module is licensed under **LGPL-3**.
