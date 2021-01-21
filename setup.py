"""Setup script for qt-range-slider"""

import os.path
import setuptools

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
	README = fid.read()

# This call to setup() does all the work
setuptools.setup(
	name="qt-range-slider",
	version="0.2.0",
	description="Qt widget-slider with two thumbs (min/max values)",
	long_description=README,
	long_description_content_type="text/markdown",
	url="https://github.com/introkun/qt-range-slider",
	author="Sergey G",
	author_email="introkun@gmail.com",
	license="MIT",
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
	],
	packages=setuptools.find_packages(),
	include_package_data=True,
	install_requires=[
		"pyqt5"
	],
	python_requires='>=3.6',
)
