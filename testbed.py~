from configobj import ConfigObj

configFile = 'config.conf'
cfg     = ConfigObj(configFile)


del_files_bool = cfg.get('Preferences').as_bool('rename_trailer')  # This works perfectly! cfg.get(Key).as_bool(value)
print del_files_bool

if del_files_bool : print 'HAHAHA'



