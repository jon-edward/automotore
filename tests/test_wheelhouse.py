from pathlib import Path
from subprocess import CalledProcessError, check_call
import sys
from tempfile import TemporaryDirectory
import unittest

from automotore.wheelhouse import WheelhouseConfig, create_wheelhouse

requirements = "numpy==2.2.5\nscikit-learn==1.6.1"

class TestWheelhouse(unittest.TestCase):
    _venv_dir = None
    _venv_python = None
    _requirements_path = None
    _output_path = None

    def setUp(self):
        """ Create a temporary directory for the venv, requirements file, and output file. """
        temp_dir = self.enterContext(TemporaryDirectory())

        self._venv_dir = Path(temp_dir) / "venv"

        if sys.platform == "win32":
            self._venv_python = self._venv_dir / "Scripts" / "python.exe"
        else:
            self._venv_python = self._venv_dir / "bin" / "python3"
        self._requirements_path = Path(temp_dir) / "requirements.txt"
        self._output_path = Path(temp_dir) / "packages.pyz"

        # create venv
        check_call([
            sys.executable,
            "-m",
            "venv",
            str(self._venv_dir),
        ])  

        # create requirements file
        self._requirements_path.write_text(requirements)
    
    def tearDown(self):
        """ Remove paths created in setUp, temp_dir will be deleted automatically. """
        self._venv_dir = None
        self._venv_python = None
        self._requirements_path = None
        self._output_path = None

    def test_create_wheelhouse(self):
        create_wheelhouse(WheelhouseConfig(requirements_path=self._requirements_path, output_path=self._output_path))
        self.assertTrue(self._output_path.exists())

    def test_install_one_package(self):
        create_wheelhouse(WheelhouseConfig(requirements_path=self._requirements_path, output_path=self._output_path))

        # check that numpy is not installed
        with self.assertRaises(CalledProcessError):
            check_call([
                self._venv_python,
                "-c",
                "import numpy",
            ])
        
        # check that scikit-learn is not installed
        with self.assertRaises(CalledProcessError):
            check_call([
                self._venv_python,
                "-c",
                "import sklearn",
            ])

        # install numpy
        check_call([
            self._venv_python,
            str(self._output_path),
            "install",
            "numpy",
        ])

        # check that numpy is installed
        check_call([
            self._venv_python,
            "-c",
            "import numpy as np; assert np.__version__ == '2.2.5'",
        ])

        # check that scikit-learn is not installed
        with self.assertRaises(CalledProcessError):
            check_call([
                self._venv_python,
                "-c",
                "import sklearn",
            ])
    
    def test_install_all_packages(self):
        create_wheelhouse(WheelhouseConfig(requirements_path=self._requirements_path, output_path=self._output_path))

        # check that numpy is not installed
        with self.assertRaises(CalledProcessError):
            check_call([
                self._venv_python,
                "-c",
                "import numpy",
            ])
        
        # check that scikit-learn is not installed
        with self.assertRaises(CalledProcessError):
            check_call([
                self._venv_python,
                "-c",
                "import sklearn",
            ])

        # install all packages
        check_call([
            self._venv_python,
            str(self._output_path),
            "install",
        ])

        # check that numpy is installed
        check_call([
            self._venv_python,
            "-c",
            "import numpy as np; assert np.__version__ == '2.2.5'",
        ])

        # check that scikit-learn is installed
        check_call([
            self._venv_python,
            "-c",
            "import sklearn; assert sklearn.__version__ == '1.6.1'",
        ])
