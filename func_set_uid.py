
import pandas as pd

def set_uid(source_dict, warning):
    """ set_uid function : set unique study subject id
    
    set_uid function can be called by engineer to get the id list for a study
    cohort, and generate a unique id for populations from different data sources
    when multiple research centers are involved. it only read in the 'id' associated column from seperate files, 
    using the source file dictionary. 

    Arges:
        source_dict: source file dictionary object

    Returns:
        uid_pool: encoded unique id list for all the subjects involved in a study

    Raises:
        Error: fail to get file dictionary from source:
        Error: fail to get subject ids from file
    """

    uid_pool = []
    diff_uid_pool = []

    for source_key in source_dict.keys():# Loop through all sources
        try:
            
            file_dict = source_dict[source_key]# load file dictionaries for current data source
            source_key = str(source_key)# coerce source_key as string type
            uid_list_old = None # keep unique id list from last file by last iteration 
            for file_key in file_dict.keys():# loop through files 
                if not file_dict[file_key]['include']:
                    continue
                try:
                    
                    file_path = str(file_dict[file_key]['path'])
                    id_colname = str(file_dict[file_key]['keys']['id']['colname']) # get id columna name in current source file
                    id_df = pd.read_csv(file_path, usecols=[id_colname]) # read only id column from csv file
                    uid_list_new = list(map((source_key+'_').__add__, map(str,list(set(id_df[id_colname]))) )) # encode unique string uid list for this source file
                    print("-- source: "+source_key+' -- file: '+ file_path +' -- unique subjects #: '+str(len(uid_list_new)))
                    
                    if uid_list_old is None:# pass first file id list
                        uid_list_old = uid_list_new 
                        uid_list = uid_list_new
                        continue
                    else:
                        uid_list = list(set(uid_list_old).intersection(uid_list_new)) # find intersection of id lists from multiple files
                        diff_uid_list = list(set(list(set(uid_list_new)-set(uid_list)) + list(set(uid_list_old)-set(uid_list))))
                        print("-- source: "+source_key+ " -- intersection unique subjects #:"+str(len(uid_list)))
                        if len(diff_uid_list) != 0 and warning:
                            print( '-- Warning: subjects [ '+' '.join(diff_uid_list)+' ] are dropped!')

                except:
                    print('-- Error: fail to get subject ids from file: ' + file_path+' --')
                
                diff_uid_pool = list(diff_uid_pool) + list(diff_uid_list)
        
        except:
            print('- Error: fail to get file dictionary from source:' + str(source_key)+' -')

        uid_pool = list(uid_pool) + list(uid_list) # append current source uid_list to uid_pool

    return uid_pool, diff_uid_pool