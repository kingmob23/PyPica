import os
import argparse
from PIL import Image


class ImageProcessor:
    def __init__(self, image_path):
        if not os.path.isfile(image_path):
            raise ValueError(f"File not found: {image_path}")
        self.image = Image.open(image_path)
        self.image_path = image_path

    def get_info(self):
        """
        Prints essential information about the image such as format, mode, size, and palette.
        """
        print(f"Format: {self.image.format}")
        print(f"Mode: {self.image.mode}")
        print(f"Size: {self.image.size}")
        if self.image.palette:
            print(f"Palette: this image has a palette. To display it use --palette.")
        else:
            print("Palette: None")

    def crop_image(self, left, upper, right, lower):
        """
        Crops the image to a box (left, upper, right, lower).
        """
        width, height = self.image.size

        # Check if crop dimensions are within image dimensions
        if left < 0 or upper < 0 or right > width or lower > height:
            raise ValueError(
                f"Invalid crop dimensions. Image dimensions are {width}x{height}."
                f" Please provide crop dimensions within these bounds.")

        if left >= right or upper >= lower:
            raise ValueError(
                f"Invalid crop dimensions. Please ensure that left < right and upper < lower."
            )

        frame = (left, upper, right, lower)
        cropped_image = self.image.crop(frame)
        cropped_image.save(self._get_output_filename('cropped'))

    def crop_empty(self):
        """
        Crops the image to its non-empty content. This is done by finding the bounding box 
        of the non-empty regions. The method assumes that "empty" space is white (pixel value 255).
        """
        gray_image = self.image.convert('L')

        # Binarize the image
        binary_image = gray_image.point(lambda p: int(p > 0))

        # Project onto the x and y axes
        x_projection = [any(binary_image.getpixel((x, y)) for y in range(
            binary_image.height)) for x in range(binary_image.width)]
        y_projection = [any(binary_image.getpixel((x, y)) for x in range(
            binary_image.width)) for y in range(binary_image.height)]

        left = x_projection.index(True)
        right = len(x_projection) - x_projection[::-1].index(True)
        upper = y_projection.index(True)
        lower = len(y_projection) - y_projection[::-1].index(True)

        self.image = self.image.crop((left, upper, right, lower))
        self.image.save(self._get_output_filename('cropped_empty'))

    def get_palette(self):
        """
        Generates a palette image from the image if its in P mode.
        """
        palette = self.image.getpalette()

        if palette is None:
            raise ValueError("Image does not have a palette.")

        num_colors = len(palette) // 3
        side = int(num_colors ** 0.5)
        actual_side = side if side * side == num_colors else side + 1
        new_image = Image.new('RGB', (actual_side, actual_side))

        for y in range(actual_side):
            for x in range(actual_side):
                color_index = y * actual_side + x
                if color_index < num_colors:
                    r, g, b = palette[color_index*3:color_index*3+3]
                    new_image.putpixel((x, y), (r, g, b))

        new_image.save(self._get_output_filename('palette'))

    def adjust_colors(self, red_coefficient, green_coefficient, blue_coefficient):
        """
        Adjusts the color channels (red, green, blue) by the given coefficients.
        """
        if self.image.mode not in ['RGB', 'RGBA']:
            raise ValueError(
                f"Unsupported image mode for color adjustment: {self.image.mode}")

        coefficients = (red_coefficient, green_coefficient, blue_coefficient)
        new_image = self.image.point(lambda i: i * coefficients[i % 3])
        new_image.save(self._get_output_filename('adjusted'))

    def invert_colors(self):
        """
        Inverts the color channels of the image.
        """
        if self.image.mode not in ['RGB', 'RGBA']:
            raise ValueError(
                f"Unsupported image mode for color inversion: {self.image.mode}")

        new_image = self.image.point(lambda i: 255 - i)
        new_image.save(self._get_output_filename('inverted'))

    def _get_output_filename(self, prefix):
        basename = os.path.basename(self.image_path)
        base, ext = os.path.splitext(basename)
        return f'{prefix}_{base}{ext}'


def main():
    parser = argparse.ArgumentParser(
        description="A simple command-line image processor that supports various image processing operations."
    )

    parser.add_argument(
        "image_path",
        help="Path to the image file."
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Gives essential information about the image."
    )

    parser.add_argument(
        "--crop",
        nargs=4,
        type=int,
        metavar=("LEFT", "UPPER", "RIGHT", "LOWER"),
        help="Crops the image to a box defined by two points: (LEFT, UPPER, RIGHT, LOWER)."
    )

    parser.add_argument(
        "--crop_empty",
        action="store_true",
        help="Crops the image to its non-empty content by removing empty space around the content of the image."
    )

    parser.add_argument(
        "--palette",
        action="store_true",
        help="Generates a palette image from the image if its in P mode."
    )

    parser.add_argument(
        "--adjust_colors",
        nargs=3,
        type=float,
        metavar=("RED_COEFFICIENT", "GREEN_COEFFICIENT", "BLUE_COEFFICIENT"),
        help="Adjusts the color channels (red, green, blue) by the given coefficients."
    )

    parser.add_argument(
        "--invert",
        action="store_true",
        help="Inverts the color channels of the image."
    )

    args = parser.parse_args()

    try:
        processor = ImageProcessor(args.image_path)

        if args.info:
            processor.get_info()

        if args.crop:
            processor.crop_image(*args.crop)

        if args.crop_empty:
            processor.crop_empty()

        if args.palette:
            processor.get_palette()

        if args.adjust_colors:
            processor.adjust_colors(*args.adjust_colors)

        if args.invert:
            processor.invert_colors()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
