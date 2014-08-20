from setuptools import setup, find_packages

import simplecv_barcode


setup(name="simplecv2-barcode",
      version=simplecv_barcode.__version__,
      description="simplecv plugin that provides barcode detection",
      long_description=("Plugin for simplecv library, framework for computer (machine) vision in Python, "
                        "providing a unified, pythonic interface to image acquisition, conversion, "
                        "manipulation, and feature extraction."),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Manufacturing',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
          'Topic :: Multimedia :: Graphics :: Graphics Conversion',
          'Topic :: Scientific/Engineering :: Image Recognition',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      keywords='opencv, cv, machine vision, computer vision, image recognition, simplecv',
      author='Sight Machine Inc',
      author_email='support@sightmachine.com',
      url='http://simplecv.org',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      zip_safe=False,
      install_requires=['simplecv>=2.0'],
      package_data={
          'simplecv_barcode':
              ['data/test/standard/*.png',
               'data/sampleimages/*.png']
      },
      entry_points={
          'simplecv.image': [
              'simplecv_barcode = simplecv_barcode.image_plugin'
          ],
          'simplecv.factory': [
              'Barcode = simplecv_barcode.features:Barcode'
          ]
      },
      )
