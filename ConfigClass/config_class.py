from configobj import ConfigObj

class ConfigStruct(object):
    def __init__(self) :
                  
        try:
            self.config_filename = 'config.ini'
            configObj = ConfigObj(self.config_filename)
        
            # Program options   
            self.save_path          = configObj['Preferences']['path_to_save']
            self.quality            = configObj['Preferences']['quality']
            self.custom_label       = configObj['Preferences']['custom_string']
            self.num_to_dl          = configObj.get('Preferences').as_int('number_to_dl')
            self.file_age           = configObj.get('Preferences').as_float('old_file_age')
            
            
            # These below are all boolean values    
            self.del_files            = configObj.get('Preferences').as_bool('del_old_files')
            self.rename_trailer       = configObj.get('Preferences').as_bool('rename_trailer')
            self.download_clips       = configObj.get('Preferences').as_bool('download_clips')
            self.multi_part           = configObj.get('Preferences').as_bool('multi_part')
            self.verbose_output       = configObj.get('Preferences').as_bool('verbose_output')
            self.log_file             = configObj.get('Preferences').as_bool('log_file')
            
            # These are catergories from hd-trailers and boolean values   
            self.download_latest         = configObj.get('Download From').as_bool('latest')
            self.most_watched            = configObj.get('Download From').as_bool('most_watched')
            self.top_movies              = configObj.get('Download From').as_bool('top_movies')
            self.opening_this_week       = configObj.get('Download From').as_bool('opening_this_week')
            self.coming_soon             = configObj.get('Download From').as_bool('coming_soon')
            
            # Program variables 
            self.site_pref          = 'http://movietrailers.apple.com'   #download from here
            self.filetype_dl        = 'mov', 'mp4', 'avi'
            self.base_url           = 'http://www.hd-trailers.net'     
            self.dl_trailer_count   = 0   
            self.dl_clip_count      = 0
            self.total_downloaded   = 1  
            self.current_version      = 1.1
        except Exception as e:
            print "Error occured reading the config file - %s" %e    
  


        
