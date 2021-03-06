import os

import general.ui.pySideHelper as uiH
reload( uiH )

from Qt import QtGui,QtCore

import pyqt.threadCopy.threadCopy as trhC
reload( trhC )

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
reload( fl )
import pipe.mayaFile.mayaFilePropertiesUI as mfp
reload( mfp )
import pipe.nukeFile.nukeFilePropertiesUI as nkp
reload( nkp )
import pipe.mayaFile.mayaFile as mfl
reload( mfl )
import pipe.sequence.sequence as sq
reload( sq )
import pipe.sequence.sequenceUI as sqUI
reload( sqUI )
import pipe.shot.shot as sh
reload( sh )
import pipe.shot.shotUI as shUI
reload( shUI )
import pipe.settings.settings as sti
reload( sti )
import pipe.settings.settingsUi as stiUi
reload( stiUi )
import pipe.textureFile.textureFile as tfl
reload( tfl )
import pipe.task.taskUi as tskUi
reload(tskUi)
import pipe.materialDist.materialDist as mtlDist
reload( mtlDist )
from sys import platform as _platform
import subprocess

INMAYA = False
try:
	import maya.cmds as mc
	INMAYA = True
except:
	pass
INNUKE = False
try:
	import nuke
	INNUKE = True
except:
	pass

INHOU = False
try:
	import hou
	import pipe.houdiniFile.houdiniFile as hfl
	import pipe.houdiniFile.houdiniNewFile as hflNew
	reload(hflNew )
	reload( hfl )
	INHOU = True
except:
	pass

#load UI FILE
try:
    PYFILEDIR = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    import sys
    PYFILEDIR = os.path.dirname(os.path.abspath(sys.argv[0]))

uifile = PYFILEDIR + '/manager.ui'
fom, base = uiH.loadUiType( uifile )


class ManagerUI(base,fom):
	"""manager ui class"""
	def __init__(self, parent = uiH.getMayaWindow() ):
		if INMAYA:
			if uiH.USEPYQT:
				super(base, self).__init__(parent)
			else:
				super(ManagerUI, self).__init__(parent)
		else:
			if uiH.USEPYQT:
				super(base, self).__init__(parent)
			else:
				super(ManagerUI, self).__init__(parent)
		self.setupUi(self)
		self.serverPath = ''
		self.settings = sti.Settings()
		if not self.settings.exists:
			self.loadSettingsUi()
		self.changeInternalPaths = False
		self.autoMakeTx = False
		self.loadProjectsPath()
		self.fillProjectsCombo()
		self.fillAssetsTable()
		self._makeConnections()
		self.loadTaksUi()
		self._loadConfig()
		self.serverHelp_wg.hide()
		self.assets_tw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.assets_tw.customContextMenuRequested.connect(self.showMenu)

		self.shots_tw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.shots_tw.customContextMenuRequested.connect(self.showMenu)
		self.setObjectName( 'ManagerUI' )

	def loadTaksUi(self):
		"""docstring for loadTaksUi"""
		self.taskUi = tskUi.TasksUi( str( self.projects_cmb.currentText()), None )
		self.tasks_lay.addWidget( self.taskUi )

	###################################
	#LOAD SETTINGS
	def loadProjectsPath(self):
		"""docstring for loadProjectsPath"""
		gen = self.settings.General
		if gen:
			basePath = gen[ "basepath" ]
			if basePath:
				if basePath.endswith( '\\' ):
					basePath = basePath[:-1]
				prj.BASE_PATH = basePath.replace( '\\', '/' )
			serverPath = gen[ "serverpath" ]
			if serverPath:
				self.serverPath = serverPath
			useMayaSubFolder = gen[ "usemayasubfolder" ]
			if useMayaSubFolder == 'True':
				prj.USE_MAYA_SUBFOLDER = True
			else:
				prj.USE_MAYA_SUBFOLDER = False
			changeInternalPaths = gen[ "changeinternalpaths" ]
			if useMayaSubFolder == 'True':
				self.changeInternalPaths = True
			if gen.has_key( 'automaketx' ):
				autoMakeTx = gen[ "automaketx" ]
				if autoMakeTx == 'True':
					self.autoMakeTx = True
			skin = gen[ "skin" ]
			if skin:
				uiH.loadSkin( self, skin )

	def _loadConfig(self):
		"""load config settings"""
		his = self.settings.History
		if his:
			if 'lastproject' in his:
				lastProject = his[ "lastproject" ]
				if lastProject:
					index = self.projects_cmb.findText( lastProject )
					if not index == -1:
						self.projects_cmb.setCurrentIndex(index)
						self.updateUi()
			if 'lasttab' in his:
				lastTab = his[ "lasttab" ]
				self.tabWidget.setCurrentIndex( int( lastTab ))
			if 'lastsequence' in his:
				lastSequence = his[ "lastsequence" ]
				if lastSequence:
					items = self.sequences_lw.findItems( lastSequence , QtCore.Qt.MatchExactly )
					if items:
						items[0].setSelected(True)
						if uiH.USEPYQT:
							self.sequences_lw.setItemSelected( items[0], True )
						self.sequences_lw.setCurrentItem( items[0] )
						self.sequences_lw.itemActivated.emit( items[0] )
			if 'lastusernote' in his:
				lastusernote = his[ 'lastusernote' ]
				self.taskUi.setUserNote( lastusernote )
		self._loadHistoryFiles()

	def _loadHistoryFiles(self):
		"""docstring for _loadHistoryFiles"""
		his = self.settings.History
		if his:
			self.menuHistory.clear()
			if "lastfiles" in his:
				lastFiles = his[ "lastfiles" ]
				for l in lastFiles.split( ',' ):
					if l:
						self.addFileToHistoryMenu( l )

	def _saveConfig(self):
		lastTab = self.tabWidget.currentIndex()
		lastProj = str(self.projects_cmb.currentText())
		selItem = self.sequences_lw.selectedItems()
		lastSeq = ''
		if selItem:
			lastSeq = str( selItem[0].text() )
		lastUserNote = self.taskUi.currentUserNote
		self.settings.write( 'History', 'lastproject', lastProj )
		self.settings.write( 'History', 'lastSequence', lastSeq )
		self.settings.write( 'History', 'lasttab', lastTab )
		self.settings.write( 'History', 'lastusernote', lastUserNote  )

	def setProjectsBasePath(self):
		"""select a base Path for the projects"""
		fil = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
		if fil:
			self.settings.write( 'General', 'basepath', fil )
			prj.BASE_PATH = fil
			self.fillProjectsCombo()
			self.updateUi()

	def loadMaterialDist(self):
		"""docstring for fname"""
		setUi = mtlDist.MaterailDist( self )
		setUi.show()
		res = setUi.exec_()

	def loadSettingsUi(self):
		"""docstring for fname"""
		setUi = stiUi.Settings( self )
		setUi.show()
		res = setUi.exec_()
		if res:
			self.loadProjectsPath()
			self.updateFullUi()
			self._loadConfig()
	#
	###################################
	#UI STUFF
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

	def _getCurrentTab(self):
		"""return the visible table in the ui"""
		currentTab = self.tabWidget.currentIndex()
		if currentTab == 0:
			tabwid = self.assets_tw
		elif currentTab == 1:
			tabwid = self.shots_tw
		return tabwid

	def _makeConnections(self):
		"""create the connections in the ui"""
		self.connect( self.refresh_btn            , QtCore.SIGNAL("clicked()") , self.updateUi )
		self.connect( self.matDist_btn            , QtCore.SIGNAL("clicked()") , self.loadMaterialDist )
		QtCore.QObject.connect( self.projects_cmb, QtCore.SIGNAL( "activated( const QString& )" ), self.updateUi )
		QtCore.QObject.connect( self.actionNew_Project, QtCore.SIGNAL( "triggered()" ), self._newProject )
		QtCore.QObject.connect( self.actionNew_Asset, QtCore.SIGNAL( "triggered()" ), self._newAsset )
		QtCore.QObject.connect( self.actionNew_Sequence, QtCore.SIGNAL( "triggered()" ), self._newSequence )
		QtCore.QObject.connect( self.actionNew_Shot, QtCore.SIGNAL( "triggered()" ), self._newShot )
		QtCore.QObject.connect( self.actionCopy_Selected_From_Server, QtCore.SIGNAL( "triggered()" ), self.copySelectedAssetsFromServer )
		QtCore.QObject.connect( self.actionGlobal_Settings, QtCore.SIGNAL( "triggered()" ), self.loadSettingsUi )
		QtCore.QObject.connect( self.actionReference_Selected_Items, QtCore.SIGNAL( "triggered()" ), self.referenceSelected )
		QtCore.QObject.connect( self.actionSet_Projects_Path, QtCore.SIGNAL( "triggered()" ), self.setProjectsBasePath )
		QtCore.QObject.connect( self.sequences_lw, QtCore.SIGNAL( "itemClicked( QListWidgetItem* )" ), self.fillShotsTable )
		QtCore.QObject.connect( self.sequences_lw, QtCore.SIGNAL( "itemActivated( QListWidgetItem* )" ), self.fillShotsTable )
		QtCore.QObject.connect( self.sequences_lw, QtCore.SIGNAL( "itemPressed( QListWidgetItem* )" ), self.fillShotsTable )
		#TABLE SIGNALS
		QtCore.QObject.connect( self.assets_tw, QtCore.SIGNAL( "itemDoubleClicked (QTableWidgetItem *)" ), self.openFile )
		QtCore.QObject.connect( self.assets_tw, QtCore.SIGNAL( "itemClicked (QTableWidgetItem *)" ), self.setStatusInfo )
		QtCore.QObject.connect( self.shots_tw, QtCore.SIGNAL( "itemDoubleClicked (QTableWidgetItem *)" ), self.openFile )
		QtCore.QObject.connect( self.shots_tw, QtCore.SIGNAL( "itemClicked (QTableWidgetItem *)" ), self.setStatusInfo )
		#SERVER SIGNALS
		QtCore.QObject.connect( self.compareServer_chb, QtCore.SIGNAL( "stateChanged  (int)" ), self.updateFullUi )
		#search signals
		QtCore.QObject.connect( self.search_asset_le, QtCore.SIGNAL( "textEdited (const QString&)" ), self.searchAsset )
		QtCore.QObject.connect( self.search_shot_le, QtCore.SIGNAL( "textEdited (const QString&)" ), self.searchShot )

	def setStatusInfo(self, item):
		"""set the status bar message based on item selected from table"""
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		self.setStatusBarMessage( str( asset.path ) )

	def searchShot(self, fil):
		"""search asset based on line edit string"""
		#fil = self.search_asset_le.text()
		for i in range( self.shots_tw.rowCount() ):
			match = False
			item = self.shots_tw.item( i, 0 )
			if fil.lower() in str( item.text() ).lower():
				match = True
			self.shots_tw.setRowHidden( i, not match )

	def showMenu(self, pos):
		tabwid = self._getCurrentTab()
		item = tabwid.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		menu=QtGui.QMenu(self)
		if INHOU:
			fils = menu.addMenu('Files')
			nukIcon = QtGui.QIcon( PYFILEDIR + '/icons/houdini.png' )
			actionNewFile = QtGui.QAction(nukIcon,"New File", fils)
			fils.addAction( actionNewFile )
			self.connect( actionNewFile, QtCore.SIGNAL( "triggered()" ), self.newHoudiniFile )
			fils.addSeparator()
			#OPEN IN CURRENT NUKE
			fls = [ hfl.houdiniFile( a.path ) for a in fl.filesInDir( asset.dirPath, False ) if a.path.endswith('.hip')]
			for f in fls:
				nukIcon = QtGui.QIcon( PYFILEDIR + '/icons/houdini.png' )
				actionOpenInCurrent = QtGui.QAction(nukIcon,f.name, fils)
				fils.addAction( actionOpenInCurrent )
				self.connect( actionOpenInCurrent, QtCore.SIGNAL( "triggered()" ), lambda val = f : self.openHoudiniFile(val) )
		propIcon = QtGui.QIcon( PYFILEDIR + '/icons/question.png' )
		actionProperties = QtGui.QAction(propIcon, "Properties", menu)
		menu.addAction( actionProperties )
		self.connect( actionProperties, QtCore.SIGNAL( "triggered()" ), self.properties )
		folderIcon = QtGui.QIcon( PYFILEDIR + '/icons/folder.png' )
		actionOpenInExplorer = QtGui.QAction(folderIcon,"Open File in explorer", menu)
		menu.addAction( actionOpenInExplorer )
		self.connect( actionOpenInExplorer, QtCore.SIGNAL( "triggered()" ), self.openFileLocation )
		#COPY PATH
		actionSaveScene = QtGui.QAction("Copy File Path", menu)
		menu.addAction( actionSaveScene )
		self.connect( actionSaveScene, QtCore.SIGNAL( "triggered()" ), self.copyFilePath )
		#OPEN RENDER PATH
		actionSaveScene = QtGui.QAction(folderIcon,"Open Render Folder", menu)
		menu.addAction( actionSaveScene )
		self.connect( actionSaveScene, QtCore.SIGNAL( "triggered()" ), self.openRenderFolder )
		#OPEN RENDER PATH
		videoIcon = QtGui.QIcon( PYFILEDIR + '/icons/video.png' )
		actionOpenPlayblast = QtGui.QAction(videoIcon,"Open Playblast", menu)
		menu.addAction( actionOpenPlayblast )
		self.connect( actionOpenPlayblast, QtCore.SIGNAL( "triggered()" ), self.openPlayblast )
		menu.addSeparator()
		#DOWNLOAD UPLOAD
		downIcon = QtGui.QIcon( PYFILEDIR + '/icons/download.png' )
		uploIcon = QtGui.QIcon( PYFILEDIR + '/icons/upload.png' )
		actionCopyServer = QtGui.QAction( downIcon, "Download From Server", menu)
		actionCopyServer.setIcon( downIcon )
		menu.addAction(actionCopyServer)
		self.connect( actionCopyServer, QtCore.SIGNAL( "triggered()" ), self.copyFromServer )
		actionToServer = QtGui.QAction( uploIcon, "Upload To Server", menu)
		menu.addAction(actionToServer)
		self.connect( actionToServer, QtCore.SIGNAL( "triggered()" ), self.copyToServer )
		menu.addSeparator()
		if INMAYA:
			fils = menu.addMenu('Versions')
			#OPEN IN CURRENT NUKE
			fls = [ mfl.mayaFile( a.path ) for a in fl.filesInDir( asset.dirPath+'/Versions/', False ) if a.path.endswith('.ma')]
			for f in fls:
				nukIcon = QtGui.QIcon( PYFILEDIR + '/icons/maya.png' )
				actionOpenInCurrent = QtGui.QAction(nukIcon,f.name + ' - ' + f.date, fils)
				fils.addAction( actionOpenInCurrent )
				self.connect( actionOpenInCurrent, QtCore.SIGNAL( "triggered()" ), lambda val = f : self.openMayaFile(val) )
			#OPEN IN CURRENT MAYA
			mayaIcon = QtGui.QIcon( PYFILEDIR + '/icons/maya.png' )
			actionOpenInCurrent = QtGui.QAction(mayaIcon,"Open in This Maya", menu)
			menu.addAction( actionOpenInCurrent )
			self.connect( actionOpenInCurrent, QtCore.SIGNAL( "triggered()" ), self.openFileInCurrentMaya )
			menu.addSeparator()
			#IMPORT
			impIcon = QtGui.QIcon( PYFILEDIR + '/icons/import.png' )
			actionImport = QtGui.QAction(impIcon,"Import", menu)
			menu.addAction( actionImport )
			self.connect( actionImport, QtCore.SIGNAL( "triggered()" ), self.importFile )
			menu.addSeparator()
			#COPY TIME SETTINGS
			timeIcon = QtGui.QIcon( PYFILEDIR + '/icons/time.png' )
			actionCopyTime = QtGui.QAction(timeIcon,"Copy Time Settings", menu)
			menu.addAction( actionCopyTime )
			self.connect( actionCopyTime, QtCore.SIGNAL( "triggered()" ), self.copyTimeSettings )
			menu.addSeparator()
			#REFERENCE
			refIcon = QtGui.QIcon( PYFILEDIR + '/icons/reference.png' )
			actionReference = QtGui.QAction(refIcon,"Reference", menu)
			menu.addAction( actionReference )
			self.connect( actionReference, QtCore.SIGNAL( "triggered()" ), self.reference )
			menu.addSeparator()
			#SAVE IN THIS SCENE
			savIcon = QtGui.QIcon( PYFILEDIR + '/icons/save.png' )
			actionSaveScene = QtGui.QAction(savIcon,"Save Scene Here!", menu)
			menu.addAction( actionSaveScene )
			self.connect( actionSaveScene, QtCore.SIGNAL( "triggered()" ), self.saveScene )
		elif INNUKE:
			#OPEN IN CURRENT NUKE
			nukIcon = QtGui.QIcon( PYFILEDIR + '/icons/nuke.png' )
			actionOpenInCurrent = QtGui.QAction(nukIcon,"Open in This Nuke", menu)
			menu.addAction( actionOpenInCurrent )
			self.connect( actionOpenInCurrent, QtCore.SIGNAL( "triggered()" ), self.openFileInCurrentNuke )
			#SAVE IN THIS SCENE
			savIcon = QtGui.QIcon( PYFILEDIR + '/icons/save.png' )
			actionSaveScene = QtGui.QAction(savIcon,"Save Scene Here!", menu)
			menu.addAction( actionSaveScene )
			self.connect( actionSaveScene, QtCore.SIGNAL( "triggered()" ), self.saveNukeScene )


		menu.popup(tabwid.viewport().mapToGlobal(pos))

	def openHoudiniFile(self, fil):
		"""open houdini File in current Scene"""
		fil.open()

	def openMayaFile(self, fil):
		if fil.isZero:
			mc.file( new = True, force = True )
			fil.save()
		else:
			fil.open()


	def newHoudiniFile(self):
		"""docstring for fname"""
		tabwid = self._getCurrentTab()
		item = tabwid.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		dia = hflNew.HoudiniNewFile( asset, self )
		dia.show()
		res = dia.exec_()

	def searchAsset(self, fil):
		"""search asset based on line edit string"""
		#fil = self.search_asset_le.text()
		for i in range( self.assets_tw.rowCount() ):
			match = False
			for j in range( self.assets_tw.columnCount() ):
				item = self.assets_tw.item( i, j )
				if fil.lower() in str( item.text() ).lower():
					match = True
					break
			self.assets_tw.setRowHidden( i, not match )

	def setStatusBarMessage(self, message):
		"""docstring for setStatusBarMessage"""
		self.statusbar.showMessage( message )

	def closeEvent(self, event):
		self._saveConfig()

	def dragEnterEvent(self, event):
		event.acceptProposedAction()


	#
	###################################
	#FILL UI
	def updateUi(self):
		"""update ui"""
		self.updateTaksUi()
		if str( self.projects_cmb.currentText()) == 'All':
			self.tabWidget.setTabEnabled(0, False);
			self.tabWidget.setTabEnabled(1, False);
		else:
			self.tabWidget.setTabEnabled(0, True);
			self.tabWidget.setTabEnabled(1, True);
			self.fillAssetsTable()
			self.fillSequenceList()

	def updateTaksUi(self):
		"""docstring for fname"""
		self.taskUi.project = str( self.projects_cmb.currentText())
		self.taskUi.refresh()

	def updateFullUi(self):
		"""docstring for updateFullUi"""
		self.fillProjectsCombo()
		self.fillAssetsTable()
		self.fillSequenceList()

	def fillProjectsCombo(self):
		"""fill projects combo with projects in local disc"""
		lastProj = str(self.projects_cmb.currentText())
		self.projects_cmb.clear()
		localProjects = prj.projects( prj.BASE_PATH )
		projects = []
		if self.compareServer_chb.isChecked(): #SERVER MODE ON
			serverProjects = prj.projects( self.serverPath )
			for s in serverProjects:
				if any( l == s for l in localProjects ):
					continue
				projects.append( s )
		projects.extend( localProjects )
		self.projects_cmb.addItems( ['All'] + projects )
		index = self.projects_cmb.findText( lastProj )
		if not index == -1:
			self.projects_cmb.setCurrentIndex(index)

	def fillAssetsTable(self):
		"""fill the table with the assets in the project"""
		proj = prj.Project( str( self.projects_cmb.currentText()), prj.BASE_PATH )
		if not proj.name:
			return
		assets = proj.assets
		color = [QtGui.QColor( "#CACAD4" ),
				QtGui.QColor( "green" ),
				QtGui.QColor( "red" ),
				QtGui.QColor( "#000000" )    #FILE NOT EXISTS
				]
		serverComColor = [QtGui.QColor( "#CACAD4" ), #BOTH IN ZERO
						QtGui.QColor( "#00CC00" ),   #BOTH IN SINCRO
						QtGui.QColor( "#FF0000" ),   #NEEDS DOWNLOAD
						QtGui.QColor( "#CC66FF" ),   #NEEDS UPLOAD
						QtGui.QColor( "#000000" )    #FILE NOT EXISTS
						]
		if self.compareServer_chb.isChecked(): #SERVER MODE ON
			serverProj = prj.Project( str( self.projects_cmb.currentText()), self.serverPath )
			serverAssets = serverProj.assets
			finalAssets = []
			for a in serverAssets:
				if any( b.name == a.name for b in assets ):
					continue
				finalAssets.append( a )
			assets.extend( finalAssets )
		self.assets_tw.setRowCount( len( assets ) )
		self.assets_tw.setColumnWidth( 0, 200 )
		if not assets:
			return
		for i,a in enumerate( assets ):
			item = QtGui.QTableWidgetItem( a.name )
			#item.setFlags(QtCore.Qt.ItemIsEnabled)
			item.setCheckState(QtCore.Qt.Unchecked )
			item.setData(32, a )
			if a.hasPreviewImage:
				imagePath = a.previewImagePath.path
			else:
				imagePath = PYFILEDIR + '/icons/no_Preview.jpg'
			item.setData(QtCore.Qt.DecorationRole, QtGui.QPixmap( imagePath ).scaled(56, 56, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation));
			self.assets_tw.setItem( i, 0, item )
			files = [
				a.modelPath,
				a.shadingPath,
				a.hairPath,
				a.rigPath,
				a.finalPath
				]
			if self.compareServer_chb.isChecked(): #SERVER MODE ON
				for v,f in enumerate(files):
					if f.exists:
						item = QtGui.QTableWidgetItem( f.date )
					else:
						item = QtGui.QTableWidgetItem( 'No Exists' )
					item.setCheckState(QtCore.Qt.Unchecked )
					item.setData(32, f )
					filePath = str( f.path )
					stat = 0
					if self.serverPath in f.path:                                      # THIS FILE IS ONLY ON SERVER
						if f.exists:
							stat = 2
							if f.isZero:
								stat = 0
						else:
							stat = 4
					else:
						serverFile = fl.File( filePath.replace( prj.BASE_PATH + '/', self.serverPath ) )
						if not serverFile.exists and f.exists:                    # LOCAL EXISTS SERVER NOT
							stat = 3
							if f.isZero:
								stat = 0
						elif serverFile.exists and not f.exists:
							stat = 2
							if serverFile.isZero:
								stat = 0
						elif serverFile.exists and f.exists:
							if serverFile.isZero and f.isZero:                      # BOTH ARE ZERO
								stat = 0
							else:
								if f.isOlderThan( serverFile ):                     # LOCAL OLDER THAN SERVER
									item.setText( f.date + '||' + serverFile.date )
									stat = 2
								elif serverFile.isOlderThan( f ):                   # SERVER OLDER THAN LOCAL
									item.setText( f.date + '||' + serverFile.date )
									stat = 3
								else:                                               # BOTH IN SINCRO
									stat = 1
						else:
							stat = 4                                                # FILE NOT EXISTS!
					if uiH.USEPYQT:
						item.setBackgroundColor( serverComColor[ stat ])
					else:
						item.setBackground( serverComColor[ stat ] )
					self.assets_tw.setItem( i, v + 1, item )
			else:
				status = a.status
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
		proj = prj.Project( str( self.projects_cmb.currentText() ), prj.BASE_PATH )
		if not proj.name:
			return
		self.sequences_lw.clear()
		self.shots_tw.clearContents()
		seqs = proj.sequences
		if self.compareServer_chb.isChecked(): #SERVER MODE ON
			serverProj = prj.Project( str( self.projects_cmb.currentText()), self.serverPath )
			finalSeqs = []
			for s in serverProj.sequences:
				if any( s.name == b.name for b in seqs ):
					continue
				finalSeqs.append( s )
			seqs.extend( finalSeqs )
		if not seqs:
			return
		self.sequences_lw.addItems( [s.name for s in seqs ])

	def fillShotsTable(self):
		"""fill the tables with the shots of the selected sequence"""
		proj = prj.Project( str( self.projects_cmb.currentText()), prj.BASE_PATH )
		sequence  = sq.Sequence( str( self.sequences_lw.selectedItems()[0].text() ), proj )
		shots = sequence.shots
		color = [QtGui.QColor( "grey" ),
				QtGui.QColor( "green" ),
				QtGui.QColor( "#FF0000" ),
				QtGui.QColor( "#000000" )    #FILE NOT EXISTS
				]
		serverComColor = [QtGui.QColor( "#CACAD4" ), #BOTH IN ZERO
						QtGui.QColor( "#00CC00" ),   #BOTH IN SINCRO
						QtGui.QColor( "#FF0000" ),   #NEEDS DOWNLOAD
						QtGui.QColor( "#CC66FF" ),   #NEEDS UPLOAD
						QtGui.QColor( "#000000" )    #FILE NOT EXISTS
						]
		if self.compareServer_chb.isChecked(): #SERVER MODE ON
			serverProj = prj.Project( str( self.projects_cmb.currentText()), self.serverPath )
			serverSequence  = sq.Sequence( str( self.sequences_lw.selectedItems()[0].text() ), serverProj )
			serverShots = serverSequence.shots
			finalShots = []
			for a in serverShots:
				if any( b.name == a.name for b in shots ):
					continue
				finalShots.append( a )
			shots.extend( finalShots )
		self.shots_tw.setRowCount( len( shots ) )
		shots = sorted(shots, key=lambda s: s.name[s.name.index('_')+1:])
		for i,s in enumerate( shots ):
			item = QtGui.QTableWidgetItem( s.name )
			item.setCheckState(QtCore.Qt.Unchecked )
			item.setData(32, s )
			self.shots_tw.setItem( i, 0, item )
			files = [ #THIS MUST HAVE THE ORDER OF THE TABLE COLUMNS
				s.layPath,
				s.animPath,
				s.skinFixPath,
				s.hrsPath,
				s.vfxPath,
				s.simPath,
				s.litPath,
				s.compPath
				]
			status = s.status
			if self.compareServer_chb.isChecked(): #SERVER MODE ON
				for v,f in enumerate(files):
					if f.exists:
						item = QtGui.QTableWidgetItem( f.date )
					else:
						item = QtGui.QTableWidgetItem( 'No Exists' )
					item.setCheckState(QtCore.Qt.Unchecked )
					item.setData(32, f )
					filePath = str( f.path )
					stat = 0
					if self.serverPath in f.path:                                      # THIS FILE IS ONLY ON SERVER
						if f.exists:
							stat = 2
							if f.isZero:
								stat = 0
						else:
							stat = 4
					else:
						serverFile = fl.File( filePath.replace( prj.BASE_PATH + '/', self.serverPath ) )
						if not serverFile.exists and f.exists:                    # LOCAL EXISTS SERVER NOT
							stat = 3
						elif serverFile.exists and not f.exists:
							stat = 2
							if serverFile.isZero:
								stat = 0
						elif serverFile.exists and f.exists:
							if serverFile.isZero and f.isZero:                      # BOTH ARE ZERO
								stat = 0
							else:
								if f.isOlderThan( serverFile ):                     # LOCAL OLDER THAN SERVER
									item.setText( f.date + '||' + serverFile.date )
									stat = 2
								elif serverFile.isOlderThan( f ):                   # SERVER OLDER THAN LOCAL
									item.setText( f.date + '||' + serverFile.date )
									stat = 3
								else:                                               # BOTH IN SINCRO
									stat = 1
						else:
							stat = 4                                                # FILE NOT EXISTS!
					if uiH.USEPYQT:
						item.setBackgroundColor( serverComColor[ stat ])
					else:
						item.setBackground( serverComColor[ stat ] )
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

	#
	###################################
	#CREATE
	def _newProject(self):
		"""create new project ui"""
		dia = prjUi.ProjectCreator(self)
		res = dia.exec_()
		if res:
			self.fillProjectsCombo()

	def _newAsset(self):
		"""creates new Asset"""
		dia = assUi.AssetCreator( self )
		dia.show()
		index = dia.projects_cmb.findText( str( self.projects_cmb.currentText()) )
		if not index == -1:
			dia.projects_cmb.setCurrentIndex(index)
		res = dia.exec_()
		if res:
			self.fillAssetsTable()

	def _newSequence(self):
		"""creates a new sequence"""
		dia = sqUI.SequenceCreator(self)
		dia.show()
		index = dia.projects_cmb.findText( str( self.projects_cmb.currentText()) )
		if not index == -1:
			dia.projects_cmb.setCurrentIndex(index)
		res = dia.exec_()
		if res:
			self.fillSequenceList()

	def _newShot(self):
		"""creates a new Shot"""
		dia = shUI.ShotCreator( self.projects_cmb.currentText(), self.sequences_lw.selectedItems()[0].text(), self )
		dia.show()
		index = dia.projects_cmb.findText( str( self.projects_cmb.currentText()) )
		if not index == -1:
			dia.projects_cmb.setCurrentIndex(index)
		res = dia.exec_()
		if res:
			self.fillShotsTable()

	#
	###################################
	#HISTORY
	def addFileToHistory(self, asset):
		"""docstring for addFileToHistory"""
		#ADD TO HISTORY opened FILE
		his = self.settings.History
		lastFiles = ''
		if his:
			if "lastfiles" in his:
				savedFiles = his[ "lastfiles" ]
				savedFiles = savedFiles.replace( asset.path + ',', '' )
				historyCount = 10
				for a in savedFiles.split( ',' ):
					if historyCount == 0:
						break
					if not a:
						continue
					lastFiles += a + ','
					historyCount -= 1
		self.settings.write( 'History', 'lastfiles', asset.path + ',' + lastFiles )
		self._loadHistoryFiles()

	def addFileToHistoryMenu(self, path):
		"""docstring for addFileToHistoryMenu"""
		asset = mfl.mayaFile( path )
		actionOpenHistory = QtGui.QAction( asset.path, self.menuHistory )
		self.menuHistory.addAction( actionOpenHistory )
		self.connect( actionOpenHistory, QtCore.SIGNAL( "triggered()" ), lambda val = asset : self.openHistoryFile(val) )

	def openHistoryFile(self, asset):
		"""docstring for openHistoryFile"""
		self.addFileToHistory( asset )
		asset.open()

	#
	###################################
	#
	def copyFilePath(self):
		"""docstring for copyFilePath"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		command = 'echo ' + asset.path + '| clip'
		os.popen(command)

	def openPlayblast(self):
		"""docstring for fname"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		os.system("start "+ str( asset.path.replace( '.ma', '.mov' ) ) )

	def openFile(self,item):
		"""open selected Asset"""
		#item = self.assets_tw.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		os.system("start "+ str( asset.path ) )
		self.addFileToHistory( asset )
		self.setStatusBarMessage( str( asset.path ) )
		#os.popen( MAYAPATH + ' ' + str( asset.path ))

	def openFileLocation(self):
		"""openFile in explorer"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		if _platform == 'win32':
			subprocess.Popen(r'explorer /select,"'+ asset.path.replace( '/','\\' ) +'"')
		else:
			subprocess.Popen(['nautilus',asset.path])

	def openFileInCurrentMaya(self):
		"""docstring for openFileInCurrentMaya"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		self.addFileToHistory( asset )
		if asset.isZero:
			mc.file( new = True, force = True )
			asset.save()
		else:
			asset.open()

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

	def openRenderFolder(self):
		"""docstring for openRenderFolder"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		assOrShot = prj.shotOrAssetFromFile( asset )
		if assOrShot:
			if assOrShot.type == 'asset':
				#versionNumber = self._getVersionNumber( renderPath + assOrShot.project.name + '/Asset/' + assOrShot.name )
				pat = self.settings.General[ 'renderpath' ] + assOrShot.project.name + '/Asset/' + assOrShot.name + '/'
			elif assOrShot.type == 'shot':
				#R:\Pony_Halloween_Fantasmas\Terror\s013_T13\Chicos_Beauty
				#versionNumber = self._getVersionNumber( renderPath + assOrShot.project.name + '/' + assOrShot.sequence.name + '/' + assOrShot.name )
				pat =  self.settings.General[ 'renderpath' ] + assOrShot.project.name + '/' + assOrShot.sequence.name + '/' + assOrShot.name + '/'
			subprocess.Popen(r'explorer "'+ pat.replace( '/','\\' ) +'"')


	def importFile(self):
		"""import file to current Maya"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		asset.imp()

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
		#TODO HERE WE NEED TO DETECT IF WE ARE IN A SHOT
		gen = self.settings.General
		assetPerShot = gen[ "useassetspershot" ]
		if assetPerShot == 'True':
			shotSel = prj.shotOrAssetFromFile( mfl.currentFile() )
			#assetspath + assetname + department + file
			newFil = asset.copy( shotSel.assetsPath + asset.path.split( 'Assets/' )[-1] )
			newFil.reference()
		else:
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
		if asset.extension == '.ma':
			props = mfp.MayaFilePropertiesUi(asset,self, False )
		elif asset.extension == '.nk':
			props = nkp.NukeFilePropertiesUi(asset,self, False)
		props.show()

	def openFileInCurrentNuke(self):
		"""docstring for openFileInCurrentNuke"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		root = nuke.root()
		if not root.knob( 'pipPorject' ):
			pipProj = nuke.String_Knob( 'pipPorject', 'Project' )
			root.addKnob( pipProj )
		if not root.knob( 'pipSequence' ):
			pipSeq = nuke.String_Knob( 'pipSequence', 'Sequence' )
			root.addKnob( pipSeq )
		if not root.knob( 'pipShot' ):
			pipShot = nuke.String_Knob( 'pipShot', 'Shot' )
			root.addKnob( pipShot )
		root[ 'pipPorject' ].setValue( str( self.projects_cmb.currentText() ) )
		root[ 'pipSequence' ].setValue( str( self.sequences_lw.selectedItems()[0].text() ) )
		row = item.row()
		root[ 'pipShot' ].setValue( tab.item ( row, 0 ).text() )
		if asset.isZero:
			root[ 'name' ].setValue( asset.path )
		else:
			asset.open()

	def saveNukeScene(self):
		"""docstring for saveNukeScene"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		asset.newVersion()
		asset.save()

	#
	###################################
	#SERVER/LOCAL
	def copyFromServer(self):
		"""copy selected asset from server"""
		tab = self._getCurrentTab()
		item = tab.currentItem()
		if uiH.USEPYQT:
			asset = item.data(32).toPyObject()
		else:
			asset = item.data(32)
		self.copyAssetFromServer( asset )
		self.updateUi()

	def copyToServer(self):
		"""copy selected asset to server"""
		quit_msg = "Are you sure you want to copy this file to SERVER?"
		reply = QtGui.QMessageBox.question(self, 'Message', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			tab = self._getCurrentTab()
			item = tab.currentItem()
			if uiH.USEPYQT:
				asset = item.data(32).toPyObject()
			else:
				asset = item.data(32)
			self.copyAssetToServer( asset )
			self.updateUi()

	def copySelectedAssetsFromServer(self):
		"""copy all the assets from server"""
		assets = self._getSelectedItemsInCurrentTab()
		for a in assets:
			self.copyAssetFromServer( a )
		self.updateUi()

	def copyAssetFromServer(self, asset):
		"""main function to copy asset from server"""
		filePath = str( asset.path )
		if asset.path.endswith( '.ma' ):# MAYA FILE
			#COPY TEXTURES AND REFERENCES RECURSIVE
			if self.serverPath in filePath:
				localFile = mfl.mayaFile( filePath.replace( self.serverPath, prj.BASE_PATH + '/' ) )
				localFile.newVersion()
				asset.copy( localFile.path )
				if self.changeInternalPaths:
					print 'in changeInternalPaths'
					deps, textures = self.getDependenciesToCopy( localFile )
					self.changeIntPaths( [localFile.path ], self.serverPath, prj.BASE_PATH + '/' )
					toCopy = self.filesToCopy( deps, self.serverPath, prj.BASE_PATH + '/' )
					if toCopy:
						print toCopy
					"""
						dia = trhC.MultiProgressDialog( toCopy, self.serverPath, prj.BASE_PATH + '/', self )
						dia.show()
						res = dia.exec_()
						if res:
							self.changeIntPaths( toCopy, self.serverPath, prj.BASE_PATH + '/' )
							if self.autoMakeTx:
								for t in textures:
									self.makeTxForTexture( t, self.serverPath, prj.BASE_PATH + '/' )
					"""
			else:
				serverFile = mfl.mayaFile( filePath.replace( prj.BASE_PATH + '/', self.serverPath ) )
				asset.newVersion()
				serverFile.copy( asset.path )
				if self.changeInternalPaths:
					deps, textures = self.getDependenciesToCopy( asset )
					self.changeIntPaths( [asset.path ], self.serverPath, prj.BASE_PATH + '/' )
					toCopy = self.filesToCopy( deps, self.serverPath, prj.BASE_PATH + '/' )
					if toCopy:
						dia = trhC.MultiProgressDialog( toCopy, self.serverPath, prj.BASE_PATH + '/', self )
						dia.show()
						res = dia.exec_()
						if res:
							self.changeIntPaths( toCopy, self.serverPath, prj.BASE_PATH + '/' )
							if self.autoMakeTx:
								for t in textures:
									self.makeTxForTexture( t, self.serverPath, prj.BASE_PATH + '/' )
		else:
			if self.serverPath in filePath:
				localFile = fl.File( filePath.replace( self.serverPath, prj.BASE_PATH + '/' ) )
				localFile.newVersion()
				asset.copy( str( localFile.path ))
			else:
				localFile = fl.File( filePath.replace( prj.BASE_PATH + '/', self.serverPath ) )
				asset.newVersion()
				localFile.copy( str( asset.path ))

	def changeIntPaths( self, files, serverPath, localPath ):
		"""docstring for changeIntPaths"""
		for f in files:
			if not f.endswith( '.ma' ):
				continue
			localFile = mfl.mayaFile( f.replace( serverPath, localPath ) )
			stinfo = os.stat( localFile.path )
			localFile.changePathsBrutForce( srchAndRep =  [ serverPath, localPath ] )
			os.utime( localFile.path,(stinfo.st_atime, stinfo.st_mtime))

	def copySelectedAssetsToServer(self):
		"""copy all the assets from server"""
		assets = self._getSelectedItemsInCurrentTab()
		for a in assets:
			self.copyAssetToServer( a )
		self.updateUi()

	def filesToCopy(self, fils, serverPath, localPath):
		"""return files that really need to be copied to local or if they allready exists"""
		filesToC = []
		for f in fils:
			if not f.exists:
				continue
			fToCopy = fl.File( f.path.replace( serverPath, localPath ) )
			if fToCopy.path in filesToC:
				continue
			if fToCopy.exists:
				if not fToCopy.isOlderThan( f ):
					continue
			filesToC.append( f.path )
		return filesToC

	def getDependenciesToCopy(self, asset):
		"""return the textures, reference and caches from file"""
		result = []
		refs = asset.allReferences()
		textures = asset.textures
		for r in refs:
			textures.extend( r.textures )
		finalTextures = []
		for t in textures:
			if t.hasUdim:
				finalTextures.extend( t.udimPaths )
			else:
				finalTextures.append( t )
		caches = asset.caches
		result.extend( refs )
		result.extend( textures )
		result.extend( caches )
		return result, textures

	def copyAssetToServer(self, asset):
		"""main function to copy asset to server"""
		filePath = str( asset.path )
		if asset.path.endswith( '.ma' ):# MAYA FILE
			#COPY TEXTURES AND REFERENCES RECURSIVE
			if self.serverPath in filePath: #THIS FILE ONLY EXISTS IN SERVER SO THERE IS NO NEED
				return
			else:
				serverFile = mfl.mayaFile( filePath.replace( prj.BASE_PATH + '/', self.serverPath ) )
				serverFile.newVersion()
				asset.copy( serverFile.path )
				if self.changeInternalPaths:
					deps, textures = self.getDependenciesToCopy( asset )
					self.changeIntPaths( [asset.path ], prj.BASE_PATH + '/', self.serverPath )
					toCopy = self.filesToCopy( deps,  prj.BASE_PATH + '/', self.serverPath )
					if toCopy:
						dia = trhC.MultiProgressDialog( toCopy, prj.BASE_PATH + '/', self.serverPath, self )
						dia.show()
						res = dia.exec_()
						if res and self.changeInternalPaths:
							self.changeIntPaths( toCopy, prj.BASE_PATH + '/', self.serverPath )
							if self.autoMakeTx:
								for t in textures:
									self.makeTxForTexture( t, prj.BASE_PATH + '/', self.serverPath )

		else:
			if self.serverPath in filePath: #THIS FILE ONLY EXISTS IN SERVER SO THERE IS NO NEED
				return
			else:
				localFile = fl.File( filePath.replace( prj.BASE_PATH + '/', self.serverPath ) )
				asset.copy( str( localFile.path ))

	def makeTxForTexture(self, texture, serverPath, localPath  ):
		newTextFile = tfl.textureFile( texture.path.replace( serverPath, localPath ) )
		newTextFile.makeTx()
	#
	###################################
	#

def main():
	if INMAYA:
		if mc.window( 'ManagerUI', q = 1, ex = 1 ):
			mc.deleteUI( 'ManagerUI' )
	global PyForm
	PyForm=ManagerUI(parent=QtGui.QApplication.activeWindow())
	PyForm.show()

if __name__=="__main__":
	import sys
	a = QtGui.QApplication(sys.argv)
	global PyForm
	a.setStyle('plastique')
	PyForm=ManagerUI()
	PyForm.show()
	sys.exit(a.exec_())

