;   File = example-jpeg-to-xcf.py
;
;   This program is free software: you can redistribute it and/or modify
;   it under the terms of the GNU General Public License as published by
;   the Free Software Foundation; either version 3 of the License, or
;   (at your option) any later version.
;
;   This program is distributed in the hope that it will be useful,
;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;   GNU General Public License for more details.
;
;   You should have received a copy of the GNU General Public License
;   along with this program.  If not, see <http://www.gnu.org/licenses/>.
;
;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
;;;  Function - script-fu-example-jpg-to-xcf
;;;
;;;  Converts all jpeg images in selected directory to gimp xcf
;;;  format.
;;;
;;;  Filename Case insensitive. (converts xyz.jpg or XYZ.JPG)
;;;
;;;  Interactive program to be run WITHOUT AN IMAGE LOADED.
;;;
;;;  Program prompts for a source (jpgs) and target (xcfs)
;;;  directories.
;;;
;;;  Program runs on either Linux or Windows Host O/S, using the
;;;  appropriate path - filename separator ( "/" or "\").
;;;
;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
( define ( script-fu-example-jpg-to-xcf 
   sourceDirectory targetDirectory )
   ( let*
      (
         ; Declare and Init local variables
         ( returnVal #f )
         ; Guess host OS based on directory path separator
         ( isLinux (  >  
            ( length ( strbreakup sourceDirectory "/" ) )
            ( length ( strbreakup sourceDirectory "\\" ) ) ) )
         ; Form path/file patternSource based on OS 
         ( patternSource ( if isLinux
            ( string-append sourceDirectory "/*.[jJ][pP][gG]" )
            ( string-append sourceDirectory "\\*.[jJ][pP][gG]" ) ) )
         ( patternTarget ( if isLinux
            ( string-append targetDirectory "/*.[xX][cC][fF]" )
            ( string-append targetDirectory "\\*.[xX][cC][fF]" ) ) )
         ; List of files to be converted formatted for current Host
         ; O/S
         ( filelistSource ( cadr ( file-glob patternSource 1 ) ) )
         ( filelistExists ( cadr ( file-glob patternTarget 1 ) ) )
         ( checkFileExists filelistExists )
         ; Place holders for image variables - updated per image
         ( theImage 0 )
         ( theDrawable 0 )
         ( currentFile "" )
         ( baseName "" )
         ( outFilename "" )
         ; Constants used to assign values to parasites on new image
         ( doIt #t )
         ( checkFile "" )
      ) ; End declaration of Local Variables
      ;
      ; Run if images closed, message if not.
      ( if ( < 0 ( car ( gimp-image-list ) ) )
         ( gimp-message "Close open Images & Rerun" )
         ( begin
            ;
            ; Run within scope of let* and local variables
            ; 'baseName' is filename without .jpg extension
            ; 'outFilename' is filename with .xcf extension
            ; Step through each file in list with while loop.
            ( while ( not ( null? filelistSource ) )
               ( set! doIt #t )
               ( set! checkFileExists filelistExists )
               ( set! currentFile ( car filelistSource ) )
               ; Get open and get Image ID of current file
               ( set! theImage
                  ( car ( gimp-file-load RUN-NONINTERACTIVE 
                     currentFile currentFile ) ) )
               ( if isLinux
                  ; Target path-filename if Host OS is Linux
                  ( begin 
                     ( set! baseName ( car ( reverse
                        ( strbreakup currentFile "/" ) ) ) )
                     ( set! baseName ( car ( strbreakup baseName "." ) ) )
                     ( set! outFilename ( string-append
                           targetDirectory "/" baseName ".xcf" ) )
                  ) ; End begin - Host OS is Linux
                  ; Target path-filename if Host OS is Windows
                  ( begin 
                     ( set! baseName ( car ( reverse
                        ( strbreakup currentFile "\\" ) ) ) )
                     ( set! baseName ( car ( strbreakup baseName "." ) ) )
                     ( set! outFilename ( string-append
                           targetDirectory "\\" baseName ".xcf" ) )
                  ) ; End begin - if Host OS is Windows
               ) ; End if isLinux
               ; Check to see if outFilename exists so we don't overwrite
               ( while ( not ( null? checkFileExists ) )
                  ( set! checkFile ( car checkFileExists ) )
                  ( if ( string=? outFilename checkFile )
                     ( set! doIt #f ) )
                  (set! checkFileExists ( cdr checkFileExists ) )
               ) ; End while checkFileExists
               ( if doIt
                  ( begin
                     ; Get / set Drawable ID, need it for file save.
                     ( set! theDrawable ( car 
                        ( gimp-image-merge-visible-layers theImage 0 ) ) )
                     ; Save file - gimp xcf format
                     ( gimp-xcf-save 
                        RUN-NONINTERACTIVE theImage theDrawable
                        outFilename outFilename )
                  ) ; End begin
               ) ; End if doIt
               ( gimp-image-delete theImage )
               ; Update while loop iteration parameter
               (set! filelistSource ( cdr filelistSource ) )
            ) ; End while
         ); End outer begin
      ) ; End outer if
      ( set! returnVal #t )
   ) ; End let*
) ; End define
;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
( script-fu-register "script-fu-example-jpg-to-xcf" ; Function Name
   "1 ) Import JPG to XCF (Directory)"    ; Menu Label
   "This script is an interactive script to convert all of the jpegs 
   in a source directory into Gimp xcf format files in a target 
   directory.  The script is designed to be run WITHOUT ANY IMAGE 
   LOADED. Runs from Gimp shell in Linux and Windows."
   "Stephen Kiel"       ; Author
   "2013, Stephen Kiel" ; Copyright
   "July 2013"          ; Creation Date
   ""                   ; Valid Image Type - No Image required
    ; We actually don't want any images open when we run this
    ;   script, so it must be available from the menu when an
    ;   image is not loaded.  This script will determine the IDs
    ;   of the Image and Drawable itself rather than having them
    ;   passed as parameters.
   ; Interactive widgets
   SF-DIRNAME "JPG Originals (source) Directory" ""
   SF-DIRNAME "XCF Working   (target) Directory" ""
) ; End script-fu-register
( script-fu-menu-register 
   "script-fu-example-jpg-to-xcf" "<Image>/Example-Scm")
;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
