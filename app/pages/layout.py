import os
from h2o_wave import Q, app, ui, data

from .utilities import *

config = {
    "app_title": "ZeroShort-ActivityMonitor",
    "sub_title": "Interpretable Zero-Shot Learning for Sensor-Based Human Activity Recognition",
    "footer_text": 'Copyright 2022 @nipdep, Made using <a href="https://wave.h2o.ai" target="_blank">H2O Wave</a>',
    'description': "",
    }


async def initialize_app(q):
    q.user.font_color = '#fec827'
    q.user.primary_color = '#fec827'
    q.page['meta'] = ui.meta_card(box='')
    if q.user.config is None:
        q.user.config = config
        q.user.default_config = config
        q.client.selected_tab = 'home_tab'

    if q.user.logo is None:
        q.user.logo, = await q.site.upload(['static/logo1.jpg'])
        q.user.logo_height = '50'

    if q.app.illustration is None:
        q.app.illustration, = await q.site.upload(['static/ill2.png'])

    if q.app.loader is None:
        q.app.loader, = await q.site.upload(['static/PG25.gif'])
        # q.app.loader, = await q.site.upload(['static/skeletons/Cycling_original_skel.gif'])

    if q.app.prf_pic1 is None:
        q.app.prf_pic1, = await q.site.upload(['static/sticker-man.png'])

    if q.app.prf_pic2 is None:
        q.app.prf_pic2, = await q.site.upload(['static/sticker-women.png'])

    if q.user.all_data is None:
        q.user.all_data = load_df()

    if q.app.gifs is None:
        await load_gifs(q)

    q.user.init = True

async def load_gifs(q):
    q.app.gifs = {}
    root_path = 'static/skeletons/'
    for gif_path in os.listdir(root_path):
        activity = gif_path.split(".")[0]#.replace(" ", "_")
        full_path = root_path+gif_path
        act, = await q.site.upload([full_path])
        q.app.gifs.update({activity: act})

    print("all gif keys >> ", q.app.gifs.keys())
    


def create_layout(q: Q, tag=None):
    config = q.user.config
    q.page.drop()

    q.page['header'] = ui.header_card(
        box='header',
        title=config['app_title'],
        subtitle=config['sub_title'],
        icon='TFVCLogo',
        icon_color='#222',
        items=[
            ui.button(name='home_tab', label=' ', icon='Home', primary=True, width='40px'),
            ui.button(name='about_tab', label=' ', icon='info', primary=True, width='40px'),
            ui.button(name='setting_tab', label=' ', icon='Settings', primary=True, width='40px'),
            ui.text(
                """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
                """
            ),
            ui.text("<img src='"+q.user.logo+"' width='" +
                    str(q.user.logo_height)+"px'>"),
        ],
 
    )
    # nav_items = 
    if q.client.generate_dashboard:
        nav_items += [
            ui.tab(name='#', label='', icon='BulletedListBulletMirrored'),
            ui.tab(name='dashboard_tab', label='Dashboard', icon='Processing'),
        ]

    # navbar_items = [ui.inline(items=[
    #     ui.tabs(name='tabs', value=q.args.tabs, link=True, items=nav_items)
    # ])]

    # q.page['navbar'] = ui.form_card(box=ui.box(
    #     zone='navbar'), title='', items=navbar_items)
    q.page['footer'] = ui.footer_card(
        box='footer', caption=config['footer_text'])

    zones = ui.zone(name='content', zones=[ui.zone(
        name='content_0', size='650px', direction='row')])
    if tag in ['feature']:
        zones = ui.zone(name='content', zones=[
            ui.zone(name='content_0', size='600px', direction='row'),
            ui.zone(name='content_1', size='500px', direction='row'),

        ])
    elif tag == 'setting':
        zones = ui.zone(name='content', zones=[
            ui.zone(name='content_1', size='300px', direction='row'),
            ui.zone(name='content_0', size='80px', direction='row'),

        ])
    elif tag in ['launch', 'status']:
        zones = ui.zone(name='content', direction='row', #size='560px', 
            zones=[
                ui.zone(name='content_0', size='25%', direction='column'),
                ui.zone(name='content_1', size='75%', direction='column', zones=[
                    ui.zone(name='content_11', size='45%', direction='column'),
                    ui.zone(name='content_12', size='30%', direction='row', zones=[
                        ui.zone(name='content_121', size='50%', direction='column'),
                        ui.zone(name='content_122', size='50%', direction='column')
                    ]),
                    ui.zone(name='content_13', size='25%', direction='column')
                ])
            ])

    elif tag == 'home':
        # zones = ui.zone(name='content_0', size='650px')
        zones = ui.zone(name='content', direction='row', #size='560px', 
            zones=[
                ui.zone(name='content_0'),
            ])

    else:
        print(tag)
        pass

    q.page['meta'] = ui.meta_card(box='',
                                  themes=[
                                    ui.theme(
                                        name='cdark',
                                        primary=q.user.primary_color,
                                        text=q.user.font_color,
                                        card='#000',
                                        page='#1b1d1f',
                                    ),
                                    ui.theme(
                                        name='ixdlabs_twitter',
                                        primary='#0c0882',
                                        text='#000000',
                                        card='#e9f5f7',
                                        page='#cbd4d3',
                                    )
                                  ],
                                  theme='ixdlabs_twitter',
                                  title=config['app_title'] + '| H2O Wave',
                                  # stylesheet=ui.inline_stylesheet(style),
                                  layouts=[
                                      ui.layout(
                                          breakpoint='l',
                                        #   width='996px',
                                          zones=[
                                              ui.zone(
                                                  name='header', size='75px', direction='row'),
                                            #   ui.zone(
                                                #   name='navbar', size='90px', direction='row'),
                                              zones,
                                              ui.zone('footer'),
                                          ])
                                  ])

async def render_template(q: Q, page_cfg):
    create_layout(q, tag=page_cfg['tag'])

    if page_cfg['tag'] == 'home':
        caption = """<div style='width:70%;margin-left:15%'>"""
        caption += """5 months Ding Tai Fung order data on online ordering platform"""
        # caption += f"<br><br><img src='{q.app.caption}' width='80%' height='200px'>"
        caption += "<br><hr></div>"
        # q.page['content_left'] = ui.tall_info_card(
        #     box=ui.box(zone='content_0', height='600px'),
        #     name='launch_app',
        #     title=config["app_title"],
        #     caption=caption,
        #     category=config["sub_title"],
        #     label='Launch',
        #     image=q.app.illustration,
        #     image_height='120px'
        # )

        q.page['content_left'] = ui.profile_card(
            box=ui.box(zone='content_0', height='600px'),
            image=q.app.illustration,
            persona=ui.persona(
                title=config["app_title"],
                subtitle=config["sub_title"],
                image=q.user.logo,
                size='l'
            ),
            items=[
                ui.buttons(items=[ui.button(name='launch_app', label='Launch')], justify='center')
            ]
        )
    elif page_cfg['tag'] == 'about':
        q.page['content_00'] = ui.form_card(box=ui.box(
            zone='content_0', width='100%', order=1), title='', items=[])

    elif page_cfg['tag'] == 'dashboard':
        q.page['content_00'] = ui.form_card(box=ui.box(
            zone='content_0', width='100%', order=1), title='', items=[])

    elif page_cfg['tag'] == 'setting':
        q.page['content_01'] = ui.section_card(box=ui.box(
            zone='content_0'), title='', subtitle='', items=page_cfg['save_buttons'])
        q.page['content_10'] = ui.form_card(box=ui.box(
            zone='content_1', width='40%', order=1), title='', items=page_cfg['setting_items'])
        q.page['content_11'] = ui.form_card(box=ui.box(
            zone='content_1', width='30%', order=2), title='', items=page_cfg['upload_items'])
        q.page['content_12'] = ui.form_card(box=ui.box(
            zone='content_1', width='30%', order=3), title='', items=page_cfg['color_picker_items'])


    elif page_cfg['tag'] == 'launch':
        q.page['content_00'] = page_cfg['subject_table']
        q.page['content_01'] = page_cfg['activity_table']
        q.page['content_10'] = page_cfg['activity_freq_plot']
        q.page['content_11'] = page_cfg['superclass_prec_plot']
        q.page['content_12'] = page_cfg['time_frame']
        # q.page['content_15'] = page_cfg['main_table']


    await q.page.save()