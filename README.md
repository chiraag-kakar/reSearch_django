# reSearch_django


```
API Endpoints
```

* https://restresearch.pythonanywhere.com/api/v1/index/

```HTTP Method : POST```

Content :
```
{
"data" : "hello world"
}
```

Response :
```
{
    "status": 1
}
```

---

* https://restresearch.pythonanywhere.com/api/v1/search/

```HTTP Method : GET```

Content :
```
{
"data" : "hello"
}
```

Response :
```
{
    "docs": [
        [
            1,
            0,
            "hello world"
        ]
    ]
}
```

` Note : 1 is the frequency and 0 is the id assigned to the document `

---


* https://restresearch.pythonanywhere.com/api/v1/clear/

```HTTP Method : GET```

Response :
```
{
    "info": "All the indexes has been cleared."
}
```

---

* https://restresearch.pythonanywhere.com/api/v1/all/

```HTTP Method : GET```

Response :
```
{
    "docs": [
        [
            0,
            "hello world"
        ]
    ]
}
```

<!--https://restresearch.pythonanywhere.com/api/v1/doc/<int:id>/-->
