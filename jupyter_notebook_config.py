
   
# Traitlet configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    'masspecviewer': {
        'command': ['python3', '-m', 'bokeh', 'serve', 'bokehfolderapp', '-p', '{port}','--allow-websocket-origin=*'],
        'port': 3333,
        'timeout': 120,
        #'launcher_entry': {
        #    'enabled': True,
        #    'icon_path': '/home/jovyan/.jupyter/open-refine-logo.svg',
        #    'title': 'OpenRefine',
        #},
    },
}