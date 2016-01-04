from _misc import *

class GLWidget_Input:
	def __init__(self):
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.updateGL)
		#self.timer.setSingleShot(True)

	def mousePressEvent(self, event):
		self.setCursor(Qt.BlankCursor)
		self.mousePosWhenClicked = self.mousePos()
		self.centerCursor()
		self.timer.start(10)

	def mouseReleaseEvent(self, event):
		self.timer.stop()
		self.setMousePos(self.mousePosWhenClicked)
		self.setCursor(Qt.ArrowCursor)

	def center(self):
		sz=self.size()
		return QPoint(sz.width()/2,sz.height()/2)

	def mousePos(self):			return self.mapFromGlobal(QCursor.pos())
	def setMousePos(self, p):	QCursor.setPos(self.mapToGlobal(p))
	def centerCursor(self):		self.setMousePos(self.center())

	def mouseMovement(self):
		c=self.center()
		m=QPointF(self.mousePos()-c)
		dx,dy = m.x()/c.x(),m.y()/c.y()
		fovy,aspect = gluGetPerspective()
		return dx*fovy*aspect,dy*fovy

	def Input(self, lookSpeed=32.0,moveSpeed=.1):
		if self.timer.isActive():
			mouse_dx,mouse_dy = self.mouseMovement()
			self.centerCursor()

			buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
			c = (-1 * numpy.mat(buffer[:3,:3]) * numpy.mat(buffer[3,:3]).T).reshape(3,1)
			glTranslate(c[0],c[1],c[2])
			m = buffer.flatten()
			glRotate( mouse_dx*lookSpeed, m[1],m[5],m[9])
			glRotate( mouse_dy*lookSpeed, m[0],m[4],m[8])

			# compensate roll
			glRotated(-atan2(-m[4],m[5]) * 57.295779513082320876798154814105 ,m[2],m[6],m[10])
			glTranslate(-c[0],-c[1],-c[2])

			x,y,z=self.wasd
			if z or x or y:
				t=moveSpeed ; x*=t;y*=t;z*=t
				glTranslate(z*m[2],z*m[6],z*m[10])
				glTranslate(x*m[0],x*m[4],x*m[8])
				glTranslate(y*m[1],y*m[5],y*m[9])

	wasd=[0,0,0]
	def keyPressEvent(self, e):
		k=e.key()
		if k == Qt.Key_A:				self.wasd[0] =  1.0
		elif k == Qt.Key_D:				self.wasd[0] = -1.0
		elif k == Qt.Key_Shift:			self.wasd[1] =  1.0
		elif k == Qt.Key_Space:			self.wasd[1] = -1.0
		elif k == Qt.Key_S:				self.wasd[2] = -1.0
		elif k == Qt.Key_W:				self.wasd[2] =  1.0
		else: super (self.__class__, self).keyPressEvent(e)

	def keyReleaseEvent(self, e):
		k=e.key()
		if k == Qt.Key_A:				self.wasd[0]=0.0
		elif k == Qt.Key_D:				self.wasd[0]=0.0
		elif k == Qt.Key_Shift:			self.wasd[1]=0.0
		elif k == Qt.Key_Space:			self.wasd[1]=0.0
		elif k == Qt.Key_S:				self.wasd[2]=0.0
		elif k == Qt.Key_W:				self.wasd[2]=0.0
		else: super (self.__class__, self).keyReleaseEvent(e)

