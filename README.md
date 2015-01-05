XBMC-Trailer-Downloader
=======================

Scrapes hd-trailers.net and downloads trailers for use with XBMC and Cinema Experience script.

To install : pip install -r requirements.txt

* Trailers can be downloaded at a resolution of 480/720/1080. 

* Trailers that have been downloaded and are older than x days can be deleted. 

* Trailers can be renamed with a custom string appended to the end of the filename. Cinema Experience script will only play trailers with a filename
  ending in -trailer. This is set to happen by default, but can be changed to anything or nothing.

* HD-Trailers.net has multi-part trailers - ie trailer1, trailer2, trailer3, these can all be downloaded for a movie as well the extra
  clips, interviews etc. Single trailers can be downloaded for a movie as well.

* XBMC-Trailer-Downloader can be run completely silently with no console output or debug file logging. Console output is enabled by default. 

* Each subsection of HD-Trailers.net can be scraped, latest, most-watched, top-movies, opening-this-week and coming-soon. Please set a high value for num_to_dl in the config.ini if you intend are scraping the whole site. Duplicates will not be downloaded.


****Please modify the config.ini with your save location for trailers. ****


