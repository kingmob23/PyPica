# PyPica - Command-line Image Processor 

PyPica is a command-line image processing tool that supports various operations. It's designed with simplicity and ease of use in mind, providing a variety of essential image processing functions through an intuitive command-line interface.

## Features

- Display essential information about an image
- Crop an image to specific dimensions
- Crop an image to its non-empty content
- Generate a palette image from the image
- Adjust the color channels (red, green, blue) by given coefficients
- Invert the color channels of the image

## Installation

PyPica requires Python 3.6+ to run.

Clone the repository:

```bash
git clone https://github.com/kingmob23/PyPica.git
```

Navigate to the PyPica directory:

```bash
cd PyPica
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To use PyPica, navigate to the directory containing the image you want to process and run the `app.py` script with the desired options.

Here's an example of how to display essential information about an image:

```bash
python3 app.py your_image.png --info
```

You can find more details about other options by running:

```bash
python3 app.py --help
```

## License

This project is licensed under the terms of the MIT License.
