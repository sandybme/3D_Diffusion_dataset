import bpy # use in blender scripting
import random

# Set the world background to white
bpy.data.worlds['World'].node_tree.nodes['Background'].inputs[0].default_value = (1, 1, 1, 1)

# Make sure the film is not transparent
bpy.context.scene.render.film_transparent = False

# If using Eevee, disable any environmental effects that may affect the background color
bpy.context.scene.eevee.use_gtao = False
bpy.context.scene.eevee.use_bloom = False
bpy.context.scene.eevee.use_ssr = False
bpy.context.scene.eevee.use_ssr_refraction = False


def generate_random_color():
    # Keep generating a color until it is neither white nor gray
    while True:
        color = [random.random() for _ in range(3)] + [1.0]  # RGB + Alpha
        # Check if the color is not white or gray (all channel values are the same)
        if color[0] != color[1] or color[1] != color[2] or color[0] not in (1.0, 0.5):
            break
    return color
obj = bpy.context.view_layer.objects.active
mat = bpy.data.materials.new(name="RandomColorMaterial")
mat.diffuse_color = generate_random_color()  # Set the color
obj.data.materials.append(mat)

# Assign it to the object
obj = bpy.context.view_layer.objects.active
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)

# Set the render resolution
bpy.context.scene.render.resolution_x = 512
bpy.context.scene.render.resolution_y = 512
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Assuming that the object is already at the desired angle and the camera is looking at it,
# If not, you would need to manually set the camera angle to match the picture's angle

# Render the image
bpy.ops.render.render(write_still=True)

# Specify the path to save the rendered image
rendered_image_path = '/Users/Sandhanakrishnan/Desktop/rendered_image.png'
bpy.data.images['Render Result'].save_render(filepath=rendered_image_path)
