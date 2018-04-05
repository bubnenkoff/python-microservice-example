### Запуск

Можно так:
`uwsgi --http :9000 --wsgi-file main.py --callable app`

Или через конфиг:
`uwsgi --ini config.ini`

### Запрос

Пример запроса на выборку:
```
{
	"table_name": "transactions",
	"filters": [{
	  	"opcode" : [5, 472, 677, 905],
	  	"instrument_type_id":[1, 888, 474, 905, 4747],
		"status":["fail", "success", "wait"],
		"start_date": "2018-01-01",
		"end_date": "2018-01-02",
		"limit": 100,
		"offset": 0,
	}],
	"exclude_columns":["cs1", "cs2", "cs3", "cs4", "cs5"],
	"join": ["price", "cost"],
	"count": false
}
```

Все столбцы в разделе `filters` являются прямым аналогом имен столбцов из БД, кроме `start_date` и `end_date`. Они заменяю столбец `created`.

`table_name` пока не используется и может быть опущено.
`exclude_columns` и `join` так же могут быть опущены.

Минифицированная версия (без дат) для удобного копи-паста с включенным флагом `"count": false`:
```
curl -d '{"table_name":"transactions","filters":[{"opcode":[5,472,677, 905],"instrument_type_id":[1,888,474,905,4747],"status":["fail","success","wait"],"limit": 100, "offset": 0 }],"exclude_columns":["cs1","cs2","cs4","cs5"],"join":["price","cost"],"count":true}' -H "Content-Type: application/json" -X POST http://localhost:9000/
```
C датами:
```
curl -d '{"table_name":"transactions","filters":[{"opcode":[5,472,677,905],"instrument_type_id":[1,888,474,905,4747],"status":["fail","success","wait"],"start_date":"2018-01-01","end_date":"2018-01-02","limit": 100, "offset": 0}],"exclude_columns":["cs1","cs2","cs3","cs4","cs5"],"join":["price","cost"],"count":false}' -H "Content-Type: application/json" -X POST http://localhost:9000/
```

##### Сборка образа докера

`sudo docker build -t bubnenkoff/test2 .`

Запуск:

`docker run --net="host" bubnenkoff/test2`

Пример установки ENV (без этого не запустится)
`export config=/home/bubnenkov/code/microservices/tr_extractor/config.ini`

Пример установки ENV внутри самого докера:
`docker run --net="host" -e config='/app/tr_extractor/config.ini' bubnenkoff/test2`

