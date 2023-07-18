from h2o_wave import ui
from .layout import render_template

async def setting_page(q, details=None):
    save_buttons = [
        ui.buttons(justify='end', items=[
            ui.button(name='config_save', label='Save', primary=True),
            ui.button(name='config_reset', label='Reset', primary=True)
        ])]
    setting_items = [
        ui.textbox(name='client_title',
                   label='Client Title',
                   value=q.user.config['app_title']),
        ui.textbox(name='client_description',
                   label='Client Description',
                   value=q.user.config['description'],
                   multiline=True),
        ui.textbox(name='app_subtitle',
                   label='App Sub-Title',
                   value=q.user.config['sub_title']),
    ]
    upload_items = [
        ui.inline(items=[
            ui.file_upload(name='config_upload_logo', label='Upload Logo!', multiple=False,
                           file_extensions=['png', 'jpeg', 'jpg'], max_file_size=10, max_size=15,
                           width='250px', height='200px'),
            ui.spinbox(name='logo_height', label='Logo Height',
                       min=10, max=100, step=5, value=int(q.user.logo_height)),

        ])]

    color_picker_items = [
        ui.color_picker(name='color_primary', label='Primary Color',
                        value=q.user.primary_color, inline=True, ),
        ui.color_picker(name='font_color', label='Font Color',
                        value=q.user.font_color, inline=True, ),
    ]

    cfg = {
        'tag': 'setting',
        'setting_items': setting_items,
        'upload_items': upload_items,
        'save_buttons': save_buttons,
        'color_picker_items': color_picker_items
    }
    await render_template(q, cfg)