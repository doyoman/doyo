/*
###readme
联通809免流转换（测试）
每次更新订阅都会获取最新的免流参数
免流前提是你的节点服务端xray支持免流

在线url编码网站：http://www.jsons.cn/urlencode/

安装方法：
前提装好了node和npm
npm install axios express
npm install pm2 -g
pm2 start 809_Converter_Server.js

使用方法
订阅链接：
http://你的IP:3000/sub?sublink=加上经过url编码的订阅链接

vmess链接：
http://你的IP:3000/sub?vmess=加上经过url编码的vmess链接，可以添加多个，url编码时换行隔开

拼接好的url就是新的订阅链接，在软件上手动或定时更新即可
*/

const axios = require("axios");
const crypto = require('crypto');
const express = require("express");

const app = express();

app.get('/sub', async function (req, res) {
try {
    if (req.query.vmess) {
        const vmessDataLi = req.query.vmess.split("vmess://").filter(i => i && i.trim()).map(item => deBase64(item));
        const reVmessLi = await reVmess(vmessDataLi);
        const text = enBase64(reVmessLi.join("\n"));
        res.send(text);
    } else if (req.query.sublink) {
        console.log(req.query.sublink);
        const data = await getSub(req.query.sublink);
        const reVmessLi = await reVmess(data);
        const text = enBase64(reVmessLi.join("\n"));
        res.send(text);
    }
} catch (error) {
    console.log(error);
    res.send("出错了！这个链接不行哦！");
}
});

app.listen(3000, () => console.log("启动成功，端口3000"));


function getFakeID() {
    const str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let result = "";
    for (let i = 0; i < 22; i++) {
        result += str.charAt(Math.floor(Math.random() * str.length));
    }
    return result
}

function getUrl(spip, spport, fakeid) {
    const spkey = getMd5(`if5ax/?fakeid=${fakeid}&spid=81117&pid=81117&spip=${spip}&spport=${spport}3d99ff138e1f41e931e58617e7d128e2`);
    const headers = {
        'Host': 'dir.wo186.tv:809',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36'
    };

    const options = {
        headers: headers,
    };

    const url = `http://dir.wo186.tv:809/if5ax/?fakeid=${fakeid}&spid=81117&pid=81117&spip=${spip}&spport=${spport}&spkey=${spkey}`;
    return axios.get(url, options).then(rsp => rsp.data.url);
}

async function reVmess(vmessLi) {
    let reVmessLi = [];
    let n = 0;
    const v = vmessLi.filter(i => i && i.trim());
    for (let item of v) {
        item = JSON.parse(item);
        const fakeid = getFakeID();
        let { add, port, ps, path } = item;
        if (/\/if5ax\//.test(path)) {
          add = path.match(/.*&spip=(.*?)&.*/)[1];
          port = path.match(/.*&spport=(.*?)&.*/)[1];
        }
        const url = await getUrl(add, port, fakeid);
        path = url.split(":809")[1];
        const ip = url.split(":809")[0].replace(/http:\/\//, "");
        n += 1;
        item = {
            ...item,
            add: ip,
            port: 809,
            host: ip,
            path: path,
            ps: `${ps}-联通809免流${n}`
        }
        reVmessLi.push("vmess://" + enBase64(JSON.stringify(item)));
    }
    return reVmessLi
}

async function getSub(subLink) {
    const data = await axios.get(subLink).then(rsp => rsp.data);
    const vmessLi = deBase64(data).split("\n").filter(item => /vmess:\/\//.test(item));
    return vmessLi.map(i => {
        i = i.replace(/[\r\n]/g, "").replace(/vmess:\/\//, "");
        return deBase64(i)
    })
}

function getMd5(str) {
    return crypto.createHash('md5').update(str, 'utf8').digest('hex');
}

function enBase64(str) {
    return new Buffer(str).toString("base64");
}

function deBase64(str) {
    return new Buffer(str, "base64").toString();
}
