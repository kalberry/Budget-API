# Budget Scheduler API

## Description
This project will receive and output data based on budget scheduling needs.
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
### List all bills
**Definition**
`GET /bills`
**Response**
`200 OK` on success

```json
[
  {
    "id": "6",
    "name": "National Grid",
    "cost": "43.47",
    "due_date": 0,
    "frequency": 30,
    "last_paid": "03-07-2020",
    "category": "utilities"
  },
  {
    "id": "12",
    "name": "Spectrum",
    "cost": "49.99",
    "due_date": 7,
    "frequency": 30,
    "last_paid": "03-14-2020",    
    "category": "utilities"
  }
]
```

### List all pay period expenses
**Definition**
`GET /ppe`
**Response**
`200 OK` on success

```json
[
  {
    "id": "3",
    "name": "Groceries",
    "cost": "250",
    "category": "food"
  },
  {
    "id": "5",
    "name": "Gas",
    "cost": "40.00",
    "category": "automotive"
  }
]
```

### Add new bills
**Definition**
`POST /bills`

**Arguments**
- `"name":string` name of the company you pay the bill to
- `"cost:float"` how much the bill costs per month
- `"due_date:int"` What day per month the bill falls on. Choose this or frequency
- `"frequency:int"` How many days until the next bill is due. Choose this or due_date
- `"last_paid:string"` Date when the last bill was paid in "MM-DD-YYYY" format
- `"category:string"` Optional. If the user wants to put it in a specific category

**Response**

`201 Created` on success

```json
{
  "id": "6",
  "name": "National Grid",
  "cost": "43.47",
  "due_date": 0,
  "frequency": 30,
  "last_paid": "03-07-2020",
  "category": "utilities"
}
```

### Add new pay period expenses
**Definition**
`POST /ppe`

**Arguments**
- `"name":string` name of the company you pay the bill to
- `"cost:float"` how much the bill costs per month
- `"category:string"` Optional. If the user wants to put it in a specific category

**Response**

`201 Created` on success

```json
{
  "id": "6",
  "name": "National Grid",
  "cost": "43.47",
  "category": "utilities"
}
```

## Lookup bill details
**Definition**
`GET /bills/<id>`

**Response**
- `404 Not Found` if the bill does not exist
- `200 OK` on success

``` json
{
  "id": "6",
  "name": "National Grid",
  "cost": "43.47",
  "due_date": 0,
  "frequency": 30,
  "last_paid": "03-07-2020",
  "category": "utilities"
}

```
## Lookup pay period expense details
**Definition**
`GET /ppe/<id>`

**Response**
- `404 Not Found` if the bill does not exist
- `200 OK` on success

``` json
{
  "id": "6",
  "name": "National Grid",
  "cost": "43.47",
  "category": "utilities"
}
```

## Delete a bill

**Definition**
`DELETE /bills/<id>`

**Response**
- `404 Not Found` if the bill does not exist
- `204 No Content` if the bill is deleted

## Delete a pay period expense

**Definition**
`DELETE /ppe/<id>`

**Response**
- `404 Not Found` if the pay period expense does not exist
- `204 No Content` if the pay period expense is deleted
