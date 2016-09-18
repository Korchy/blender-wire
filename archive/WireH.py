# ---------------------------------------------------------------------------------------------------------------------
# Альтернативная версия аддона
# Для работы рекомендуется использование аддона WireS !
# ---------------------------------------------------------------------------------------------------------------------
# Аддон для рендера в режиме сетки (wireframe) в cycles с использованием freestyle
# Вариант H: Не показывать процесс рендера, зато без ошибок очищаются ребра помеченные под freestyle
# ---------------------------------------------------------------------------------------------------------------------

bl_info = {
    "name": "WireH",
    "category": "Render",
}

import bpy
from bpy.app.handlers import persistent
import time


@persistent
def onrenderfinished(scene):
    global is_render_finished
    is_render_finished = True
    return {'FINISHED'}


class WireframeRender(bpy.types.Operator):
    """Wireframe Render"""
    bl_idname = "render.wireframe_render"
    bl_label = "Wireframe Render"
    bl_arr = []

    def onrenderfinished(self):
        current_active = bpy.context.active_object
        for elem in self.bl_arr:
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
        global is_render_finished
        is_render_finished = False
        bpy.ops.render.render('INVOKE_DEFAULT')
        while is_render_finished is False:
          time.sleep(0.2)
        self.onrenderfinished()
        return {'FINISHED'}

addon_keymaps = []


def register():
    bpy.utils.register_class(WireframeRender)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(WireframeRender.bl_idname, 'F12', 'PRESS', ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(WireframeRender)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
