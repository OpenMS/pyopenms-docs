
   
# Traitlet configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    'msbokehapps': {
        'command': ['python3', '-m', 'bokeh', 'serve', 'msmapviewerapp', "--allow-websocket-origin=*", "--port", "{port}", "--prefix", "{base_url}msbokehapps", "--disable-index-redirect", "--log-file", "/home/jovyan/bokehlog.txt"],
        'timeout': 300,
        'absolute_url': True,
        'launcher_entry': {
            'enabled': True,
            'icon_path': '/home/jovyan/OpenMS.svg',
            'title': 'pyOpenMS Apps and Dashboards',
        },
    },
}
