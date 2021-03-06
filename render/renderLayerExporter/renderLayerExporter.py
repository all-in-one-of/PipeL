import render.renderlayer.renderlayer as rlayer
reload( rlayer )
import cPickle as pickle
import maya.cmds as mc
import pipe.file.file as fl
import pipe.mayaFile.mayaFile as mfl
import render.aov.aov as aov
reload( aov )
import general.mayaNode.mayaNode as mn

class RenderLayerExporter(object):
	"""export information from lighting scene"""
	def __init__(self, pathDir):
		self._path = pathDir
	
	@property
	def dataPath(self):
		"""return path for file"""
		return fl.File( self._path + '/renderLayerData.data' )

	@property
	def lightPath(self):
		"""return path for lights file"""
		return mfl.mayaFile( self._path + '/lights.ma' )

	@property
	def shaderPath(self):
		"""return the path for the shader file"""
		return mfl.mayaFile( self._path + '/shaders.ma' )

	@property
	def aovsPath(self):
		"""return the path for the aovs file"""
		return fl.File( self._path + '/aovs.data' )

	@property
	def lightLinkPath(self):
		"""return the path for the aovs file"""
		return fl.File( self._path + '/lights.data' )

	@property
	def masterPath(self):
		"""return the path for the masterLayer data"""
		return fl.File( self._path + '/master.data' )

	#EXPORT
	def export(self, exdata = True, exlights = True, exaovs = True, exshaders = True, exmaster = True):
		"""export information of scene to path"""
		if exdata:
			self.exportData()
		if exshaders:
			self.exportShaders()
		if exlights:
			self.exportLights()
		if exaovs:
			self.exportAovs()
		if exmaster:
			self.exportMasterLayerSettings()

	def exportMasterLayerSettings(self):
		"""export master layer settings so we can re apply it"""
		master = rlayer.RenderLayer( 'defaultRenderLayer' )
		master.makeCurrent()
		masterData = {}
		nodes = ['defaultArnoldRenderOptions','defaultResolution','defaultRenderGlobals']
		mnNodes =[ mn.Node( n ) for n in nodes ]
		for n in mnNodes:
			for a in n.listAttr( se = True, v = True,  w = True ):
				try:
					masterData[a] = a.v
				except:
					continue
		pickle.dump( masterData, open( self.masterPath.path, "wb" ) )
		

	def exportData(self):
		"""export data from scene, objects overrides in renderlayers.. etc"""
		lays = rlayer.renderlayers()
		data = {}
		for l in lays:
			if l.name == 'defaultRenderLayer':
				continue
			data[l.name] = {'objects':l.objects,                  # OBJECTS IN LAYER
							'values' :l.overridesWithValues,      # OVERRIDED ATTRIBUTES ONLY CHANGED VALUES
							'conns'  :l.overridesWithConnections[0], # OVERRIDED ATTRIBUTES CHANGED CONNECTIONS
							'shader' :l.overridedShader           # OVERRIDE RENDERLAYER SHADER
							}
		pickle.dump( data, open( self.dataPath.path, "wb" ) )
	
	def exportLights(self):
		"""export lights from scene"""
		#TODO! REMOVE CONSTRAINS
		lights = mc.ls( typ=['light','aiAreaLight','aiSkyDomeLight','aiVolumeScattering','aiSky'], l=1 )
		mc.editRenderLayerGlobals( currentRenderLayer = 'defaultRenderLayer' )
		litsToExport = []
		for li in lights:
			finalLi = li.split( '|' )
			if len(finalLi) == 1:
				litsToExport.append( finalLi[0] )
			else:
				litsToExport.append( finalLi[1] )
		if litsToExport:
			mc.select( litsToExport, r=1, ne=1 )
			mc.file( self.lightPath.path, op="v=0", typ="mayaAscii", pr=1, es=1 )
			#export Light Linking
			self.exportLightLinking()

	def exportLightLinking(self):
		"""export all the lightlinking in the scene"""
		lights    = [a for a in mc.ls( typ = ['light','aiAreaLight'] ) if not 'eye' in a]
		allShapes = [s for s in mc.ls( type = 'geometryShape', ni = 1) if not (mc.objectType( s ) in ( 'aiAreaLight','aiSkyDomeLight' ))]
		litLinks  = {}
		for l in lights:
			lightLinkShapes = mc.lightlink( query=True, light=l ,shp=1,t=0,set=0,h=0)
			litLinks[l]	    = list( set( allShapes ) - set( lightLinkShapes ) )#SHAPES WITH NO LINK TO THIS LIGHT
		pickle.dump( litLinks, open( self.lightLinkPath.path, "wb" ) )

	def exportAovs(self):
		"""export aovs from scene"""
		aovs    = mc.ls( typ = 'aiAOV' )
		aovData = {}
		for a in aovs:
			aovData[a]            = {}
			aovData[a]['enabled'] = mc.getAttr( a + '.enabled' )
			aovData[a]['name']    = mc.getAttr( a + '.name'    )
			aovData[a]['type']    = mc.getAttr( a + '.type'    )
		pickle.dump( aovData, open( self.aovsPath.path, "wb" ) )

	def exportShaders(self):
		"""export custom shaders from scene, ex: shaders for masks etc..."""
		lays = rlayer.renderlayers()
		finalExport = []
		for l in lays:
			if l.name == 'defaultRenderLayer':
				continue
			if l.overridedShader:
				finalExport.append( l.overridedShader )
			else:
				if l.overridesWithConnections[1]:
					finalExport.extend( l.overridesWithConnections[1] )
		if finalExport:
			shadersToExport = []
			for i in finalExport:
				if mc.referenceQuery( i, inr = True ) or i in shadersToExport: #is a referenced node
					continue
				if mc.referenceQuery( i.a.surfaceShader.input, inr = True ): #check if shader is a reference
					continue
				if i.a.displacementShader.input:
					if mc.referenceQuery( i.a.displacementShader.input, inr = True ): #check if displacement is a reference
						continue
				shadersToExport.append( i )
			mc.select( shadersToExport, r = 1, ne = 1 )
			mc.file( self.shaderPath.path, op = "v=0", typ = "mayaAscii", pr = 1, es = 1 )

	#IMPORT
	def importAll(self, imdata = True, imlights = True, imaovs = True, imshaders = True, immaster = True, asset = '', searchAndReplace = ['',''] ):
		"""import all data into scene"""
		if immaster:
			self.importMasterSettings()
		if imlights and self.lightPath.exists:
			self.importLights( asset, searchAndReplace )
		if imaovs and self.aovsPath.exists:
			self.importAovs()
		if imshaders and self.shaderPath.exists:
			self.importShaders()
		if imdata and self.dataPath.exists:
			self.importData( asset, searchAndReplace )

	def importLights(self, asset = '', searchAndReplace = ['',''] ):
		"""import lights in scene"""
		if self.lightPath.exists:
			self.lightPath.imp()
			if self.lightLinkPath.exists:
				self.importLightLinking( asset, searchAndReplace )

	def importLightLinking(self, asset = '', searchAndReplace = ['',''] ):
		"""import light linking to lights"""
		LayersInfo = pickle.load( open( self.lightLinkPath.path, "rb") )
		mc.refresh( su = 1 )
		if not asset == '':
			LayersInfo = self.filterLightLinksData( LayersInfo , asset, searchAndReplace )
		for l in LayersInfo.keys():
			objsToBreakLink = []
			for link in LayersInfo[l]:
				if mc.objExists( link ):
					objsToBreakLink.append( link )
			mc.lightlink( b = True, light = l, o = objsToBreakLink )
		mc.refresh( su = 0 )

	def filterLightLinksData(self, LayersInfo , asset, sAr = ['',''] ):
		"""filter light linking data for the specific asset"""
		lightData = [(a.replace( sAr[0], sAr[1] ),LayersInfo[a].replace( sAr[0], sAr[1] )) for a in LayersInfo.keys() if asset in a]
		return dict( lightData )
	
	def importAovs(self):
		"""import aovs into scene"""
		LayersInfo = pickle.load( open( self.aovsPath.path, "rb") )
		mc.refresh( su = 1 )
		for ao in LayersInfo.keys():
			aov.create( ao, LayersInfo[ao]['name'], LayersInfo[ao]['type'], LayersInfo[ao]['enabled'] )
		mc.refresh( su = 0 )

	def importShaders(self):
		"""import shaders into scene"""
		if self.shaderPath.exists:
			self.shaderPath.imp()

	def importData( self, asset = '', searchAndReplace = ['',''] ):
		"""import data from file
		asset = Only import for the asset that you want
		searchAndReplace = Change any part of the objects name to another word"""
		pickleData = pickle.load( open( self.dataPath.path, "rb" ) )
		layers = [RenderLayerData(l,d) for l,d in pickleData.items() if not ':' in l]
		for l in layers:
			if not searchAndReplace [0]== '' or not searchAndReplace[1] == '':
				l.filterMe( asset, searchAndReplace )
			l.create()
			l.addObjects()
			l.makeOverrides()
			l.makeOverrideConnections()
			l.makeShaderOverride()

	def importMasterSettings(self):
		"""import master settings from data file"""
		pickleData = pickle.load( open( self.masterPath.path, "rb" ) )
		master = rlayer.RenderLayer( 'defaultRenderLayer' )
		master.makeCurrent()
		for a in pickleData.keys():
			try:
				a.v = pickleData[a]
			except:
				continue

class RenderLayerData(rlayer.RenderLayer):
	"""this is RenderLayerData object to handle the data from external files to create the render layer"""
	def __init__(self, name, data):
		super(RenderLayerData, self).__init__( name )
		self._objects   = data[ 'objects' ]
		self._overrides = data[ 'values'  ]
		self._overconns = data[ 'conns'   ]
		self._shader    = data[ 'shader'  ]

	@property
	def dataObjects(self):
		"""return the objects in the layer"""
		return self._objects

	@property
	def dataOverrides(self):
		"""return the overrides in the layer"""
		return self._overrides

	@property
	def dataOverconns(self):
		"""return the overrided connections"""
		return self._overconns

	@property
	def dataShader(self):
		"""return the overrided shader"""
		return self._shader

	def filterMe(self, asset = '', sAr = ['', ''] ):
		"""filter data based on asset name and searchAndReplace data"""
		if self._objects:
			self._objects = [ mn.Node( o.name.replace( sAr[0], sAr[1] ) ) for o in self._objects ]
		if self._overrides:
			self._overrides = dict( [ (mn.Node( a.name.replace( sAr[0], sAr[1] )), self._overrides[a] ) for a in self._overrides.keys() ] )
		if self._overconns:
			self._overconns = dict( [(mn.Node(a.name.replace( sAr[0], sAr[1] )), mn.Node(self._overconns[a].name.replace( sAr[0], sAr[1] ))) for a in self._overconns.keys() ] )

	def addObjects(self):
		"""docstring for addObjects"""
		if not self.dataObjects:
			return
		self.add( self.dataObjects )

	def makeOverrides(self):
		"""make the overrdies based on data"""
		self.overridesWithValues = self.dataOverrides

	def makeOverrideConnections(self):
		"""docstring for makeOverrideConnections"""
		self.overridesWithConnections = self.dataOverconns

	def makeShaderOverride(self):
		"""docstring for makeShaderOverride"""
		if self.dataShader:
			self.overridedShader = self.dataShader.a.surfaceShader.input.node
		


