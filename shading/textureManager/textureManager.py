import general.mayaNode.mayaNode as mn
import pipe.textureFile.textureFile as tfl

class Manager(object):
	"""
	manage textures in current scene
	"""
	def __init__(self):
		pass

	@property
	def textures(self):
		"""
		return the textures in the scene
		"""
		return mn.ls( typ = ['file', 'aiImage'] )

	def toTx(self, textures, autoCreate = True):
		"""
		convert and change path to toTx
		"""
		for n in textures:
			if n.type == 'aiImage':
				attr = "filename"
			else:
				attr = "ftn"
			f = tfl.textureFile( n.attr( attr ).v )
			if not f.exists:
				continue
			if not f.hasTx:
				f.makeTx( True )
			toTx = f.toTx()
			n.attr( attr ).v = toTx.path

	def createTx(self, textures):
		"""create tx version"""
		for n in textures:
			if n.type == 'aiImage':
				attr = "filename"
			else:
				attr = "ftn"
			f = tfl.textureFile( n.attr( attr ).v )
			if not f.exists:
				continue
			if not f.hasTx:
				f.makeTx( True )

	def allToTx(self):
		"""
		convert all the textures to Tx
		"""
		self.toTx( self.textures )

	def toPng(self, textures ):
		"""
		convert and change path to toPng
		"""
		for n in textures:
			if n.type == 'aiImage':
				attr = "filename"
			else:
				attr = "ftn"
			f = tfl.textureFile( n.attr( attr ).v )
			if f.hasPng:
				toPng = f.toPng()
				n.attr( attr ).v = toPng.path

	def allToPng(self):
		"""
		convert all the textures to Png
		"""
		self.toPng( self.textures )

	def moveToFolder(self, textures, folderPath):
		"""
		Move the textures to a folder
		"""
		for n in textures:
			if n.type == 'aiImage':
				attr = "filename"
			else:
				attr = "ftn"
			f = tfl.textureFile( n.attr( attr ).v )
			if not f.exists:
				continue
			newFile = f.copy( folderPath )
			n.attr( attr ).v = newFile.path

	def replacePath(self, textures, searchAndReplace = ['','']):
		"""
		change the path of the texture, search and replace are optional
		"""
		for n in textures:
			if n.type == 'aiImage':
				attr = "filename"
			else:
				attr = "ftn"
			n.attr( attr ).v = n.attr( attr ).v.replace( searchAndReplace[0], searchAndReplace[1] )

	def renameTexture(self, texture, newName):
		"""docstring for renameTextures"""
		if texture.type == 'aiImage':
			attr = "filename"
		else:
			attr = "ftn"
		f = tfl.textureFile( texture.attr( attr ).v )
		f.rename( newName + f.extension )
		texture.attr( attr ).v = f.path
		if f.hasTx():
			txVer = f.toTx()
			txVer.rename( newName + txVer.extension )
