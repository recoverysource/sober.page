Sober Pages
===========

Sober Pages service as a directory services for 12-step focused websites and
aims to provide support for basic maintenance tasks.

See full project details at https://sober.page/.

About Data
----------

Location: ``data/domains/<group>.yaml``

Format:
```
<tag>:
  title: website title
  keywords: list, of, regions
  target: <URL>
  type: forward OR cname
  # feed can also be a list of feeds
  feed: <type>^<URL>
```

Optional Arguments: keywords, type, feed
