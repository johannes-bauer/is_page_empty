# is_page_empty

A simple package/script that checks whether a given image file is empty.

Install it with one of the optional dependencies `skimage`, `imageio`, or `pil` or provide that skimage, imageio, or pillow are installed.

Then you can check whether an image file is empty using the commandline:

```bash
if is_page_empty some_image.png; then echo "Yes, it's empty"; else echo "No, it's not empty."; fi
```

Or you can use the package to check programmatically

```python
import is_page_empty
if is_empty('path/to/image/file.png'):
    print("That file is empty.")
```

The script simply cuts the page into small squares, counts the number of pixels below a certain threshold in each, and compares the sum of those numbers in the squares with the highest numbers to a cutoff threshold.

This has been very robust, in my experience, for scanned text; in particular in double-sided prints, where some of the print on the other side may shine through, and in pages with punched holes, which are rendered black in the print.
