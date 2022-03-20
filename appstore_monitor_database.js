/*
AppStore价格监控数据库版
30 0-23/6 * * * appstore_monitor_database.js
*/

const axios = require("axios");
const redis = require("redis");

(async () => {
    const redisurl = process.env.redisurl;
    const client = redis.createClient({
        url: redisurl
    });
    client.on('error', (err) => console.log('Redis Client Error', err));
    await client.connect();
    if (await client.ping() == "PONG") {
        console.log("数据库连接成功！");
    } else {
        console.log("数据库连接失败！");
    }

    const list_url = "https://raw.githubusercontent.com/doyoman/doyo/main/list.json";
    const opt = {
        headers: {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
        }
    }

    let list;
    try {
        list = await axios.get(list_url, opt).then(rsp => rsp.data);
    } catch (error) {
        list = await axios.get("https://ghproxy.com/" + list_url, opt).then(rsp => rsp.data);
    }

    const text_list = [];
    for (let item of list) {
        const { id, country, name } = item;
        const price = await axios.get(`https://itunes.apple.com/lookup?id=${id}&country=${country}`, opt).then(rsp => rsp.data['results'][0]['price']);
        let symbol;
        if (country == "cn") {
            symbol = "¥";
        } else if (country == "us") {
            symbol = "$";
        } else {
            console.log("此国家金额标识未添加！");
        }
        text_list.push({
            id,
            name,
            price,
            country,
            symbol
        });
    }
    const oldapps = JSON.parse(await client.get("apps"));

    if (oldapps == null) {
        console.log("当前数据库中没有app价格数据。。。");
        const text = text_list.map(i => `${i.name}：${i.price}${i.symbol}`).join("\n");
        // console.log(text);
        await sendMessage(text);
    } else {
        let fls;
        for (const app of oldapps) {
            fls = text_list.map(j => {
                if (j.id == app.id && j.price != app.price) {
                    return {
                        name: app.name,
                        oldprice: app.price,
                        newprice: j.price,
                        symbol: app.symbol
                    }
                } else {
                    return null;
                }
            }).filter(fl => fl != null);
        }
        if (fls.length == 0) {
            console.log("所有价格未改变");
            await sendMessage("所有app价格都没变！");
        } else {
            console.log(`有${fls.length}个app价格发生变动！`);
            const text = fls.map(i => `${i.name}：${i.oldprice}${i.symbol}  ==>  ${i.newprice}${i.symbol}`).join("\n");
            // console.log(text);
            await sendMessage(text);
        }

    }
    await client.set("apps", JSON.stringify(text_list));
    await client.quit()

})();

async function sendMessage(message) {
    const botToken = process.env.EU_BOT;
    const botId = process.env.EU_ID;
    const barkKey = process.env.BARK_PUSH;

    if (barkKey) {
        const title = encodeURIComponent("AppStore价格监控");
        const text = encodeURIComponent(message);
        if (/http/.test(barkKey)) {
            await axios.get(`${barkKey}/${title}/${text}`);
        } else {
            const url2 = `https://api.day.app/${barkKey}/${title}/${text}`;
            await axios.get(url2);
        }

    }

    if (botToken) {
        const url1 = `https://api.telegram.org/bot${botToken}/sendMessage`;
        const data1 = {
            'chat_id': botId,
            'text': `*AppStore价格监控*
  
  ${message}`,
            'parse_mode': 'markdown'
        };
        await axios.post(url1, data1);
    }

}