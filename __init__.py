# Nikita Akimov
# interplanety@interplanety.org

from .addon import Addon
import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "Wire",
    'category': 'Render',
    'author': 'Nikita Akimov',
    'version': (0, 0, 1),
    'blender': (2, 78, 0),
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-wire/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-wire/',
    'description': 'Allows render with wireframe'
}


@persistent
def onrenderfinished(scene):
    sceneupdateposthadler = bpy.app.handlers.scene_update_post
    if onsceneupdatepost not in sceneupdateposthadler:
        sceneupdateposthadler.append(onsceneupdatepost)
    return {'FINISHED'}


@persistent
def onsceneupdatepost(scene):
    bpy.app.handlers.scene_update_post.remove(onsceneupdatepost)
    current_active = scene.objects.active
    for elem in WireframeRender.bl_arr:
        bpy.context.scene.objects.active = elem
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_freestyle_edge(clear=True)
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = current_active
    layers = bpy.context.scene.render.layers
    for layer in layers:
        layer.freestyle_settings.linesets.remove(layer.freestyle_settings.linesets["WireLineSet"])
    bpy.context.scene.render.use_freestyle = False
    bpy.app.handlers.render_complete.remove(onrenderfinished)
    bpy.app.handlers.render_cancel.remove(onrenderfinished)
    return {'FINISHED'}


class WireframeRender(bpy.types.Operator):
    """Wireframe Render"""
    bl_idname = "render.wireframe_render"
    bl_label = "Wireframe Render"
    bl_arr = []

    def execute(self, context):
        context.scene.render.use_freestyle = True
        layers = context.scene.render.layers
        for layer in layers:
            layer.freestyle_settings.linesets.new(name="WireLineSet")
            layer.freestyle_settings.linesets["WireLineSet"].select_edge_mark = True
        current_active = bpy.context.active_object
        objects = bpy.context.scene.objects
        for current_object in objects:
            for i, l in enumerate(bpy.context.scene.layers):
                if current_object.layers[i] is True and current_object.layers[i] == l:
                    if current_object.type == "MESH" and current_object.hide is False and current_object.hide_render is False:
                        bpy.context.scene.objects.active = current_object
                        self.bl_arr.append(current_object)
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.mesh.mark_freestyle_edge(clear=False)
                        bpy.ops.object.editmode_toggle()
        bpy.context.scene.objects.active = current_active
        rendercompletehadler = bpy.app.handlers.render_complete
        if onrenderfinished not in rendercompletehadler:
            rendercompletehadler.append(onrenderfinished)
        rendercancelhadler = bpy.app.handlers.render_cancel
        if onrenderfinished not in rendercancelhadler:
            rendercancelhadler.append(onrenderfinished)
        bpy.ops.render.render('INVOKE_DEFAULT')
        return {'FINISHED'}


addon_keymaps = []


def register():
    if not Addon.dev_mode():
        bpy.utils.register_class(WireframeRender)
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(WireframeRender.bl_idname, 'F12', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        bpy.utils.unregister_class(WireframeRender)
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
