from h2o_wave import ui
from .layout import render_template

async def about_page(q, details=None):
    cfg = {
        'tag': 'about',
    }
    await render_template(q, cfg)