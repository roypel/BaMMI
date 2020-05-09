

def parse_feelings(context, snapshot):
    if 'feelings' not in snapshot:
        raise KeyError("Snapshot is missing the Feelings data")
    return context.format_returned_data('feelings', snapshot['feelings'])


parse_feelings.field = 'feelings'
