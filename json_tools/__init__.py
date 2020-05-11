from json_tools.encoder import SimpleJSONEncoder
from json_tools.encoder import RefJSONEncoder
from json_tools.encoder import AllRefJSONEncoder
from json_tools.encoder import (is_elemental, is_collection,
                                 is_custom_class, hashable, to_hashable)
from json_tools.loader import load_json_file
import json_tools._constants as constants

__author__ = constants.__author__
__license__ = constants.__license__
__url__ = constants.__url__
__version__ = constants.__version__