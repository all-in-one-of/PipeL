import os

import general.ui.pySideHelper as uiH
reload( uiH )
uiH.set_qt_bindings()
from Qt import QtGui,QtCore

import subprocess
import ConfigParser
import pipe.project.project   as prj
reload( prj )
import pipe.project.projectUI as prjUi
reload( prjUi )
import pipe.asset.assetUI as assUi
reload( assUi )
import pipe.sets.setsUI as setUi
reload( setUi )
import pipe.file.file as fl
import pipe.mayaFile.mayaFilePropertiesUI as mfp
reload( mfp )
import pipe.mayaFile.mayaFile as mfl
reload( mfl )
import pipe.sequence.sequence as sq
reload( sq )
import pipe.sequence.sequenceUI as sqUI
reload( sqUI )
import pipe.shot.shotUI as shUI
reload( shUI )
INMAYA = False
try:
	import maya.cmds as mc
	INMAYA = True
except:
	pass

#load UI FILE
PYFILEDIR = os.path.dirname( os.path.abspath( __file__ ) )
MAYAPATH = 'C:/"Program Files"/Autodesk/Maya2013/bin/maya.exe'

uifile = PYFILEDIR + '/manager.ui'
fom, base = uiH.loadUiType( uifile )

settingsFile =  str( os.getenv('USERPROFILE') ) + '/settings.ini'


class ManagerUI(base,fom):
	"""manager ui class"""
	def __init__(self):
		if INMAYA:
			if uiH.USEPYQT:
				super(base, self).__init__(uiH.getMayaWindow())
			else:
				super(ManagerUI, self).__init__(uiH.getMayaWindow())
		else:
			if uiH.USEPYQT:
				super(base, self).__init__()
			else:
				super(ManagerUI, self).__init__()
		self.setupUi(self)
		self.loadProjectsPath()
		self.fillProjectsCombo()
		self.fillAssetsTable()
		self._makeConnections()
		self._loadConfig()
		self.assets_tw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.assets_tw.customContextMenuRequested.connect(self.showMenu)
		
		self.shots_tw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.shots_tw.customContextMenuRequested.connect(self.showMenu)

		self.sets_tw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.sets_tw.customContextMenuRequested.connect(self.showMenu)
		uiH.loadSkin( self, 'QTDarkGreen' )

	def loadProjectsPath(self):
		"""docstring for loadProjectsPath"""
		if not os.path.exists( settingsFile ):
			return
		Config = ConfigParser.ConfigParser()
		Config.read( settingsFile )
		if Config.has_section( "GeneralSettings" ):
			basePath = Config.get("GeneralSettings", "basepath")
			if basePath:
				prj.BASE_PATH = basePath

	def _loadConfig(self):
		"""load config settings"""
		if not os.path.exists( settingsFile ):
			return
		Config = ConfigParser.ConfigParser()
		Config.read( settingsFile )
		lastProject = Config.get("BaseSettings", "lastproject")
		lastProject = Config.get("BaseSettings", "lastproject")
		if lastProject:
			index = self.projects_cmb.findText( lastProject )
			if not index == -1:
				self.projects_cmb.setCurrentIndex(index)
		lastTab = Config.getint("BaseSettings", "lasttab")
		self.tabWidget.setCurrentIndex( lastTab )
		lastSequence = Config.get("BaseSettings", "lastsequence")
		if lastSequence:
			items = self.sequences_lw.findItems( lastSequence , QtCore.Qt.MatchExactly )
			if items:
				items[0].setSelected(True)
				if uiH.USEPYQT:
					self.sequences_lw.setItemSelected( items[0], True )
				self.sequences_lw.setCurrentItem( items[0] )
				self.sequences_lw.itemActivated.emit( items[0] )

	def _saveConfig(self):
		Config = ConfigParser.ConfigParser()
		Config.read( settingsFile )
		if not Config.has_section( 'BaseSettings' ):
			Config.add_section( 'BaseSettings' )
		lastTab = self.tabWidget.currentIndex()
		lastProj = str(self.projects_cmb.currentText())
		selItem = self.sequences_lw.selectedItems()
		lastSeq = ''
		if selItem:
			lastSeq = str( selItem[0].text() )
		Config.set( 'BaseSettings', 'lastproject', lastProj )
		Config.set( 'BaseSettings', 'lastSequence', lastSeq )
		Config.set( 'BaseSettings', 'lasttab', lastTab )
		with open( settingsFile, 'w' ) as cfgfile:
			Config.write(cfgfile)

	def setProjectsBasePath(self):
		"""select a base Path for the projects"""
		fil = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
		if fil:
			Config = ConfigParser.ConfigParser()
			Config.read( settingsFile )
			if not Config.has_section( 'GeneralSettings' ):
				Config.add_section( 'GeneralSettings' )
			Config.set( 'GeneralSettings', 'basepath', fil )
			with open( settingsFile, 'w' ) as cfgfile:
				print 'writing config file'
				Config.write(cfgfile)
			prj.BASE_PATH = fil
			self.fillProjectsCombo()
			self.updateUi()


	def _makeConnections(self):
		"""create the connections in the ui"""
		self.connect( self.refresh_btn            , QtCore.SIGNAL("clicked()") , self.updateUi )		
		QtCore.QObject.connect( self.projects_cmb, QtCore.SIGNAL( "currentIndexChanged( const QString& )" ), self.updateUi )
		QtCore.QObject.connect( self.projects_cmb, QtCore.SIGNAL( "currentIndexChanged( const QString& )" ), self.updateUi )
		QtCore.QObject.connect( self.projects_cmb, QtCore.SIGNAL( "currentIndexChanged( const QString& )" ),self.updateUi )
		QtCore.QObject.connect( self.actionNew_Project, QtCore.SIGNAL( "triggered()" ), self._newProject )
		QtCore.QObject.connect( self.actionNew_Asset, QtCore.SIGNAL( "triggered()" ), self._newAsset )
		QtCore.QObject.connect( self.actionNew_Set, QtCore.SIGNAL( "triggered()" ), self._newSet )
		QtCore.QObject.connect( self.actionNew_Sequence, QtCore.SIGNAL( "triggered()" ), self._newSequence )
		QtCore.QObject.connect( self.actionNew_Shot, QtCore.SIGNAL( "triggered()" ), self._newShot )
		QtCore.QObject.connect( self.actionCopy_Selected_From_Server, QtCore.SIGNAL( "triggered()" ), self.copySelectedAssetsFromServer )
		QtCore.QObject.connect( self.actionReference_Selected_Items, QtCore.SIGNAL( "triggered()" ), self.referenceSelected )
		QtCore.QObject.connect( self.actionSet_Projects_Path, QtCore.SIGNAL( "triggered()" ), self.setProjectsBasePath )
		QtCore.QObject.connect( self.sequences_lw, QtCore.SIGNAL( "itemClicked( QListWidgetItem* )" ), self.fillShotsTable )
		QtCore.QObject.connect( self.sequences_lw, QtCore.SIGNAL( "itemActivated( QListWidgetItem* )" ), self.fillShotsTable )
		QtCore.QObject.connect( self.sequences_lw, QtCore.SIGNAL( "itemPressed( QListWidgetItem* )" ), self.fillShotsTable )
		#TABLE SIGNALS
		QtCore.QObject.connect( self.sets_tw, QtCore.SIGNAL( "itemClicked (QTableWidgetItem *)" ), self.setStatusInfo )
		QtCore.QObject.connect( self.sets_tw, QtCore.SIGNAL( "itemDoubleClicked (QTableWidgetItem *)" ), self.openFile )
		QtCore.QObject.connect( self.assets_tw, QtCore.SIGNAL( "itemDoubleClicked (QTableWidgetItem *)" ), self.openFile )
		QtCore.QObject.connect( self.assets_tw, QtCore.SIGNAL( "itemClicked (QTableWidgetItem *)" ), self.setStatusInfo )
		QtCore.QObject.connect( self.shots_tw, QtCore.SIGNAL( "itemDoubleClicked (QTableWidgetItem *)" ), self.openFile )
		QtCore.QObject.connect( self.shots_tw, QtCore.SIGNAL( "itemClicked (QTableWidgetItem *)" ), self.setStatusInfo )
		#SERVER SIGNALS
		QtCore.QObject.connect( self.compareServer_chb, QtCore.SIGNAL( "stateChanged  (int)" ), self.updateUi )
		#search signals
		QtCore.QObject.connect( self.search_asset_le, QtCore.SIGNAL( "textEdited (const QString&)" ), self.searchAsset )
		QtCore.QObject.connect( self.search_shot_le, QtCore.SIGNAL( "textEdited (const QString&)" ), self.searchShot )

	def updateUi(self):
		"""update ui"""
		self.fillAssetsTable()
		self.fillSequenceList()
		self.fillSetTable()

	def searchShot(self, fil):
		"""search asset based on line edit string"""
		#fil = self.search_asset_le.text()
		for i in range( self.shots_tw.rowCount() ):
			match = False
			item = self.shots_tw.item( i, 0 )
			if item.text().contains(fil):
				match = True
			self.shots_tw.setRowHidden( i, not match )

	def searchAsset(self, fil):
		"""search asset based on line edit string"""
		#fil = self.search_asset_le.text()
		for i in range( self.assets_tw.rowCount() ):
			match = False
			for j in range( self.assets_tw.columnCount() ):
				item = self.assets_tw.item( i, j )
				if item.text().contains(fil):
					match = True
					break
			self.assets_tw.setRowHidden( i, not match )

	def fillProjectsCombo(self):
		"""fill projects combo with projects in local disc"""
		self.projects_cmb.clear()
		self.projects_cmb.addItems( prj.projects() )

	def fillAssetsTable(self):
		"""fill the table with the assets in the project"""
		proj = prj.Project( str( self.projects_cmb.currentText()) )
		if not proj.name:
			return
		assets = proj.assets
		self.assets_tw.setRowCount( len( assets ) )
		color = [QtGui.QColor( "grey" ),
				QtGui.QColor( "green" ),
				QtGui.QColor( "red" )]
		if not assets:
			return
		serverPath = self.serverPath_le.text()
		for i,a in enumerate( assets ):
			item = QtGui.QTableWidgetItem( a.name )
			#item.setFlags(QtCore.Qt.ItemIsEnabled)
			item.setCheckState(QtCore.Qt.Unchecked )
			item.setData(32, a )
			self.assets_tw.setItem( i, 0, item )
			files = [
				a.modelPath,
				a.shadingPath,
				a.rigPath,
				a.hairPath,
				a.finalPath
				]
			status = a.status
			if self.compareServer_chb.isChecked(): #SERVER MODE ON
				for v,f in enumerate(files):
					item = QtGui.QTableWidgetItem( f.date )
					#item.setFlags(QtCore.Qt.ItemIsEnabled)
					item.setCheckState(QtCore.Qt.Unchecked )
					item.setData(32, f )
					filePath = str( f.path )
					serverFile = fl.File( filePath.replace( prj.BASE_PATH, serverPath ) )
					if status[v] == 0:
						item.setText( '' )
					stat = status[v]
					if serverFile.exists and f.exists:
						if not serverFile.isZero:
							if f.isOlderThan( serverFile ):
								item.setText( f.date + '||' + serverFile.date )
								stat = -1
							else:
								stat = 1
						elif f.isZero:
							stat = 0
						else:
							stat = 1
					if uiH.USEPYQT:
						item.setBackgroundColor( color[ stat ])
					else:
						item.setBackground( color[ stat ] )
					self.assets_tw.setItem( i, v + 1, item )
			else:
				for v,f in enumerate(files):
					if f.exists:
						item = QtGui.QTableWidgetItem( f.date )
					else:
						item = QtGui.QTableWidgetItem( 'Not Exists!' )
					#item.setFlags(QtCore.Qt.ItemIsEnabled)
					item.setCheckState(QtCore.Qt.Unchecked )
					item.setData(32, f )
					if status[v] == 0:
						item.setText( '' )
					if uiH.USEPYQT:
						item.setBackgroundColor( color[ status[v] ])
					else:
						item.setBackground( color[ status[v] ] )
					self.assets_tw.setItem( i, v + 1, item )

	def fillSequenceList(self):
		"""fill list of sequence"""
		proj = prj.Project( self.projects_cmb.currentText() )
		if not proj.name:
			return
		self.sequences_lw.clear()
		self.shots_tw.clearContents()
		seqs = proj.sequences
		if not seqs:
			return
		self.sequences_lw.addItems( [s.name for s in seqs ])
		
	def fillShotsTable(self):
		"""fill the tables with the shots of the selected sequence"""
		proj      = prj.Project( str( self.projects_cmb.currentText() ))
		sequence  = sq.Sequence( str( self.sequences_lw.selectedItems()[0].text() ), proj )
		self.shots_tw.setRowCount( len( sequence.shots ) )
		color = [QtGui.QColor( "grey" ),
				QtGui.QColor( "green" ),
				QtGui.QColor( "red" )]
		serverPath = self.serverPath_le.text()
		for i,s in enumerate( sequence.shots ):
			item = QtGui.QTableWidgetItem( s.name )
			item.setCheckState(QtCore.Qt.Unchecked )
			item.setData(32, s )
			self.shots_tw.setItem( i, 0, item )
			files = [
				s.layPath,
				s.animPath,
				s.hrsPath,
				s.vfxPath,
				s.simPath,
				s.litPath,
				s.compPath
				]
			status = s.status
			if self.compareServer_chb.isChecked(): #SERVER MODE ON
				for v,f in enumerate(files):
					item = QtGui.QTableWidgetItem( f.date )
					item.setCheckState(QtCore.Qt.Unchecked )
					item.setData(32, f )
					filePath = str( f.path )
					serverFile = fl.File( filePath.replace( prj.BASE_PATH, serverPath ) )
					if status[v] == 0:
						item.setText( '' )
					stat = status[v]
					if serverFile.exists and f.exists:
						if not serverFile.isZero:
							if f.isOlderThan( serverFile ):
								item.setText( f.date + '||' + serverFile.date )
								stat = -1
							else:
								stat = 1
						elif f.isZero:
							stat = 0
						else:
							stat = 1
					if uiH.USEPYQT:
						item.setBackgroundColor( color[ stat ])
					else:
						item.setBackground( color[ stat ] )
					self.shots_tw.setItem( i, v + 1, item )
			else:
				for v,f in enumerate(files):
					if f.exists:
						item = QtGui.QTableWidgetItem( f.date )
					else:
						item = QtGui.QTableWidgetItem( 'Not Exists' )
					item.setCheckState(QtCore.Qt.Unchecked )
					item.setData(32, f )
					if status[v] == 0:
						item.setText( '' )
					if uiH.USEPYQT:
						item.setBackgroundColor( color[ status[v] ])
					else:
						item.setBackground( color[ status[v] ] )
					self.shots_tw.setItem( i, v + 1, item )

	def fillSetTable(self):
		"""fill the table of the sets"""
		proj = prj.Project( str( self.projects_cmb.currentText()) )
		if not proj.name:
			return
		sets = proj.sets
		self.sets_tw.setRowCount( len( sets ) )
		color = [QtGui.QColor( "grey" ),
				QtGui.QColor( "green" ),
				QtGui.QColor( "red" )]
		if not sets:
			return
		serverPath = self.serverPath_le.text()
		for i,a in enumerate( sets ):
			item = QtGui.QTableWidgetItem( a.name )
			item.setCheckState(QtCore.Qt.Unchecked )
			self.sets_tw.setItem( i, 0, item )
			item.setData(32, a )
			files = [
				a.modelPath,
				a.finalPath
				]
			status = a.status
			if self.compareServer_chb.isChecked(): #SERVER MODE ON
				for v,f in enumerate(files):
					item = QtGui.QTableWidgetItem( f.date )
					item.setCheckState(QtCore.Qt.Unchecked )
					item.setData(32, f )
					filePath = str( f.path )
					serverFile = fl.File( filePath.replace( prj.BASE_PATH, serverPath ) )
					if status[v] == 0:
						item.setText( '' )
					stat = status[v]
					if serverFile.exists and f.exists:
						if not serverFile.isZero:
							if f.isOlderThan( serverFile ):
								item.setText( f.date + '||' + serverFile.date )
								stat = -1
							else:
								stat = 1
						elif f.isZero:
							stat = 0
						else:
							stat = 1
					if uiH.USEPYQT:
						item.setBackgroundColor( color[ stat ])
					else:
						item.setBackground( color[ stat ] )
					self.sets_tw.setItem( i, v + 1, item )
			else:
				for v,f in enumerate(files):
					item = QtGui.QTableWidgetItem( f.date )
					item.setCheckState(QtCore.Qt.Unchecked )
					item.setData(32, f )
					if status[v] == 0:
						item.setText( '' )
					if uiH.USEPYQT:
						item.setBackgroundColor( color[ status[v] ])
					else:
						item.setBackground( color[ status[v] ] )
					self.sets_tw.setItem( i, v + 1, item )

	def _newProject(self):
		"""create new project ui"""
		dia = prjUi.ProjectCreator()
		res = dia.exec_()
		if res:
			self.fillProjectsCombo()

	def _newAsset(self):
		"""creates new Asset"""
		dia = assUi.AssetCreator()
		dia.show()
		index = self.projects_cmb.currentIndex()
		dia.projects_cmb.setCurrentIndex(index)
		res = dia.exec_()
		if res:
			self.fillAssetsTable()

	def _newSet(self):
		"""create a new set"""
		dia = setUi.SetCreator()
		dia.show()
		index = self.projects_cmb.currentIndex()
		dia.projects_cmb.setCurrentIndex(index)
		res = dia.exec_()
		if res:
			self.fillSetTable()

	def _newSequence(self):
		"""creates a new sequence"""
		dia = sqUI.SequenceCreator()
		dia.show()
		index = self.projects_cmb.currentIndex()
		dia.projects_cmb.setCurrentIndex(index)
		res = dia.exec_()
		if res:
			self.fillSequenceList()

	def _newShot(self):
		"""creates a new Shot"""
		dia = shUI.ShotCreator( self.projects_cmb.currentText(), self.sequences_lw.selectedItems()[0].text() )
		dia.show()
		index = self.projects_cmb.currentIndex()
		dia.projects_cmb.setCurrentIndex(index)
		res = dia.exec_()
		if res:
			self.fillShotsTable()

	def openFile(self,item):
		"""open selected Asset"""
		#item = self.assets_tw.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		os.system("start "+ str( asset.path ) )
		self.setStatusBarMessage( str( asset.path ) )
		#os.popen( MAYAPATH + ' ' + str( asset.path ))

	def setStatusInfo(self, item):
		"""set the status bar message based on item selected from table"""
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		self.setStatusBarMessage( str( asset.path ) )

	def showMenu(self, pos):
		menu=QtGui.QMenu(self)
		actionProperties = QtGui.QAction("Properties", menu)
		menu.addAction( actionProperties )
		self.connect( actionProperties, QtCore.SIGNAL( "triggered()" ), self.properties )
		actionOpenInExplorer = QtGui.QAction("Open File in explorer", menu)
		menu.addAction( actionOpenInExplorer )
		self.connect( actionOpenInExplorer, QtCore.SIGNAL( "triggered()" ), self.openFileLocation )
		if INMAYA:
			#COPY TIME SETTINGS
			actionCopyTime = QtGui.QAction("Copy Time Settings", menu)
			menu.addAction( actionCopyTime )
			self.connect( actionCopyTime, QtCore.SIGNAL( "triggered()" ), self.copyTimeSettings )
			menu.addSeparator()
			#REFERENCE
			actionReference = QtGui.QAction("Reference", menu)
			menu.addAction( actionReference )
			self.connect( actionReference, QtCore.SIGNAL( "triggered()" ), self.reference )
			#IMPORT
			actionImport = QtGui.QAction("Import", menu)
			menu.addAction( actionImport )
			self.connect( actionImport, QtCore.SIGNAL( "triggered()" ), self.importFile )
			#OPEN IN CURRENT MAYA
			actionOpenInCurrent = QtGui.QAction("Open in This Maya", menu)
			menu.addAction( actionOpenInCurrent )
			self.connect( actionOpenInCurrent, QtCore.SIGNAL( "triggered()" ), self.openFileInCurrentMaya )
			#SAVE IN THIS SCENE
			actionSaveScene = QtGui.QAction("Save Scene Here!", menu)
			menu.addAction( actionSaveScene )
			self.connect( actionSaveScene, QtCore.SIGNAL( "triggered()" ), self.saveScene )

		#actionCopyServer = QtGui.QAction("Copy From Server", menu)
		#menu.addAction(actionCopyServer)
		#self.connect( actionCopyServer, QtCore.SIGNAL( "triggered()" ), self.copyFromServer )
		tabwid = self._getCurrentTab()
		menu.popup(tabwid.viewport().mapToGlobal(pos))

	def openFileLocation(self):
		"""openFile in explorer"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		subprocess.Popen(r'explorer /select,"'+ asset.path.replace( '/','\\' ) +'"')

	def saveScene(self):
		"""save scene here"""
		quit_msg = "Are you sure you want to save in this file?"
		reply = QtGui.QMessageBox.question(self, 'Message', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			tab = self._getCurrentTab()
			item = tab.currentItem()
			if uiH.USEPYQT:
				asset = item.data(32).toPyObject()
			else:
				asset = item.data(32)
			print asset.name
			asset.newVersion()
			asset.save()

	def openFileInCurrentMaya(self):
		"""docstring for openFileInCurrentMaya"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		asset.open()

	def importFile(self):
		"""import file to current Maya"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		asset.imp()
		

	def _getCurrentTab(self):
		"""return the visible table in the ui"""
		currentTab = self.tabWidget.currentIndex()
		if currentTab == 0:
			tabwid = self.assets_tw
		elif currentTab == 1:
			tabwid = self.sets_tw
		elif currentTab == 2:
			tabwid = self.shots_tw
		return tabwid

	def copyTimeSettings(self):
		"""copy time settings from selected scene"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		tim = asset.time
		mc.currentUnit( time=tim['tim'], linear = tim['lin'], angle = tim[ 'angle' ] )
		mc.playbackOptions( min = tim[ 'min' ],
							ast = tim[ 'ast' ], 
							max = tim[ 'max' ], 
							aet = tim[ 'aet' ] )

	def reference(self):
		"""reference file into scene"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		asset.reference()

	def referenceSelected(self):
		"""reference selected items"""
		for a in self._getSelectedItemsInCurrentTab():
			a.reference()
		
	def properties(self):
		"""get ui with properties of asset"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		props = mfp.MayaFilePropertiesUi(asset,self)
		props.show()

	def copyFromServer(self):
		"""copy selected asset from serrver"""
		serverPath = self.serverPath_le.text()
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		self.copyAssetFromServer( asset )
		self.updateUi()


	def _getSelectedItemsInCurrentTab(self):
		"""return the selected assets in current Tab"""
		tab = self._getCurrentTab()
		assets = []
		for r in range( tab.rowCount() ):
			for c in range( tab.columnCount() ):
				item = tab.item( r, c )
				if item.checkState() == 2:
					if uiH.USEPYQT:
						asset = item.data(32).toPyObject()
					else:
						asset = item.data(32)
					assets.append(asset)
		return assets

	def copySelectedAssetsFromServer(self):
		"""copy all the assets from server"""
		assets = self._getSelectedItemsInCurrentTab()
		serverPath = self.serverPath_le.text()
		for a in assets:
			self.copyAssetFromServer( a )
		self.updateUi()

	def copyAssetFromServer(self, asset):
		"""main function to copy asset from server"""
		serverPath = self.serverPath_le.text()
		filePath = str( asset.path )
		if asset.path.endswith( '.ma' ):# MAYA FILE
			#COPY TEXTURES AND REFERENCES RECURSIVE
			serverFile = mfl.mayaFile( filePath.replace( prj.BASE_PATH, serverPath ) )
			serverFile.copy( str( asset.path ))
		else:
			serverFile = fl.File( filePath.replace( prj.BASE_PATH, serverPath ) )
			serverFile.copy( str( asset.path ))

	def setStatusBarMessage(self, message):
		"""docstring for setStatusBarMessage"""
		self.statusbar.showMessage( message )

	def closeEvent(self, event):
		self._saveConfig()

	

def main():
	global PyForm
	PyForm=ManagerUI()
	PyForm.show()


if __name__=="__main__":
	import sys
	a = QtGui.QApplication(sys.argv)
	global PyForm
	a.setStyle('plastique')
	PyForm=ManagerUI()
	PyForm.show()
	sys.exit(a.exec_())
		
