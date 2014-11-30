#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Modules:
- visibility: polar scanline algorithm.
- common:     classes and operations which may be used by different files.
- gui:        graphic implementation.


"""

import visibility
from common.guicontrol import init_display
from common.guicontrol import config_canvas
from common.guicontrol import run_algorithm
from common.io import open_file
from common.prim import get_count
from common.prim import reset_count

children = (
           ( 'visibility',  None, 'Visibilidade' ),
	   )

__all__ = map (lambda p: p[0], children)
