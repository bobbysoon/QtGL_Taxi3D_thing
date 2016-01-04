from _misc import *

from OpenGL.GL.shaders import compileShader,compileProgram,glUseProgram

class GLWidget_UnProjector:
	def __init__(self):
		self.shader_UnProjector=None

	def __init__UnProjector(self):
		vert= open('GLWidget_UnProjector.vert').read()
		frag= open('GLWidget_UnProjector.frag').read()

		VERTEX_SHADER=				compileShader(vert, GL_VERTEX_SHADER)
		FRAGMENT_SHADER=			compileShader(frag, GL_FRAGMENT_SHADER)
		self.shader_UnProjector=	compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)

		self.res=		glGetUniformLocation( self.shader_UnProjector, 'res' ) # view resolution

		self.c1=		glGetUniformLocation( self.shader_UnProjector, 'c1' ) # the spheres
		self.c2=		glGetUniformLocation( self.shader_UnProjector, 'c2' ) # aka, 'centroids'

		self.near11=	glGetUniformLocation( self.shader_UnProjector, 'near11' )
		self.near12=	glGetUniformLocation( self.shader_UnProjector, 'near12' )
		self.near21=	glGetUniformLocation( self.shader_UnProjector, 'near21' )
		self.near22=	glGetUniformLocation( self.shader_UnProjector, 'near22' )
		self.far11=		glGetUniformLocation( self.shader_UnProjector, 'far11' )
		self.far12=		glGetUniformLocation( self.shader_UnProjector, 'far12' )
		self.far21=		glGetUniformLocation( self.shader_UnProjector, 'far21' )
		self.far22=		glGetUniformLocation( self.shader_UnProjector, 'far22' )

	def paintGL_UnProjector(self):
		if not self.shader_UnProjector: self.__init__UnProjector()

		glUseProgram(self.shader_UnProjector)

		v=	glGetFloatv(GL_VIEWPORT)
		glUniform2f(self.res, v[2],v[3])

		c1,c2=self.centroids
		glUniform3f(self.c1, *c1)
		glUniform3f(self.c2, *c2)

		v=	glGetIntegerv( GL_VIEWPORT )
		m=	glGetDoublev( GL_MODELVIEW_MATRIX )
		p=	glGetDoublev( GL_PROJECTION_MATRIX )

		w,h=v[2:] ; kwa={'modelMatrix':m, 'projMatrix':p, 'viewport':v}

		#nearz,farz=0,-1
		nearz,farz=-1,0 # because 0,1 dont work. So far will be origin plane
		glUniform3f(self.near11,	*UnProject(0,0,nearz,	**kwa))
		glUniform3f(self.near12,	*UnProject(0,h,nearz,	**kwa))
		glUniform3f(self.near21,	*UnProject(w,0,nearz,	**kwa))
		glUniform3f(self.near22,	*UnProject(w,h,nearz,	**kwa))

		glUniform3f(self.far11,		*UnProject(0,0,farz,	**kwa))
		glUniform3f(self.far12,		*UnProject(0,h,farz,	**kwa))
		glUniform3f(self.far21,		*UnProject(w,0,farz,	**kwa))
		glUniform3f(self.far22,		*UnProject(w,h,farz,	**kwa))

		#glRectf(-.75,-.75,.75,.75)
		glRectf(-1,-1,1,1)
