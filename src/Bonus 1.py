def top10_resource_visiting_time(top10_table , full_table):
    for top_records in top10_table:
        if top_records in full_table:
            top10_resource_log[top_records] = bytes
    return top10_resource_log


def full_record(full_table , address , log_time , resource):
    if address in full_table:
        address_log[address].append ( log_time )
    else:
        address_log[address] = [log_time]
    if resource in full_table:
        resource_log[resource].append ( log_time )
    else:
        resource_log[resource] = [log_time]
    return full_table,ddress_log,resource_log

#full_table=address_log=resource_log = Counter ()
#full_table , address_log , resource_log = full_record ( full_table , address , log_time , resource )