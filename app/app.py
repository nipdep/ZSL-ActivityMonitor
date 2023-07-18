# H2O-Wave Application Template
#     __Version__ : 0.1
#     __Last_updated__ : 13/07/2023
#     __Authors__ : @nipdep

# routing is defined
from h2o_wave import Q, app, ui, data, main, on, handle_on

from .pages.layout import * 
from .pages.home_page import home_page
from .pages.setting_page import setting_page
from .pages.about_page import about_page
from .pages.user_page import *
from .utils import * 

import warnings
warnings.filterwarnings("ignore")

def set_popup(q, activity):
    activity_gif = q.app.gifs[activity]
    q.page['meta'].dialog = ui.dialog(
            title=activity,
            name='  ',
            width='400px',
            # items=[ui.text(f"<img src={q.app.loader}/>")])
            items=[ui.text(f"<img src={activity_gif}/>")])
    

@app('/')
async def serve(q: Q):
    print(q.args)
    # cmd_list = ['preview_card-0']
    # for c in q.args:
    #     if c in cmd_list: 
    #         print(c)

    details = {'status': 'default'}
    if q.args.reset:
        q.user.init = False

    # if q.client.theme_dark == None:
    #     q.client.theme_dark = True

    if q.user.init != True:
        details = {'status': 'default'}
        await initialize_app(q)

    if q.args.config_save or q.args.config_upload_logo is not None:
        q.user.config['app_title'] = q.args.client_title
        q.user.config['description'] = q.args.client_description
        q.user.config['sub_title'] = q.args.app_subtitle
        if q.args.config_upload_logo is not None:
            link = q.args.config_upload_logo[0]
            q.user.logo = link
            q.user.logo_height = q.args.logo_height
        q.user.font_color = q.args.font_color
        if q.args.font_color is not None or q.args.color_primary is not None:
            q.user.font_color = q.args.font_color
            q.user.primary_color = q.args.color_primary
        q.args.tabs = 'setting_tab'

    if q.args.select_subject:
        q.client.subject = q.args.select_subject
        q.args.tabs = 'launch_tab'

    if q.args.launch_app:
        q.args.tabs = 'launch_tab'

    if q.args.home_tab:
        q.args.tabs = 'home_tab'

    if q.events.content_12:
        print(f"You selected {q.events.content_12.select_marks}")
    
    print(">> Tab >> ", q.args.tabs)

    if q.args.tabs == 'about_tab':
        await about_page(q, details)
    elif q.args.tabs == 'home_tab':
        await home_page(q, details)
    elif q.args.tabs == 'launch_tab':
        await launch_page(q, details)
    elif q.args.setting_tab == True:
        await setting_page(q, details)
    elif q.events.content_12:
        activity = q.events.content_12.select_marks[0]['activity'].replace(" ", "_")
        set_popup(q, activity)
    else:
        await home_page(q, details)

    await q.page.save()