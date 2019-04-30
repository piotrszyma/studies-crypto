import random
import shutil
import unittest
import pathlib
import subprocess
import tempfile

import parameterized

from libs import crypto_libs
from libs import utils
from config import settings


def perform_encryption(message_name, output_name):
  command = ' '.join(f"""
    ../.venv/bin/python3 main.py enc
    --config_path=config/config.ini
    --input_path=/tmp/test_folder/{message_name}
    --increment_iv
    --output_path=/tmp/test_folder/{output_name}
    """.split())
  subprocess.run(command.split(' '), stdout=subprocess.PIPE)


class MainTests(unittest.TestCase):

  def test_cpa_insecure(self):
    test_path = pathlib.Path('/tmp/test_folder')
    test_path.mkdir(exist_ok=True)

    msg0 = utils.random_bytes(16)

    msg0_path = pathlib.Path(test_path, 'msg0')
    msg0_path.write_bytes(msg0)

    perform_encryption('msg0', 'cypher0')

    cypher0 = pathlib.Path(test_path, 'cypher0').read_bytes()
    iv0 = cypher0[-16:]
    calculated_iv1 = utils.increment_bytes(iv0)

    msg1 = utils.xor_bytes(utils.xor_bytes(msg0, iv0), calculated_iv1)
    msg1_path = pathlib.Path(test_path, 'msg1')
    msg1_path.write_bytes(msg1)

    perform_encryption('msg1', 'cypher1')

    cypher1 = pathlib.Path(test_path, 'cypher1').read_bytes()

    assert cypher1 == cypher0[:-16] + calculated_iv1

    shutil.rmtree(test_path)