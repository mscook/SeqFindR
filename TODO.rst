Current small fixes:
    * -o OUTPUT, --output OUTPUT flag does not do anything
    * Improve current Argparse setup
    * Provide a rotation option. 

Image rotation can be accomplished by doing something like this:: 
   
    import Image
    img = Image.open("plot.jpg")
    img2 = img.rotate(45)
    img2.show()
    img2.save("rotate.jpg")
