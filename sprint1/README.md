# FSTR API

FSTR API is an API that allows to POST, GET, PATCH objects
in FSTR DB with your app

## TASKS

### submitData POST method

My first task was creating a Python class to work
with FSTR DB.

I used Django Framework and Python Rest Framework.
Firstly, I created project, installed all 
instruments, secondly, I created models to compare
with FSTR DB. Then I started to work with
JSONRequest with Serializer and creating
view class. 

### submitData/<```id```> GET method

Second task was creating a response to request 
with id of PerevalAdded object.
I simply created get method to new view and did
filtering by id.

### submitData/<```id```> PATCH method

Third task was updating objects of Database using
PerevalAdded object id and JSONRequest. I
filtered PerevalAdded object, filtered other
objects what has connection to PerevalAdded object,
validating data and then patching it.

### submitData/?user_email=<```email```> GET method

Last task was creating GET method with query parameter
```user_email``` to response all PerevalAdded objects
info what was posted by this user (PK of User objects
is email). I did filtration and used previous
```GET method``` JSON Response format to add them in
```result``` array

## USAGE

### submitData POST method


This method is posting JSON Request with defined schema
and response is JSON with items: status, message,
id

Request example:
```json
{
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
 
  "add_time": "2021-09-22 13:18:13",
  "user": {"email": "qwerty@mail.ru", 		
        "fam": "Пупкин",
		 "name": "Василий",
		 "otc": "Иванович",
        "phone": "+7 555 55 55"}, 
 
   "coords":{
  "latitude": "45.3842",
  "longitude": "7.1525",
  "height": "1200"},
    
  "level":{"winter": "",
  "summer": "1А",
  "autumn": "1А",
  "spring": ""},
 
   "images": [{"data":"<картинка1>", "title":"Седловина"},
            {"data":"<картинка>", "title":"Подъём"}]
}
```

If Request is valid and all operations went successfully, then
response will be like this:

```json
{"status": 200, "message": null, "id": <id>}
```
```<id>``` will be PerevalAdded object id

If Request is not valid, then response will be:

```json
{"status": 400, "message": <error>, "id":  null}
```
```<error>``` will be Error message; what went wrong

If error is not ValidationError, then it will Response same json.

### submitData/<```id```> GET method

This method responses PerevalAdded object info by filtering its
id, given in query

Example of successful response:

```json
{
  "status": 200,
  "object": {
    "id": "2",
    "time_added": "2024-10-29 15:05:02.015892+00:00",
    "beautyTitle": "пер.",
    "otherTitles": "Триев",
    "connect": "",
    "add_time": "2021-09-22T13:18:13Z",
    "spring": "",
    "summer": "1А",
    "autumn": "1А",
    "winter": "",
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200",
    "user": "qwerty@mail.ru"
  }
}
```

If there is no PerevalAdded object with this id, then response will
be looking like this:

```json
{
    "status": 400,
    "message": "Объекта нет в базе данных",
    "id": 0
}
```

or 

```json
{"status": 400, "message": <error>, "id":  null}
```
```<error>``` will be Error message; what went wrong

### submitData/<```id```> PATCH method

This method patching PerevalAdded, Coords, Images, PerevalImages
objects if JSON request is valid, PerevalAdded object status is _New_
and all operations was successful

Request example:
```json
{
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
 
  "add_time": "2021-09-22 13:18:13",
  "user": {"email": "qwerty@mail.ru", 		
        "fam": "Пупкин",
		 "name": "Василий",
		 "otc": "Иванович",
        "phone": "+7 555 55 55"}, 
 
   "coords":{
  "latitude": "45.3842",
  "longitude": "7.1525",
  "height": "1200"},
    
  "level":{"winter": "",
  "summer": "1А",
  "autumn": "1А",
  "spring": ""},
 
   "images": [{"data":"<картинка1>", "title":"Седловина"},
            {"data":"<картинка>", "title":"Подъём"}]
}
```

If validation was failed, then response will be like this:
```json
{"state":0, "message": <error>}
```
```<error>``` will be Error message; what went wrong

If PerevalAdded object status is not New, then response will be:
```json
{"state":0, "message": "Запись не новая"}
```

Successful response looks like that:
```json
{"state": 1, "message": null}
```

### submitData/?user_email=<```email```> GET method

This method responses all PerevalAdded objects info what has same
```User.email``` as ```email```

If this User is not in FSTR Database, then response will be:
```json
{
  "state":0,
  "message":"Пользователя с такой почтой не существует",
  "result": null
}
```
Else, will be shown User`s PerevalAdded objects info in ```result```
```json
{
    "state": 1,
    "message": null,
    "result": [
        {
            "status": 200,
            "object": {
                "id": "1",
                "time_added": "2024-10-29 15:04:20.814534+00:00",
                "beautyTitle": "пер.",
                "otherTitles": "Триев",
                "connect": "",
                "add_time": "2021-09-22T13:18:13Z",
                "spring": "",
                "summer": "1А",
                "autumn": "1А",
                "winter": "",
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200",
                "user": "qwerty@mail.ru"
            }
        },
  ...]
}
```

## License

[MIT](https://choosealicense.com/licenses/mit/)