
   
# Traitlet configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    'massspecviewer': {
        'command': ['python3', '-m', 'bokeh', 'serve', 'bokehappfolder', '--address', '0.0.0.0', '--port', '{port}', '--prefix', '{base_url}/proxy/{port}', '--allow-websocket-origin=*', '--use-xheaders'],
        'port': 3333,
        'timeout': 120,
        'launcher_entry': {
            'enabled': True,
            'icon_path': '/home/jovyan/OpenMS.svg',
            'title': 'pyOpenMS MS Viewer',
        },
    },
}
