SeqFindR release map
====================

See open `issues`_. Feel free to fork, clone, fix, test, push and send a pull
request. Please, before you submit a pull request, could you sync with the 
upstream (this) master. Please see this `tutorial`_ on how to do this.


Minor
-----

Current small fixes:
    * Provide a figure rotation option

Image rotation can be accomplished by doing something like this::
   
    import Image
    img = Image.open("plot.jpg")
    img2 = img.rotate(45)
    img2.show()
    img2.save("rotate.jpg")


Major
-----

Current major fixes/improvements:
    * make into a web app
    * tests !!!

.. _issues: https://github.com/mscook/SeqFindR/blob/master/TODO.rst
.. _tutorial: https://help.github.com/articles/syncing-a-fork
