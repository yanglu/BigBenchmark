import time
import execnet
from abstractclasses.abstractcoordinator import AbstractCoordinator
from .message import *

class ExampleCoordinator(AbstractCoordinator) :
    ''' A simple example coordinator of a test benchmark which does nothing but sending and receiving message'''
    def __init__(self) :
	self._load_result=False
	self._execute_result=False
	
    def initialize(self,config,channels) :
	'''send a command to initialize the other side '''
	for ch in channels :
	    sendMessage(CMD_INIT,config,ch)
	for ch in channels :
	    msg=getMessage(ch.receive())
	    if msg.header==INIT_COMPLETED :
		pass
	    else:
		pass
	print "Initialization completed!"
	    
    def distributeLoading(self,config,channels) :
	'''divide loading to several clients'''
	load_start=time.time()
	work = "a piece of work"

	for ch in channels :
	    sendMessage(CMD_LOAD,work,ch)
	for ch in channels :
	    msg=getMessage(ch.receive())
	    if msg.header==LOAD_COMPLETED :
		pass
	    else:
		pass
	self._load_result=time.time()-load_start
	print "Loading completed!"
	
    def distributeExecution(self,config,channels) :
	execute_start=time.time()
	work = "a piece of work"

	for ch in channels :
	    sendMessage(CMD_LOAD,work,ch)
	for ch in channels :
	    msg=getMessage(ch.receive())
	    if msg.header==EXECUTE_COMPLETED :
		pass
	    else:
		pass
	self._execute_result=time.time()-execute_start
	print "Execution completed!"
	
    def showResult(self,config,channels):
	print 'Loading time is %5.3f.' %self._load_result
	print 'Execution time is %5.3f.' %self._execute_result
    

    