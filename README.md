WSITools
=========



Tools to aid Digital pathology deep learning projects.

* Free software: MIT license
* Documentation: https://wsitools.readthedocs.io/en/latest/index.html

Features
--------
WSITools is a whole slide image processing toolkit. It provides efficient ways to extract patches from whole slide 
images, and some other useful features for pathological image processing.
Currently, it supports four patch extraction scenarios:
1. Extract patches from WSIs
2. Extract patches from WSIs and their label (i.e. their directory name)
    1. TODO: Incomplete
3. Extract patches from a fixed and a float WSI
4. Extract patches from a fixed and a float WSI in places that intersect annotation objects
    1. TODO: Incomplete

## Additional Features
1. Detect tissue in a WSI
2. Export and parsing annotation from [QuPath](https://qupath.github.io/) and [Aperio Image Scope](https://www.leicabiosystems.com/digital-pathology/manage/aperio-imagescope/) 
3. WSI registration for image pairs [[Paper]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0220074)
4. Reconstruct WSI from the processed image patches

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

--------

