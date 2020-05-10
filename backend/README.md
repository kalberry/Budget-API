# Budget Scheduler API

## Description
This project will receive, calculate and output data based on budget scheduling needs.
It will communicate with a database and perform calculations for the user.

## Usage
The responses will have the form

```json
{
  "data": "Mixed type holding the content of the response",
  "message": "Description of what happened"
}
```

## API

## **Users**

### Create new user
**Definition**

`POST /api/v1/auth/register`

**Arguments**

- `"email":string` email of the user
- `"password_hash:string"` user's password hash
- `"last_pay_date:string"` Last paid date in "MM-DD-YYYY" format
- `"pay_frequency:int"` How often the user gets paid in days
- `"pay_dates:int"` Dates the user gets paid every month

**Response**

- `401 Unauthorized` if the user is not authorized for this request
- `201 Created` on success

``` json
{
  "id": 4,
  "email": "janedoe@email.com",
  "last_pay_date": "03/02/2020",
  "pay_frequency": 14,
  "pay_dates": [0]
}
```

### Login user
**Definition**

`POST /api/v1/auth/login`

**Arguments**

- `"email":string` email of the user
- `"password_hash:string"` user's password hash

**Response**

- `404 Not Found` if email or password is invalid
- `401 Unauthorized` if the user is not authorized for this request
- `200 OK` on success

``` json
{
  "id": 4,
  "email": "janedoe@email.com",
  "last_pay_date": "03/02/2020",
  "pay_frequency": 14,
  "pay_dates": [0]
}
```

## Update users

**Definition**

`PUT /api/v1/users`

**Arguments**

- `"id":int` id of the user
- `"email":string` optional. Update the email of the user
- `"password_hash:string"` optional. Update the user's password hash
- `"last_pay_date:string"` optional. Update the last paid date in "MM-DD-YYYY" format
- `"pay_frequency:int"` optional. Update how often the user gets paid in days
- `"pay_dates:int"` optional. Update dates the user gets paid every month

**Response**

- `404 Not Found` if the user is not found
- `401 Unauthorized` if the user is not authorized for this request
- `200 OK` on success

### Get all user data
**Definition**

`GET /api/v1/users`

**Arguments**

- `"id":int` optional. Return all information given a user id

**Response**

- `404 Not Found` if user does not exist
- `401 Unauthorized` if the user is not authorized for this request
- `200 OK` on success

``` json
[
  {
    "id": 4,
    "email": "janedoe@email.com",
    "last_pay_date": "03/02/2020",
    "pay_frequency": 14,
    "pay_dates": [0],
    "bills":
    [
      {
        "id": 6,
        "name": "National Grid",
        "cost": "43.47",
        "due_date": 0,
        "frequency": 30,
        "last_paid": "03-07-2020",
        "category": "utilities"
      },
      {
        "id": 12,
        "name": "Spectrum",
        "cost": "49.99",
        "due_date": 7,
        "frequency": 30,
        "last_paid": "03-14-2020",    
        "category": "utilities"
      }
    ],
    "pay_period_expenses":
    [
      {
        "id": 3,
        "name": "Groceries",
        "cost": "250",
        "category": "food"
      },
      {
        "id": 5,
        "name": "Gas",
        "cost": "40.00",
        "category": "automotive"
      }
    ]
  },
  {
    "id": 5,
    "email": "johndoe@email.com",
    "last_pay_date": "02/25/2020",
    "pay_frequency": 0,
    "pay_dates": [1,15],
    "bills":
    [
      {
        "id": 6,
        "name": "National Grid",
        "cost": "43.47",
        "due_date": 0,
        "frequency": 30,
        "last_paid": "03-07-2020",
        "category": "utilities"
      },
      {
        "id": 12,
        "name": "Spectrum",
        "cost": "49.99",
        "due_date": 7,
        "frequency": 30,
        "last_paid": "03-14-2020",    
        "category": "utilities"
      }
    ],
    "pay_period_expenses":
    [
      {
        "id": 3,
        "name": "Groceries",
        "cost": "250",
        "category": "food"
      },
      {
        "id": 5,
        "name": "Gas",
        "cost": "40.00",
        "category": "automotive"
      }
    ]
  }
]
```

## **Bills**

### Add new bills
**Definition**

`POST /api/v1/bills`

**Arguments**

- `"user_id":int` id of the user the bill will apply to
- `"name":string` name of the company you pay the bill to
- `"cost:float"` how much the bill costs per month
- `"due_date:int"` What day per month the bill falls on. Choose this or frequency
- `"frequency:int"` How many days until the next bill is due. Choose this or due_date
- `"last_paid:string"` Date when the last bill was paid in "MM-DD-YYYY" format
- `"category:string"` Optional. If the user wants to put it in a specific category

**Response**

- `401 Unauthorized` if the user is not authorized for this request
- `400 Bad Request` if information is missing from the request
- `201 Created` on success

```json
{
  "id": 6,
  "name": "National Grid",
  "cost": "43.47",
  "due_date": 0,
  "frequency": 30,
  "last_paid": "03-07-2020",
  "category": "utilities"
}
```

## Lookup all bills
**Definition**

`GET /api/v1/bills`

**Arguments**

- `"id":int` optional. Returns bill data based on bill ids
- `"user_id":int` optional. Returns a list of bills that the id of the user the bill will apply to

**Response**

- `404 Not Found` if the bill does not exist
- `401 Unauthorized` if the user is not authorized for this request
- `400 Bad Request` if information is missing from the request
- `200 OK` on success

``` json
[
  {
    "id": 6,
    "name": "National Grid",
    "cost": "43.47",
    "due_date": 0,
    "frequency": 30,
    "last_paid": "03-07-2020",
    "category": "utilities",
    "user_id": 4
  },
  {
    "id": 12,
    "name": "Spectrum",
    "cost": "49.99",
    "due_date": 7,
    "frequency": 30,
    "last_paid": "03-14-2020",    
    "category": "utilities"
  }
]
```

## Update bill

**Definition**

`PUT /api/v1/bills`

**Arguments**

- `"id":int` id of the bill
- `"name":string` optional. Change the name of the company you pay the bill to
- `"cost:float"` optional. Change how much the bill costs per month
- `"category:string"` optional. Change the category

**Response**

- `404 Not Found` if the bill is not found
- `401 Unauthorized` if the user is not authorized for this request
- `200 OK` on success

## Delete a bill

**Definition**

`DELETE /api/v1/bills`

**Arguments**

- `"id":int` Deletes bills based on bill ids

**Response**

- `404 Not Found` if the bill does not exist for that user
- `401 Unauthorized` if the user is not authorized for this request
- `204 No Content` if the bill is deleted

## **Pay Period Expenses**

### Add new pay period expenses
**Definition**

`POST /api/v1/ppe`

**Arguments**

- `"user_id":int` id of the user adding to pay period expenses
- `"name":string` name of pay period expense
- `"cost:float"` how much the pay period expense costs
- `"category:string"` optional. If the user wants to put it in a specific category

**Response**

- `401 Unauthorized` if the user is not authorized for this request
- `201 Created` on success

```json
{
  "id": 6,
  "name": "National Grid",
  "cost": "43.47",
  "category": "utilities"
}
```

## Delete a pay period expense

**Definition**

`DELETE /api/v1/ppe`

**Arguments**

- `"id":int` Deletes pay period expenses based on pay period expenses ids

**Response**

- `404 Not Found` if the pay period expense does not exist for that user
- `401 Unauthorized` if the user is not authorized for this request
- `204 No Content` if the pay period expense is deleted

## Lookup pay period expense details
**Definition**

`GET /api/v1/ppe`

**Arguments**

- `"id":int` optional. Returns pay period expenses data based on pay period expense ids
- `"user_id":int` optional. Returns a list of pay period expenses that the id of the user the pay period expense will apply

**Response**

- `404 Not Found` if the pay period expense does not exist
- `401 Unauthorized` if the user is not authorized for this request
- `200 OK` on success

``` json
[
  {
    "id": 6,
    "name": "National Grid",
    "cost": "43.47",
    "category": "utilities",
    "user_id": 4
  },
  {
    "id": 5,
    "name": "Gas",
    "cost": "40.00",
    "category": "automotive"
  }
]

```

## Update pay period expense

**Definition**

`PUT /api/v1/ppe/<id>`

**Arguments**

- `"name":string` optional. Change the name of the company you pay the bill to
- `"cost:float"` optional. Change how much the bill costs per month
- `"due_date:int"` optional. Change what day per month the bill falls on. Choose this or frequency
- `"frequency:int"` optional. Change how many days until the next bill is due
- `"last_paid:string"` optional. Change date when the last bill was paid in "MM-DD-YYYY" format
- `"category:string"` optional. Change the category

**Response**

- `404 Not Found` if the pay period expense is not found
- `401 Unauthorized` if the user is not authorized for this request
- `200 OK` on success

## **Budget Schedule**

## Get budget schedule

**Definition**

`GET /api/v1/budgetschedule`

**Arguments**

- `"user_id":int` returns a list of expenses in the pay periods. Default is 24
- `"count":int` optional. Amount of pay periods to return. Max 48

**Response**

- `404 Not Found` if the user id is not found
- `401 Unauthorized` if the user is not authorized for this request
- `400 Bad Request` if the arguments of count is above 48
- `200 OK` on success

``` json
[
  {
    "pay_date": "05/08/2020",
    "end_pay_date": "05/21/2020",
    "pay_period_expenses":
    [
      {
        "id": 3,
        "name": "Groceries",
        "cost": "250",
        "category": "food"
      },
      {
        "id": 5,
        "name": "Gas",
        "cost": "40.00",
        "category": "automotive"
      }
    ],
    "bills":
    [
      {
        "id": 6,
        "name": "National Grid",
        "cost": "43.47",
        "due_date": 0,
        "frequency": 30,
        "last_paid": "03-07-2020",
        "category": "utilities"
      },
      {
        "id": 12,
        "name": "Spectrum",
        "cost": "49.99",
        "due_date": 7,
        "frequency": 30,
        "last_paid": "03-14-2020",    
        "category": "utilities"
      }
    ]
  },
  {
    "pay_date": "05/22/2020",
    "end_pay_date": "06/04/2020",
    "pay_period_expenses":
    [
      {
        "id": 3,
        "name": "Groceries",
        "cost": "250",
        "category": "food"
      },
      {
        "id": 5,
        "name": "Gas",
        "cost": "40.00",
        "category": "automotive"
      }
    ],
    "bills":
    [
      {
        "id": 13,
        "name": "Netlfix",
        "cost": "13.99",
        "due_date": 27,
        "frequency": 0,
        "last_paid": "04-27-2020",
        "category": "entertainment"
      },
      {
        "id": 14,
        "name": "Spotify",
        "cost": "49.99",
        "due_date": 1,
        "frequency": 0,
        "last_paid": "04-01-2020",    
        "category": "entertainment"
      }
    ]
  }
]
```
