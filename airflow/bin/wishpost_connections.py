import sys
import os

class WishPostConnections(object):

    @classmethod
    def connect_wishpost(cls):

        # Import required arguments to run Data Platform
        sys_path = os.environ.get('WISHPOST_PATH')
        sys.path.insert(0,sys_path)
        sys.dont_write_bytecode = True

        from wishpost.core.options import define_for_scripts
        from wishpost.server import WishPostApplication
        from wishpost.server import configure
        from tornado.options import options
        from cl.utils.tornadoutil.extopts import ExtOpt

        # Connect to application
        define_for_scripts()
        options.env = os.environ.get('AIRFLOW_ENV')
        configure()
        application = WishPostApplication(options, None)
        from wishpost.model import lib as wosp_lib
        from wishchain.model import lib as chain_lib
        import copy as cp
        db_conn = cp.deepcopy(wosp_lib.CONNECTION_TO_DB)

        db_conn['wishchain'] = list(
            set(chain_lib.CONNECTION_TO_DB[chain_lib.MAIN_CONNECTION]) -
            set(wosp_lib.CONNECTION_TO_DB[wosp_lib.MAIN_CONNECTION]))
        application.connect(db_collection=db_conn)

        if not hasattr(options, 'application'):
            try:
                ExtOpt.define('application', default=None, hidden=True,
                              type=object)
            except:
                pass
        options.application = application
