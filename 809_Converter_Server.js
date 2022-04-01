/*
###readme
联通809免流转换（测试）
每次更新订阅都会获取最新的免流参数
免流前提是你的节点服务端xray支持免流

在线url编码网站：http://www.jsons.cn/urlencode/

我建的(可直接使用)：
https://mianliu.doyo.workers.dev/?sublink=加上经过url编码的vmess链接或订阅链接，可以添加多个，url编码时换行隔开

自建指南：
前提装好了node和npm
1、mkdir 809sub && cd 809sub
2、wget https://raw.githubusercontent.com/doyoman/doyo/main/809_Converter_Server.js
3、npm install axios express
4、npm install pm2 -g
5、pm2 start 809_Converter_Server.js

使用方法：
一把唆
http://你的IP:3000/sub?sublink=加上经过url编码的vmess链接或订阅链接，可以添加多个，url编码时换行隔开

！注意，添加太多链接会导致url过长

拼接好的url就是新的订阅链接，在软件上手动或定时更新即可
*/

const axios = require("axios");
const crypto = require('crypto');
const express = require("express");

const app = express();

app.get('/sub', async function (req, res) {
try {
    if (req.query.sublink && req.query.sublink.length != 0) {
        const linkLi = req.query.sublink.split("\n");
        console.log(linkLi)
        const vmessLi = await getVmess(linkLi);
        const vmessS = vmessLi.filter(i => i && i.trim());
        let i = 0;
        const reVmessLi = await Promise.all(vmessS.map(v => {
          i++;
          return reVmess(v, i)
        }));
        const text = enBase64(reVmessLi.join("\n"));
        res.send(text);
    } else {
        res.send("请在sublink=后加上你经过url编码的订阅链接或vmess链接,如有多个请在编码前以换行符隔开。")
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
    const spkey = getMd5(`if5ax/?fakeid=${fakeid}&spid=31117&pid=31117&spip=${spip}&spport=${spport}3d99ff138e1f41e931e58617e7d128e2`);
    const headers = {
        'Host': 'dir.wo186.tv:809',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36'
    };

    const options = {
        headers: headers,
    };

    const url = `http://dir.wo186.tv:809/if5ax/?fakeid=${fakeid}&spid=31117&pid=31117&spip=${spip}&spport=${spport}&spkey=${spkey}`;
    return axios.get(url, options).then(rsp => rsp.data.url);
}

async function reVmess(v, n) {
    let item = JSON.parse(v);
    const fakeid = getFakeID();
    let { add, port, ps, path } = item;
    if (/\/if5ax\//.test(path)) {
      add = path.match(/.*&spip=(.*?)&.*/)[1];
      port = path.match(/.*&spport=(.*?)&.*/)[1];
    }
    const url = await getUrl(add, port, fakeid);
    path = url.split(":809")[1];
    const ip = url.split(":809")[0].replace(/http:\/\//, "");
    item = {
        ...item,
        add: ip,
        port: 809,
        host: ip,
        path: path,
        ps: `${ps}-联通809免流${n}`
    }
    const text = "vmess://" + enBase64(JSON.stringify(item));
    return text;
}

async function getVmess(linkLi) {
    let vmessLi = [];
    for (link of linkLi) {
        if (/vmess:\/\//.test(link)) {
            vmessLi.push(deBase64(link.replace(/vmess:\/\//, "")));
        } else if (/http:\/\//.test(link) || /https:\/\//.test(link)) {
            const data = await axios.get(link).then(rsp => rsp.data)
            const sub = deBase64(data).split("\n").filter(item => /vmess:\/\//.test(item));
            for (let j of sub) {
                j = j.replace(/[\r\n]/g, "").replace(/vmess:\/\//, "");
                vmessLi.push(deBase64(j));
            }
        }
    }
    return vmessLi;
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
