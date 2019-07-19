#!/usr/bin/env python

# import __main__ as main
from .variables import *
from .plot_utils import *

from . import style

style.set_color_cycle()
# # from .style import use
# # import .style
# # import from_palettable
#
# __all__ = ['style']


# try:
#     config_file = Path(main.__file__).parent.resolve() / 'config.yaml'
#     conf = yaml.load(str(config_file))
#     style_name = conf['style_name']
#     print(f"Loading {style_name} from {config_file}")
# except Exception as e:
#     print(e)
#     print('fallback to aps style')
#     style_name = 'aps_article'
#
# use('aps_article')
