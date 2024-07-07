Sober Pages
===========

Sober Pages service as a directory services for 12-step focused websites and
aims to provide support for basic maintenance tasks.

See full project details at https://sober.page/.

About Data
----------

**Location:** ``data/domains/<group>.yaml``

**Format [[YAML](https://handbook.recoverysource.net/essentials/yaml.html)]:**
```
<subdomain>:
  title: website title
  keywords: list, of, regions
  target: <URL>
  type: forward OR cname
  feed: <type>^<URL>[^<options>]
```

**Required:** subdomain, title, target

**Rules:**

- ``data/domains/*.yaml`` MUST be [valid YAML](https://yaml-online-parser.appspot.com/)
- [``title``, ``keywords``] may be mixed-case, all other fields must be lower-case
- ``target`` should be the shortest functional URL (without
[path/query/fragment](https://handbook.recoverysource.net/essentials/websites.html#url))
- ``feed`` may be a [YAML list](https://handbook.recoverysource.net/essentials/yaml.html)
of feed locations (type+url)
- ``subdomain`` is limited to one (1) per ``target``
- ``subdomain`` format should follow ``[type][area]-[district]`` (e.g. aa0-5)
- ``subdomain`` may append characters to resolve conflicts (e.g. aa1-4north)
- ``feed/type`` must be one of [``aamod``, ``tsml``]
