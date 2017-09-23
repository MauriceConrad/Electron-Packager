#! /usr/bin/python
import os
import errno
import json

thisPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/..")

bundleFile = open(thisPath + "/Bundle.json")
bundle = json.loads(bundleFile.read())
bundleFile.close()


def relPathParse(path):
    return path.replace("~", os.path.expanduser("~"))

def symLink(src, dst):
    try:
        os.symlink(src, dst)
    except OSError, e:
        if e.errno == errno.EEXIST:
            os.remove(dst)
            os.symlink(src, dst)

def makeFileDirsExists(src):
    exists = os.path.exists(src)
    if exists == False:
        try:
            os.makedirs(os.path.realpath(src + "/../"));
        except:
            pass
    return exists

def pathParse(path):
    return path.replace(" ", "\\ ")

def repeat_to_length(string_to_expand, length):
   return (string_to_expand * ((length/len(string_to_expand))+1))[:length]

def versionInt(versionStr):
    newInt = int(versionStr.replace("v", "").replace(".", ""))
    intLength = len(str(newInt))
    requiredLength = 10
    fillZeros = requiredLength - intLength

    intStr = str(newInt) + repeat_to_length("0", fillZeros)

    return int(intStr)


def downloadFile(url, file_name):
    print "Download resource"
    print url
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        statusDetailed = file_size_dl * 100. / file_size
        status = int(statusDetailed)
        progressFile = open(thisPath + "/MacOS/Progress.app/Contents/Resources/progress", "wb")
        progressFile.write(str(status))
        progressFile.close()
        print str(statusDetailed) + " %"

    f.close()
    progressFile = open(thisPath + "/MacOS/Progress.app/Contents/Resources/progress", "wb")
    progressFile.write("complete")
    progressFile.close()

src = relPathParse(bundle["electron"]["destination"])
bundlePath = src + "/" +bundle["electron"]["bundle"]
version = versionInt(bundle["electron"]["version"])
resources = bundle["electron"]["resources"]


def openApp():
    # Create new symlink for every outsources resource
    for item in resources:
        currPath = bundlePath + "/Contents/" + item
        targetPath = thisPath + "/" + item
        symLink(currPath, targetPath)

        pass
    print "Open app..."
    # Execute app now
    # Create path to executable
    execPath = (thisPath + "/" + bundle["executable"]).replace(" ", "\\ ")
    # Run command
    os.system(execPath)
    pass


def downloadApp():
    print "Bundle has to be downloaded"
    # Initialize communication file for progress indicator
    progressAppPath = thisPath + "/MacOS/Progress.app";
    progressFile = open(progressAppPath + "/Contents/Resources/progress", "wb")
    progressFile.write("0")
    progressFile.close()
    print "Open Progress.app"
    # Open Progress indicator as background task (Works out of the box)
    os.system(pathParse(progressAppPath + "/Contents/MacOS/applet") + " &")
    # Set registry url to the source of 'electron' package which is used as refernece for electron data
    npmUrl = "https://registry.npmjs.org/electron"

    print "Load Data from registry"
    print npmUrl

    # Get data from npm registry
    data = json.loads(urllib2.urlopen(npmUrl).read())
    # Get latest version of electron
    latestVersion = data["dist-tags"]["latest"]
    # Create git path for latest version
    url = 'https://github.com/electron/electron/releases/download/v' + latestVersion + '/electron-v' + latestVersion + '-darwin-x64.zip'
    # Set download path
    downloadFilePath = src + "/Electron-v" + latestVersion + ".zip"
    # Download source to download path
    downloadFile(url, downloadFilePath)
    # Download finished
    print "Finished Download"
    print "Saved at " + downloadFilePath
    # Unzip
    os.system('unzip -o ' + downloadFilePath + ' -d ' + src)
    # Delete zip file
    os.remove(downloadFilePath)
    # Open app
    openApp()


# Check bundle path for existence
exists = makeFileDirsExists(bundlePath)

if exists == True:
    # If it exists
    print "Is there"
    # Get bundle version
    versionFile = open(src + "/version")
    currVersion = versionInt(versionFile.read())
    print "Current version: " + str(currVersion)
    print "Required version:" + str(version)
    versionFile.close()
    # Check version for being compatible with the version of the app
    if currVersion >= version:
        # If version of app is <= version of bundle in ~/Libaray/Electron/...
        openApp()
        pass

    else:
        # If version is too low
        # Import urlib2 now becase it's needed
        import urllib2
        # Download app
        downloadApp()
        pass

    pass
else:
    # If bundle does not exists
    # Import urlib2 now becase it's needed
    import urllib2
    # Download app
    downloadApp()
    pass
