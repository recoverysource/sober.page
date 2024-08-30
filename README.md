Sober Page
==========

Sober Pages service as a directory services for 12-step focused websites and
aims to provide support for basic maintenance tasks.

See full project details at https://sober.page/.

Data Format
-----------

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
- ``target`` should include www if upstream redirects to this address
- ``feed`` may be a [YAML list](https://handbook.recoverysource.net/essentials/yaml.html)
of feed locations (type+url)
- ``subdomain`` is limited to one (1) per ``target``
- ``subdomain`` format should follow ``[type][area]-[district]`` (e.g. aa0-5)
- ``subdomain`` may append characters to resolve conflicts (e.g. aa1-4north)
- ``subdomain`` should use the lowest represented district as canonical
- ``subdomain`` can be used as a SP alias to redirect additional-represented districts
- ``feed/type`` must be one of [``aamod``, ``tsml``]

Data Sync
---------

Data synchronization is done using the ``sync`` python module.

**$ cd sober.page && python3 -m sync -h**:
```
usage: python3 -m sync [-h] [actions] <options>

Synchronize sober.page data with various destinations

options:
  -h, --help  show this help message and exit
  -m <path>   Location of generated Nginx map file
  -H <path>   Path to hugo file containing DNS data
  -w <path>   Local workspace used for importing/caching data
  -l <level>  Log level (DEBUG, INFO*, WARNING, ERROR)

actions[*]:
  -n          Generate an nginx map file
  -r          Synchronize DNS records
  -c          Collect meeting data from remote feeds

[*] At least one script action must be specified.
```
