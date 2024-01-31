import bpy

from src.operators.create_id_mask import CreateIDMaskOperator
from src.operators.id_editor_create_id import IDEDITOR_CreateIDOperator
from src.operators.id_editor_paint import IDEDITOR_PaintIDMaskOperator
from src.operators.id_editor_remove_id import IDEDITOR_RemoveIDOperator
from src.types.colors import get_color


class IDMaskEditorPanel(bpy.types.Panel):
    bl_idname = "ID_MASK_EDITOR_PT_Panel"
    bl_label = "ID Mask Editor"
    bl_category = "Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False

        if not context.object.type == 'MESH':
            return False

        return context.object.mode == "EDIT"

    def draw(self, context):
        layout = self.layout
        layout.use_property_decorate = True

        mesh = context.object.data
        properties = mesh.id_mask_editor_properties

        target_attribute_row = layout.row(align=True)
        has_attribute = properties.target_attribute

        target_attribute_row.prop_search(
            properties,
            'target_attribute',
            mesh,
            'color_attributes',
            icon='GROUP_VCOL'
        )
        target_attribute_row.operator(CreateIDMaskOperator.bl_idname, icon='ADD', text="")

        if not has_attribute:
            return

        layout.prop(properties, "colors")
        color = get_color(properties.colors)
        self.draw_options(context, layout, properties, color)

        layout.separator()

        row = layout.row()

        col = row.column()
        col.operator(IDEDITOR_PaintIDMaskOperator.bl_idname, icon='VPAINT_HLT')
        col.template_list(
            'IDMaskEditorIDList',
            'IDMaskEditorIDList',
            properties,
            'possible_ids',
            properties,
            'active_id',
            rows=3
        )

        col = row.column(align=True)
        col.operator(IDEDITOR_CreateIDOperator.bl_idname, icon='ADD', text="")
        col.operator(IDEDITOR_RemoveIDOperator.bl_idname, icon='REMOVE', text="")



    def draw_options(self, context, layout, props, element):

        has_render_ui = 'render_ui' in dir(element)
        has_connected_properties = 'connected_properties' in dir(element) and len(element.connected_properties) > 0

        if not has_render_ui and not has_connected_properties:
            return

        object_box = layout.box()

        if has_render_ui:
            element.render_ui(context, object_box, props)
            return

        for setting in element.connected_properties:
            object_box.prop(props, setting)