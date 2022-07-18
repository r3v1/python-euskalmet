Instalación
###########

Requerimientos
==============

Antes de empezar, conviene tener presentes las siguientes consederaciones:

- El proyecto está implementado en ``Python 3.9``, pero debería funcionar con ``>=Python 3.8``.
- Se ha probado con éxito en los sistemas Ubuntu 18.04, Debian 10, Debian 11 y Arch Linux. No debería
    ser un problema el despliegue en otro sistema Linux, pero sí en Windows. En serio, instálate Ubuntu aunque sea.

.. warning::
    No tengo ni idea de cómo se puede comportar en Windows.

Instalación con Pypi
====================

Simplemente, basta con ejecutar:

.. code-block:: bash

    pip install python-euskalmet

Instalación desde código fuente
==================================

Se puede clonar el repositorio mediante SSH con:

.. code-block:: bash

    git clone git@github.com:r3v1/python-euskalmet.git

o introduciendo el usuario y contraseña del usuario:

.. code-block:: bash

    git clone https://github.com/r3v1/python-euskalmet.git

También conviene generar un entorno virtual para aislar al sistema y activarlo con:

.. code-block:: bash

    virtualenv venv
    source venv/bin/activate

Luego, se deberán instalar las dependencias con:

.. code-block:: bash

    pip install -U -r requirements.txt



