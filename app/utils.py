from h2o_wave import Q, ui
import pandas as pd
from h2o_wave import Q, ui, copy_expando


""" DAI UTILS """


def ui_choices(alist):
    return [ui.choice(name=c, label=c) for c in alist]


def get_table_from_df(df: pd.DataFrame, rows: int, name: str, size: str):
    df = df.copy().reset_index(drop=True)
    columns = [ui.table_column(name=str(x), label=str(
        x), sortable=True, searchable=False, filterable=False) for x in df.columns.values]
    rows = min(rows, df.shape[0])
    try:
        table = ui.table(
            name=name, columns=columns,
            rows=[ui.table_row(name=str(i), cells=[str(df[col].values[i])
                                                   for col in df.columns.values]) for i in range(rows)],
            groupable=False,
            downloadable=True,
            resettable=True,
            multiple=False,
            height=size
        )
    except:
        table = ui.table(
            name=name, columns=[ui.choice('0', '0')],
            rows=[ui.table_row(name='0', cells=[str('No data found')])]
        )
    return table


async def update_theme(q: Q):

    copy_expando(q.args, q.client)

    if q.client.theme_dark:
        q.client.icon_color = "#CDDD38"
        q.page["meta"].theme = "light"
        # q.page['header'].icon_color = q.client.icon_color

    else:
        q.client.icon_color = "#FFFFFF"
        q.page["meta"].theme = "h2o-dark"
        # q.page['header'].icon_color = q.client.icon_color

    q.page["misc"].items[2].toggle.value = q.client.theme_dark

    await q.page.save()


def set_user_arguments(q: Q, elements):
    for element in elements:
        q.user[element] = q.args[element]


def make_markdown_row(values):
    return f"| {' | '.join([str(x) for x in values])} |"


def make_markdown_table(fields, rows):
    return '\n'.join([
        make_markdown_row(fields),
        make_markdown_row('-' * len(fields)),
        '\n'.join([make_markdown_row(row) for row in rows]),
    ])

# ====== Dataset Utils =====


def read_dataset_form(q):
    data = {}
    data['dataset name'] = q.args['dt_name']
    data['description'] = q.args['dt_desc']
    data['type'] = q.args['dt_type']
    data['path'] = q.args['dt_path']
    return data
