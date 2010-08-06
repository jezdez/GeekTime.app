from setuptools import setup

import GeekTime

setup(
    name='GeekTime',
    version=GeekTime.__version__,
    author=GeekTime.__author__,
    author_email='jannis@leidel.info',
    py_modules=['GeekTime'],
    app=['GeekTime.py'],
    setup_requires=['py2app'],
    options={
        'py2app': {
            'plist': {
                'CFBundleIdentifier': 'me.jezdez.geektime',
                'LSUIElement': True,
                'CFBundleVersion': GeekTime.__version__,
            },
        },
    },
)
