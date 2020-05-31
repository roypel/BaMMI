from PIL import Image as PILIm


def parse_color_image(context, snapshot):
    if 'color_image' not in snapshot:
        raise KeyError("Snapshot is missing the Color Image data")
    save_path = context.generate_path('color_image.jpg')
    size = snapshot['color_image']['width'], snapshot['color_image']['height']
    image_data_path = snapshot['color_image']['data']
    import os
    print(f"WE're HERE: {os.getcwd()} we see: {os.listdir('/usr/src/BaMMI')} and above us: {os.listdir('..')}")
    print(f"DATA IS HERE: {os.listdir(os.path.dirname(f'{image_data_path}/../../..'))}")
    with open(image_data_path, 'rb') as f:
        image_data = f.read()
    image = PILIm.new('RGB', size)
    image.frombytes(image_data)
    image.save(save_path)
    return context.format_returned_data('color_image', save_path)


parse_color_image.field = 'color_image'
