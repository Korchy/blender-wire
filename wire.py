# Nikita Akimov
# interplanety@interplanety.org

from copy import copy
import functools
import os
import tempfile
import bpy


class Wire:

    _backup = {
        'var': {},
        'subdivision_modifiers': [],
        'selection': [],
        'restore_camera_view': False,
        'work_area_type': None,
    }
    _temp_mask_file_name = 'wireframe_mask.png'
    _wireframe_node_group_name = 'wireframe_node_group'

    @classmethod
    def wireframe_render(cls, context):
        # render with wireframe
        cls._backup_settings(context=context)
        cls._configure_scene_for_wireframe_render(context=context)
        bpy.ops.render.opengl()     # render wireframe mask
        wireframe_mask_file = os.path.join(tempfile.gettempdir(), cls._temp_mask_file_name)
        image = bpy.data.images['Render Result']
        image.save_render(filepath=wireframe_mask_file)
        if cls._temp_mask_file_name in bpy.data.images:
            bpy.data.images[cls._temp_mask_file_name].reload()
        else:
            bpy.data.images.load(filepath=wireframe_mask_file, check_existing=True)
        cls._restore_settings(context=context)
        # composite wireframe with render
        cls._composite_wireframe(context=context)

    @classmethod
    def _backup_settings(cls, context):
        # backup current settings
        cls._clear_backup()
        cls._backup['var']['wire'] = [context.preferences.themes[0].view_3d, copy(context.preferences.themes[0].view_3d.wire)]
        cls._backup['var']['film_transparent'] = [context.scene.render, copy(context.scene.render.film_transparent)]
        cls._backup['var']['type'] = [context.space_data.shading, copy(context.space_data.shading.type)]
        cls._backup['var']['light'] = [context.space_data.shading, copy(context.space_data.shading.light)]
        cls._backup['var']['color_type'] = [context.space_data.shading, copy(context.space_data.shading.color_type)]
        cls._backup['var']['single_color'] = [context.space_data.shading, copy(context.space_data.shading.single_color)]
        cls._backup['var']['background_type'] = [context.space_data.shading, copy(context.space_data.shading.background_type)]
        cls._backup['var']['background_color'] = [context.space_data.shading, copy(context.space_data.shading.background_color)]
        cls._backup['var']['show_ortho_grid'] = [context.space_data.overlay, copy(context.space_data.overlay.show_ortho_grid)]
        cls._backup['var']['show_floor'] = [context.space_data.overlay, copy(context.space_data.overlay.show_floor)]
        cls._backup['var']['show_axis_x'] = [context.space_data.overlay, copy(context.space_data.overlay.show_axis_x)]
        cls._backup['var']['show_axis_y'] = [context.space_data.overlay, copy(context.space_data.overlay.show_axis_y)]
        cls._backup['var']['show_axis_z'] = [context.space_data.overlay, copy(context.space_data.overlay.show_axis_z)]
        cls._backup['var']['show_cursor'] = [context.space_data.overlay, copy(context.space_data.overlay.show_cursor)]
        cls._backup['var']['show_text'] = [context.space_data.overlay, copy(context.space_data.overlay.show_text)]
        cls._backup['var']['show_annotation'] = [context.space_data.overlay, copy(context.space_data.overlay.show_annotation)]
        cls._backup['var']['show_extras'] = [context.space_data.overlay, copy(context.space_data.overlay.show_extras)]
        cls._backup['var']['show_relationship_lines'] = [context.space_data.overlay, copy(context.space_data.overlay.show_relationship_lines)]
        cls._backup['var']['show_outline_selected'] = [context.space_data.overlay, copy(context.space_data.overlay.show_outline_selected)]
        cls._backup['var']['show_bones'] = [context.space_data.overlay, copy(context.space_data.overlay.show_bones)]
        cls._backup['var']['show_motion_paths'] = [context.space_data.overlay, copy(context.space_data.overlay.show_motion_paths)]
        cls._backup['var']['show_object_origins'] = [context.space_data.overlay, copy(context.space_data.overlay.show_object_origins)]
        cls._backup['var']['show_wireframes'] = [context.space_data.overlay, copy(context.space_data.overlay.show_wireframes)]
        cls._backup['var']['file_format'] = [context.scene.render.image_settings, copy(context.scene.render.image_settings.file_format)]
        for obj in bpy.data.objects:
            if context.preferences.addons[__package__].preferences.use_optimal_display:
                if 'Subdivision' in obj.modifiers:
                    for modifier in obj.modifiers:
                        if modifier.name == 'Subdivision':
                            cls._backup['subdivision_modifiers'].append([modifier, copy(modifier.show_only_control_edges)])
            if obj.select_get():
                cls._backup['selection'].append(obj)
        if context.space_data.region_3d.view_perspective != 'CAMERA':
            cls._backup['restore_camera_view'] = True

    @classmethod
    def _clear_backup(cls):
        # clear backup data
        cls._backup['var'] = {}
        cls._backup['subdivision_modifiers'] = []
        cls._backup['selection'] = []
        cls._backup['restore_camera_view'] = False
        cls._backup['work_area_type'] = None

    @classmethod
    def _restore_settings(cls, context):
        # restore settings from the backup
        for preference in cls._backup['var']:
            setattr(cls._backup['var'][preference][0], preference, cls._backup['var'][preference][1])
        if context.preferences.addons[__package__].preferences.use_optimal_display:
            for modifier in cls._backup['subdivision_modifiers']:
                modifier[0].show_only_control_edges = modifier[1]
        for obj in cls._backup['selection']:
            obj.select_set(True)
        if cls._backup['restore_camera_view']:
            bpy.ops.view3d.view_camera()
        bpy.data.images['Render Result'].render_slots.active_index = 0

    @classmethod
    def _configure_scene_for_wireframe_render(cls, context):
        # configure scene for wireframe render - all white, wireframe - black
        context.preferences.themes[0].view_3d.wire = (0.0, 0.0, 0.0)
        context.scene.render.film_transparent = False
        for obj in bpy.data.objects:
            if context.preferences.addons[__package__].preferences.use_optimal_display:
                if 'Subdivision' in obj.modifiers:
                    for modifier in obj.modifiers:
                        if modifier.name == 'Subdivision':
                            modifier.show_only_control_edges = True
            obj.select_set(False)
        context.space_data.shading.type = 'SOLID'
        context.space_data.shading.light = 'FLAT'
        context.space_data.shading.color_type = 'SINGLE'
        context.space_data.shading.single_color = (1.0, 1.0, 1.0)
        context.space_data.shading.background_type = 'VIEWPORT'
        context.space_data.shading.background_color = (1.0, 1.0, 1.0)
        context.space_data.overlay.show_ortho_grid = False
        context.space_data.overlay.show_floor = False
        context.space_data.overlay.show_axis_x = False
        context.space_data.overlay.show_axis_y = False
        context.space_data.overlay.show_axis_z = False
        context.space_data.overlay.show_cursor = False
        context.space_data.overlay.show_text = False
        context.space_data.overlay.show_annotation = False
        context.space_data.overlay.show_extras = False
        context.space_data.overlay.show_relationship_lines = False
        context.space_data.overlay.show_outline_selected = False
        context.space_data.overlay.show_bones = False
        context.space_data.overlay.show_motion_paths = False
        context.space_data.overlay.show_object_origins = False
        context.space_data.overlay.show_wireframes = True
        if context.space_data.region_3d.view_perspective != 'CAMERA':
            bpy.ops.view3d.view_camera()
        bpy.data.images['Render Result'].render_slots.active_index = 1  # render to slot 2
        context.scene.render.image_settings.file_format = 'PNG'

    @classmethod
    def _composite_wireframe(cls, context):
        # composite wireframe with render
        if not context.scene.use_nodes:
            context.scene.use_nodes = True
        # split window to show compositor and render result
        current_area = context.area
        cls._backup['work_area_type'] = current_area.type
        bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5)
        new_area = context.screen.areas[-1]
        current_area.ui_type = 'CompositorNodeTree'
        new_area.type = 'IMAGE_EDITOR'
        new_area.spaces.active.image = bpy.data.images['Render Result']
        # modify compositing node tree
        if cls._wireframe_node_group_name not in context.scene.node_tree.nodes:
            # group
            group_node_tree = bpy.data.node_groups.new(type='CompositorNodeTree', name=cls._wireframe_node_group_name)
            group_node_tree.inputs.new(type='NodeSocketColor', name='Image')
            group_node_alpha_input = group_node_tree.inputs.new(type='NodeSocketFloat', name='Alpha')
            group_node_alpha_input.default_value = 1.0
            group_node_tree.outputs.new(type='NodeSocketColor', name='Image')
            group_input_node = group_node_tree.nodes.new(type='NodeGroupInput')
            group_input_node.location = (-800.0, 0.0)
            group_output_node = group_node_tree.nodes.new(type='NodeGroupOutput')
            group_output_node.location = (200.0, 0.0)
            group_node = context.scene.node_tree.nodes.new(type='CompositorNodeGroup')
            group_node.node_tree = group_node_tree
            group_node.name = cls._wireframe_node_group_name
            composite_node = next(iter([node for node in context.scene.node_tree.nodes if node.bl_idname == 'CompositorNodeComposite']), None)
            group_node.location = (composite_node.location.x, composite_node.location.y + 150)
            link_to_composite = next(iter(composite_node.inputs['Image'].links), None)
            if link_to_composite:
                socket_to_composite = link_to_composite.from_socket
                context.scene.node_tree.links.remove(link_to_composite)
                context.scene.node_tree.links.new(socket_to_composite, group_node.inputs['Image'])
            else:
                unlinked_render_layers_node = next(iter([node for node in context.scene.node_tree.nodes if node.bl_idname == 'CompositorNodeRLayers' and node.outputs['Image'].is_linked is False]), None)
                if unlinked_render_layers_node:
                    context.scene.node_tree.links.new(unlinked_render_layers_node.outputs['Image'], group_node.inputs['Image'])
            render_layers_node = next(iter([node for node in context.scene.node_tree.nodes if node.bl_idname == 'CompositorNodeRLayers']), None)
            if render_layers_node:
                context.scene.node_tree.links.new(render_layers_node.outputs['Alpha'], group_node.inputs['Alpha'])
            context.scene.node_tree.links.new(group_node.outputs['Image'], composite_node.inputs['Image'])
            # group nodes
            image_node = group_node_tree.nodes.new(type='CompositorNodeImage')
            # image_node.image = wireframe_mask_image
            image_node.image = bpy.data.images[cls._temp_mask_file_name]
            image_node.location = (-600.0, 500.0)
            alpha_over_node_1 = group_node_tree.nodes.new(type='CompositorNodeAlphaOver')
            alpha_over_node_1.location = (-400.0, 200.0)
            alpha_over_node_1.inputs[1].default_value = context.preferences.addons[__package__].preferences.wire_color
            group_node_tree.links.new(image_node.outputs['Image'], alpha_over_node_1.inputs['Fac'])
            group_node_tree.links.new(group_input_node.outputs['Image'], alpha_over_node_1.inputs[2])
            alpha_over_node_2 = group_node_tree.nodes.new(type='CompositorNodeAlphaOver')
            alpha_over_node_2.location = (-200.0, 0.0)
            group_node_tree.links.new(alpha_over_node_1.outputs['Image'], alpha_over_node_2.inputs[2])
            group_node_tree.links.new(group_input_node.outputs['Image'], alpha_over_node_2.inputs[1])
            group_node_tree.links.new(group_input_node.outputs['Alpha'], alpha_over_node_2.inputs['Fac'])
            group_node_tree.links.new(alpha_over_node_2.outputs['Image'], group_output_node.inputs['Image'])
        else:
            alpha_over_node_1 = next(iter([node for node in context.scene.node_tree.nodes[cls._wireframe_node_group_name].node_tree.nodes if node.bl_idname == 'CompositorNodeAlphaOver' and node.inputs[1].is_linked is False]))
            if alpha_over_node_1:
                alpha_over_node_1.inputs[1].default_value = context.preferences.addons[__package__].preferences.wire_color
        # join splited window and return previous type (by timer to make an update interval)
        override_context = context.copy()
        override_context['area'] = current_area
        bpy.app.timers.register(functools.partial(cls._restore_work_area_type, current_area, new_area, override_context), first_interval=0.5)

    @classmethod
    def _restore_work_area_type(cls, current_area, new_area, override_context):
        # join splitted areas and return previous area type
        if bpy.app.version[:2] == (2, 80):
            # 2.80
            bpy.ops.screen.area_join(override_context, min_x=current_area.x, min_y=current_area.y, max_x=new_area.x, max_y=new_area.y)
        else:
            # 2.81
            bpy.ops.screen.area_join(override_context, cursor=(current_area.x, current_area.y + current_area.width + 1))
        if cls._backup['work_area_type']:
            current_area.type = cls._backup['work_area_type']

    @classmethod
    def clear_composite_wireframe(cls, context):
        # clear composite wireframe setup
        wireframe_group = next(iter([node for node in context.scene.node_tree.nodes if node.name == cls._wireframe_node_group_name]), None)
        if wireframe_group:
            image_link = next(iter(wireframe_group.inputs['Image'].links), None)
            socket_to_composite = None
            if image_link:
                socket_to_composite = image_link.from_socket
            context.scene.node_tree.nodes.remove(wireframe_group)   # remove wireframe node group
            composite_node = next(iter([node for node in context.scene.node_tree.nodes if node.bl_idname == 'CompositorNodeComposite' and node.inputs['Image'].is_linked is False]), None)
            if composite_node:
                context.scene.node_tree.links.new(socket_to_composite, composite_node.inputs['Image'])
