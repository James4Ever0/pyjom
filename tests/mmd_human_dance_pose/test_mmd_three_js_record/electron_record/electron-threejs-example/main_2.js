const {
    app,
    BrowserWindow
} = require('electron');
// const electron = require("electron");
// const {
//     app,
//     BrowserWindow
// } = electron;

const DownloadManager = require("electron-download-manager");

DownloadManager.register({
    downloadFolder: app.getPath("downloads")
});

// app.on("ready", () => {
//     let mainWindow = new BrowserWindow();
// });

let mainWindow;

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
        transparent: true
    });

    mainWindow.setIgnoreMouseEvents(true) // holy shit.

    // and load the index.html of the app.
    mainWindow.loadURL('file://' + __dirname + '/index_2.html'); // the evil three.js animation.
    mainWindow.webContents.openDevTools();

    // Emitted when the window is closed.
    mainWindow.on('closed', function() {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        mainWindow = null;
    });

});