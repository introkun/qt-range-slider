import sys
import unittest

from PyQt5.QtCore import Qt, QRect, QEvent, QSize, QPoint
from PyQt5.QtTest import QTest
from PyQt5.QtGui import QPaintEvent, QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from qt_range_slider import QtRangeSlider


def _mouse_move(widget: QWidget, new_position: QPoint):
	print(f"move mouse to ({new_position.x()}, {new_position.y()})")
	event = QMouseEvent(QEvent.MouseMove, new_position, \
			Qt.LeftButton, Qt.NoButton, Qt.NoModifier)
	QApplication.sendEvent(widget, event)

def _draw_widget(widget: QWidget):
	unused_event = QPaintEvent(QRect(0, 0, 1, 1))
	widget.resizeEvent(unused_event)
	widget.paintEvent(unused_event)

def _gb_to_bytes(gb_count):
	return gb_count * 1024 ** 3


class QtRangeSliderTest(unittest.TestCase):
	"""Tests for qt_range_slider
	"""
	@classmethod
	def setUpClass(cls):
		cls._app = QApplication(sys.argv)
		cls._form = QMainWindow()
		cls._initial_size = QSize(500, 100)
		cls._form.setFixedWidth(cls._initial_size.width())
		cls._form.setFixedHeight(cls._initial_size.height())

	def test_init(self):
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10, 3, 5)
		self.assertIsNotNone(slider)
		with self.assertRaises(ValueError):
			QtRangeSlider(QtRangeSliderTest._form, 0, 10, 5, 3)

	# pylint: disable=no-self-use
	def test_paint_event(self):
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10, 3, 5)
		_draw_widget(slider)

	def test_ticks(self):
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10, 3, 5)
		slider.set_ticks_count(5)
		# pylint: disable=protected-access
		self.assertEqual(slider._ticks_count, 5)
		_draw_widget(slider)


	def test_thumb_values(self):
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10)
		slider.set_left_thumb_value(3)
		# pylint: disable=protected-access
		self.assertEqual(slider._left_thumb.value, 3)
		slider.set_left_thumb_value(5)
		# pylint: disable=protected-access
		self.assertEqual(slider._left_thumb.value, 5)

	def test_change_size_while_dragging(self):
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, _gb_to_bytes(10), \
			_gb_to_bytes(3), _gb_to_bytes(5))
		slider.setMouseTracking(True)
		_draw_widget(slider)
		# pylint: disable=protected-access
		left_thumb_position = slider._left_thumb.rect.center()

		_mouse_move(slider, left_thumb_position)
		QTest.mousePress(slider, Qt.LeftButton, pos=left_thumb_position)

		new_position = left_thumb_position
		new_position.setX(new_position.x() - 10)
		_mouse_move(slider, new_position)

		QTest.mouseRelease(slider, Qt.LeftButton)
		self.assertEqual(slider.get_left_thumb_value(), 2684354560)

		left_thumb_position = slider._left_thumb.rect.center()
		new_width = QtRangeSliderTest._initial_size.width() - 50
		QTest.mouseMove(slider, pos=left_thumb_position)
		QTest.mousePress(slider, Qt.LeftButton, pos=left_thumb_position)
		slider.setMaximumSize(QSize(new_width, QtRangeSliderTest._initial_size.height()))
		_draw_widget(slider)
		new_position = left_thumb_position
		new_x = new_position.x() - 30
		new_position.setX(new_x)
		_mouse_move(slider, new_position)

		QTest.mouseRelease(slider, Qt.LeftButton)
		self.assertEqual(slider.get_left_thumb_value(), 894784853)

	def test_dragging_right_thumb(self):
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, _gb_to_bytes(10), \
			_gb_to_bytes(3), _gb_to_bytes(5))
		slider.setMouseTracking(True)
		_draw_widget(slider)
		# pylint: disable=protected-access
		right_thumb_center = slider._right_thumb.rect.center()

		_mouse_move(slider, right_thumb_center)
		QTest.mousePress(slider, Qt.RightButton, pos=right_thumb_center)

		right_thumb_center.setX(right_thumb_center.x() - 10)
		_mouse_move(slider, right_thumb_center)

		QTest.mouseRelease(slider, Qt.RightButton)
		self.assertEqual(slider.get_right_thumb_value(), 4384445781)

	def test_invalid_ticks_count(self):
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10)
		with self.assertRaises(ValueError):
			slider.set_ticks_count(-10)

	def test_set_incorrect_right_thumb_value(self):
		max_value = 10
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, max_value)
		slider.set_right_thumb_value(max_value + 2)
		self.assertEqual(slider.get_right_thumb_value(), max_value)

	def test_set_incorrect_left_thumb_value(self):
		min_value = 0
		slider = QtRangeSlider(QtRangeSliderTest._form, min_value, 10)
		slider.set_left_thumb_value(min_value - 2)
		self.assertEqual(slider.get_left_thumb_value(), min_value)

	def test_set_left_thumb_value_greater_than_right(self):
		left_thumb_value = 3
		right_thumb_value = 5
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10, left_thumb_value, right_thumb_value)
		slider.set_left_thumb_value(right_thumb_value + 2)
		self.assertEqual(slider.get_left_thumb_value(), left_thumb_value)

	def test_set_right_thumb_value_less_than_left(self):
		left_thumb_value = 3
		right_thumb_value = 5
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10, left_thumb_value, right_thumb_value)
		slider.set_right_thumb_value(left_thumb_value - 2)
		self.assertEqual(slider.get_right_thumb_value(), right_thumb_value)

	def test_set_same_left_thumb_value(self):
		left_thumb_value = 3
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10, left_thumb_value, 5)
		slider.set_left_thumb_value(left_thumb_value)
		self.assertEqual(slider.get_left_thumb_value(), left_thumb_value)

	def test_set_same_right_thumb_value(self):
		right_thumb_value = 5
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10, 3, right_thumb_value)
		slider.set_right_thumb_value(right_thumb_value)
		self.assertEqual(slider.get_right_thumb_value(), right_thumb_value)
