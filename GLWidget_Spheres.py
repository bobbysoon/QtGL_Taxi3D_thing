from _misc import *

from OpenGL.GL import shaders

class GLWidget_Spheres:
	def __init__(self):
		self.quadratic = gluNewQuadric()
		gluQuadricNormals(self.quadratic, GLU_SMOOTH)
		gluQuadricTexture(self.quadratic, GL_TRUE)

		self.shader_Spheres=None # need gl context first. defer shader's init to when 1st drawn

	def __init__Spheres(self):
		vert= open('GLWidget_Spheres.vert').read()
		frag= open('GLWidget_Spheres.frag').read()

		VERTEX_SHADER = shaders.compileShader(vert, GL_VERTEX_SHADER)
		FRAGMENT_SHADER = shaders.compileShader(frag, GL_FRAGMENT_SHADER)
		self.shader_Spheres = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
		self.shader_color = glGetUniformLocation( self.shader_Spheres, 'color' )

	def drawSphere(self, pos,col):
		glUniform4f(self.shader_color, *col )
		glPushMatrix()
		glTranslatef(*pos)
		gluSphere(self.quadratic, 1 ,12,12)
		glPopMatrix()

	def paintGL_Spheres(self):
		if not self.shader_Spheres: self.__init__Spheres()

		shaders.glUseProgram(self.shader_Spheres)

		c1,c2=self.centroids
		self.drawSphere( c1 , (1,0,0,1) )
		self.drawSphere( c2 , (0,0,1,1) )


