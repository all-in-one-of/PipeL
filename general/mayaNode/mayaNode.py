'''
File: mayaNodes.py
Author: Ignacio Urruty
Description: Handle maya nodes in a more easy way..

How to Use:
Global Methods:
	ls() # return a list of nodes

Nodes:
	node = mn.Node( 'pSpehere1' ) # create node
	Properties:
		node.name                       # return name of node
		node.name = 'newName'           # rename node
		node.exists                     # node Exists?
		node.fullname                   # return a string with the fullname of the node |group1|group2|node
		node.parent                     # return the directly parent node
		node.parent = node2             # set new parent for node if None is node2 then parent to world, also support strings
		node.allparent                  # return an array of all the parent nodes in order
		node.children                   # return all the children of the node
		node.locked = True              # lock node
		v = node.locked                 # return if the node is locked
		node.type                       # node type
		node.namespace                  # return namespace of object if there is one
		node.namespace = newNameSpace   # move node to new namespace, it will create it if not exists
		node.namespace = 'newNameSpace' # move node to new namespace string, it will create it if not exists

	Methods:
		node()                # select node
		node.delete()         # delete node
		node.duplicate()      # duplicate and return a new Node object
		node.istype( 'type' ) # check if the node is a specific type

	TODO:
		node.inputs      # get incomming connections to node
		node.outputs     # get outcomming connections to node
		node.isinstance
		node.isreference

Attributes:
	att = node.a.tx
	att = node.attr( 'tx' )      # setAttr USEFULL for loops when you need to set many attrs
	Properties:
		node.a.tx.node               # get Node
		node.a.tx.v = 10             # setAttr
		node.a.t.v = ( 0.5, 10, 20 ) # setAttr for attributes with children
		node.a.myString.v = 'Hello'  # setAttr for strings also supported =)
		node.a.tx.v += 5             # setAttr Add value tu current, also works with -*/
		v = node.a.tx.v              # getAttr
		node.a.tx.exists             # node attribute Exists?
		node.a.t.children            # In this case return tx, ty and tz
		node.a.tx.type               # attribute type
		node.a.tx.locked = True      # set lock state for node attribute
		v = node.a.tx.locked         # get lock state for node attribute
		v = node.a.tx.max            # get max value if this attr has, None if not
		node.a.tx.max = 10           # set max value
		v = node.a.tx.min            # get min value if this attr has, None if not
		node.a.tx.min = 10           # set min value
		v = node.a.tx.default        # get default value
		node.a.tx.default = 10       # set default value
		node.a.tx.overrided = True   # create an override
		node.a.tx.overrided = False  # remove an override
		v = node.a.tx.overrided      # know if the attribute has an override in current render layer
	Methods:
		node.a.tx.delete()           # delete node attribute
		node.a.custom.add( dataType = None, attributeType = None ) # add a custom attr =)

	Connections:
		Properties:
			node.a.tx.input                        # get input connection to attribute
			node.a.tx.output                       # get output connections to attribute, this allways return an array
			node.a.tx.hascon                       # check if the node attribute has a connection
		Methods:
			node.a.tx >> node2.a.ty                # connectAttr of node to node2
			node.a.tx.connect( node2.a.ty )        # connectAttr of node to node2
			node.a.tx << node2.a.ty                # connectAttr inverse
			node.a.tx.connect( node2.a.ty, False ) # connectAttr inverse
			node.a.tx // node2.a.ty                # disconnectAttr of node to node2
			node.a.tx.disconnect( node2.a.ty )     # disconnectAttr of node to node2
			node.a.tx.disconnect()                 # also support to just break the connection, this will disconnect if this has an input connection
			node.a.tx | node2.a.ty                 # isConnected ? USE THE PIPE
			node.a.tx.isconnected( node2.a.ty )    # isConnected

	TODO:
		node.a.tx.key              # make a key in current frame

Namespace:
	n = Namespace( 'lit' ) # Namespace node
	Properties:
		n.exists        # check if namespace exists
		n.children      # get children namespaces
		n.nodes         # return the nodes that are in the namespace
		n.parent        # get parent of namespace
		n.isempty       # check if namespace is empty
	Methods:
		n.create()      # create namespace if not exists
		n.set()         # set namespace to current
		n.move( other ) # move all the node of namespace to other namespace
		n >> other      # move all the node of namespace to other namespace using >>
		n.remove()      # remove namespace

		Statics:
			Namespace.fromNode( Node ) # return Namespace from Node
			TODO:
				Namespace.all() # return al Namespaces

'''

try:
	import maya.cmds as mc
except:
	print 'running from outside maya'
import re

"""
SETTINGS:
	Here we can setup some global settings =)
"""
AUTO_CREATE_NAMESPACE    = True  # create namespace if not exists when you try to set to current
FORCE_CONNECTION         = True  # automatically break connection if there is one that you want to connect
AUTO_UNLOCK_ATTR         = False # automatically unlock attribute for connections or for setting value
AUTO_OVERRIDE_ATTR       = False # automatically override attribute if you set it in a renderLayer different than default

def ls( strToSearch = None, **args ):
	"""return a list of Nodes"""
	cmd = ''
	if strToSearch:
		cmd += '"' + strToSearch + '",'
	for a in args.keys():
		val = args[a]
		if isinstance(val, str):
			cmd += a + '="' + args[a] + '",'
		else:
			cmd += a + '=' + str( args[a] ) + ','
	nodes = eval( "mc.ls(" + cmd + ")" )
	if nodes:
		return [ Node(n) for n in nodes ]


class Node(object):
	"""base class to handle maya nodes more easy"""
	def __init__(self, name ):
		self._name = name

	def __str__(self):
		return self._name

	def __repr__(self):
		return self._name

	def __call__(self):
		"""select node when you call it =)"""
		if not self.exists:
			raise NodeNotFound( self._name )
		mc.select( self._name )

	@property
	def name(self):
		"""return name of node"""
		return self._name

	@name.setter
	def name(self, newName ):
		"""rename object"""
		if not self.exists:
			raise NodeNotFound( self._name )
		self._name = mc.rename( self.name, newName )

	@property
	def fullname(self):
		"""return the FullName of the node, if not exists return False"""
		if not self.exists:
			raise NodeNotFound( self._name )
		return mc.ls( '*' + self._name, l = True )[0]

	@property
	def parent(self):
		"""return the parent of the node"""
		if not self.exists:
			raise NodeNotFound( self._name )
		p = mc.listRelatives( self._name, p = True )
		if p:
			return Node( p[0] )
		else:
			return None

	@parent.setter
	def parent(self, newParent):
		"""set a new parent for node, supports string and Node, if newParent = None, set to world"""
		if not self.exists:
			raise NodeNotFound( self.name )
		if not newParent:
			mc.parent( self.name, w = True )
			return
		elif isinstance( newParent, str):
			newParent = Node( newParent )
		if not newParent.exists:
			raise NodeNotFound( newParent.name )
		mc.parent( self.name, newParent.name )

	@property
	def allparents(self):
		"""return all parents of the node... recursive"""
		if not self.exists:
			raise NodeNotFound( self._name )
		p = self.parent
		nods = []
		if p != None:
			nods.append( p )
			newNodes = p.allparents
			if newNodes:
				nods.extend( newNodes )
		else:
			return None
		return nods

	@property
	def children(self):
		"""return children of the node"""
		if not self.exists:
			raise NodeNotFound( self._name )
		c = mc.listRelatives( self._name, c = True )
		if c:
			return [ Node( a ) for a in c ] #check how to handle arrays of nodes
		else:
			return None

	@property
	def exists(self):
		"""check if the node really exists"""
		return mc.objExists( self._name )

	@property
	def type(self):
		"""return Node Type"""
		if not self.exists:
			raise NodeNotFound( self._name )
		return mc.objectType( self.name )

	def istype(self, typ ):
		"""check if the node is a specific type"""
		if not self.exists:
			raise NodeNotFound( self._name )
		return mc.objectType( self.name, isType = typ )

	@property
	def a(self):
		"""Return attribute object to work with =)"""
		if not self.exists:
			raise NodeNotFound( self._name )
		return NodeAttributeCollection( self )

	@property
	def namespace(self):
		"""return namespace of node"""
		return Namespace.fromNode( self )

	@namespace.setter
	def namespace( self, newNamespace ):
		"""move to other namespace"""
		if isinstance( newNamespace, str ):
			newNamespace = Namespace( newNamespace )
		if not newNamespace.exists:
			if AUTO_CREATE_NAMESPACE:
				newNamespace.create()
			else:
				raise NamespaceNotFound( newNamespace.name )
		oldName = self.name
		if self.namespace.name == ':':
			self.name = newNamespace.name[1:] + ':' + oldName
		else:
			self.name = oldName.replace( self.namespace.name[1:], newNamespace.name[1:] )

	def attr(self, attribute):
		if not self.exists:
			raise NodeNotFound( self._name )
		return NodeAttribute(self, attribute)

	@property
	def locked(self):
		"""lock Node"""
		if not self.exists:
			raise NodeNotFound( self.name )
		return mc.lockNode( self.name, q = True, l = True )[0]

	@locked.setter
	def locked(self, state):
		"""unlock Node"""
		if not self.exists:
			raise NodeNotFound( self.name )
		mc.lockNode( self.name, l = state )

	def duplicate(self, newName = None):
		"""duplicate node"""
		if not self.exists:
			raise NodeNotFound( self.name )
		if newName:
			mc.duplicate( self.name, n = newName )
		else:
			mc.duplicate( self.name )

	def delete(self):
		"""delete node"""
		if not self.exists:
			raise NodeNotFound( self.name )
		mc.delete( self.name )


class NodeAttribute(object):
	def __init__(self, node, attribute):
		self._node = node
		self._attribute = attribute

	@property
	def fullname(self):
		"""full name of the attribute with the node --> node.attribute string"""
		return self._node.name + "." + self._attribute

	@property
	def name(self):
		"""name of the attribute"""
		return self._attribute

	@property
	def node(self):
		"""return node of the current attribute"""
		return self._node

	@property
	def v(self):
		"""attribute value"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		return mc.getAttr( self.fullname )

	@v.setter
	def v(self, value):
		"""Set the attribute value.. 
		Handle different types"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		ty = self.type
		hasNumber = re.match( r'.+(\d)', ty )
		if hasNumber:
			if len( value ) == int( hasNumber.groups(0)[0] ):
				for v,a in enumerate( self.children ):
					if AUTO_UNLOCK_ATTR:
						a.locked = False
					if AUTO_OVERRIDE_ATTR:
						a.overrided = True
					mc.setAttr( a.fullname, value[v] )
			else:
				raise ValueError( "The attribute %s has different amount of values"%self._attribute )
		elif ty == 'string': #Set STRING Value
			if AUTO_UNLOCK_ATTR:
				self.locked = False
			if AUTO_OVERRIDE_ATTR:
				self.overrided = True
			mc.setAttr(self.fullname, value, type=ty)
		else:
			if AUTO_UNLOCK_ATTR:
				self.locked = False
			if AUTO_OVERRIDE_ATTR:
				self.overrided = True
			mc.setAttr( self.fullname, value )

	@property
	def children(self):
		"""Return children attributes"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		children = mc.attributeQuery( self._attribute, node = self._node.name, lc = True )
		if children:
			return [ NodeAttribute(self._node, a) for a in children ]
		return None

	@property
	def type(self):
		"""return Attribute Type"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		return mc.getAttr(self.fullname, type=True)

	@property
	def exists(self):
		"""attribute exists? """
		tmpAttr = re.sub( '\[\d+\]$', '' , self._attribute )
		return mc.attributeQuery( tmpAttr, node=self._node.name, ex=True)

	@property
	def locked(self):
		"""lock attribute"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		return mc.getAttr( self.name, l = True )

	@locked.setter
	def locked(self, state):
		"""lock attribute"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		mc.setAttr( self.name, l = state )

	@property
	def max(self):
		"""return max value if it has, else None"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		return mc.addAttr( self.name, q = True, max = True )

	@max.setter
	def max(self, value):
		"""set new max value for attribute"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		mc.addAttr( self.name, e = True, max = value )

	@property
	def min(self):
		"""return min value if it has, else None"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		return mc.addAttr( self.name, q = True, min = True )

	@min.setter
	def min(self, value):
		"""set new min value for attribute"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		mc.addAttr( self.name, e = True, min = value )

	@property
	def default(self):
		"""return default value if it has, else None"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		return mc.attributeQuery( self._attribute, n = self._node.name, ld = True )[0]

	@default.setter
	def default(self, value):
		"""set new default value for attribute"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		mc.addAttr( self.name, e = True, dv = value )

	@property
	def input(self):
		"""get input connection if there is one, None if not"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		con = mc.listConnections( self.fullname, p = True, d = False )
		if con:
			condata = con[0].split( '.', 1 )
			return NodeAttribute( Node( condata[0] ), condata[1] )
		return None

	@property
	def output(self):
		"""get output connections if there is one, None if not, this return an array"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		con = mc.listConnections( self.fullname, p = True, s = True )
		if con:
			con = [ NodeAttribute(Node(a[:a.index('.')]), a[a.index('.')+1:]) for a in con ]
		return con

	@property
	def overrided(self):
		"""return if the attribute has override"""
		lay = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )
		if not 'defaultRenderLayer' == lay:
			if any( a.node.name == lay for a in c.a.v.output ):
				return True
		return False

	@overrided.setter
	def overrided(self, value):
		"""set an override for attribute"""
		lay = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )
		if not 'defaultRenderLayer' == lay:
			if value:
				mc.editRenderLayerAdjustment( self.fullname ,layer= lay )
			else:
				mc.editRenderLayerAdjustment( self.fullname , remove=True )

	def __rshift__(self, other):
		"""connect attribute using >> """
		self.connect( other )

	def __lshift__(self, other):
		"""connect attribute using << """
		self.connect( other, False )

	def connect( self, other, inOrder = True ):
		"""connect attribute to another or inverse, determined by inOrder"""
		"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		if not other.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		"""
		if inOrder:
			if AUTO_UNLOCK_ATTR:
				other.name.locked = False
			mc.connectAttr( self.fullname, other.fullname, f = FORCE_CONNECTION )
		else:
			if AUTO_UNLOCK_ATTR:
				self.name.locked = False
			mc.connectAttr( other.fullname, self.fullname, f = FORCE_CONNECTION )

	def __floordiv__(self, other):
		"""discconect attribute using // """
		self.disconnect( other )

	def disconnect(self, other = None ):
		"""disconnect attributes, if other is None... it will disconnect to what ever is connected =)"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		if not other:
			con = self.inp
			if con:
				mc.disconnectAttr( con, self.name )
				return
		if not other.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		mc.disconnectAttr( self.name, other.name )

	def __or__(self, other):
		"""is connected ? using | THE PIPE =) """
		return self.isConnected( other )

	def isConnected(self, other, inOrder = True ):
		"""check if the attributes are connected"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		if not other.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		if inOrder:
			return mc.isConnected( self.name, other.name )
		else:
			return mc.isConnected( other.name, self.name )

	def delete(self):
		"""delete attribute"""
		if not self.exists:
			raise AttributeNotFound( self._node.name, self._attribute )
		mc.deleteAttr(self._node.name, at=self._attribute)

	def add( self, dataType = None, attributeType = None ):
		"""add custom attribute"""
		cmd = 'mc.addAttr("' + self._node.name + '", longName = "' + self._attribute + '", k = True '
		if attributeType:
			cmd += ' ,attributeType = "' + attributeType + '"'
		if dataType:
			cmd += ' ,dataType = "' + dataType + '"'
		if not dataType and not attributeType:
			raise KeyError( 'You need to specify the attributeType or the dataType to add this attribute' )
		cmd += ')'
		print cmd
		eval( cmd )


class NodeAttributeCollection(object):

    def __init__(self, node):
        self._node = node

    def __getattr__(self, attribute):
        return NodeAttribute(self._node, attribute)

	def add(self, attribute): #TODO
		pass


class Namespace(object):
	"""class to control namespaces"""
	def __init__(self, namespace = None ):
		"""if namespace is None... it will take current"""
		if not namespace:
			self._namespace = mc.namespaceInfo( cur = True )
		else:
			self._namespace = namespace 
		if not self._namespace.startswith( ':' ):
			self._namespace = ':' + self._namespace

	def __str__(self):
		"""return string format"""
		return self._namespace

	def __enter__( self ):
		return self

	def __exit__( self, type, value, traceback ):
		mc.namespace( set=self._namespace )

	@property
	def name(self):
		"""return the namespace in string"""
		return self._namespace
	
	def create(self):
		"""create namespace if doesn't exists"""
		if not self.exists:
			names = self._namespace[1:].split(':')
			with Namespace( ':' ).set():
				tmpParent = ''
				for s in names:
					if not mc.namespace( ex = tmpParent + ':' + s ):
						mc.namespace( add = s, p = tmpParent + ':' )
					tmpParent += ':' + s 

	@property
	def exists(self):
		"""check if current namespace exists"""
		return mc.namespace( ex = self._namespace )

	@property
	def children(self):
		"""return the children of the namespace if exists"""
		if not self.exists:
			raise NamespaceNotFound( self.name )
		with self.set():
			childs = mc.namespaceInfo( lon=True )
		if childs:
			childs = [ Namespace( n ) for n in childs ]
		return childs

	@property
	def nodes(self):
		"""return the nodes that have the namespace"""
		if not self.exists:
			raise NamespaceNotFound( self.name )
		with self.set():
			nods = mc.namespaceInfo( lod = True )
			if nods:
				return [ Node( n ) for n in nods ]
		return None

	@property
	def parent(self):
		"""return the parent of the current namespace"""
		if not self.exists:
			raise NamespaceNotFound( self.name )
		p = namespace.rindex(':')
		if p == 0:
			return ':'
		else:
			return namespace[ :p ]

	@property
	def empty(self):
		"""return if the namespace is empty"""
		nods = self.nodes
		if nods:
			return True
		else:
			return False

	def remove(self):
		"""remove namespace if exists"""
		if not self.exists:
			raise NamespaceNotFound( self.name )
		mc.namespace( rm = self.name )

	def set(self):
		"""set namespace to current"""
		if not self.exists:
			if AUTO_CREATE_NAMESPACE:
				self.create()
		nsTempSet = Namespace()
		mc.namespace( set = self._namespace )
		return nsTempSet

	def move(self, other):
		"""move current nodes in namespace to other, also support if other is a string"""
		if not self.exists:
			raise NamespaceNotFound( self.name )
		if isinstance( other, str ):
			other = Namespace( other )
		if not other.exists:
			if AUTO_CREATE_NAMESPACE:
				other.create()
			else:
				raise NamespaceNotFound( other.name )
		mc.namespace( mv = [ self.name, other.name ], f = True )
		self._namespace = other.name

	def __rshift__(self,other):
		"""move namespace from this namespace to another with >>"""
		self.move( other )

	def rename(self, newName):
		"""rename current namespace, it will rename all childs namespaces"""
		if not self.exists:
			raise NamespaceNotFound( self.name )
		mc.namespace( ren = newName, f = True )

	@staticmethod
	def fromNode(node):
		"""return namespace from Node"""
		p = node.name.rfind( ':' )
			
		if p == -1:
			return Namespace( ':' )
		else:
			return Namespace( ':'+ node.name[ :p ] )


class AttributeNotFound( Exception ):
	def __init__(self, node, attribute ):
		self._message = "Node '%s' has no attribute '%s'." % ( node, attribute )

	def __str__(self):
		return self._message

class NodeNotFound( Exception ):
	def __init__(self, node ):
		self._message = "Node '%s' doesn\'t exists." % ( node )

	def __str__(self):
		return self._message

class NamespaceNotFound( Exception ):
	def __init__(self, namespace ):
		self._message = "Namespace '%s' doesn\'t exists." % ( namespace )

	def __str__(self):
		return self._message 
