bl_info = {
    "name": "Automatic Normal & AO Maps",
    "category": "Material"
}

import bpy
import os

# To Do:
# Add error detection clauses; Right now it just spits out debug if anything
# isn't properly configured. It should tell you why it's breaking.


def CreateImage():
    ''' Creates a new image in blender '''
    image = bpy.data.images.new(name = 'Untitled',width = 4096, height = 4096)
    return image

def AddImageToMaterial(myImage):
    ''' Adds an image texture to the active object material'''
    # Create new image texture
    texture = bpy.data.textures.new(name = 'Map', type = 'IMAGE')
    # Assign my image to it
    texture.image = myImage
    # Acquire the active object
    object = bpy.context.active_object
    # Get the active object's first material
    material = object.data.materials['Material']
    # Add a new texture slot
    materialTexture = material.texture_slots.add()
    # Set to 'texture'
    materialTexture.texture = texture
    
    # Set image to active UV layer
    for uv_face in object.data.uv_textures.active.data:
        uv_face.image = myImage
    # Fix the circular reference stack error by disabling this texture
    material.use_textures[0] = False
    
    
def UVUnwrapActive():
    ''' UV Unwraps the active object '''
    print('UV unwrapping active object...')
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.uv.unwrap()
    print('Unwrapped successfully.')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
def SaveImage(name,image):
    ''' Save provided image with provided name in file directory '''
    print('Saving,"%s"...' % name) 
    image.filepath_raw = "//" + name + ".png"
    image.file_format = 'PNG'
    image.save()
    print('"%s",Saved!' % name)
    
def BakeNormal(image):
    ''' Bake the selected objects normals to the active object texture '''
    print('Baking normals...')
    # Set bake type to normal
    bpy.data.scenes["Scene"].render.bake_type = 'NORMALS'
    # Set normal space to 'tangent'
    bpy.data.scenes["Scene"].render.bake_normal_space = 'TANGENT'
    # Enable 'Bake Selected to Active'
    bpy.data.scenes["Scene"].render.use_bake_selected_to_active = True
    # Bake Normal Map!
    bpy.ops.object.bake_image()
    print('Normals baked successfully.')
    print('Saving normal map...')
    # Save the normal map file
    SaveImage('Normal',image)
    print('Normal map saved.')
    
def BakeAO(image):
    ''' Bake the selected objects AO to the active object texture '''
    print('Baking AO...')
    # Set bake type to 'AO'
    bpy.data.scenes["Scene"].render.bake_type = 'AO'
    # Enable 'Bake Selected to Active'
    bpy.data.scenes["Scene"].render.use_bake_selected_to_active = True
    # Bake AO Map!
    bpy.ops.object.bake_image()
    print('AO baked successfully.')
    print('Saving AO map...')
    SaveImage('AO',image)
    print('AO map saved.')

def GeneratePlane():
    ''' Creates a plane for the baking to be done to '''
    # Get current active object
    object = bpy.context.active_object
    # Create plane, this will swap the plane to the new active
    bpy.ops.mesh.primitive_plane_add()
    aObject = bpy.context.active_object
    aObject.scale = (2,2,1)
    # Create material & add to plane
    material = bpy.data.materials.new('Material')
    aObject.data.materials.append(material)
    # Set the old active to a selected object
    object.select = True
    
class AutomaticMaps(bpy.types.Operator):
    ''' Automated Normal & AO Map Generation Operator '''
    # ID for the UI
    bl_idname = 'object.map_generation'
    # Display name in the UI
    bl_label = 'Automatic Normal & AO'
    # Enable registering this operator
    bl_options = {'REGISTER'}
    
    def execute(self,context):
        ''' Execute this operator '''
        GeneratePlane()
        UVUnwrapActive()
        mapImage = CreateImage()
        AddImageToMaterial(mapImage)
        BakeNormal(mapImage)
        BakeAO(mapImage)
        return {'FINISHED'}
        
        
        
def register():
    ''' Register 'AutomaticMaps' operator '''
    bpy.utils.register_class(AutomaticMaps)


def unregister():
    ''' Unregister 'AutomaticMaps' operator '''
    bpy.utils.unregister_class(AutomaticMaps)
    
    
if __name__ == '__main__':
    register()