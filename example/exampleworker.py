import execnet
from abstractclasses.abstractworker import AbstractWorker
from .message import *

class ExampleWorker(AbstractWorker):
    '''An example of how to subclass AbstractWorker and inmplement a simple benchmark that does nothing but sending and receiving messages '''
    def __init__(self):
       
	pass
 
    def initialize(self,config,channel,msg):
	''' You can create driver or scale parameter or doing anything else here '''
	sendMessage(INIT_COMPLETED,None,channel)

    def startLoading(self,config,channel,msg):
	sendMessage(LOAD_COMPLETED,None,channel)
	
    def startExecution(self,config,channel,msg):
	sendMessage(EXECUTE_COMPLETED,None,channel)
	
    def moreProcessing(self,config,channel,msg):
	'''hook'''
	return None