
   
# Traitlet configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    'massspecviewer': {
        'command': ['python3', '-m', 'bokeh', 'serve', 'bokehappfolder', "--allow-websocket-origin=*", "--port", "{port}", "--prefix", "{base_url}massspecviewer", "--disable-index-redirect", "--log-file", "/home/jovyan/bokehlog.txt"],
        'timeout': 300,
        'absolute_url': True,
        'launcher_entry': {
            'enabled': True,
            'icon_path': '/home/jovyan/OpenMS.svg',
            'title': 'pyOpenMS MS Viewer',
        },
    },
}
