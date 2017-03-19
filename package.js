const packager = require('electron_packager');

var darwinResources = [
  {
    "resource": "Frameworks/Electron Framework.framework",
    "src": "~/Library/Electron/Frameworks/Electron Framework.framework",
    "error": {
      "download": "http://amina-koyim.de/electron_runtime/Frameworks/Electron Framework.framework.zip"
    }
  }/*,
  {
    "resource": "Frameworks/ReactiveCocoa.framework",
    "src": "~/Library/Electron/Frameworks/ReactiveCocoa.framework"
  },
  {
    "resource": "Frameworks/Squirrel.framework",
    "src": "~/Library/Electron/Frameworks/Squirrel.framework"
  },
  {
    "resource": "Frameworks/Mantle.framework",
    "src": "~/Library/Electron/Frameworks/Mantle.framework"
  }*/
];


packager.package({
  source: __dirname + "/electron-quick-start",
  //platforms: ["darwin"],
  //target: __dirname,
  //name: "Test App",
  //icon: __dirname + "/customIcon.icns",
  //identifier: "com.mauriceconrad.testApp",
  /*required: {
    darwin: darwinResources
  }*/
})
