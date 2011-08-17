class AbstractWorker:
    '''abbstract worker '''
    def __init__(self):
	''' All subclass constructor should not take any argument. You can do more initializing work in initializing method '''
	pass
    
    def initialize(config,channel):
	''' initialization. You might want to send a INIT_COMPLETED message back''' 
	return None

    def startLoading(config,channel):
	''' Actual loading. You might want to send a LOAD_COMPLETED message back with the loading time'''
	return None
	
    def startExecution(config,channel):
	''' Actual execution. You might want to send a EXECUTE_COMPLETED message back with the loading time'''
	return None
	
    def moreProcessing(config,channel):
	'''hook'''
	return None


