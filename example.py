import sys

from hfilesize import FileSize

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel

from qt_range_slider import QtRangeSlider

def _size(size):
	print(f'size: {size}')
	if size < 0:
		print('size is negative, resetting to 0')
		size = 0
	return '{:.02fH}'.format(FileSize(size))

# pylint: disable=too-many-arguments
def _render_only_slider(layout, min_value = 0, max_value = 10):
	inner_layout = QHBoxLayout()
	slider = QtRangeSlider(layout.parent(), min_value, max_value)
	slider.setMinimumWidth(500)
	inner_layout.addWidget(slider)

	layout.addLayout(inner_layout)

def _render_slider_with_labels(layout, min_value = 0, max_value = 10, \
	left_thumb_value=0, right_thumb_value=None, size_value=False):
	inner_layout = QHBoxLayout()

	label_min = QLabel(_size(left_thumb_value) if size_value else str(left_thumb_value))
	label_min.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
	label_min.setFixedWidth(70)
	_right_thumb_value = right_thumb_value if right_thumb_value else max_value
	label_max = QLabel(_size(_right_thumb_value) if size_value else str(_right_thumb_value))
	label_max.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
	label_max.setFixedWidth(70)
	slider = QtRangeSlider(layout.parent(), min_value, max_value, left_thumb_value, right_thumb_value)
	slider.setMinimumWidth(500)
	inner_layout.addWidget(label_min)
	inner_layout.addWidget(slider)
	inner_layout.addWidget(label_max)
	layout.addLayout(inner_layout)

	# connect signal-slots
	if not size_value:
		slider.left_thumb_value_changed.connect(label_min.setNum)
		slider.right_thumb_value_changed.connect(label_max.setNum)
		return slider

	slider.left_thumb_value_changed.connect(lambda x: label_min.setText(_size(x)))
	slider.right_thumb_value_changed.connect(lambda x: label_max.setText(_size(x)))
	return slider


def main():
	app = QApplication(sys.argv)

	main_window = QWidget()
	main_window.setMinimumSize(640, 480)
	layout = QVBoxLayout(main_window)

	min_value = 0
	max_value = 10
	_render_only_slider(layout, min_value, max_value)
	_render_slider_with_labels(layout, min_value, max_value)
	_render_slider_with_labels(layout, min_value, max_value, min_value + 1, \
		max_value - 1)
	min_value = 0
	max_value = 10*1024*1024*1024
	_render_slider_with_labels(layout, min_value, max_value, max_value // 3, \
		max_value * 3 // 4, size_value=True)

	slider = _render_slider_with_labels(layout, min_value, max_value, max_value // 3, \
		max_value * 3 // 4, size_value=True)
	slider.setMinimumWidth(500)
	slider.set_ticks_count(10)

	main_window.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
