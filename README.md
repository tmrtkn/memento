# memento


## An example call

You can call app e.g. like this
```
curl -k "https://localhost:5000/add?url=foo" -H "Authorization:Memento Memento1" -X POST -d @request.data
```
or
```
curl -k "https://localhost:5000/add" -H "Authorization:Memento Memento1" -X POST -d "url=http://example.com/"
```

