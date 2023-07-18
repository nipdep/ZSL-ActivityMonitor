from h2o_wave import ui, Q
from .layout import render_template
from .utilities import *

async def home_page(q, details=None):

    # build registered user card 
    cfg = {
        'tag': 'home',
        'items': [ui.text("Home Page")],
    }
    await render_template(q, cfg)



