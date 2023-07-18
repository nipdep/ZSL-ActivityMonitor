from h2o_wave import Q, ui
import pandas as pd
from h2o_wave import Q, ui, copy_expando

# read data csv

def read_csv_to_df():
    df=pd.read_csv("./archive order/final.csv")
    final_df=pd.DataFrame(df)

    #print(data)
    return final_df


final_df = read_csv_to_df()


def get_tup_list():
    # to plot line graph of revenue vs time
    revenue_over_time = final_df.groupby('date')['total'].sum()
    temp_df = final_df['date'].to_frame().join(revenue_over_time)
    data_tup_list =list(map(tuple, final_df.to_numpy()))
    data_tup_list =list(map(tuple, final_df.drop("order_id", axis=1).to_numpy()))
    return data_tup_list[:10]



# for histogram revenue by category
category_revenue = final_df.groupby('category')["price"].sum()
cat_rev_df=pd.DataFrame({'category':category_revenue.index, 'rev_cat':category_revenue.values})
cat_rev_tup_list = list(map(tuple, cat_rev_df.to_numpy()))

# for histogram revenue by product
product_revenue = final_df.groupby('product_name')["price"].sum()
prod_rev_df=pd.DataFrame({'product_name':product_revenue.index, 'rev_prod':product_revenue.values})
prod_rev_tup_list = list(map(tuple, prod_rev_df.to_numpy()))           



async def display_progress_bar(q: Q, doc):
    q.page['meta'].dialog = ui.dialog(
        name="name" if 'name' in doc else doc['name'],
        title="" if 'title' in doc else doc['title'],
        items=[] if 'items' in doc else doc['items'],
        closable=False if 'closable' in doc else doc['closable'],
        primary=True if 'primary' in doc else doc['primary']
    )
    await q.page.save()
    await q.sleep(1)

    if len(final_df) == 0:
        table = ui.table(
            name='name',
            columns=[ui.table_column(name='-', label='-', link=False)],
            rows=[ui.table_row(name='-', cells=[str('No data found!')])])
        return table

    if not sortables:
        sortables = []
    if not filterables:
        filterables = []
    if not searchables:
        searchables = []
    if not icons:
        icons = {}
    if not progresses:
        progresses = {}
    if not tags:
        tags = {}
    if not min_widths:
        min_widths = {}
    if not max_widths:
        max_widths = {}

    cell_types = {}
    for col in icons.keys():
        cell_types[col] = ui.icon_table_cell_type(color=icons[col]['color'])
    for col in progresses.keys():
        cell_types[col] = ui.progress_table_cell_type(
            color=progresses[col]['color'])
    for col in tags.keys():
        cell_types[col] = ui.tag_table_cell_type(name="tag_" + col,
                                                 tags=tags[col]['tags'])

    columns = [
        ui.table_column(
            name=str(x),
            label=str(x),
            sortable=True if x in sortables else False,
            filterable=True if x in filterables else False,
            searchable=True if x in searchables else False,
            cell_type=cell_types[x] if x in cell_types.keys() else None,
            min_width=min_widths[x] if x in min_widths.keys() else None,
            max_width=max_widths[x] if x in max_widths.keys() else None,
            link=True if x == link_col else False,
        ) for x in final_df.columns.values
    ]

    table = ui.table(name=name,
                     columns=columns,
                     rows=[
                         ui.table_row(name=str(i),
                                      cells=[
                                          str(df[col].values[i])
                                          for col in df.columns.values
                         ]) for i in range(df.shape[0])
                     ],
                     multiple=multiple,
                     groupable=groupable,
                     downloadable=downloadable,
                     resettable=resettable,
                     height=height,
                     checkbox_visibility=checkbox_visibility)

    return table


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
