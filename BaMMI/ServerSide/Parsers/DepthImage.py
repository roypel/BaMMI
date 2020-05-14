import matplotlib.pyplot as plt
import numpy as np


def parse_depth_image(context, snapshot):
    if 'depth_image' not in snapshot:
        raise KeyError("Snapshot is missing the Depth Image data")
    path = context.path('depth_image.jpg')
    depth_image = np.fromfile(snapshot['depth_image']['data'], dtype=float)
    depth_image = np.reshape(depth_image, (snapshot['depth_image']['height'], snapshot['depth_image']['width']))
    plt.imsave(path, depth_image, cmap='hot')
    return context.format_returned_data('depth_image', path)


parse_depth_image.field = 'depth_image'
