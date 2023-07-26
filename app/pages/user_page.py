from h2o_wave import ui, site, data
from .layout import render_template
from .utilities import *
import random
# import plotly.io as pio
# pio.templates.default = "plotly_dark"

async def launch_page(q, details=None):
    
    # subject selection list / table
    subjects = q.user.all_data['subject'].unique()
    sub_cards = [ui.inline([ui.persona(title=r, subtitle=" ", size='xs', name=r, image=random.choice([q.app.prf_pic1, q.app.prf_pic2])),
                            ui.button(name='select_subject', label='View', icon='CaretRight8', value=r)], justify='between') for i,r in enumerate(subjects)]
    subject_table = ui.form_card(
        box=ui.box('content_0', 
                   order=1, 
                #    width='100%', 
                #    height='700px'
                   ),
        items=[
                # ui.button(name='add_jd', label='Add Job Description', primary=True, icon='CircleAdditionSolid', width='100%'),
               ui.text_m(content='Subjects'),]+sub_cards,
    )
    

    if q.client.subject:
        subject = q.client.subject 
    else:
        subject = subjects[0]
    print("Subject >> ", subject)
    sub_df = q.user.all_data.loc[q.user.all_data['subject'] == subject]
    print("subject-DataFrame >>", sub_df)

    agg_df = sub_df.copy()
    agg_df['mins'] = 5 
    agg_result_df = agg_df.groupby('prediction').agg({'subject': 'count', 'mins': 'sum', 'super_prediction': 'first', 'phase': 'first'}).reset_index()
    agg_result_df.columns = ['action', 'count', 'time', 'super', 'phase']

    columns = [
        ui.table_column(name='activity', label='Activity', sortable=False, searchable=True, max_width='200px'),
        ui.table_column(name='n_instances', label='# Instances', data_type='number'),
        ui.table_column(name='total_time', label='Total Time [minutes]', data_type='number'),
        ui.table_column(name='superclass', label='Activity Superclass', filterable=True),
        ui.table_column(name='prediction_phase', label='Inference Mode', cell_type=ui.tag_table_cell_type(name='tags', tags=[
                    ui.tag(label='seen', color='#D2E3F8'),
                    ui.tag(label='unseen', color='$mint'),
                    ])
        )
    ]

    activity_table = ui.form_card(
        box=ui.box('content_11', order=0),
        items=[
            ui.table(name='activities',
                     columns=columns,
                     rows=[ui.table_row(
                        name=r[0],
                        cells=[str(e) for e in r]
                     )for r in agg_result_df.values.tolist()],
                     groupable=True,
                     downloadable=True,
                     resettable=True,
                     height='600px'
                    )
        ]
    )

    instance_counts = [(k,v) for k,v in sub_df['prediction'].value_counts(sort=True).to_dict().items()]
    print("instance_counts > ", instance_counts)
    activity_freq_plot = ui.plot_card(
        box=ui.box('content_121', order=1),
        title='Activity Frequency',
        data=data(fields=['activity', 'count'], rows=instance_counts, pack=True),
        plot=ui.plot([
            ui.mark(type='interval', x='=count', y='=activity')
        ])
    )

    superclass_prec = [(k,v) for k,v in sub_df['super_prediction'].value_counts(normalize=True, sort=True).to_dict().items()]
    superclass_prec_plot = ui.plot_card(
        box=ui.box('content_122', order=1),
        title='Activity Type Frequency',
        data=data(fields=['type', 'count'], rows=superclass_prec, pack=True),
        plot=ui.plot([
            ui.mark(coord='theta', type='interval', x='=type', y='=count', y_min=0)
        ])
    )

    one_hot_df = pd.get_dummies(sub_df, columns=['prediction'], prefix='', prefix_sep='')
    melted_df = pd.melt(one_hot_df, id_vars=['timestamp'], value_vars=sub_df['prediction'].unique())
    melted_df['timestamp'] -= melted_df['timestamp'].min()
    time_frame = ui.plot_card(
        box=ui.box('content_13', order=2),
        title='Activity Time Frames',
        data=data(fields=['timestamp', 'activity', 'value'], rows=melted_df.values.tolist(), pack=True),
        plot=ui.plot([
            ui.mark(type='interval', x='=timestamp', y='=value', color='=activity', y_min=0, y_max=1)
        ]),
        # interactions=['brush', 'scale_zoom'],
        events=['select_marks'],
    )

    cfg = {
        'tag': 'launch',
        'subject_table': subject_table,
        'activity_table': activity_table,
        'activity_freq_plot': activity_freq_plot,
        'superclass_prec_plot': superclass_prec_plot,
        'time_frame': time_frame,
        # 'main_table':table_df,
    }
    await render_template(q, cfg)