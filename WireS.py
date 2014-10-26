# ---------------------------------------------------------------------------------------------------------------------
# Аддон для рендера в режиме сетки (wireframe) в cycles с использованием freestyle
# Вариант 1: показывается процесс рендера, но не очищаются помеченные под freestyle ребра
# ---------------------------------------------------------------------------------------------------------------------

bl_info = {
    "name": "WireS",
    "category": "Render",
}

import bpy
from bpy.app.handlers import persistent


@persistent
def onrenderfinished(scene):
    # Обработчик после завершения рендера - необходимо декорировать через persistent
    # Глобальной функцией т.к. почему-то если делать методом класса -
    # добавляется в обработчик bpy.app.handlers.render_complete при каждом вызове скрипта
    # для всех объектов - снять выделение ребер freestyle
    current_active = scene.objects.active
    for elem in WireframeRender.bl_arr:
        bpy.context.scene.objects.active = elem
        # нужно очищать ребра, но вылетает с ошибкой
#        bpy.ops.object.mode_set(mode='EDIT')
#        bpy.ops.mesh.select_all(action='SELECT')
#        bpy.ops.mesh.mark_freestyle_edge(clear=True)
#        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = current_active
    # Удалить WireLineSet
    layers = bpy.context.scene.render.layers
    for layer in layers:
        layer.freestyle_settings.linesets.remove(layer.freestyle_settings.linesets["WireLineSet"])
    # выкл. freestyle
    bpy.context.scene.render.use_freestyle = False
    # удалить обработчик события
    bpy.app.handlers.render_complete.remove(onrenderfinished)
    bpy.app.handlers.render_cancel.remove(onrenderfinished)
    return {'FINISHED'}


class WireframeRender(bpy.types.Operator):
    """Wireframe Render"""
    bl_idname = "render.wireframe_render"   # уникальный id
    bl_label = "Wireframe Render"           # уникальное имя
    bl_arr = []                             # массив для обрабатываемых объектов

    def execute(self, context):
        # исполняемый модуль
        # вкл. freestyle
        context.scene.render.use_freestyle = True
        # для всех RenderLayer создать WireLineSet и включить Edge_mark
        layers = context.scene.render.layers
        for layer in layers:
            layer.freestyle_settings.linesets.new(name="WireLineSet")
            layer.freestyle_settings.linesets["WireLineSet"].select_edge_mark = True
        # для всех объектов - выделить ребра freestyle
        current_active = bpy.context.active_object
        objects = bpy.context.scene.objects
        for current_object in objects:
            for i, l in enumerate(bpy.context.scene.layers):
                # только для объектов на видимых слоях
                if current_object.layers[i] is True and current_object.layers[i] == l:
                    if current_object.type == "MESH" and current_object.hide is False and current_object.hide_render is False:
                        bpy.context.scene.objects.active = current_object
                        print(current_object.name)
                        self.bl_arr.append(current_object)    # добавить в массив
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.select_all(action='SELECT')    # выделить все рабра
                        bpy.ops.mesh.mark_freestyle_edge(clear=False)
                        bpy.ops.object.editmode_toggle()
        bpy.context.scene.objects.active = current_active
        # зарегистрировать обработчик после завершения рендера
        rendercompletehadler = bpy.app.handlers.render_complete
        if onrenderfinished not in rendercompletehadler:
            rendercompletehadler.append(onrenderfinished)
        rendercancelhadler = bpy.app.handlers.render_cancel
        if onrenderfinished not in rendercancelhadler:
            rendercancelhadler.append(onrenderfinished)
        # запустить рендер
        bpy.ops.render.render('INVOKE_DEFAULT')
        return {'FINISHED'}

# keymaps
addon_keymaps = []


def register():
    # регистрация класса
    bpy.utils.register_class(WireframeRender)
    # регистрация keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(WireframeRender.bl_idname, 'F12', 'PRESS', ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))


def unregister():
    # разрегистрация класса
    bpy.utils.unregister_class(WireframeRender)
    # разрегистрация keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
