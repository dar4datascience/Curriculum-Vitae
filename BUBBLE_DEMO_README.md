# Bubble Animation Demo - Quick Start

## Prerequisites

Make sure you have Quarto installed:
```bash
quarto --version
```

If not installed, get it from: https://quarto.org/docs/get-started/

## Run Locally

### Option 1: Preview (Recommended)
```bash
quarto preview bubble_animation_demo.qmd
```

This will:
- Render the document
- Open in your browser
- Auto-reload on changes

### Option 2: Render to HTML
```bash
quarto render bubble_animation_demo.qmd
```

Then open `bubble_animation_demo.html` in your browser.

## What You'll See

- **10 interactive bubbles** representing skills/technologies
- **Click a bubble**: Zooms to center, shows details
- **Drag bubbles**: Move them around
- **Click background**: Reset to normal view
- **Physics simulation**: Bubbles float and avoid collisions

## Customization

Edit the `data` array in the `.qmd` file (around line 17):

```javascript
data = [
  {
    id: 1, 
    name: "Your Skill", 
    category: "Category", 
    value: 85,           // Size (0-100)
    icon: "🚀",          // Any emoji
    desc: "Description"
  },
  // Add more...
]
```

### Tips

- **value**: Controls bubble size (higher = bigger)
- **icon**: Use any emoji from https://emojipedia.org/
- **Colors**: Edit the gradient in line 95 (`style("background", ...)`)
- **Speed**: Adjust `duration(2000)` values (milliseconds)

## How It Works

Uses **Observable JS** in Quarto:
- D3.js v7 for animations
- Force simulation for physics
- Reactive cells for data flow

No build step needed - Quarto handles everything!

## Troubleshooting

**Bubbles not appearing?**
- Check browser console (F12)
- Ensure Quarto is up to date

**Slow performance?**
- Reduce number of bubbles
- Lower `duration` values
- Simplify overlay HTML

**Want images instead of emojis?**
Replace icon with image URLs and use SVG patterns (like the original yesenia.io site).
