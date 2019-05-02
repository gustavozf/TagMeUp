# TagMeUp

TagMeUp is a simple annotation tool made enterely using the Python language and the OpenCV library. 
With no installation/build required, the software is a terminal-based and easy to use labelling tool. 
Annotations can be made by a pre-defined sized frames, or by drag and dropping in the image sample, being saved as a JSON format file that can be later convertted.

### Prerequisites

The tool works in Python 3. Other than that, all you need to keep TagMeUp working is the libraries OpenCV and JSON for the Python Language. These can be installed by the following commands:

```
conda install -c conda-forge opencv 
conda install -c jmcmurray json 
```

### How To Use 

TagMeUp works by using the following command:

```
python3 tag_me_up.py -i "YOUR_INPUT"
```

All the possible arguments are:
```
"-i" or "--image"       : Path to the image sample or directory of images to be labelled.
"-d" or "--dimensions"  : Annotation's default size. Can be used as HEIGHTxWIDHT (ex.: "96x128") or as a proportion of the original input image sample (ex.: 0.1). Default: "32x32".
"-p" or "--init_point"  : Initial point of the annotation. Options:  tl (Top Left) or c (Center). Default: "c".
"-n" or "--num_classes" : Total of classes to be labelled. Default: 1.
"-o" or "--output"      : Output directory. Default: "/PATH/TagMeUp/output/"
"-e" or "--extension"   : Output image file format for cropped patches. Options: "png" or "jpg". Dafault: "png".
```

Images can be tagged by user mouse clicks (default annotation size) or by drag and dropping (free annotation). After the annotations are made, some operations can be performed:
```
+------------+--------------------------------------------+
| r          |  Reset annotations                         |
+------------+--------------------------------------------+
| w          | Change class to be annotated               |
+------------+--------------------------------------------+
| z          | Delete last tag                            |
+------------+--------------------------------------------+
| x          | Reinsert last deleted tag                  |
+------------+--------------------------------------------+
| c          | Crop images from tags                      |
+------------+--------------------------------------------+
| a          | Get previous image                         |
+------------+--------------------------------------------+
| d          | Get next image                             |
+------------+--------------------------------------------+
| s          | Save tags to jason file                    |
+------------+--------------------------------------------+
| esc        | Quit                                       |
+------------+--------------------------------------------+
```

