from GLWidget_Input import *
from GLWidget_Spheres import *
from GLWidget_UnProjector import *

class GLWidget(QGLWidget, GLWidget_Input , GLWidget_Spheres , GLWidget_UnProjector ):
	def __init__(self, parent):
		QGLWidget.__init__(self, parent)
		GLWidget_Input.__init__(self)
		GLWidget_Spheres.__init__(self)
		GLWidget_UnProjector.__init__(self)

		self.setMinimumSize(128,128)
		self.setFocusPolicy(Qt.StrongFocus)

	isPainting=False # QTimer and updateGL: should i be concerned?
	def paintGL(self):
		if not self.isPainting:
			self.isPainting=True
			self.Input()
			glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
			self.paintGL_Spheres()
			self.paintGL_UnProjector()
			glFlush()
			self.isPainting=False
		else:
			print 'gah'

	def resizeGL(self, width, height):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		ratio= float(width)/float(height)
		gluPerspective(45,ratio,3,40)
		glViewport(0, 0, width, height)
		glMatrixMode(GL_MODELVIEW)
		#glLoadIdentity()

	def initializeGL(self):
		#glEnable(GL_LIGHTING)
		glShadeModel(GL_SMOOTH)
		#glEnable(GL_LIGHT0)
		#glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.45, 0.0, 1.0))
		#glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 10.0, 10.0, 10.0))
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)
		glEnable(GL_CULL_FACE)

		gluLookAt(
			9,0,0,
			0,0,0,
			0,1,0)

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

