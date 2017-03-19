# Electron Packager

A Electron packager that packages you .app bundle smaller than 1 MB.

## How does it works?

The packaged *.app bundle* doesn't include (e.g. Electron Framework.framework) huge files like big frameworks but store them globally in the library of the system.

These global required resources are accessible from every *.app* that is packaged in this way. Therefore you just have to install the required resources one times.

### Works out of the box

Yes. The packaged .app bundle contains a small downloading process for the required resources. The specific mirrors are explained more detailed below.

## Install
 ```bash
 npm install electron_packager -g
 ```

## Command Line Interface

  All CLI arguments are optional except the *src*.
 ```bash
 electron_packager src=/path/to/app/folder
 ```
|Argument|Value|Default|
|---|---|---|
|src|/path/to/app|*Required* |
|target|/path/to/output|Parent folder of *src* |
|platform|'darwin' &#124;&#124; 'win' &#124;&#124; 'linux' &#124;&#124; 'all' |'all'|
|name|Custom Name|*{package.json->name}* |
|icon|/path/to/icon/file|false|
|identifier|com.developer.myapp|com.*{package.json->author}*.*{package.json->name}* |

**Please make sure that the packager actually only suppports macOS (darwin)!**

*Support for windows and linux is in development.*

### Functionality

 The functionality is very modular.

 In ```AppBundle.app/Contents/Bundle.json``` you'll find a file that contains within the object **resources** all resources that are required but not included in the .app bundle. Therefore it's theoretically possible to set custom required resources with custom mirrors. And yes, the electron_packager supports custom requirements but mostly it doesn't matters and there is no use case for it. But that's how it works.

 This is, how the Bundle.json normally looks like:

 ```json
 {
   "resources": [
     {
       "resource": "Frameworks/Electron Framework.framework",
       "src": "~/Library/Electron/Frameworks/Electron Framework.framework",
       "error": {
         "download": "http://amina-koyim.de/electron_runtime/Frameworks/Electron Framework.framework.zip"
       }
     },
     {
       "resource": "Frameworks/ReactiveCocoa.framework",
       "src": "~/Library/Electron/Frameworks/ReactiveCocoa.framework",
       "error": {
         "download": "http://amina-koyim.de/electron_runtime/Frameworks/ReactiveCocoa.framework.zip"
       }
     },
     {
       "resource": "Frameworks/Squirrel.framework",
       "src": "~/Library/Electron/Frameworks/Squirrel.framework",
       "error": {
         "download": "http://amina-koyim.de/electron_runtime/Frameworks/Squirrel.framework.zip"
       }
     },
     {
       "resource": "Frameworks/Mantle.framework",
       "src": "~/Library/Electron/Frameworks/Mantle.framework",
       "error": {
         "download": "http://amina-koyim.de/electron_runtime/Frameworks/Mantle.framework.zip"
       }
     }
   ],
   "executable": "MacOS/Electron"
 }

 ```

 As you can see, it's a very simple structure. And you shouldn't touch it normally.
 In the *error* key of a resource item, there is a key named *download*. That is the mirror that will be used if the required resource can't be found.


## Module

 ```javascript
const packager = require('electron_packager');

packager.package({
  source: __dirname + "/electron-quick-start", // Optional.  This is an example that will work with the git repository
  platforms: ["darwin"], // Optional. "darwin" ||
  target: __dirname,
  name: "Test App",
  icon: __dirname + "/customIcon.icns",
  identifier: "com.mauriceconrad.testApp"/*,
  resources: { Don't use this property by default!
    darwin: Custom Requirements
  }*/
});
 ```
### Custom requirements

As already explained, the possibility to set a custom array of required resources that are **not** included is still there because it's a modular technique but I don't think that you need a custom array for the most scenarios.
The path in the **resource** key is a relative path from the ```/Contents/``` folder of the *.app bundle*. The **src** key is a global path that points on a folder named *Electron* in user's library by default.

By default the following resources are required:
1. (```Bundle.app/Contents/```)```Frameworks/Electron Framework.framework```
2. (```Bundle.app/Contents/```)```Frameworks/ReactiveCocoa.framework```
3. (```Bundle.app/Contents/```)```Frameworks/Squirrel.framework```
4. (```Bundle.app/Contents/```)```Frameworks/Mantle.framework```
