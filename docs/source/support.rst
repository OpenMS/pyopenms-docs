Support
=======

Feature Requests
****************

:term:`pyOpenMS` is an evolving project. We are happy to learn about missing features you would like to
see in :term:`pyOpenMS`.

Feel free to open an issue on `GitHub issue <https://github.com/OpenMS/OpenMS/issues>`_
 to request a novel feature.

Troubleshooting
***************

If you encounter a problem running :term:`pyOpenMS` feel free to contact
us by opening a `GitHub issue <https://github.com/OpenMS/OpenMS/issues>`_
or the `OpenMS Gitter chat channel <https://gitter.im/OpenMS/OpenMS/>`_.

Please provide information on what :term:`pyOpenMS` version you have installed.
You can check if importing :term:`pyOpenMS` works and print your :term:`pyOpenMS` version with:

.. code-block:: python
    :linenos:

    from pyopenms import *

    print("Version: " + VersionInfo.getVersion())
    print("OpenMP: " + str(OpenMSBuildInfo.isOpenMPEnabled()))
    print("Build type: " + OpenMSBuildInfo.getBuildType())
    print("Architecture: " + OpenMSOSInfo.getBinaryArchitecture())

