const {
    app,
    BrowserWindow,
    ipcMain
} = require('electron');


const fs = require('fs')
let mainWindow;
// const {
//     download
// } = require("electron-dl")

// Quit when all windows are closed.
app.on('window-all-closed', function() {
    if (process.platform != 'darwin')
        app.quit();
});

// This method will be called when Electron has done everything
// initialization and ready for creating browser windows.
app.on('ready', function() {
    // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        frame: false,
        transparent: true,
        webPreferences: {
            // nodeIntegration: true,
            // nodeIntegrationInWorker: true,
            // nodeIntegrationInSubFrames: true,
            sandbox: false
        }
    });

    mainWindow.setIgnoreMouseEvents(false)

    // and load the index.html of the app.
    mainWindow.loadURL('file://' + __dirname + '/index.html').then(() => {
        console.log("EXECUTING JAVASCRIPT")
        mainWindow.webContents.executeJavaScript("animate()").then((videoblob) => {
            console.log("2", videoblob);
        })
        console.log("2 EXECUTING") // this is not blocking. not allowing below run.
        mainWindow.webContents.executeJavaScript("superDataFetcher()").then((videoblob) => {
            console.log("3", videoblob);
            let buffer = Buffer.from(videoblob)
            fs.writeFileSync('main.webm', buffer);
            console.log("FILE WRITTEN")
        })
        console.log("3 EXECUTING")



    })
    //     console.log(videoblob);});
    // mainWindow.webContents.openDevTools();
    // // this will change size.
    // Emitted when the window is closed.
    // mainWindow.on("download", (event, info) => {
    //     console.log("downloading")
    //     console.log(event, info)
    //     download(BrowserWindow.getFocusedWindow(), info.url, info.properties)
    //         .then(dl => window.webContents.send("download complete", dl.getSavePath()));
    // });
    // mainWindow.on("did-finish-load", () => {
    //     alert("EXECUTING JAVASCRIPT")
    //     var videoblob = mainWindow.webContents.executeJavaScript("animate()");
    //     console.log(videoblob);
    // })
    mainWindow.on('closed', function() {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        mainWindow = null;
    });
});