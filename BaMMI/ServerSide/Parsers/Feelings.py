

def parse_pose(context, snapshot):
    if 'feelings' not in snapshot:
        raise KeyError("Snapshot is missing the Feelings data")
    return {k: v for k, v in snapshot.items() if k in ['feelings', 'datetime']}


parse_pose.field = 'feelings'
