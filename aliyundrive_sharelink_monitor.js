/*
[task_local]
0 0-23/3 * * * https://raw.githubusercontent.com/doyoman/doyo/main/aliyundrive_sharelink_monitor.js, tag=aliyundrive分享链接更新监控, img-url=eye.fill.system, enabled=true
*/

let share_links = "";

const $ = API("aliyundrive链接监控", true);

(async () => {
  $.log("begin...");
  if ($.env.isNode){
    share_links = process.env.al_share_links || [];
  }else{
    share_links = $.read("share_links") || share_links;
  }
  if (share_links.length == 0){
    await sendMessage("请添加分享链接...");
    $.done();
  }
  
  const share_link_list = share_links.split("&") || share_links.split("\n");
  $.log(`共有${share_link_list.length}条监控链接！`);
  const share_list = [];
  const share_pwd = "";
  for (link of share_link_list){
    if (/folder/.test(link)){
      const info = link.match(/.*com\/s\/(.*)\/folder\/(.*)/);
      share_list.push({
        link: info[0],
        share_id: info[1],
        parent_file_id: info[2]
      });
    }else{
      const info = link.match(/.*com\/s\/(.*)/);
      share_list.push({
        link: info[0],
        share_id: info[1],
        parent_file_id: "root"
      });
    }
  }
  let i = 1;
  for (share of share_list){
    const {link, share_id, parent_file_id} = share;
    const share_token = await getToken(share_id, share_pwd);
    const items = await getFileList(share_token, share_id, parent_file_id);
    if ($.read(share_id)) {
      if ($.read(share_id) !== items.length){
        $.write(items.length, share_id);
        await sendMessage(`您监控的第${i}个阿里云盘分享资源有更新啦！`, "点我前去查看...", link);
      }else{
        await sendMessage(`您监控的第${i}个阿里云盘分享资源没有更新!`, "点我前去查看...", link)
      }
    }else{
      $.write(items.length, share_id);
      await sendMessage(`您监控的第${i}个阿里云盘分享链接共有${items.length}个文件或文件夹！`, "点我前去查看...", link)
    }
    await $.wait(2000);
    i++
  }
})();

async function getToken(share_id, share_pwd) {
  const rawbody = JSON.stringify({
  "share_id" : share_id,
  "share_pwd" : share_pwd
  })
  const headers = {
    'Host': 'api.aliyundrive.com',
    'Accept': 'application/json, text/plain, */*',
    'X-Canary': 'client=web,app=adrive,version=v2.3.1',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Content-Type': 'application/json;charset=utf-8',
    'Origin': 'https://www.aliyundrive.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.aliyundrive.com/',
    'Content-Length': rawbody.length
    }
  return $.http.post({
    url: "https://api.aliyundrive.com/v2/share_link/get_share_token",
    body: rawbody,
    headers
  }).then(rsp => {
    const body = JSON.parse(rsp.body);
    return body.share_token
  });
}

function getFileList(share_token, share_id, parent_file_id) {
  const rawbody = JSON.stringify({
  "share_id" : share_id,
  "limit" : 100,
  "parent_file_id" : parent_file_id
});
  const headers = {
    'Host': 'api.aliyundrive.com',
    'Accept': 'application/json, text/plain, */*',
    'X-Canary': 'client=web,app=adrive,version=v2.3.1',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Content-Type': 'application/json;charset=utf-8',
    'Origin': 'https://www.aliyundrive.com',
    'Content-Length': rawbody.length,
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1',
    'Referer': 'https://www.aliyundrive.com/',
    'Connection': 'keep-alive',
    'x-share-token': share_token
    };
  return $.http.post({
    url: "https://api.aliyundrive.com/adrive/v3/file/list",
    body: rawbody,
    headers
  }).then(rsp => {
    const body = JSON.parse(rsp.body);
    return body.items
  })
}

async function sendMessage(message, content="", url="") {
  if ($.env.isNode){
    const barkKey = process.env.BARK_PUSH || "";
    if (barkKey) {
      if (/http/.test(barkKey)) {
        await $.http.get(`${barkKey}/${encodeURIComponent($.name)}/${encodeURIComponent(message)}?url=${url}`);
      } else {
        const url2 = `https://api.day.app/${barkKey}/${encodeURIComponent($.name)}/${encodeURIComponent(message)}?url=${url}`;
        await $.http.get(url2);
      }
    }
  }else{
    $.notify($.name, message, content, {"open-url": url});
  }
}

function ENV(){const e="function"==typeof require&&"undefined"!=typeof $jsbox;return{isQX:"undefined"!=typeof $task,isLoon:"undefined"!=typeof $loon,isSurge:"undefined"!=typeof $httpClient&&"undefined"!=typeof $utils,isBrowser:"undefined"!=typeof document,isNode:"function"==typeof require&&!e,isJSBox:e,isRequest:"undefined"!=typeof $request,isScriptable:"undefined"!=typeof importModule}}function HTTP(e={baseURL:""}){const{isQX:t,isLoon:s,isSurge:o,isScriptable:n,isNode:i,isBrowser:r}=ENV(),u=/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/;const a={};return["GET","POST","PUT","DELETE","HEAD","OPTIONS","PATCH"].forEach(h=>a[h.toLowerCase()]=(a=>(function(a,h){h="string"==typeof h?{url:h}:h;const d=e.baseURL;d&&!u.test(h.url||"")&&(h.url=d?d+h.url:h.url),h.body&&h.headers&&!h.headers["Content-Type"]&&(h.headers["Content-Type"]="application/x-www-form-urlencoded");const l=(h={...e,...h}).timeout,c={onRequest:()=>{},onResponse:e=>e,onTimeout:()=>{},...h.events};let f,p;if(c.onRequest(a,h),t)f=$task.fetch({method:a,...h});else if(s||o||i)f=new Promise((e,t)=>{(i?require("request"):$httpClient)[a.toLowerCase()](h,(s,o,n)=>{s?t(s):e({statusCode:o.status||o.statusCode,headers:o.headers,body:n})})});else if(n){const e=new Request(h.url);e.method=a,e.headers=h.headers,e.body=h.body,f=new Promise((t,s)=>{e.loadString().then(s=>{t({statusCode:e.response.statusCode,headers:e.response.headers,body:s})}).catch(e=>s(e))})}else r&&(f=new Promise((e,t)=>{fetch(h.url,{method:a,headers:h.headers,body:h.body}).then(e=>e.json()).then(t=>e({statusCode:t.status,headers:t.headers,body:t.data})).catch(t)}));const y=l?new Promise((e,t)=>{p=setTimeout(()=>(c.onTimeout(),t(`${a} URL: ${h.url} exceeds the timeout ${l} ms`)),l)}):null;return(y?Promise.race([y,f]).then(e=>(clearTimeout(p),e)):f).then(e=>c.onResponse(e))})(h,a))),a}function API(e="untitled",t=!1){const{isQX:s,isLoon:o,isSurge:n,isNode:i,isJSBox:r,isScriptable:u}=ENV();return new class{constructor(e,t){this.name=e,this.debug=t,this.http=HTTP(),this.env=ENV(),this.node=(()=>{if(i){return{fs:require("fs")}}return null})(),this.initCache();Promise.prototype.delay=function(e){return this.then(function(t){return((e,t)=>new Promise(function(s){setTimeout(s.bind(null,t),e)}))(e,t)})}}initCache(){if(s&&(this.cache=JSON.parse($prefs.valueForKey(this.name)||"{}")),(o||n)&&(this.cache=JSON.parse($persistentStore.read(this.name)||"{}")),i){let e="root.json";this.node.fs.existsSync(e)||this.node.fs.writeFileSync(e,JSON.stringify({}),{flag:"wx"},e=>console.log(e)),this.root={},e=`${this.name}.json`,this.node.fs.existsSync(e)?this.cache=JSON.parse(this.node.fs.readFileSync(`${this.name}.json`)):(this.node.fs.writeFileSync(e,JSON.stringify({}),{flag:"wx"},e=>console.log(e)),this.cache={})}}persistCache(){const e=JSON.stringify(this.cache,null,2);s&&$prefs.setValueForKey(e,this.name),(o||n)&&$persistentStore.write(e,this.name),i&&(this.node.fs.writeFileSync(`${this.name}.json`,e,{flag:"w"},e=>console.log(e)),this.node.fs.writeFileSync("root.json",JSON.stringify(this.root,null,2),{flag:"w"},e=>console.log(e)))}write(e,t){if(this.log(`SET ${t}`),-1!==t.indexOf("#")){if(t=t.substr(1),n||o)return $persistentStore.write(e,t);if(s)return $prefs.setValueForKey(e,t);i&&(this.root[t]=e)}else this.cache[t]=e;this.persistCache()}read(e){return this.log(`READ ${e}`),-1===e.indexOf("#")?this.cache[e]:(e=e.substr(1),n||o?$persistentStore.read(e):s?$prefs.valueForKey(e):i?this.root[e]:void 0)}delete(e){if(this.log(`DELETE ${e}`),-1!==e.indexOf("#")){if(e=e.substr(1),n||o)return $persistentStore.write(null,e);if(s)return $prefs.removeValueForKey(e);i&&delete this.root[e]}else delete this.cache[e];this.persistCache()}notify(e,t="",a="",h={}){const d=h["open-url"],l=h["media-url"];if(s&&$notify(e,t,a,h),n&&$notification.post(e,t,a+`${l?"\n多媒体:"+l:""}`,{url:d}),o){let s={};d&&(s.openUrl=d),l&&(s.mediaUrl=l),"{}"===JSON.stringify(s)?$notification.post(e,t,a):$notification.post(e,t,a,s)}if(i||u){const s=a+(d?`\n点击跳转: ${d}`:"")+(l?`\n多媒体: ${l}`:"");if(r){require("push").schedule({title:e,body:(t?t+"\n":"")+s})}else console.log(`${e}\n${t}\n${s}\n\n`)}}log(e){this.debug&&console.log(`[${this.name}] LOG: ${this.stringify(e)}`)}info(e){console.log(`[${this.name}] INFO: ${this.stringify(e)}`)}error(e){console.log(`[${this.name}] ERROR: ${this.stringify(e)}`)}wait(e){return new Promise(t=>setTimeout(t,e))}done(e={}){s||o||n?$done(e):i&&!r&&"undefined"!=typeof $context&&($context.headers=e.headers,$context.statusCode=e.statusCode,$context.body=e.body)}stringify(e){if("string"==typeof e||e instanceof String)return e;try{return JSON.stringify(e,null,2)}catch(e){return"[object Object]"}}}(e,t)}