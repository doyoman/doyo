const { type, name } = $arguments;
const compatible_outbound = {
  tag: 'COMPATIBLE',
  type: 'block',
};

let compatible;
let config = JSON.parse($files[0]);
let proxies = await produceArtifact({
  name,
  type: /^1$|col/i.test(type) ? 'collection' : 'subscription',
  platform: 'sing-box',
  produceType: 'internal',
});

// console.log(config.outbounds);

config.outbounds.map(i => {
  if ("outbounds" in i && i.outbounds.includes("{all}") && "filter" in i) {
    i.outbounds = i.outbounds.filter(item => item != "{all}" && item != "block");

    let include_rule = i.filter.find(a => a.action == "include");
    let exclude_rule = i.filter.find(a => a.action == "exclude");

    let p;
    if (include_rule && exclude_rule) {
      let a = getTags(proxies, include_rule.keywords[0], true);
      let b = getTags(a, exclude_rule.keywords[0]);
      p = a.map(c => c.tag).filter(item => !b.includes(item));
    } else if (include_rule) {
      p = getTags(proxies, include_rule.keywords[0]);
    } else if (exclude_rule) {
      let a = getTags(proxies);
      let b = getTags(proxies, exclude_rule.keywords[0]);
      p = a.filter(item => !b.includes(item));
    }

    i.outbounds.push(...p);
    delete i.filter;
  } else if ("outbounds" in i && i.outbounds.includes("{all}") && !("filter" in i)) {
    i.outbounds = i.outbounds.filter(item => item != "{all}");
    i.outbounds.push(...getTags(proxies));
  }
});

config.outbounds.push(...proxies);

config.outbounds.forEach(outbound => {
  if (Array.isArray(outbound.outbounds) && outbound.outbounds.length === 0) {
    if (!compatible) {
      config.outbounds.push(compatible_outbound);
      compatible = true;
    }
    outbound.outbounds.push(compatible_outbound.tag);
  }
});

$content = JSON.stringify(config, null, 2);

function getTags(proxies, regex, noTag = false) {
  if (regex) {
    regex = new RegExp(regex);
  }
  if (noTag) {
    return (regex ? proxies.filter(p => regex.test(p.tag)) : proxies);
  } else {
    return (regex ? proxies.filter(p => regex.test(p.tag)) : proxies).map(p => p.tag);
  }
}