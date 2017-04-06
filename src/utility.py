import re

import datetime
import traceback


def line_split(line):
    # a='199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245'
    result = ()
    try:
        delimiters = " - - [", " -0400] \"GET ", " -0400] \"POST ", " -0400] \"HEAD ", "]", "\""
        regex_pattern = '|'.join(map(re.escape, delimiters))
        split0 = re.split(regex_pattern, line)
        split1 = split0[-1].strip(' ').strip('\n').split(" ")
        if len(split1) == 2:
            split1[-1] = split1[-1].replace('-', '0')
            split1[-1] = int(split1[-1])
        split0.pop()
        if split0[-1].strip(' ') == "HTTP/1.0":
            split0.pop()
        split2 = split0 + split1

        if len(split2) == 5:
            result = split2
        else:
            result = split2 + [0]

        if len(result) == 5:
            return result
    except:
        pass
    return (None, None, None, None, None)

#
#
#
def time_dif_in_sec(start_time, end_time):
    try:
        # import datetime as dt
        fmt = '%d/%b/%Y:%H:%M:%S'
        d1 = datetime.datetime.strptime(start_time, fmt)
        d2 = datetime.datetime.strptime(end_time, fmt)

        diff = d2 - d1
        diff_sec = diff.total_seconds()
        return diff_sec
    except ValueError:
        traceback.print_exc()


#
#write line to file end
#
def write_to_file(file_path,line):
    try:
        with open(file_path, 'a') as file:
            file.writelines(line+"\n")
    except IOError:
        traceback.print_exc()