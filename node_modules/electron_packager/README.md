# Electron Packager

A electron packager that packages your application bundle less than 1 MB!

Please keep in mind that this works only on *macOS* at the moment.

## How does it work?

The packaged application bundle of your app is so small because it doesn't contains large resources like `Electron Framework.framework`. These resources are stored globally in the library of a user (*macOS*).

If the resources in your library do not exist, a downloading process will be started.

A detailed explanation how the packer works sou find below.


## Module

### Install
```bash
npm install electron_packager
```

```javascript
const electronPackager = require("electron_packager");
```

### Packaging an app

```javascript
electronPackager.package({
  source: "your/source/electron/app/directory",
  platform: "darwin", // At the moment only darwin possible
  target: "your/target/folder", // Default: your/source/directory/..
  name: "My app name", // Default: name from package.json
  icon: "your/icon/file.icns", // Default: false
  identifier: "com.yourapp.yourcompany", // Default: a combination of properties from package.json
  version: "latest" // Electron version you want to use! Default: "latest"
  /*required: {
    darwin: darwinResources
  }*/
}, function(err, result) {
  if (err) return console.error(err);
  console.log(result);
});

```

As you see, you can specify the electron version, your bundle shall be bundled with.
This is important because all applications on one user account use the same electron resources.

## CLI

```bash
npm install electron_packager -g
```


```bash
electron_packager src=<source> target=<target> name=YourApp icon=/your/icon/file.icns identifier=com.yourApp.yourCompany version=latest
```

| Argument   | Default                         |
|------------|---------------------------------|
| src        | *Required*                      |
| target     | Parent directory of source      |
| name       | package.json->name              |
| icon       | **false**                       |
| identifier | Combine package.json properties |
| version    | **latest**                      |


#### Version Logic

If an application is used to start, the background manage process checks it's version and the version of the resources within the library. If the version of your app is higher than the version of the resources within the library, a downloading process will download the latest version of electron.

If the app's version is lower than the installed version within the library, your program is going to open.

## Detailed

### Resources

The packaged bundle contains the file `Bundle.json` at `AppBundle.app/Contents/Bundle.js`.
This file is very important because it contains all resources that are stored globally within the library.

This file looks lie this:

```json
{
  "electron": {
    "version": "v1.6.11",
    "destination": "~/Library/Electron",
    "bundle": "Electron.app",
    "resources": [
      "Frameworks/Electron Framework.framework",
      "Frameworks/Squirrel.framework",
      "Frameworks/Mantle.framework",
      "Frameworks/ReactiveCocoa.framework",
      "Resources/electron.asar"
    ]
  },
  "executable": "MacOS/Electron"
}
```

Normally you shouldn't touch the file!

### Manage

To control the download logic and a lot of stuff before your electron app starts, a python handler is called. This handler is represented by the file `manage.py` at `AppBundle.app/Contents/MacOS/manage.py`.

Have a look! :)
