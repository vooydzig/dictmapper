dictmapper
=
Data mapper from one deserialized json object to another.

The "Why"
--
Let's say You have two APIs that both consume and produce data as JSON.
One returns data in schema A, and You want to transform this data and push it onto another API with schema B.

Here comes `dictmapper`! 

Using dict mapper You can create quick and simple mappings from one schema to another using JSONPath syntax.

The "How"
--  

Check `tests.py` for full list of examples and supported operations. Below is quick example:

```python
from mapper import JSONMapper, Mapping
#assume the following returns valid JSON data
# for example returns {"foo": 1}
source = json.loads(FirstApi.get_data_from_endpoint(endpoint)) 

m = JSONMapper(mapping=[Mapping(source='foo', destination='bar', transform=None)])

#assume the following consumes valid JSON data
# for example consumes {'bar': [number]}
SecondApi.post_data_to_endpoint(endpoint2, json.dumps(m.map(source_data)))
```
 
If anything goes wrong feel free to submit a ticket.

The dependency
--
`dictmapper` uses `jsonpath_rw` to parse JSONPaths. Check it out here: https://github.com/kennknowles/python-jsonpath-rw



Licence
--

DO WHAT YOU WANT WHEN FAME IS DUE
 
Version 1, July 2018
Copyright (C) 2018 Tomasz Wójcik

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

DO WHAT YOU WANT WHEN FAME IS DUE

TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
0. This is modified version of WTFPL(http://www.wtfpl.net) 
1. You just do what you want as long as:
 - You mention original author on either Twitter, Facebook, reddit or other social media(preferably with link to project)
 - You starred original repository on GitHub **or** give similar recognition on other repository hubs (bitbucket, GitLab, etc.)