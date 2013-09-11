import os
import sys
import shutil
import hashlib
import unittest
import subprocess
from six.moves.urllib import request
import sanity_tests
import client_tests
import server_tests
import complex_tests
from waferslim import tests as waferslim_tests


here = os.path.abspath(os.path.dirname(__file__))


def main():
    suite = unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromModule(sanity_tests),
        unittest.defaultTestLoader.loadTestsFromModule(client_tests),
        unittest.defaultTestLoader.loadTestsFromModule(server_tests),
        unittest.defaultTestLoader.loadTestsFromModule(complex_tests),
        unittest.defaultTestLoader.loadTestsFromModule(waferslim_tests),
    ])
    result = unittest.TextTestRunner().run(suite)
    if result.wasSuccessful():
        if waferslim_smoke_test():
            download_fitnesse()
            return run_fitnesse()
    return 1


def waferslim_smoke_test():
    smoke_env = dict(os.environ)
    smoke_env['PYTHONPATH'] = here
    return 0 == subprocess.call(
        ['python', '-m', 'waferslim.smoke'],
        env=smoke_env,
        cwd=os.path.join(here, 'waferslim')
    )


def run_fitnesse():
    '''
    Locally you can run fitnesse server using command:
    java -jar fitnesse-standalone.jar -e 0 -p 9123
    '''
    suite_name = 'RocSuite'
    subprocess.call([
        'java',
        '-jar',
        'fitnesse-standalone.jar',
        '-i',
    ], cwd=here)
    try:
        shutil.copytree(os.path.join(here, suite_name),
                        os.path.join(here, 'FitNesseRoot', suite_name))
    except OSError:
        pass
    return subprocess.call([
        'java',
        '-jar',
        'fitnesse-standalone.jar',
        '-c', suite_name + '?suite&format=text',
    ], cwd=here)


def download_fitnesse():
    fitnesse_url = ('http://fitnesse.org/fitnesse-standalone.jar' +
                    '?responder=releaseDownload&release=20130530')
    fitnesse_path = os.path.join(here, 'fitnesse-standalone.jar')
    expected_md5 = 'c357d8717434947ed4dbbf8de51a8016'
    if os.path.exists(fitnesse_path):
        with open(fitnesse_path, 'rb') as fp:
            digest = hashlib.md5(fp.read()).hexdigest()
        if digest == expected_md5:
            return
        else:
            print('Warning: md5 digest does not match:')
            print(digest, expected_md5)
    response = request.urlopen(fitnesse_url)
    with open(fitnesse_path, 'wb') as out_file:
        out_file.write(response.read())


if __name__ == '__main__':
    sys.exit(main())
