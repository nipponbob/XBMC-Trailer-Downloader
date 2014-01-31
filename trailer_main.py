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

#Variables    
save_path_var      = config['Preferences']['path_to_save']
quality_var        = config['Preferences']['quality']
num_to_dl_var      = config['Preferences']['number_to_dl']
file_age_var       = config['Preferences']['old_file_age']
custom_label_var   = config['Preferences']['custom_string']

#These below are all boolean values    
del_files_bool       = config['Preferences']['delete_old_files']
rename_trailer_bool  = config['Preferences']['rename_trailer']
download_clips_bool  = config['Preferences']['download_clips']
multi_part_bool      = config['Preferences']['multi_part_trailer']
verbose_output_bool  = config['Preferences']['verbose_output']
log_file_bool        = config['Preferences']['log_file']

#These are catergories from hd-trailers and boolean values   
download_latest_bool    = config['Download From']['latest']
most_watched_bool       = config['Download From']['most_watched']
top_movies_bool         = config['Download From']['top_movies']
opening_this_week_bool  = config['Download From']['opening_this_week']
coming_soon_bool        = config['Download From']['coming_soon']

#Program prefs - load these fom file in later version!!!!!
site_pref          = 'http://movietrailers.apple.com'   #download from here
filetype_var       = 'mov', 'mp4', 'avi'
base_url           = 'http://www.hd-trailers.net'     
download_count_var = 0   



def writeDebug(debug_info):
#******** This writes a line to the debug file as well as to the console
#         Console output is only enabled if verbose_output ==  1  
#
    debug_info_payload = time.strftime("%d/%m/%Y ") + time.strftime("%H:%M:%S - ") + debug_info  # payload is 'DATE' + 'TIME' + '-' + 'MESG'
    if log_file_bool == '1' :
        with open("debug.log", "a") as f:       # open the file and append to it
            f.write(debug_info_payload + '\n')  # write our payload and a newline
    if verbose_output_bool == '1' : print(debug_info_payload)



#  
#  name: checkLink
#  @param
#  @return
#  
def checkLink(active_link):
# ********* Check to see if the link contains a movie
#           we want to download  
#              
    file_name = active_link.split('/')[-1] 
    
    if multi_part_bool == '1' :
        grab_type = '-tlr1'
        if site_pref in active_link and quality_var in active_link and grab_type in active_link: # Check site and resolution
               writeDebug("Found multipart :" + active_link)  
               if checkDuplicate(file_name) != 'DUPE' :				   
                   downloadLink(active_link)    # pass the link and download it
        grab_type = '-tlr2'
        if site_pref in active_link and quality_var in active_link and grab_type in active_link: # Check site and resolution
               writeDebug("Found mulipart : " + active_link)                                                                                     # check to see if the link matches our 
               if checkDuplicate(file_name) != 'DUPE' :
                    print(' DUPE CHECK ', checkDuplicate(file_name))
                    downloadLink(active_link)    # pass the link and download it  
        grab_type = '-tlr3'
        if site_pref in active_link and quality_var in active_link and grab_type in active_link: # Check site and resolution
               writeDebug("Found multipart :" + active_link)  
               if checkDuplicate(file_name) != 'DUPE' :
				   downloadLink(active_link)    # pass the link and download it
        grab_type = '-tlr4'
        if site_pref in active_link and quality_var in active_link and grab_type in active_link: # Check site and resolution
               writeDebug("Found multipart :" + active_link)  
               if checkDuplicate(file_name) != 'DUPE' :
				   downloadLink(active_link)    # pass the link and download it
           
    if multi_part_bool == '0' :          
        grab_type = '-tlr1'
        if site_pref in active_link and quality_var in active_link and grab_type in active_link: # Check site and resolution
               writeDebug("Found : " + active_link)                                                                                     # check to see if the link matches our 
               if checkDuplicate(file_name) != 'DUPE' :
                   downloadLink(active_link)    # pass the link and download it

    if download_clips_bool == '1' :
	grab_type = 'clip'
    	if site_pref in active_link and quality_var in active_link and grab_type in active_link: # Check site and resolution
             writeDebug("Found : " + active_link)                                                                                     # check to see if the link matches our 
             if checkDuplicate(file_name) != 'DUPE' :
                 downloadLink(active_link)    # pass the link and download it


#  
#  name: downloadLink
#  @param
#  @return
#  

def downloadLink(url):
# ******** Download the file to save_path_var location
#
 
    file_name = url.split('/')[-1] 
    request = urllib2.Request(url)                    # prepare the url to be opened
    request.add_header('User-agent', 'Quicktime')     # we are now a Quicktime player 
    u = urllib2.urlopen(request)                      # open the url we have created
    f = open(save_path_var + file_name, 'wb')         # f is the file we will write to (wb - write, binary)                    
    meta = u.info()         # get the metainfo from the url we have open
    file_size = int(meta.getheaders("Content-Length")[0])      # grab the filesize
    writeDebug('Downloading - ' + file_name) 
    if verbose_output_bool == '0' : print ("Downloading: %s to: %s" % (file_name, save_path_var))

    file_size_dl = 0          # how much have we downloaded
    block_sz = 8192           # block size - we will download this much at once
    while True:
        buffer = u.read(block_sz)   # read 8192 bytes from our url
        if not buffer:
            break
        file_size_dl += len(buffer)      # update our file size progress
        f.write(buffer)                  # write the buffer to our file
        status = r"TOTAL: %s Bytes- DONE: %4d Bytes [%3.2f%%]" % (file_size, file_size_dl, file_size_dl * 100. / file_size)   # magic from stackexchange
        status = status + chr(8)*(len(status)+1)                                        # more magic
        print (status),                                                                 # print the magic   ',' keeps it all on one line
    writeDebug("Downloaded - " + file_name)
    global download_count_var 
    download_count_var += 1
    if verbose_output_bool == '0' : print('Downloaded : ', file_name)
    f.close() 



def checkDuplicate(filename):
# ********* Checks for duplicate filename
#           This renames filename to filename + custom_label_var
#           before searching.
    extracted_filename = extractFilename(filename)
    if custom_label_var != '' : search_str = extracted_filename[0] + custom_label_var + extracted_filename[1]  
    elif custom_label_var == '' : search_str = extracted_filename[0] + extracted_filename[1] 
    for filename in os.listdir(save_path_var):    
        if filename == search_str : 
            writeDebug('Duplicate detected, not downloading ' + filename)
            return('DUPE')
            break
            



def extractFilename(filename):
# ********** Takes a filename and returns a tuple with
#            filename[0] and extension[1] --> 
     sizeofstr = len(filename) 
     sizeofstr = sizeofstr - 4
     extracted_file_ext = filename[sizeofstr:len(filename)]
     extracted_file_name = filename.replace(extracted_file_ext, '')
     return extracted_file_name, extracted_file_ext


     
def renameTrailers():
# ********** Rename all files in the save_path_var folder,
#            adding custom_label_var to the end of the filename    
    for filename in os.listdir(save_path_var):      
        if not custom_label_var in filename and not 'clip' in filename:
             if filename.endswith(filetype_var):                         # File ext to search for
                 path = os.path.join(save_path_var, filename)            # Location + filename   
                 extracted_filename = extractFilename(filename)
                 if extracted_filename[1] == "oad" : file_ext = ".mov"                # Apple sometimes returns .load files, which seem to be .movs              
                 target = os.path.join(save_path_var, extracted_filename[0] + custom_label_var + extracted_filename[1])     # dir + file + ext
                 os.rename(path, target) 
                 writeDebug ('Renamed ' + path + ' to ' + target)
    writeDebug('No files found to rename')      

        
            
def makeNewSoup(new_link):
# ********* Search through the pages of movies to find 
#           links to download from apple movies
  writeDebug('Following url ... ' + new_link)
  new_url = requests.get(base_url + new_link)   # make a new url to scrape new page                
  data = new_url.text
  soup = BeautifulSoup(data)
  for link in soup.findAll('a'):      # find the <a href> tag                               
         try:
            if 'movie' in link['href']: 
                  if link == None : current_link = "NULL" 
                  new_current_link = link.get('href')
                  #writeDebug('Found link ... ' + new_current_link)
                  checkLink(new_current_link)     # pass our link to be checked
         except KeyError:
                 pass



def makeSoup(start_url):
# ********** Make the soup - this gets back a list of links
#                            we will search through to find trailers 
    writeDebug('*** Scraping ...  ' + start_url + ' ***')
    url = requests.get(start_url)
    data = url.text
    soup = BeautifulSoup(data)
    for link in soup.findAll('a'):                                        # find the <a href> tag
        if 'movie' in link['href'] and "autoplay" not in link['href']:    # is 'movie' in the link but not 'autoplay'
            if link == None : current_link = "NULL"                       # get rid of empty links
            current_link = link.get('href')                               # grab the link target
            makeNewSoup(current_link)                                     # start again with a new link to see if there is anything to grab



def main():
    renameTrailers()
    #if download_latest == '1' : makeSoup(base_url + '/page/1/')
    #if most_watched : ADD IN DUPLICATE DETECTION
    #if top_movies_bool == '1' : makeSoup(base_url + '/top-movies/')
    #if opening_this_week == '1' : makeSoup(base_url + '/opening-this-week/')
    #if coming_soon == '1' : makeSoup(base_url + '/coming-soon/')

    
    
if __name__ == '__main__':
    main()
