

def parse_pose(context, snapshot):
    if 'pose' not in snapshot:
        raise KeyError("Snapshot is missing the Pose data")
    pose_data = snapshot['pose']
    if 'translation' not in pose_data:
        raise KeyError("Snapshot is missing the Translation data")
    if 'rotation' not in pose_data:
        raise KeyError("Snapshot is missing the Rotation data")
    return context.format_returned_data('pose', snapshot['pose'])


parse_pose.field = 'pose'
