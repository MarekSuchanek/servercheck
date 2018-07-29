from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())
    setup(
        name='servercheck',
        version='0.1',
        keywords='server management healthcheck administration slack',
        description='Simple Python app to check health of (linux) server and its services',
        long_description=long_description,
        author='Marek Suchánek',
        author_email='suchama4@fit.cvut.cz',
        license='MIT',
        url='https://github.com/MarekSuchanek/servercheck',
        zip_safe=False,
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'servercheck = servercheck:servercheck',
            ]
        },
        install_requires=[
            'click',
            'docker',
            'Flask',
            'psutil',
            'python-daemon',
            'pyyaml',
            'requests',
        ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Framework :: Flask',
            'Intended Audience :: System Administrators',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Topic :: Utilities'
        ],
    )

