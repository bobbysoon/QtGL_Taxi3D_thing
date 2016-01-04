#!/usr/bin/python

from GLWidget import *


class BoxWidget(QWidget):
	def __init__(self,widgets, stretches, orientation):
		QWidget.__init__(self)
		self.setLayout(QBoxLayout(orientation))
		for w in widgets:
			if w:
				self.layout().addWidget(w)
				if stretches: self.layout().setStretchFactor(w,stretches[widgets.index(w)])
			else:
				self.layout().addStretch()

		m=0;self.layout().setContentsMargins(m,m,m,m)
	def addWidget(self, widget): self.layout().addWidget(widget)
	def addLayout(self, layout): self.layout().addLayout(layout)

class HBoxWidget(BoxWidget):
	def __init__(self,widgets=[], stretches=None):
		BoxWidget.__init__(self,widgets, stretches, QBoxLayout.LeftToRight)
class VBoxWidget(BoxWidget):
	def __init__(self,widgets=[], stretches=None):
		BoxWidget.__init__(self,widgets, stretches, QBoxLayout.TopToBottom)


class ValEdit(HBoxWidget):
	def __init__(self, label):
		self.spin=QDoubleSpinBox()
		HBoxWidget.__init__(self, 
					  widgets=[QLabel(label),self.spin], 
					  stretches=[0,1])
		self.value=self.spin.value
		self.setValue=self.spin.setValue
		self.valueChanged=self.spin.valueChanged

	#def setValue(self, v): self.spin.setValue(v)


class BoxLayout(QVBoxLayout):
	valueChanged = pyqtSignal(tuple)
	def __init__(self, parent):
		QVBoxLayout.__init__(self, parent)
		self.spin_dx=ValEdit('dx') ; self.addWidget(self.spin_dx)
		self.spin_dy=ValEdit('dy') ; self.addWidget(self.spin_dy)
		self.spin_dz=ValEdit('dz') ; self.addWidget(self.spin_dz)
		self.addStretch()

		self.spin_dx.valueChanged.connect(self.valueChangedSignal)
		self.spin_dy.valueChanged.connect(self.valueChangedSignal)
		self.spin_dz.valueChanged.connect(self.valueChangedSignal)

	def valueChangedSignal(self,n):
		dx=self.spin_dx.value()
		dy=self.spin_dy.value()
		dz=self.spin_dz.value()
		self.valueChanged.emit((dx,dy,dz))

	def setValues(self, dx,dy,dz ):
		self.spin_dx.setValue(dx)
		self.spin_dy.setValue(dy)
		self.spin_dz.setValue(dz)

class CentralWidget(QSplitter):
	def __init__(self, parent):
		QSplitter.__init__(self, Qt.Horizontal, parent)
		w= QWidget(self) ; w.setMinimumSize(64,64) ; w.setLayout(BoxLayout(self))
		self.glWidget= GLWidget(self) ; self.glWidget.centroids = (1,2,3),(-1,-2,-3)
		self.addWidget( self.glWidget )
		self.addWidget( w )
		self.setStretchFactor(0,1)
		self.setStretchFactor(1,1)

		dx,dy,dz=map(lambda x,y:x-y, *self.glWidget.centroids)
		print dx,dy,dz
		w.layout().setValues(dx,dy,dz) # wonky
		w.layout().valueChanged.connect(self.valueChangedEvent)

	def valueChangedEvent(self, tup ):
		c1= tuple([ n/2 for n in list(tup)])
		c2= tuple([-n/2 for n in list(tup)])
		self.glWidget.centroids = c1,c2
		self.glWidget.updateGL()

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			QApplication.quit()


class DemoMainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setCentralWidget(CentralWidget(self))


if __name__ == '__main__':
	from sys import argv
	app = QApplication(argv)
	window = DemoMainWindow()
	window.show()
	app.exec_()
