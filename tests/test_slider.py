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
		unused_event = QPaintEvent(QRect(0, 0, 1, 1))
		slider.resizeEvent(unused_event)
		slider.paintEvent(unused_event)

	def test_ticks(self):
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10, 3, 5)
		slider.set_ticks_count(5)
		# pylint: disable=protected-access
		self.assertEqual(slider._ticks_count, 5)
		unused_event = QPaintEvent(QRect(0, 0, 1, 1))
		slider.resizeEvent(unused_event)
		slider.paintEvent(unused_event)


	def test_thumb_values(self):
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10)
		slider.set_left_thumb_value(3)
		# pylint: disable=protected-access
		self.assertEqual(slider._left_thumb.value, 3)
		slider.set_left_thumb_value(5)
		# pylint: disable=protected-access
		self.assertEqual(slider._left_thumb.value, 5)

	def test_change_size_while_dragging(self):
		slider = QtRangeSlider(QtRangeSliderTest._form, 0, 10*1024**3, 3*1024**3, 5*1024**3)
		unused_event = QPaintEvent(QRect(0, 0, 1, 1))
		slider.setMouseTracking(True)
		slider.resizeEvent(unused_event)
		slider.paintEvent(unused_event)
		# pylint: disable=protected-access
		left_thumb_position = slider._left_thumb.rect

		_mouse_move(slider, left_thumb_position.center())
		QTest.mousePress(slider, Qt.LeftButton, pos=left_thumb_position.center())

		new_position = left_thumb_position.center()
		new_position.setX(new_position.x() - 10)
		_mouse_move(slider, new_position)

		QTest.mouseRelease(slider, Qt.LeftButton)
		self.assertEqual(slider.get_left_thumb_value(), 2684354560)

		new_width = QtRangeSliderTest._initial_size.width() - 50
		QTest.mouseMove(slider, pos=left_thumb_position.center())
		QTest.mousePress(slider, Qt.LeftButton, pos=left_thumb_position.center())
		slider.setMaximumSize(QSize(new_width, QtRangeSliderTest._initial_size.height()))
		slider.paintEvent(unused_event)
		new_position = left_thumb_position.center()
		new_x = new_position.x() - 30
		new_position.setX(new_x)
		_mouse_move(slider, new_position)

		QTest.mouseRelease(slider, Qt.LeftButton)
		self.assertEqual(slider.get_left_thumb_value(), 894784853)
