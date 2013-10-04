#! /usr/bin/env python
#
#   File = example-jpeg-to-xcf.py
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################
#
from gimpfu import *
import os
import re
#
def exampleJpgToXcf(srcPath, tgtPath):
    """Registered function exampleJpgToXcf, Converts all of the
    jpegs in the source directory into xcf files in a target 
    directory.  Requires two arguments, the paths to the source and
    target directories.  DOES NOT require an image to be open.
    """
    ###
    open_images, image_ids = pdb.gimp_image_list()
    if open_images > 0:
        pdb.gimp_message ("Close open Images & Rerun")
    else:
        # list all of the files in source & target directories
        allFileList = os.listdir(srcPath)
        existingList = os.listdir(tgtPath)
        srcFileList = []
        tgtFileList = []
        xform = re.compile('\.jpg', re.IGNORECASE)
        # Find all of the jpeg files in the list & make xcf file names
        for fname in allFileList:
            fnameLow = fname.lower()
            if fnameLow.count('.jpg') > 0:
                srcFileList.append(fname)
                tgtFileList.append(xform.sub('.xcf',fname))
        # Dictionary - source & target file names
        tgtFileDict = dict(zip(srcFileList, tgtFileList))
        # Loop on jpegs, open each & save as xcf
        for srcFile in srcFileList:
            # Don't overwrite existing, might be work in Progress
            if tgtFileDict[srcFile] not in existingList:
                # os.path.join inserts the right kind of file separator
                tgtFile = os.path.join(tgtPath, tgtFileDict[srcFile])
                srcFile = os.path.join(srcPath, srcFile)
                theImage = pdb.file_jpeg_load(srcFile, srcFile)
                theDrawable = theImage.active_drawable
                pdb.gimp_xcf_save(0, theImage, theDrawable, tgtFile, tgtFile)
                pdb.gimp_image_delete(theImage)
#
############################################################################
#
register (
    "exampleJpgToXcf",         # Name registered in Procedure Browser
    "Convert jpg files to xcf", # Widget title
    "Convert jpg files to xcf", # 
    "Stephen Kiel",         # Author
    "Stephen Kiel",         # Copyright Holder
    "July 2013",            # Date
    "1) Import JPG to XCF (Directory)", # Menu Entry
    "",     # Image Type - No image required
    [
    ( PF_DIRNAME, "srcPath", "JPG Originals (source) Directory:", "" ),
    ( PF_DIRNAME, "tgtPath", "XCF Working (target) Directory:", "" ),
    ],
    [],
    exampleJpgToXcf,   # Matches to name of function being defined
    menu = "<Image>/Example-Py"  # Menu Location
    )   # End register

main()
