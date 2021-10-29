
   
# Traitlet configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    'massspecviewer': {
        'command': ['python3', '-m', 'bokeh', 'serve', 'bokehappfolder', '--port', '{port}','--allow-websocket-origin=*'],
        'port': 3333,
        'timeout': 120,
        'launcher_entry': {
            'enabled': True,
            'icon_path': '/home/jovyan/.jupyter/OpenMS.svg',
            'title': 'pyOpenMS MS Viewer',
        },
    },
}