
   
# Traitlet configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    'massspecviewer': {
        'command': ['python3', '-m', 'bokeh', 'serve', 'bokehappfolder', '-p', '{port}','--allow-websocket-origin=*'],
        'port': 3333,
        'timeout': 120,
        #'launcher_entry': {
        #    'enabled': True,
        #    'icon_path': '/home/jovyan/.jupyter/open-refine-logo.svg',
        #    'title': 'OpenRefine',
        #},
    },
}