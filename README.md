mauto - as in Maya Automation
=============================
`mauto` is a macro tool for Autodesk Maya, it implements a simple
(but efficient) static analysis algorithm which solves the external and
internal dependencies of the Maya log at runtime, giving the ability to
automate _simple tasks_ without write a single line of code.

Does `mauto` replace scripting?

_Not at all!_ `mauto` helps to automate repetitive tasks through macros,
but it does not offer any kind of control flow tooling (if _this_ then _that_)
or access to low-level stuff (Maya API).


## Dependencies

- [PySide](http://qt-project.org/wiki/PySide)
- [Nose](http://nose.readthedocs.org) + [Coverage](http://coverage.readthedocs.org) + [Mock](http://mock.readthedocs.org) (testing)

> `mauto` has been tested on Maya >= 2014 but it should run in older
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
    mauto.save_macro("my_macro")  # save to disk

    # create a new macro from a maya log
    m = mauto.new_macro("my_macro", log)
    
    # list existing macros
    mauto.list_macros()

    # load and execute a macro from the library
    m = mauto.get_macro("my_macro")
    m.play()
    
    # redefine inputs
    m = mauto.get_macro("my_macro")
    m.inputs #  [input1, input2, ...]
    m.play(refs, input1=new_input1, input2=new_input2)

    # remove a macro from the library
    mauto.remove_macro("my_macro")

    # get macro filepath
    mauto.get_filepath("my_macro")

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