# Hamburger Menu Implementation Guide

## What Was Added

Your portfolio now has a responsive hamburger menu that automatically appears on screens under 768px wide (mobile devices and tablets).

## Features

### 1. **Responsive Behavior**
- **Desktop (≥768px)**: Full horizontal navigation menu visible
- **Mobile (<768px)**: Navigation collapses into hamburger icon

### 2. **Smooth Animations**
- Hamburger icon transforms into an "X" when clicked
- Menu slides down smoothly (0.3s transition)
- Clean, professional appearance

### 3. **User Experience**
- Click hamburger to open/close menu
- Menu automatically closes when you click a navigation link
- Touch-friendly with larger tap targets on mobile

### 4. **Accessibility**
- Proper `aria-label` and `aria-expanded` attributes
- Keyboard accessible
- Screen reader friendly

## Files Modified

### CSS (`css/styles.css`)
Added three new sections:
1. **Hamburger button styles** - Three-bar icon with animation
2. **Hamburger active state** - Transforms bars into an X
3. **Mobile navigation styles** - Slide-down menu behavior

### HTML (All pages)
Updated navigation structure on:
- `index.html`
- `lab02.html`
- `lab03.html`
- `lab04.html`

Each page now has:
```html
<nav>
    <button class="hamburger" aria-label="Toggle navigation">
        <span></span>
        <span></span>
        <span></span>
    </button>
    
    <ul id="nav-menu">
        <!-- navigation links -->
    </ul>
</nav>
```

### JavaScript (Added to each page)
Vanilla JavaScript that:
- Toggles the `active` class on hamburger and menu
- Updates accessibility attributes
- Closes menu when links are clicked

## How It Works

### Desktop View
- Hamburger button is hidden (`display: none`)
- Navigation menu shows horizontally as normal
- No JavaScript interaction needed

### Mobile View (< 768px)
1. Navigation menu is hidden by default (`max-height: 0`)
2. Hamburger button is visible
3. When clicked:
   - Adds `active` class to both button and menu
   - Menu slides down (`max-height: 500px`)
   - Icon animates to X shape
4. Click again or click a link to close

## Customization Options

### Change Breakpoint
In `styles.css`, find:
```css
@media (max-width: 768px) {
```
Change `768px` to your preferred breakpoint.

### Change Colors
The hamburger icon uses:
```css
background-color: white;
```
And the menu background is:
```css
background-color: #3d1461;
```

### Change Animation Speed
Find this in the CSS:
```css
transition: all 0.3s ease;
```
Change `0.3s` to your preferred speed (e.g., `0.5s` for slower).

### Change Menu Height
In mobile styles:
```css
nav ul.active {
    max-height: 500px;
}
```
Adjust `500px` if you add more navigation items.

## Adding to New Pages

When you create new lab pages, copy this navigation structure:

```html
<nav>
    <button class="hamburger" aria-label="Toggle navigation" aria-expanded="false">
        <span></span>
        <span></span>
        <span></span>
    </button>
    
    <ul id="nav-menu">
        <li><a href="index.html">Home</a></li>
        <li><a href="lab02.html">Lab 2: AI Evaluation</a></li>
        <!-- Add all your links -->
    </ul>
</nav>
```

And add this JavaScript before the closing `</body>` tag:

```html
<script>
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.getElementById('nav-menu');

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
        
        const isExpanded = hamburger.classList.contains('active');
        hamburger.setAttribute('aria-expanded', isExpanded);
    });

    const navLinks = document.querySelectorAll('#nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        });
    });
</script>
```

## Testing

To test your hamburger menu:

1. **Desktop test**: Open in browser at full width - you should see the normal horizontal menu
2. **Mobile test**: Resize browser window to under 768px wide - hamburger should appear
3. **Click test**: Click the hamburger icon - menu should slide down
4. **Animation test**: Click again - icon should animate to X shape
5. **Link test**: Click a navigation link - menu should close automatically

## Browser Compatibility

This implementation uses:
- Vanilla JavaScript (no frameworks needed)
- CSS3 transitions (supported by all modern browsers)
- Flexbox (widely supported)

Works on:
- Chrome, Firefox, Safari, Edge (all recent versions)
- Mobile browsers (iOS Safari, Chrome Mobile, etc.)

## Troubleshooting

**Menu won't open?**
- Check browser console for JavaScript errors
- Make sure `id="nav-menu"` is on the `<ul>` element

**Hamburger not visible on mobile?**
- Check that you're viewing at < 768px width
- Inspect element to ensure styles are loading

**Animation not smooth?**
- Check that CSS file is properly linked
- Verify transitions are in the CSS

## Next Steps

You may want to apply this same navigation structure to your other pages:
- `practice.html`
- `lab5.html` (when created)
- `hometown-map.html` (when created)

Just copy the navigation structure and JavaScript from any of the updated pages!
