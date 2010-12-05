#!/usr/bin/env python

 
_license_ ='''
    houExport Copyright (C) 2009  Farsheed Ashouri

    houExport is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


# ========  Maya OBJ sequence file exporter =========
#    Author: Farsheed Ashouri
#    Platform: Linux & Windows
#    Programming Language: Python 2.x
#    Created on: 19 Oct 2009
#    Status: RC1
#    Discription: this will export your polygons as wavefront object
#                 sequences. the format is name.<frame>.obj
# 
#    Usage:
#       Add this lines to your shelf:
'''
try:reload(houExport)
except:import houExport
houExport.main().houExport()
'''
#       Then select your objects and enter a name for your sequence.
#       Objects will be written in:
#           <workspace>/Houdiniexports/<scene name>/<sequence name>
#       Warning: this tool will overwite your files by default. Also it won't
#       export materal .mtl files.
#       Keep in mind that, because of script limitations,
#       once you start the process you can't stop it.
#
#    Copyright: Farsheed Ashouri | 2009
# ===================================================


version = "0.94"
import os
import sys
import maya.cmds as mc


class main:
    def __init__(self):
        'The instructor'
        # check for os
        if os.name == "posix": ext="so"
        else: ext="mll"
        # load the plug-in
        mc.loadPlugin( 'objExport.%s' % ext )

    def folderOps(self, folder):
        'check and create a folder'
        if not os.path.isdir(folder):
            os.mkdir(folder)

    def houExMain(self, *arg, **kw):
        'The main functiionality'
        # get the user input name
        objSiqName = mc.textField(self.nameField, q=1, tx=1)
        objSiqName = objSiqName.replace(" ", "_") # replace space
        # Find the current workspace area.
        cws = mc.workspace( q=True, dir=True )
        # check for "HoudiniExports" folder:
        houExFoName = "%sHoudiniExports" % (cws)
        self.folderOps(houExFoName)
        # check for current scene name
        sceName = os.path.basename(mc.file( q=1, sn=1 ))
        if not sceName: sceName = "untitled"
        sceName = sceName.replace(" ", "_") # replace space
        # check if a folder with scene name exists or not:
        sceFoName = "%s/%s" % (houExFoName, sceName)
        self.folderOps(sceFoName)
        # check if a folder with sequence not:
        siqFoName = "%s/%s" % (sceFoName, objSiqName)
        self.folderOps(siqFoName)
        # get time range:
        stTime = mc.playbackOptions( q=1 , minTime=1)
        enTime = mc.playbackOptions( q=1 , maxTime=1)
        # Start the loop of export:
        if objSiqName and objSiqName!="please_enter_a_name!":
            for i in range(int(enTime-stTime+1)):
                # set the current Frame:
                now = i+stTime
                mc.currentTime(now, e=1)
            # export:
                filePath = '%s/%s.%d.obj' % (siqFoName, objSiqName, now)
                #~ print 'final path:', filePath
                mc.file (  filePath \
        , op = "groups=1;ptgroups=1;materials=0;smoothing=1;normals=1" \
        , typ = "OBJexport" , f=1,  es=1)
            print 'File saved in: ', filePath
        else: mc.textField(self.nameField, e=1, tx="please enter a name!")

    def houExport(self):
        if mc.window('Obj_Sequence_Exporter',ex=1):
            mc.deleteUI('Obj_Sequence_Exporter')
        mc.window ('Obj Sequence Exporter', w=300, h=80, \
            t = "Obj exporter | version %s" % version)
        Mcolumn = mc.columnLayout (adj=1)
        mc.text ( l = "please enter the name:")
        self.nameField = mc.textField()
        mc.button (l ="Dance with me!", c=self.houExMain)
        mc.showWindow ('Obj_Sequence_Exporter')

if __name__ == "__main__":
    main().houExport();

# end
