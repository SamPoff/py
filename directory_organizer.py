
"""

Created on Thu May 25 12:22:51 2017
Author: Sam Poff, spoff42@gmail.com


The purpose of this program is to iterate over the files in a directory,
categorize all of the files by date, then create, and place those files in, folders
according to their date.


If working correctly the directory on the computer will be a list of
folders with 'Month_Year' names, filled with all the files either downloaded 
or last altered within that month-year period.


This is designed to work on windows only.


V2 Ideas:
    Make the format for the new folders customizable.
    Run on startup or when download is done (set prefrences for automatic cleanup).
    Different types of folders depending on the directory or file type.
    Splitting based on file type instead of date.
    Option to organize files in directory or files in folders inside directory. 
    
    move_files(): get rid of the 2016, 2017 thing. Should figure it out on its
    own.
    
    
Error:
    If you try to run the program and it tries to move a file into one of the 
    new folders but that folder already contains that file, then it will say
    'cannot create a file when that file already exists.' For instance if you
    download something, run the program so it gets put away, then download that
    same file and try to run the program again, it will crash.

<<<<<<< HEAD
   
=======
>>>>>>> gui
"""









import os
import datetime
from pathlib import Path
from winreg import *
import tkinter as tk 
from tkinter import ttk

LARGE_FONT= ("Verdana")








  
"""
This function executes when the button is pushed. To read the value selected
on the radiobuttons call 'var.get()'. In here the correct directory path should
be selcted and the rest of the code will run.
"""
def execute( var ):
    
    # Get path to directory.
    path = get_path()
    
    try:
        val = var.get()
    except AttributeError:
        val = var
    
    # Alter path to go to correct folder if necessary.
    if   val == 1 :
        path = change_dir( path, 'Desktop\\' )
    elif val == 2 :
        path = change_dir( path, 'Documents\\' )
    elif val == 3 :
        pass
    elif val == 4 :
        path = change_dir( path, 'Music\\' )
    elif val == 5 :
        path = change_dir( path, 'Pictures\\' )
    elif val == 6 :
        path = change_dir( path, 'Videos\\' )
    elif val == 7:
        execute( 1 )
        execute( 2 )
        execute( 3 )
        execute( 4 )
        execute( 5 )
        execute( 6 )

    # Get path to all the files / directories in 'Desktop'.
    all_in_dir   = list_objects_in_dir ( path )
    # Remove all the directories from the list.
    files_in_dir = remove_directories ( all_in_dir ) 
    # Make new date folders if neccesary.
    make_date_folders( files_in_dir, path )
    # Move files into respective folders.
    move_files( files_in_dir, path )
    return None

        
        
        
        
        
        
        
        
"""
This function takes in the original path leading to the downloads folder
and changes it to lead to the correct folder (Desktop, Pictures, etc).

var downloads   - String to compare to when finding start point for portion
                  of path we want to replace.
var start_index - Index of the beginning of the portion we want to replace.
var new_path    - Corrected path.

return - new_path
"""       
def change_dir( path, new_suffix ):
    
    downloads   = 'Downloads'
    start_index = 0

    # Finds the beginning of the portion of the path we want to change.
    for i in range( len( path ) ):
        if path[ i : i + 9 ] == downloads:
            start_index = i
            
    # Concatenates the new suffix onto the end.
    new_path = path[ : start_index ] + new_suffix

    return new_path









    
"""
Returns the path to the user's downloads folder.

var sub_key   - String that identifies the subkey to load.
var Downloads - Path to downloads folder. Extra slash is added.

return - Downloads
"""
def get_path():
    sub_key = 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    with OpenKey(HKEY_CURRENT_USER, sub_key) as key:
        Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
    Downloads = Downloads + '\\'
    return Downloads









 
"""
Takes in the path to a directory and returns a list of paths for all the files
/ subdirectories contained within.
 
var path_not_string - Converts path string to a windows path.
var directory_objs  - List of directories / files in parent directory.
 
return - directory_objs
"""
def list_objects_in_dir( path ):
    path_not_string = Path( path )
    directory_objs = [ child for child in path_not_string.iterdir() ]
    return directory_objs
 
 
    






 
"""
Takes in a list of directories / files and removes all directories.

var no_directories - List of objects with all directories removed.
var no_ini         - List of objects with the .ini file removed. This file has
                     something to do with windows and is hidden so I don't want
                     to move it around or mess with it.
 
return - no_ini
"""
def remove_directories( directories_and_files ):
    # Creates a new list excluding directories.        
    no_directories = [ obj for obj in directories_and_files 
                      if not os.path.isdir( obj ) ]
    # Removes any .ini files (something to do with windows, 
    # don't want to mess with it).
    no_ini = [ x for x in no_directories if x.suffix != '.ini' ]
    return no_ini
     
     







 
"""
Takes in the path to a file and returns the date it was last altered.
Return format: YYYY-MM-DD

var time           - The unix timestamp (seconds since 01Jan1970)
var corrected_time - Converts to output format.

return - corrected_time
"""
def get_time_last_alteration( path ):
    # Date formating.
    form = '%Y-%m-%d'
    time = os.path.getmtime( path )
    corrected_time = datetime.datetime.fromtimestamp( time ).strftime( form )
    return corrected_time










"""
This function takes in a list of file paths and returns their creation dates.

var dates - List of dates all the files were created on.

return - dates
"""
def get_dates( file_paths ):
    dates = [ get_time_last_alteration( path ) for path in file_paths ]
    return dates










"""
This function creates folders with given dates.

var dates_for_files - Dates for all the files in Downloads.
var years           - Years issolated from dates.
var months          - Months issolated from dates.
var month_year      - 'Month_Year' with month as letters and year as numbers.
var potential_directories - Directory path concatenated with month_year to
                            give the path name of the new folders to be made.

return - None
"""
def make_date_folders( file_paths, path ):
    
    # Get dates for all the files.
    dates_for_files = get_dates( file_paths )
    
    # Isolate year / month values from date array
    years  = [ dates_for_files[i][0:4] for i in range( len( dates_for_files ) ) ]
    months = [ dates_for_files[i][5:7] for i in range( len( dates_for_files ) ) ]
    
    # Convert month values into text instead of number 
    # (like 'May' instead of '05').
    for i in range( len( months ) ):
        if   months[i] == '01': months[i] = 'Jan'
        elif months[i] == '02': months[i] = 'Feb'
        elif months[i] == '03': months[i] = 'Mar'
        elif months[i] == '04': months[i] = 'Apr'
        elif months[i] == '05': months[i] = 'May'
        elif months[i] == '06': months[i] = 'Jun'
        elif months[i] == '07': months[i] = 'Jul'
        elif months[i] == '08': months[i] = 'Aug'
        elif months[i] == '09': months[i] = 'Sep'
        elif months[i] == '10': months[i] = 'Oct'
        elif months[i] == '11': months[i] = 'Nov'
        elif months[i] == '12': months[i] = 'Dec'
        else: print('Error in make_date_folders()') 
    
    # Combine month and year into a single string.
    month_year = [ x + '_' + y for x, y in zip( months,years ) ]

    # Create a list of potential directory names based on dates.
    potential_directories = [ path + month_year[i] 
                            for i in range( len( month_year ) ) ]

    # Create folders based on list of possible dates.
    # Folders will only be made once per possible name.
    for i in range( len( potential_directories ) ):
        if not os.path.exists( potential_directories[i] ):
            os.makedirs( potential_directories[i] )

    return None










"""
This function moves the files from 'Downloads' to their new folders. The move
is actually done by renaming them to include the new folder name. The first part 
of the function is a copy paste from make_date_folders, so those variables 
will come first:
    
    var file_paths      - Paths to all the files in the directory.
    var path            - Path to directory.
    var dates_for_files - Dates for all the files in Downloads.
    var years           - Years issolated from dates.
    var months          - Months issolated from dates.
    var month_year      - 'Month_Year' with month as letters and year as numbers.
    var potential_directories - Directory path concatenated with month_year to
                            give the path name of the new folders to be made.

The one new variable follows:
    
    var name - The name of the file path converted to a string.
   
return None
"""
def move_files( file_paths, path ):
    
    """
    Begin by making an array of month_year names for the files. This will
    be the same as the month_year names used to create the folders.
    """
    # Get dates for all the files.
    dates_for_files = get_dates( file_paths )
    
    # Isolate year / month values from date array
    years  = [ dates_for_files[i][0:4] for i in range( len( dates_for_files ) ) ]
    months = [ dates_for_files[i][5:7] for i in range( len( dates_for_files ) ) ]
    
    # Convert month values into text instead of number 
    # (like 'May' instead of '05').
    for i in range( len( months ) ):
        if   months[i] == '01': months[i] = 'Jan'
        elif months[i] == '02': months[i] = 'Feb'
        elif months[i] == '03': months[i] = 'Mar'
        elif months[i] == '04': months[i] = 'Apr'
        elif months[i] == '05': months[i] = 'May'
        elif months[i] == '06': months[i] = 'Jun'
        elif months[i] == '07': months[i] = 'Jul'
        elif months[i] == '08': months[i] = 'Aug'
        elif months[i] == '09': months[i] = 'Sep'
        elif months[i] == '10': months[i] = 'Oct'
        elif months[i] == '11': months[i] = 'Nov'
        elif months[i] == '12': months[i] = 'Dec'
        else: print('Error in make_date_folders()') 
    
    # Combine month and year into a single string.
    month_year = [ x + '_' + y for x, y in zip( months, years ) ]
    
    """
    This portion of the code does all the file moving ( re-naming really ).
    """
    
    # Move files to the correct folder.
    for i in range( len( month_year ) ):
        
        # Convert WinPath to string so it will be iterable.
        name = str( file_paths[i] )
        
        # Find out where the file name begins.
        index = 0
        for j in range( len( name ) ):
            if   name[ j : j + 8  ] == 'Desktop\\'  :
                index = j + 8
            elif name[ j : j + 10 ] == 'Documents\\':
                index = j + 10
            elif name[ j : j + 10 ] == 'Downloads\\':
                index = j + 10
            elif name[ j : j + 6  ] == 'Music\\'    :
                index = j + 6
            elif name[ j : j + 9  ] == 'Pictures\\' :
                index = j + 9
            elif name[ j : j + 7  ] == 'Videos\\'    :
                index = j + 7
<<<<<<< HEAD
=======
            

#==============================================================================
#         """
#         Working solution 
#         """
#         if   month_year[i][0:3] == 'Jan':
#             try:
#                 os.rename( file_paths[i], path + 'Jan_' + month_year[i][4:] + '\\' + name[index :] )
#             except FileExistsError:
#                 # Want to make a window open and ask if they want to re-save with 
#                 # a changed name, skip, or delete.
#==============================================================================


>>>>>>> processes

        # Different case for every month.
        # Jan
        if   month_year[i][0:3] == 'Jan':
            try:
                os.rename( file_paths[i], path + 'Jan_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # Feb        
        elif month_year[i][0:3] == 'Feb':
            try:
                os.rename( file_paths[i], path + 'Feb_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # Mar        
        elif month_year[i][0:3] == 'Mar':
            try:
                os.rename( file_paths[i], path + 'Mar_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # Apr        
        elif month_year[i][0:3] == 'Apr':
            try:
                os.rename( file_paths[i], path + 'Apr_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # May        
        elif month_year[i][0:3] == 'May':
            try:
                os.rename( file_paths[i], path + 'May_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # Jun
        elif month_year[i][0:3] == 'Jun':
            try:
                os.rename( file_paths[i], path + 'Jun_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # Jul
        elif month_year[i][0:3] == 'Jul':
            try:
                os.rename( file_paths[i], path + 'Jul_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # Aug
        elif month_year[i][0:3] == 'Aug':
            try:
                os.rename( file_paths[i], path + 'Aug_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # Sep
        elif month_year[i][0:3] == 'Sep':
            try:
                os.rename( file_paths[i], path + 'Sep_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # Oct
        elif month_year[i][0:3] == 'Oct':
            try:
                os.rename( file_paths[i], path + 'Oct_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # Nov
        elif month_year[i][0:3] == 'Nov':
            try:
                os.rename( file_paths[i], path + 'Nov_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        # Dec
        elif month_year[i][0:3] == 'Dec':
            try:
                os.rename( file_paths[i], path + 'Dec_' + month_year[i][4:] + '\\' + name[index :] )
            except FileExistsError:
                print( 'error' )
                # Want to make a window open and ask if they want to re-save with 
                # a changed name, skip, or delete.
        else: print('Boned in move_files')
        
    return None










"""
Centers the window.
"""
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))








"""
This class controlls the frame switching.
"""
class Dung_Beetle(tk.Tk):

    def __init__( self, *args, **kwargs ):
        
        tk.Tk.__init__( self, *args, **kwargs )
        
        # Window title.
        tk.Tk.wm_title( self, "Dung-Beetle" )
        
        # Change corner icon.
        tk.Tk.wm_iconbitmap( self, 'bug_2.ico' )
        
        # Resize the window
        self.geometry('275x240')
        
        # Center the window.
        center( self )
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in ( StartPage, Cleaner_Page, Documentation ):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()








"""
Start page for the program.
"""       
class StartPage( tk.Frame ):

    def __init__( self, parent, controller ):
        tk.Frame.__init__( self,parent )
        
        tk.Label( self, text = "Directory Cleaner", font=LARGE_FONT ).grid( row = 1, padx = 64, pady = 30)


        # Clean a directory button.
        button = ttk.Button(self                       , 
                            text="Clean a Directory"   ,
                            command = lambda: controller.show_frame( Cleaner_Page ) )
        button.grid( row = 5, pady = 3, sticky = 's' )
        button.config( width = 20 )

        # View documentation button.
        button2 = ttk.Button(self                      , 
                             text="View Documentation" ,
                             command = lambda: controller.show_frame( Documentation ) )
        button2.grid( row = 6, pady = 3, sticky = 's' )
        button2.config( width = 20 )








"""
Main page with radio buttons.
"""
class Cleaner_Page(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        # # Header label
        tk.Label( self, 
                  text = 'Select the directory you would like to organize.'
                  ).grid(row = 1, padx = 3, sticky = 'w')
        
        # Set variable type
        var = tk.IntVar()
        
        
        # Setup radio buttons.
        tk.Radiobutton( self                 , 
                        text = 'Desktop'     , 
                        value = 1            , 
                        variable = var       , 
                        tristatevalue = 'x'
                        ).grid(row = 3, sticky = 'w')
        tk.Radiobutton( self                 , 
                        text = 'Documents'   , 
                        value = 2            , 
                        variable = var       , 
                        tristatevalue = 'x'
                        ).grid(row = 4, sticky = 'w')
        tk.Radiobutton( self                 , 
                        text = 'Downloads'   , 
                        value = 3            , 
                        variable = var       , 
                        tristatevalue = 'x'
                        ).grid(row = 5, sticky = 'w')
        tk.Radiobutton( self                 , 
                        text = 'Music'       , 
                        value = 4            , 
                        variable = var       , 
                        tristatevalue = 'x'
                        ).grid(row = 6, sticky = 'w')
        tk.Radiobutton( self                 , 
                        text = 'Pictures'    , 
                        value = 5            , 
                        variable = var       , 
                        tristatevalue = 'x'
                        ).grid(row = 7, sticky = 'w')
        tk.Radiobutton( self                 , 
                        text = 'Videos'      , 
                        value = 6            , 
                        variable = var       , 
                        tristatevalue = 'x'
                        ).grid(row = 8, sticky = 'w')
        tk.Radiobutton( self                 , 
                        text = 'All Folders' , 
                        value = 7            , 
                        variable = var       , 
                        tristatevalue = 'x'
                        ).grid(row = 9, sticky = 'w')
        # Setup select button
        ttk.Button( self             , 
                    text = 'Select'  , 
                    command = lambda: execute( var )
                    ).grid(row = 11, padx = 5, pady = 5, sticky = 'w')
        
        # Setup back to home button
        ttk.Button( self             , 
                    text="Back"      ,
                    command = lambda: controller.show_frame( StartPage ) 
                    ).grid(row = 11, padx = 194, pady = 5, sticky = 'w')
        
     
     





"""
Will be the documentation page.
"""
class Documentation(tk.Frame):

    def __init__( self, parent, controller ):
        
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="The purpose of this program is to iterate over the" ).grid( 
                 row = 1      , 
                 sticky = 'w' )
        tk.Label(self, text="files in a directory and place them into folders"   ).grid( 
                 row = 2      , 
                 sticky = 'w' )
        tk.Label(self, text="depending on when they were first downloaded or"    ).grid( 
                 row = 3      , 
                 sticky = 'w' )
        tk.Label(self, text="last altered."                                      ).grid( 
                 row = 4      , 
                 sticky = 'w' )


        button1 = ttk.Button( self, text="Back",
                            command=lambda: controller.show_frame( StartPage ) )
        button1.grid( pady = 3 )

        button2 = ttk.Button( self, text="To Cleaner",
                            command=lambda: controller.show_frame( Cleaner_Page ) )
        button2.grid( pady = 3 )
        







"""
Init main loop 
"""
if __name__ == "__main__":
    app = Dung_Beetle()
    app.mainloop()









#==============================================================================
#                        (   )
#                     (   ) (
#                      ) _   )
#                       ( \_
#                     _(_\ \)__
#  We clean up your  (____\___))
#==============================================================================



























