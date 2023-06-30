import re
import glob

def general_ocr_corrections(input_path, output_path, lan):
    for file in glob.glob(input_path + '//' + "*.txt"):
        #language = file.split('/')[-3]
        language = lan
        filename = file.split('/')[-1]
        with open(file, 'r', encoding = 'utf8') as txt_input:
            with open(output_path + '//' + filename, 'w', encoding = 'utf8') as text_output:
                txt_input_data = txt_input.read()
                txt_output = re.sub(r'(?m)(\w|,|;|\s+|\'|\’)(~|_|=|\|)?(-+|—+)(\s+)?(\|+[^a-zA-Z0-9 ]+?)?$[\r\n]+', '\\1', txt_input_data) #De-hyphenation END LINE REGEX
                txt_output = re.sub(r'(?m)^([^a-zA-Z0-9 \|\s]+?)?(-+|—+)', ' ', txt_output) #De-hyphenation BEGIN LINE REGEX
                txt_output = re.sub(r'(?m)([a-zé]|,|;|\s+|\'|\’)(~|_|=)?(\|+)([^a-zA-Z0-9 ]+?)?$', ' ', txt_output) #De-pipization END LINE REGEX
                txt_output = re.sub(r'(?m)^([^a-zA-Z0-9 \|]+?)?(\|+)', ' ', txt_output) #begin-line depipization
                txt_output = re.sub(r'(?m)^[0-9]+([^a-zA-Z0-9 \|]+?)?$', '', txt_output) #get rid of page n rows
                txt_output = re.sub(r'(?m)(?<!\.|\)|\]|[A-Z])\n', ' ', txt_output) #get rid of single linebreaks when they are not preceded by a full stop
                txt_output = re.sub(r'(?m)(?<=[a-z])\n(?=^(\s+)?[a-z])', ' ', txt_output) #remove line breaks if two contiguous lines a and b meet these conditions:    last char of a is a lower-case alphabetic character, first char of b is a lower case char or space.
                #txt_output = re.sub(r'(?m)(?<=[Mr\.])\n(?=^[A-Z])', ' ', txt_output) #remove line breaks between 2 lines a and b if a ends with 'Mr.', 'Miss.', 'Mrs.' and b begins with upper case letter.
                txt_output = re.sub(r'(?m)( \= | \_ | \© | \~ | \} | \+ | \] | \¢ | \{ | \& | \\ | \/ | \§ | \# | \™ | \[ | \> | \¥ | \< | \% | \® | \€ | \* )', ' ', txt_output) #get rid 'safely' of UFO characters (when they are preceded and followed by a space)
                txt_output = re.sub(r'(?m) {2,}', ' ', txt_output) #get rid 'safely' of extra space chars
                txt_output = re.sub(r'(?m)(\-\s?\.\s)([a-z])', '\\2', txt_output) #fixing hyphen-dot-space issue
                txt_output = re.sub(r'(?m)^\s', '', txt_output)  # fixing hyphen-dot-space issue
                txt_output = re.sub(r'(?m)(?<=Mr\.)\n(?=^(\s+)?[A-Z])', ' ', txt_output) #remove line breaks between 2 lines a and b if a ends with 'Mr.', and b begins with upper case letter.
                txt_output = re.sub(r'(?m)(?<=Mrs\.)\n(?=^(\s+)?[A-Z])', ' ', txt_output) #remove line breaks between 2 lines a and b if a ends with 'Mrs.' and b begins with upper case letter.
                txt_output = re.sub(r'(?m)(?<=Miss\.)\n(?=^(\s+)?[A-Z])', ' ', txt_output) #remove line breaks between 2 lines a and b if a ends with 'Miss.' and b begins with upper case letter.
                if (language == 'EN') or (language == 'ES'):
                    text_output.write(txt_output)
                elif language == 'FR':
                    txt_output = re.sub(r'(\|)(\s?)(\'|\’)(?!$)', 'l\'', txt_output) #transforming "|'" into "l'"
                    text_output.write(txt_output)
                elif language == 'IT':
                    txt_output = re.sub(r'(\|)(\s?)(\'|\’)(?!$)', 'l\'', txt_output) #transforming "|'" into "l'"
                    txt_output = re.sub(r'(\s|é)@\s', ' é ', txt_output)
                    txt_output = re.sub(r' é ', ' è ', txt_output)
                    text_output.write(txt_output)
