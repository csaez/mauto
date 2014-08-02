mauto - as in Maya Automation
=============================
`mauto` is a generic macro tool for Autodesk Maya, it implements a simple
(but efficient) static analysis algorithm which solves the external and
internal dependencies at runtime,  giving you the ability to automate
repetitive tasks without write a single line of code.

Does `mauto` remove the need of scripting?

__Not at all!__ `mauto` helps to automate _simple tasks_ through macros, but
it does not contemplate any kind of control flow (if _this_ then _that_) or
the ability to access low-level stuff through the Maya API.


## Dependencies

- [PySide](http://qt-project.org/wiki/PySide)
- [Nose](http://nose.readthedocs.org) + [Coverage](http://coverage.readthedocs.org) + [Mock](http://mock.readthedocs.org) (testing)

> `mauto` has been tested on Maya 2014+ but it should run in older
versions, please let me know if you find any issues.


## Installation

Copy the `mauto` directory somewhere in your `PYTHONPATH` (maya scripts
directory should do the trick) or clone the repo and install the project
through its `setup.py` script (_highly recommended!_).

    mayapy setup.py install


## Ussage

    import mauto
    
    #  Launch the Maya GUI...
    mauto.show()

    # ... or use it through the python api.

    # create a new macro
    m = mauto.new_macro("my_macro")
    m.record()
    m.stop()
    mauto.save_macro("my_macro")

    # create a new macro from a maya log
    m = mauto.new_macro("my_macro", log)
    
    # list existing macros
    mauto.list_macros()

    # load and execute a macro from the library
    m = mauto.get_macro("my_macro")
    m.play()
    
    # redefine inputs
    m = mauto.get_macro("my_macro")
    refs = m.inputs #  dict of ext references
    refs["locator1"] = "pCube"
    m.play(refs)

    # remove a macro from the library
    mauto.remove_macro("my_macro")

#### Testing (optional)

Running the test suite:

    mayapy setup.py nosetests -v

Running tests with coverage:

    mayapy setup.py nosetests --with-coverage --cover-package=mauto


## Contributing

- [Check for open issues] (https://github.com/csaez/mauto/issues) or open
a fresh issue to start a discussion around a feature idea or a bug.
- Fork the [mauto repository on Github](https://github.com/csaez/mauto)
to start making your changes (make sure to isolate your changes in a local branch when possible).
- Write a test which shows that the bug was fixed or that the feature works
as expected.
- Send a pull request and bug the maintainer until it gets merged and
published. :)

Make sure to add yourself to `CONTRIBUTORS.md`

## Notes

For more info, refer to the [documentation](http://mauto.readthedocs.org).