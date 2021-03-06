import os
import general.ui.pySideHelper as uiH
reload( uiH )

from Qt import QtGui,QtCore

import maya.cmds as mc
import general.mayaNode.mayaNode as mn
import pipe.mayaFile.mayaFile as mfl

PYFILEDIR = os.path.dirname( os.path.abspath( __file__ ) )

uifile = PYFILEDIR + '/facerig.ui'
fom, base = uiH.loadUiType( uifile )

import rigging.face.face as fc
reload( fc )
import rigging.utils.utils as utl

class faceRigUi(base, fom):
	"""docstring for ProjectCreator"""
	def __init__(self, parent  = uiH.getMayaWindow(), *args ):
		if uiH.USEPYQT:
			super(base, self).__init__(parent)
		else:
			super(faceRigUi, self).__init__(parent)
		self.setupUi(self)
		self.setObjectName( 'faceRigUi' )
		self.connect(self.impRig_btn, QtCore.SIGNAL("clicked()"), self.importRig)
		self.connect(self.addAttrToCurve_btn, QtCore.SIGNAL("clicked()"), self.addAttrToCurve)
		self.connect(self.create_btn, QtCore.SIGNAL("clicked()"), self.create)
		self.connect(self.fillMeshToDeform_btn, QtCore.SIGNAL("clicked()"), self.fillMeshToDeform)
		self.connect(self.fillVertecesToIgnore_btn, QtCore.SIGNAL("clicked()"), self.fillVertecesToIgnore)
		self.connect(self.fillMeshToSkin_btn, QtCore.SIGNAL("clicked()"), self.fillMeshToSkin)
		self.connect(self.fillSkin_btn, QtCore.SIGNAL("clicked()"), self.fillSkin)
		self.connect(self.createSofts_btn, QtCore.SIGNAL("clicked()"), self.createSofts)
		self.connect(self.mirrorSoftRtoL_btn, QtCore.SIGNAL("clicked()"), lambda val = 'r' : self.mirrorSofts( val ))
		self.connect(self.mirrorSoftLtoR_btn, QtCore.SIGNAL("clicked()"), lambda val = 'l' : self.mirrorSofts(val))
		uiH.loadSkin( self, 'QTDarkGreen' )

	def mirrorSofts(self, origSide):
		"""mirror softs from origSide to opposite side"""
		baseSFMGrp = mn.Node( 'face_SFM_grp' )
		oppSide = 'l' if origSide == 'r' else 'r'
		for n in baseSFMGrp.children:
			n = mn.Node( n.name.split( '|' )[-1] )
			if n.name.lower().startswith( origSide ):
				nOppName = n.name.replace( origSide + '_', oppSide + '_', 1 )
				nOppName = nOppName.replace(':' + origSide + '_', ':' + oppSide + '_' )
				nOpp = mn.Node( nOppName )
				nOpp.a.falloffMode.v = n.a.falloffMode.v
				nOpp.a.falloffRadius.v = n.a.falloffRadius.v


	def fillMeshToDeform(self):
		"""docstring for fname"""
		self.meshToDeform_le.setText( mn.ls( sl = True, dag = True, s = True )[0].name )

	def fillVertecesToIgnore(self):
		"""docstring for fname"""
		self.vertecesToIgnore_lw.clear()
		vertexToRemove = mc.ls( sl = True, fl = True )
		self.vertecesToIgnore_lw.addItems( vertexToRemove )

	def fillMeshToSkin(self):
		"""docstring for fname"""
		self.meshToSkin_le.setText( mn.ls( sl = True, dag = True, s = True )[0].name )

	def fillSkin(self):
		"""docstring for fillSkin"""
		skin = utl.getSkinFromGeo( mn.ls( sl = True, dag = True, s = True )[0].name )
		print skin
		self.skin_le.setText( skin[0] )

	def importRig(self):
		"""import rig to scene"""
		mfl.mayaFile( PYFILEDIR + '/base_face_rig.ma' ).imp()

	def createSofts(self):
		"""docstring for createSofts"""
		vertexToRemove = []
		for index in xrange(self.vertecesToIgnore_lw.count()):
			vertexToRemove.append( str( self.vertecesToIgnore_lw.item(index).text() ) )
		fc.createSoftsOnFace( str( self.meshToDeform_le.text() ), vertexToRemove )

	def addAttrToCurve(self):
		"""docstring for fname"""
		for s in mn.ls( sl = True ):
			s.a.controls_count.add( minValue = 1, at = 'short', k = True )
			s.a.use_tips.add( at = 'bool', k = True )

	def create(self):
		"""create face rig based on selection"""
		meshWithRivets = str( self.meshToDeform_le.text() )
		skinMesh = str( self.meshToSkin_le.text() )
		skin = str( self.skin_le.text() )
		fc.softModsToStickys( meshWithRivets, skin, skinMesh )


def main():
	"""use this to create project in maya"""
	if mc.window( 'faceRigUi', q = 1, ex = 1 ):
		mc.deleteUI( 'faceRigUi' )
	PyForm=faceRigUi()
	PyForm.show()

