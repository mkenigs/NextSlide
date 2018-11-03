from zipfile import ZipFile
import shutil
import os
import glob
import re

def parsePPTX(file):
    setup(file)
    temp = parseXML()
    cleanup(file)
    return temp



def setup(file):
    zfile = (os.path.splitext(file)[0] + ".zip")
    shutil.copyfile(file, zfile)
    with ZipFile(zfile, 'r') as zip:
        zip.extractall()



def parseXML():
    files = glob.glob('./ppt/slides/*.xml')
    files = natural_sort(files)
    xml = []
    text = []
    for slide in files:
        with open(slide, 'r') as f:
            xml.append(f.read())
    for content in xml:
        temp = re.findall('<a:t>(.*?)</a:t>', content)
        t = " ".join(temp)
        text.append(t)
    print(text)


def cleanup(file):
    os.remove(os.path.splitext(file)[0] + ".zip")
    shutil.rmtree("ppt")
    shutil.rmtree("docProps")
    shutil.rmtree("_rels")
    os.remove("[Content_Types].xml")

#function credit to this stack overflow thread for the algo
# https://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)



if __name__ == "__main__":
    arr = parsePPTX("test.pptx")