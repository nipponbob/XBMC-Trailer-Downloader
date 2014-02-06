#  trailer_main.py
#  
#  Copyright 2014 realashe <ra@wintermute>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  


from bs4 import BeautifulSoup
from configobj import ConfigObj
import requests
import urllib2
import os
import time

#******** Load all variables from the config file
#         TODO - Check to see if file exists?!?
configFile = 'config.conf'
config     = ConfigObj(configFile)

# Program options   
save_path_var      = config['Preferences']['path_to_save']
quality_var        = config['Preferences']['quality']
num_to_dl_var      = config.get('Preferences').as_int('number_to_dl')
file_age_var       = config.get('Preferences').as_float('old_file_age')
custom_label_var   = config['Preferences']['custom_string']

# These below are all boolean values    
del_files_bool       = config.get('Preferences').as_bool('del_old_files')
rename_trailer_bool  = config.get('Preferences').as_bool('rename_trailer')
download_clips_bool  = config.get('Preferences').as_bool('download_clips')
multi_part_bool      = config.get('Preferences').as_bool('multi_part')
verbose_output_bool  = config.get('Preferences').as_bool('verbose_output')
log_file_bool        = config.get('Preferences').as_bool('log_file')

# These are catergories from hd-trailers and boolean values   
download_latest_bool    = config.get('Download From').as_bool('latest')
most_watched_bool       = config.get('Download From').as_bool('most_watched')
top_movies_bool         = config.get('Download From').as_bool('top_movies')
opening_this_week_bool  = config.get('Download From').as_bool('opening_this_week')
coming_soon_bool        = config.get('Download From').as_bool('coming_soon')
last_down = ''
num_to_dl_var -= 1

# Program variables
site_pref          = 'http://movietrailers.apple.com'   #download from here
filetype_var       = 'mov', 'mp4', 'avi'
base_url           = 'http://www.hd-trailers.net'     
download_count_var = 0   


def writeDebug(debug_info):
#******** This writes a line to the debug file as well as to the console
#         Console output is only enabled if verbose_output ==  1  
#
    debug_info_payload = time.strftime("%d/%m/%Y ") + time.strftime("%H:%M:%S - ") + debug_info  # payload is 'DATE' + 'TIME' + '-' + 'MESG'
    if log_file_bool  :
        with open("debug.log", "a") as f:       # open the file and append to it
            f.write(debug_info_payload + '\n')  # write our payload and a newline
    if verbose_output_bool : print(debug_info_payload)


def  checkDirectory(directory):
#********* Checks to see if the download dir exists,
#          if it doesn't it is created.
#
    if os.path.isdir(directory) : 
        pass
    else :
        os.mkdir(save_path_var)
        writeDebug('Directory created : ' + save_path_var)

def deleteFiles():
    del_count = 0
    seconds_in_day = 86400
    days_old = file_age_var * seconds_in_day    
    del_time = time.time() - days_old
    os.chdir(save_path_var)
    for filename in os.listdir(save_path_var):
        cur_time = os.path.getmtime(filename)
        if cur_time <= del_time : 
            os.remove(filename)
            del_count += 1                       
            WriteDebug('Deleted     : ' + filename)
    writeDebug(str(del_count) + ' files deleted.')
 
def checkLink(active_link):
# ********* Check to see if the link contains a movie
#           we want to download  
#   
    global last_down    
    file_name = active_link.split('/')[-1]
    if multi_part_bool :        # Download multiple clips for the same movie
        current_movie = active_link.split('/')[-1]      # This gets the filename from the url
        if last_down == current_movie : 
            return 
        grab_type = '-tlr'
        if site_pref in active_link and quality_var in active_link and grab_type in active_link: 
            writeDebug("Found Trailer : " + active_link)  
            if checkDuplicate(file_name) != 'DUPE' :     # Check if the file is a duplicate                  
                downloadLink(active_link)                # pass the link and download it                  
                last_down = active_link.split('/')[-1]   # This gets the filename
           
                
    if not multi_part_bool :         # Download 1 trailer for each movie
        current_movie = active_link.split('/')[-2]      # This gets the movie name from the url
        grab_type = '-tlr'       
        if last_down == current_movie : 
            return 
        if site_pref in active_link and quality_var in active_link and  grab_type in active_link :
            writeDebug("Found Trailer : " + active_link)                                           
            if checkDuplicate(file_name) != 'DUPE' :
                downloadLink(active_link)   
                last_down = active_link.split('/')[-2]   
            
 
    if download_clips_bool :          # Download clips
        grab_type = 'clip', '-fte1' 
        for grab in grab_type :
            if site_pref in active_link and quality_var in active_link and grab in active_link: 
                writeDebug("Found clip ++ : " + active_link)                                                                                    
                if checkDuplicate(file_name) != 'DUPE' :
                    downloadLink(active_link)    
               

def downloadLink(url):
# ******** Download the file to save_path_var location
#
# 
    global download_count_var     
    file_name = url.split('/')[-1]                    # Strip out the filename
    request = urllib2.Request(url)                    # Prepare the url to be opened
    request.add_header('User-agent', 'Quicktime')     # We are now a qt player as apple only allows qt players to download their files 
    u = urllib2.urlopen(request)                      # Open the url we have created
    f = open(save_path_var + file_name, 'wb')         # f is the file we will write to (wb - write, binary)                    
    meta = u.info()                                   # Get the metainfo from the url we have open
    file_size = int(meta.getheaders("Content-Length")[0])      # Grab the filesize
    
    file_size_dl = 0          # How much have we downloaded
    block_sz = 8192           # Block size - we will download this much at once
    if verbose_output_bool : writeDebug("Downloading   : %s to: %s" % (file_name, save_path_var))
    while True:
        buffer = u.read(block_sz)   # Read 8192 bytes from our url
        if not buffer:
            break
        file_size_dl += len(buffer)      # Update our file size progress
        f.write(buffer)                  # Write the buffer to our file
        status = r"TOTAL: %s Bytes- DONE: %4d Bytes [%3.2f%%]" % (file_size, file_size_dl, file_size_dl * 100. / file_size)   # Magic from stackexchange
        status = status + chr(8)*(len(status)+1)                                        # More magic
        if verbose_output_bool : print status,                                                # Print the magic   ',' keeps it all on one line
    f.close() 
    download_count_var += 1
    print '\n'
    writeDebug ('Downloaded    : ' + file_name)
    

def checkDuplicate(filename):
# ********* Checks for duplicate filename
#           This renames filename to filename + custom_label_var
#           before searching.
    extracted_filename = extractFilename(filename)   
    if custom_label_var != '' : search_str = extracted_filename[0] + custom_label_var + extracted_filename[1]  # Add the custom string to the search_str
    elif custom_label_var == '' : search_str = extracted_filename[0] + extracted_filename[1]                   # If there is no custom string
    
    for filename in os.listdir(save_path_var):    
        if filename == search_str or filename == extracted_filename[0] + extracted_filename[1] :        # Check for duplicates. The second check if for
            writeDebug('Duplicate --- : ' + filename)                           # completeness. 
            return('DUPE')
            break
            

def extractFilename(filename):
# ********** Takes a filename and returns a tuple with
#            filename[0] and extension[1] --> 
#
     sizeofstr = len(filename)      
     sizeofstr = sizeofstr - 4      
     extracted_file_ext = filename[sizeofstr:len(filename)]     # Extract the file extension
     extracted_file_name = filename.replace(extracted_file_ext, '')     # Extract the filename
     return extracted_file_name, extracted_file_ext

     
def renameTrailers():
# ********** Rename all files in the save_path_var folder,
#            adding custom_label_var to the end of the filename    
#  
    rename_count = 0
    for filename in os.listdir(save_path_var):      
        if not custom_label_var in filename and not 'clip' in filename:  # Check that custom_string and clip are not in filename
             if filename.endswith(filetype_var):                         # File ext to search for
                 path = os.path.join(save_path_var, filename)            # Location + filename   
                 extracted_filename = extractFilename(filename)
                 if extracted_filename[1] == "oad" : file_ext = ".mov"   # Apple sometimes returns files with no extension, make these .movs              
                 target = os.path.join(save_path_var, extracted_filename[0] + custom_label_var + extracted_filename[1])     # dir + file + ext
                 os.rename(path, target)   
                 rename_count += 1             
    writeDebug (str(rename_count) + ' trailers renamed.' )                 
                                             
            
def makeNewSoup(new_link):
# ********* Search through the pages of movies to find 
#           links to download from apple movies
#
    writeDebug('Following url : ' + new_link)
    new_url = requests.get(base_url + new_link)   # make a new url to scrape new page                
    data = new_url.text
    soup = BeautifulSoup(data)
    for link in soup.findAll('a'):      # find the <a href> tag                               
           try:
              if 'movie' in link['href']: 
                    if link == None : current_link = "NULL" 
                    new_current_link = link.get('href')
                    #writeDebug('Found link ... ' + new_current_link)
                    checkLink(new_current_link)
           except KeyError:
                   pass



def makeSoup(start_url):
# ********** Make the soup - this gets back a list of links
#                            we will search through to find trailers 
#
    if verbose_output_bool : writeDebug('**Scraping**  : ' + start_url)
    url = requests.get(start_url)   # Get the page to scrape
    data = url.text     
    soup = BeautifulSoup(data)  # Make the soup
    for link in soup.findAll('a'):                                        # find the <a href> tag
        if 'movie' in link['href'] and "autoplay" not in link['href']:    # is 'movie' in the link but not 'autoplay'
            if link == None : current_link = "NULL"                       # get rid of empty links
            current_link = link.get('href')                               # grab the link target            
            if download_count_var <= num_to_dl_var :
                makeNewSoup(current_link)                                     # start again with a new link to see if there is anything to grab
            else : 
                writeDebug('Download limit reached.')
                writeDebug(str(download_count_var) + ' trailers downloaded.')
                return           

def main():
    if save_path_var == '' :
        writeDebug('** No save path specified. Exiting... **')
        writeDebug('** Please edit config.conf and        **')
        writeDebug('** include a path to save to.         **')
        return
    checkDirectory(save_path_var)
    
    if download_latest_bool   : makeSoup(base_url + '/page/1/')
    if most_watched_bool      : makeSoup(base_url + '/most-watched')
    if top_movies_bool        : makeSoup(base_url + '/top-movies/')
    if opening_this_week_bool : makeSoup(base_url + '/opening-this-week/')
    if coming_soon_bool       : makeSoup(base_url + '/coming-soon/')
    
    if rename_trailer_bool    : renameTrailers() 
    if del_files_bool         : deleteFiles()
    
    if download_count_var == 0 : writeDebug('No new trailers found.')
    
if __name__ == '__main__':
    main()
