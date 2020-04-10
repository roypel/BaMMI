

def parse_pose(context, snapshot):
    if 'pose' not in snapshot:
        raise KeyError("Snapshot is missing the Pose data")
    pose_data = snapshot['pose']
    if 'translation' not in pose_data:
        raise KeyError("Snapshot is missing the Translation data")
    if 'rotation' not in pose_data:
        raise KeyError("Snapshot is missing the Rotation data")
    return {k: v for k, v in snapshot.items() if k in ['pose', 'datetime']}


parse_pose.field = 'pose'
