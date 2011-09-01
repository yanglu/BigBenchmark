#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Copyright (C) 2011
# Andy Pavlo & Yang Lu
# http:##www.cs.brown.edu/~pavlo/
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------------------

import sys
import os
import string
import re
import glob
import time
import execnet
from pprint import pprint,pformat

import drivers
from util import *
from runtime import *
from abstractclasses.abstractworker import AbstractWorker
from .message import *

## ==============================================
## createDriverClass
## ==============================================
def createDriverClass(name):
    full_name = "%sDriver" % name.title()
    mod = __import__('drivers.%s' % full_name.lower(), globals(), locals(), [full_name])
    klass = getattr(mod, full_name)
    return klass
## DEF

## ==============================================
## getDrivers
## ==============================================
def getDrivers():
    drivers = [ ]
    for f in map(lambda x: os.path.basename(x).replace("driver.py", ""), glob.glob("./drivers/*driver.py")):
        if f != "abstract": drivers.append(f)
    return (drivers)
## DEF


class TpccWorker(AbstractWorker):
    '''An example of how to subclass AbstractWorker and inmplement a simple benchmark that does nothing but sending and receiving messages '''
    def __init__(self):
	self._sf=None
	self._driver=None
	
    def initialize(self,config,channel,msg):
	''' You can create driver or scale parameter or doing anything else here '''
	self._sf=msg.data
	
	## Create a handle to the target client driver
        driverClass = createDriverClass(config['system'])
        assert driverClass != None, "Failed to find '%s' class" % config['system']
        driver = driverClass(config['ddl'])
        assert driver != None, "Failed to create '%s' driver" % config['system']
        driver.loadConfig(config)
	self._driver = driver
	sendMessage(INIT_COMPLETED,None,channel)

    def startLoading(self,config,channel,msg):
	assert self._driver!=None
	
	config['load']=True
	config['execute']=False
	config['reset']=False
	
	try:
            loadItems = (1 in w_ids)
            l = loader.Loader(self._driver,self._sf, msg.data, loadItems)
            self._driver.loadStart()
            l.execute()
            self._driver.loadFinish()   
        except KeyboardInterrupt:
            return -1
        except (Exception, AssertionError), ex:      
            traceback.print_exc(file=sys.stdout)
            raise
    
	sendMessage(LOAD_COMPLETED,None,channel)
	
    def startExecution(self,config,channel,msg):
	assert self._driver!=None
	
	config['execute']=True
	config['reset']=False
	soe= (config['stop_on_error']=='1')
	
	e = executor.Executor(self._driver, self._sf, stop_on_error=soe)
        self._driver.executeStart()
        results = e.execute(args['duration'])
        self._driver.executeFinish()
	sendMessage(EXECUTE_COMPLETED,results,channel)
	
    def moreProcessing(self,config,channel,msg):
	'''hook'''
	return None