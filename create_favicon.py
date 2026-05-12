#!/usr/bin/env python3
"""Convert JPG to favicon formats (PNG + ICO)"""

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    import subprocess
    subprocess.check_call(['pip3', 'install', '--user', 'Pillow'])
    from PIL import Image

# Open and resize image
img = Image.open('ran_fav/vase_of_flowers_1961.6.1.jpg')
img = img.convert('RGB')

# Create square crop from center
width, height = img.size
size = min(width, height)
left = (width - size) // 2
top = (height - size) // 2
img_cropped = img.crop((left, top, left + size, top + size))

# Resize to 512x512 for PNG
img_512 = img_cropped.resize((512, 512), Image.Resampling.LANCZOS)
img_512.save('favicon.png')
print('✓ Created favicon.png (512x512)')

# Create ICO with multiple sizes
img_cropped.save('favicon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
print('✓ Created favicon.ico (multi-size: 16, 32, 48, 64, 128, 256)')

print('\nFavicon files ready for Quarto website!')
