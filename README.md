# Wallet

Simple application for sending money

## Usage

Build the docker image using

```docker build -t wallet .```

After that, run `docker-compose up`

The app will be available at localhost:5010 accessible with the following API.
Migrations will create two users

 - username: UserOne | password: Test123
 - username: UserTwo | password: Test456

## API

Description of the API.
There is also a Postman JSON.

#### Status
Returns if app is up and running.
```
GET
<host>/status
```

#### Login
Logs in user
Body
```
{
    "username": <username>,
    "password": <password>
}
```

```
POST
<host>/login
```
Returns session to be used with further requests.

#### Balance
Returns logged in user balance.
Needs `session_id` in `headers`
```
GET
<host>/balance
```
Returns amount of money user has

#### Transaction
Gets all transactions for the user.
Both sent and received.
Needs `session_id` in `headers`
```
GET
<host>/transaction
```

Creates a transaction.
Needs `session_id` in `headers`
```
POST
<host>/transaction
```
Body needs to be 
```
{
    "amount": <amount to send>,
    "receiver": <username of the receiver>
}
```

## Tests

There is a set of integration tests that REQUIRE running postgres instance.
If you have docker you can simply run command such as 
```
docker run -e POSTGRES_PASSWORD=password -p 5432:5432 postgres
``` 
And everything should work out of the box. Otherwise you might need to check `config/__init__.py` and set it accordingly.

There is a small unittest regardin sending transactions.
