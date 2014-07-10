SeqFindr Developer HOWTO
========================

In addition to what is described here, `this document by Jeff Forcier`_ and 
`this talk from Carl Meyer`_ provide wonderful footings for developing on/in 
open source projects.


Maintaining a consistent development environment
-------------------------------------------------

**1)** Ensure all development in performed within a virtualenv. A good way too 
bootstrap this is via virtualenv-burrito_.

Execute the installation using::
    
    $ curl -sL https://raw.githubusercontent.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL


**2)** Make a virtualenv called SeqFindr::

    $ mkvirtualenv SeqFindr


**3)** Install autoenv_::
    
    $ git clone git://github.com/kennethreitz/autoenv.git ~/.autoenv
    $ echo 'source ~/.autoenv/activate.sh' >> ~/.bashrc


Get the current code from GitHub
--------------------------------

Something like this::

    $ cd $PATH_WHERE_I_KEEP_MY_REPOS
    $ git clone https://github.com/mscook/SeqFindr.git


Install dependencies
--------------------

Something like this::

    $ cd SeqFindr
    $ # Assuming you installed autoenv -
    $ # You'll want to say 'y' as this will activate the virtualenv each time you enter the code directory
    $ # Otherwise -
    $ # workon SeqFindr 
    $ pip install -r requirements.txt
    $ pip install -r requirements-dev.txt


Familiarise yourself with the code
----------------------------------
 
TODO.


Development workflow
--------------------

Use GitHub. You will have already cloned the SeqFindr repo (if you followed 
instructions above). To make things easier, please fork 
(https://github.com/mscook/SeqFindr/fork) and update your local copy to point to 
your fork.

Something like this::

    $ # Assuming your fork is like this
    $ # https://github.com/$YOUR_USERNAME/SeqFindr/
    $ vi .git/config
    $ # Replace:
	$ # url = git@github.com:mscook/SeqFindr.git
    $ #  with:
    $ # url = git@github.com:$YOUR_USERNAME/SeqFindr.git

With this setup you will be able to push development changes to your fork and 
submit Pull Requests to the core SeqFindr repo when you're happy. 

**Important Note:** Upstream changes will not be synced to your fork by 
default. Please, before submitting a pull request please sync your fork with 
any upstream changes (specifically handle any merge conflicts). Info on 
syncing a fork can be found here_.


Code style/testing/Continuous Integration
------------------------------------------

We try to make joining and/or modifying the SeqFindr project simple.

General:
    * As close to PEP8 as possible but I ain't no Saint. Just a long as it's 
      clean and readable,
    * Using standard lib UnitTest. There are convenience functions 
      check_coverage.sh & tests/run_tests.sh respectively. We would prefer 
      SMART test vs 100 % coverage.

In the master GitHub repository we use hooks that call:
    * landscape.io (code QC)
    * Travis CI (continuous integration)
    * ReadTheDocs (documentation building)

.. _virtualenv-burrito: https://github.com/brainsik/virtualenv-burrito
.. _autoenv: https://github.com/kennethreitz/autoenv
.. _here: https://help.github.com/articles/syncing-a-fork
.. _doctest: http://pythontesting.net/framework/doctest/doctest-introduction/

.. _`this document by Jeff Forcier`: http://www.contribution-guide.org
.. _`this talk from Carl Meyer`: http://pyvideo.org/video/2637/set-your-code-free-releasing-and-maintaining-an

