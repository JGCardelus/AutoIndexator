def clean_tree(raw_tree, remove_plural):
    branch = raw_tree[-1]
    #TODO: Check further processing
    branch = list(branch)
    branch[0] = branch[0].lower()
    if remove_plural and branch[len(branch) - 1] == 's':
        #If the last letter of the branch is an 's', remove it
        branch.pop(len(branch) - 1) #Remove s
        
    branch = "".join(branch) #Reconvert to string

    return branch

def clean_name(raw_file_name):
    old_name, extension = get_extension(raw_file_name)
    old_name = remove_special_chars(old_name)
    file_name = convert_camel_casing(old_name)
    file_name += '.' + extension
    return file_name

def convert_camel_casing(raw_file):
    file_ = ''

    file_sections = raw_file.split(' ')
    for i, file_section in enumerate(file_sections):
        if i == 0:
            file_ += file_section.lower()
        else:
            if file_[len(file_) - 1] == '-':
                #If last chunk ends with '-' next letter must be lower
                #0-hello.txt
                file_ += file_section.lower()
            else:
                #If last char is not and '-' and file_name_chunk len == 1 then prefix '-'
                if len(file_section) == 1:
                    #somethingHuge-1.txt
                    file_ += '-'

                #If last chunk ends with no '-' next letter must start with upper
                #somethingHuge.txt
                file_ += file_section[0].upper() + file_section[1:].lower()

        if len(file_section) == 1 and (i + 1) != len(file_sections):
            #If chunk is a one letter character and it is not at the end
            file_ += '-'

    return file_

def remove_docType_extension(raw_file):
    docTypes = ["doc", "pdf", "vid"]
    raw_file = raw_file.split('_')
    if raw_file[-2] in docTypes:
        raw_file.pop(-2) #prefix_prefix_doc_name.extension

    file_ = "".join(raw_file)
    return file_

def remove_special_chars(file_):
    #Replace '_'
    list_chars = list(file_)
    for i in range(len(list_chars)):
        if list_chars[i] == chr(95):
            list_chars[i] = ' '

    file_ = "".join(list_chars)
    return file_

def get_extension(file_):
    #Remove extension
    file_parts = file_.split('.')
    extension = file_parts[1]
    name_ = file_parts[0]

    return name_, extension