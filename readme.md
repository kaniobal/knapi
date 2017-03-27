Knapsack Problem Solver with REST API
=============================
Requirements
------------
* Django
* Django REST framework
* Celery
* RabbitMQ

Running
-------
1. Run RabbitMQ.
2. Run Celery worker.
3. Run Django web server.
4. Admin interface resides at /admin/, superuser deFoo with password WillvonBar is preset.
5. API can be found at /api/.

Using API
---------
To submit a knapsack problem to be solved, POST JSON of the form
```
{
  "num_items": 2,
  "capacity": 10,
  "items": [
    {
      "index": 0,
      "value": 8,
      "weight": 4
    },
    {
      "index": 1,
      "value": 10,
      "weight": 5
    }
  ]
}

```
to /api/. The response contains url to /api/<request_id>/ where the answer is given in knapsack_problem.in_knapsack_json along with other info. The format of a response is JSON unless user agent is a browser.
All requests should use simple auth with admin username/password.
