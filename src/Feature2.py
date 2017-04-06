#
# Identify the 10 resources that consume the most bandwidth on the site
# Part 1: resource_count() calculate each resource consumption (i.e., frequency * bytes)
# Part 2: top10_resource() get the top 10 resources and consumption
#  #

import traceback
import operator

from utility import write_to_file


#
# count resource
#
def resource_count(resource_table, resource, resource_bytes):
    resource = resource.replace(" HTTP/1.0", "")
    if resource not in resource_table:
        resource_table[resource] = resource_bytes
    else:
        resource_table[resource] += resource_bytes
    return resource_table


#
# write top 10 resource to file
#
def top10_resource(resource_table):
    try:
        for line in resource_table.most_common(10):
            write_to_file('log_output/resources.txt', line[0])
    except ValueError:
        traceback.print_exc()

