import sys

from hurry.filesize import size

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel

from qt_range_slider import QtRangeSlider

# pylint: disable=too-many-arguments
def _render_only_slider(parent, layout, min_value = 0, max_value = 10):
	inner_layout = QHBoxLayout(parent)
	slider = QtRangeSlider(parent, min_value, max_value)
	inner_layout.addWidget(slider)

	layout.addLayout(inner_layout)

def _render_slider_with_labels(parent, layout, min_value = 0, max_value = 10, \
	left_thumb_value=0, right_thumb_value=None, size_value=False):
	inner_layout = QHBoxLayout(parent)

	label_min = QLabel(size(left_thumb_value) if size_value else str(left_thumb_value))
	_right_thumb_value = right_thumb_value if right_thumb_value else max_value
	label_max = QLabel(size(_right_thumb_value) if size_value else str(_right_thumb_value))
	slider = QtRangeSlider(parent, min_value, max_value, left_thumb_value, right_thumb_value)
	inner_layout.addWidget(label_min)
	inner_layout.addWidget(slider)
	inner_layout.addWidget(label_max)
	layout.addLayout(inner_layout)

	# connect signal-slots
	if not size_value:
		slider.left_thumb_value_changed.connect(label_min.setNum)
		slider.right_thumb_value_changed.connect(label_max.setNum)
		return
	slider.left_thumb_value_changed.connect(lambda x: label_min.setText(size(x)))
	slider.right_thumb_value_changed.connect(lambda x: label_max.setText(size(x)))


def main():
	app = QApplication(sys.argv)

	main_window = QWidget()
	main_window.setMinimumSize(640, 480)
	layout = QVBoxLayout(main_window)

	min_value = 0
	max_value = 10
	_render_only_slider(main_window, layout, min_value, max_value)
	_render_slider_with_labels(main_window, layout, min_value, max_value)
	_render_slider_with_labels(main_window, layout, min_value, max_value, min_value + 1, \
		max_value - 1)
	min_value = 0
	max_value = 10*1024*1024*1024
	_render_slider_with_labels(main_window, layout, min_value, max_value, max_value // 3, \
		max_value * 3 // 4, size_value=True)

	main_window.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
