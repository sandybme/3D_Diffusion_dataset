import bpy
import os
import random
from mathutils import Euler

# Set the background color to white
bpy.data.worlds['World'].node_tree.nodes['Background'].inputs[0].default_value = (1, 1, 1, 1)

# Make sure the film is not transparent
bpy.context.scene.render.film_transparent = False

# Disable environmental effects in Eevee
bpy.context.scene.eevee.use_gtao = False
bpy.context.scene.eevee.use_bloom = False
bpy.context.scene.eevee.use_ssr = False
bpy.context.scene.eevee.use_ssr_refraction = False

# Add camera and set its location and rotation
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 10), rotation=(0, 0, 0))
bpy.context.scene.camera = bpy.context.object
camera = bpy.data.objects['Camera']
camera.location = (1.5562241077423096, -1.2653920650482178, 0.6461033821105957)

# Define Euler angles and set camera rotation
euler_angles = Euler((1.2442104816436768, 0.06100957468152046, 0.9029533863067627), 'XYZ')
camera.rotation_mode = 'XYZ'  # Set rotation mode
camera.rotation_euler = euler_angles

# Function to generate a random color
def generate_random_color():
    while True:
        color = [random.random() for _ in range(3)] + [1.0]  # RGB + Alpha
        if color[0] != color[1] or color[1] != color[2] or color[0] not in (1.0, 0.5):
            break
    return color

# Function to import an object from a file
def import_object(file_path):
    if file_path.endswith('.obj'):
        bpy.ops.import_scene.obj(filepath=file_path)
    elif file_path.endswith('.ply'):
        bpy.ops.wm.ply_import(filepath=file_path)

# Function to render an object and save the image
def render_and_save(obj_name, output_path):
    obj = bpy.data.objects.get(obj_name)
    if obj is None:
        print(f"Object '{obj_name}' not found.")
        return
    
    # Create and assign a random color material
    mat = bpy.data.materials.new(name=f"{obj_name}_Material")
    mat.diffuse_color = generate_random_color()
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    
    # Set the render resolution
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    
    # Render the image
    bpy.ops.render.render(write_still=True)
    
    # Save the rendered image
    bpy.data.images['Render Result'].save_render(filepath=output_path)

# Main function to render each object in the list
def main():
    # Set the path for the output folder
    output_folder = "/Users/Sandhanakrishnan/Desktop/Render/"
    
    # Set the directory containing the object files
    object_directory = "/Users/Sandhanakrishnan/Desktop/input/"
    
    # Get a list of all files in the object directory
    object_files = [os.path.join(object_directory, file) for file in os.listdir(object_directory)]
    
    # Filter the list to include only object files
    object_files = [file for file in object_files if file.endswith(('.obj', '.ply'))]
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Import and render each object
    for file_path in object_files:
        obj_name = os.path.splitext(os.path.basename(file_path))[0]  # Extract object name from file path
        import_object(file_path)
        output_path = os.path.join(output_folder, f"{obj_name}_render.png")
        render_and_save(obj_name, output_path)
        print(f"Rendered and saved: {output_path}")

if __name__ == "__main__":
    main()
