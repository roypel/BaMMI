from PIL import Image as PILIm


def parse_color_image(context, snapshot):
    if 'color_image' not in snapshot:
        raise KeyError("Snapshot is missing the Color Image data")
    path = context.path('color_image.jpg')
    size = snapshot['color_image']['width'], snapshot['color_image']['height']
    image_data_path = snapshot['color_image']['data']
    with open(image_data_path, 'rb') as f:
        image_data = f.read()
    # TODO: Fix cuz it ain't working
    image = PILIm.new('RGB', size)
    image.putdata(image_data)
    image.save(path)
    return context.format_returned_data('color_image', path)


parse_color_image.field = 'color_image'
