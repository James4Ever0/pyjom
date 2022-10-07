// import {
//     Wechaty
// } from 'wechaty';

// Could not find a declaration file
// for module 'qrcode-terminal'.
// '/media/root/help/pyjom/tests/wechat_bots/wechaty/node_modules/qrcode-terminal/lib/main.js'
// implicitly has an 'any'
// type.
// Try `npm i --save-dev @types/qrcode-terminal`
// if it exists or add a new declaration(.d.ts) file containing `declare module 'qrcode-terminal';`
// ts(7016)

// code was changed.
import {
    WechatyBuilder
} from 'wechaty'

import QRCode from 'qrcode-terminal';

// console.log(qrcode)
// console.dir(qrcode)

// this shit is installed under pyjom/node_modules without package.json over current directory. create a package.json here.

// npm init

const puppet_name = 'wechaty-puppet-wechat'; // this puppet is virtually fucked but only one untested wechat account might do this freaking job.
const browser_bin_path = '/root/.cache/ms-playwright/chromium-907428/chrome-linux/chrome';
const bot = WechatyBuilder.build({
    name: 'mybot',
    puppet: puppet_name,
    puppetOptions: {
        launchOptions: {
            executablePath: browser_bin_path,
            args: ["--no-sandbox"]
        }
    }
}) // get a Wechaty instance

// let bot = '';
// bot = new Wechaty({
//     name, // generate xxxx.memory-card.json and save login data for the next login
// });

//  二维码生成
function onScan(qrcode, status) {
    // do not ruin the freaking namespace.
    QRCode.generate(qrcode); // 在console端显示二维码
    const qrcodeImageUrl = [
        'https://wechaty.js.org/qrcode/',
        encodeURIComponent(qrcode),
    ].join('');
    console.log(qrcodeImageUrl);
}

// 登录
async function onLogin(user) {
    console.log(`贴心小助理${user}登录了`);
    if (config.AUTOREPLY) {
        console.log(`已开启机器人自动聊天模式`);
    }
    // 登陆后创建定时任务
    await initDay();
}

//登出
function onLogout(user) {
    console.log(`小助手${user} 已经登出`);
}

bot.on('scan', onScan);
bot.on('login', onLogin);
bot.on('logout', onLogout);
bot
    .start()
    .then(() => console.log('开始登陆微信'))
    .catch((e) => console.error(e));

console.log("hello world")