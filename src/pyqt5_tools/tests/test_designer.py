import os
import pathlib
import subprocess
import sys

import pytest

import pyqt5_tools.tests.testbutton
import pyqt5_tools.tests.testbuttonplugin


def test_creates_test_widget(tempdir):
    env = dict(os.environ)
    file_path = pathlib.Path(tempdir)/'tigger'
    env[pyqt5_tools.tests.testbutton.test_path_env_var] = file_path

    widget_plugin_path = pathlib.Path(
        pyqt5_tools.tests.testbuttonplugin.__file__,
    ).parent

    print('env:', env)

    with pytest.raises(subprocess.TimeoutExpired):
        subprocess.run(
            [
                str(pathlib.Path(sys.executable).with_name('pyqt5designer')),
                '--widget-path', str(widget_plugin_path),
            ],
            check=True,
            env=env,
            timeout=30,
        )

    with open(file_path, 'rb') as f:
        assert f.read() == pyqt5_tools.tests.testbutton.test_file_contents
