import os
import general.ui.pySideHelper as uiH
reload( uiH )
uiH.set_qt_bindings()
from Qt import QtGui,QtCore

import maya.cmds as mc

import pipe.database.database as db
reload( db )

PYFILEDIR = os.path.dirname( os.path.abspath( __file__ ) )

uifile = PYFILEDIR + '/tasks.ui'
fom, base = uiH.loadUiType( uifile )

uiTaskfile = PYFILEDIR + '/TaskWidget.ui'
fomTask, baseTask = uiH.loadUiType( uiTaskfile )

uiNotefile = PYFILEDIR + '/NoteWidget.ui'
fomNote, baseNote = uiH.loadUiType( uiNotefile )

class TasksUi(base, fom):
	def __init__(self,projectName, parent  = uiH.getMayaWindow() ):
		if uiH.USEPYQT:
			super(base, self).__init__(parent)
		else:
			super(TasksUi, self).__init__(parent)
		self.setupUi(self)
		self.setObjectName( 'TasksUi' )
		self.project = projectName
		self.userName = None
		self.fillUsers()
		self.fillTasks()
		self.fillStatus()
		self._makeConnections()
		self.currentTask = None

	def fillUsers(self):
		"""docstring for fillUsers"""
		self.users_cmb.clear()
		self.users_cmb.addItems( db.ProjectDataBase( self.project ).getUsers() )

	def fillStatus(self):
		"""docstring for fillStatus"""
		its = { 'waitingStart':'Waiting to Start', 'ready':'Ready to Start', 'inProgress':'In Progress', 'omit':'Omit', 'paused':'Paused', 'pendingReview':'Pending Review', 'final':'Final' }
		for i in sorted( its.keys() ):
			icon = QtGui.QIcon( PYFILEDIR + '/icons/' + i + '.png' )
			self.taskStatus_cmb.addItem( icon, its[i] )

	def _makeConnections(self):
		"""docstring for _makeConnections"""
		QtCore.QObject.connect( self.task_lw, QtCore.SIGNAL( "itemClicked( QListWidgetItem* )" ), self.updateTaskDataUi )
		QtCore.QObject.connect( self.users_cmb, QtCore.SIGNAL( "currentIndexChanged( const QString& )" ), self.fillTasks )
		QtCore.QObject.connect( self.taskStatus_cmb, QtCore.SIGNAL( "currentIndexChanged( const QString& )" ), self.changeTaskStatus )
		self.connect( self.addNote_btn             , QtCore.SIGNAL("clicked()") , self.addNote )

	@property
	def currentUser(self):
		"""docstring for currentUser"""
		return str ( self.users_cmb.currentText() )

	def addNote(self):
		"""add note to currentTask"""
		if not self.currentTask:
			return
		self.currentTask.addNote( db.ProjectDataBase( self.project ), str( self.note_te.toPlainText()), self.currentUser, self.currentTask.name, self.currentTask.area, self.currentTask.seq)
		self.updateNotes()
		self.note_te.clear()

	def fillTasks(self):
		"""fill tasks for project and user"""
		self.task_lw.clear()
		dataBase = db.ProjectDataBase( self.project )
		if not self.currentUser:
			return
		for a in dataBase.getAssetsForUser( self.currentUser ):
			itemN = QtGui.QListWidgetItem()
			itemN.setData(32, a )
			itemN.setSizeHint(QtCore.QSize(200,70));
			self.task_lw.addItem( itemN )
			self.task_lw.setItemWidget(itemN, TaskUi( a ) )

	def updateTaskDataUi(self):
		item = self.task_lw.selectedItems()[0]
		if uiH.USEPYQT:
			taskItem = item.data(32).toPyObject()
		else:
			taskItem = item.data(32)
		self.currentTask = taskItem
		self.priority_val_lbl.setText( str( taskItem.priority ) )
		self.startDate_lbl.setText( taskItem.timeStart )
		self.endDate_lbl.setText( taskItem.timeEnd )
		self.taskName_lbl.setText( taskItem.fullname )
		its = [ 'Waiting to Start', 'Ready to Start', 'In Progress', 'Omit', 'Paused', 'Pending Review', 'Final' ]
		index = self.taskStatus_cmb.findText( its[ taskItem.status ] )
		if not index == -1:
			self.taskStatus_cmb.setCurrentIndex(index)
		self.updateNotes()
		
	def updateNotes(self):
		if not self.currentTask:
			return
		self.note_lw.clear()
		for n in self.currentTask.notes(db.ProjectDataBase( self.project )):
			itemN = QtGui.QListWidgetItem()
			itemN.setData(32, n )
			itemN.setSizeHint(QtCore.QSize(200,70))
			self.note_lw.addItem( itemN )
			self.note_lw.setItemWidget(itemN, NoteUi( n ) )

	def changeTaskStatus(self):
		"""docstring for fname"""


class TaskUi(baseTask, fomTask):
	def __init__(self, task ):
		if uiH.USEPYQT:
			super(baseTask, self).__init__()
		else:
			super(TaskUi, self).__init__()
		self.setupUi(self)
		self.taskName_lbl.setText( task.fullname )
		self.date_lbl.setText( task.timeStart + ' - ' + task.timeEnd )
		self.priority_lbl.setText( str( task.priority ) )
		iconsNames = [ 'waitingStart', 'ready', 'inProgress', 'omit', 'paused', 'pendingReview', 'final' ]
		statusIcon = QtGui.QPixmap( PYFILEDIR + '/icons/' + iconsNames[ task.status ] + '.png' )
		self.status_lbl.setPixmap(statusIcon);


class NoteUi(baseNote, fomNote):
	def __init__(self, note ):
		if uiH.USEPYQT:
			super(baseNote, self).__init__()
		else:
			super(NoteUi, self).__init__()
		self.setupUi(self)
		self.userName_lbl.setText( note.user )
		self.note_lbl.setText( note.note )
		self.noteDate_lbl.setText( note.date )

def main(projectName):
	"""use this to create project in maya"""
	if mc.window( 'TasksUi', q = 1, ex = 1 ):
		mc.deleteUI( 'TasksUi' )
	PyForm=TasksUi(projectName)
	PyForm.show()

"""
import pipe.task.taskUi as tskUi
reload(tskUi)
tskUi.main( 'Catsup_Tobogan' )
"""