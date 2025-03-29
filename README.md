# Loan Management Middleware Service

## Introduction and Setup
This middleware helps translate SOAP's XML response to REST's JSON format for the Scoring engine, which
needs the transaction data for a customer to compute their credit score.


### Create a **.env** file to store secret variables for your environment and populate values for the keys listed below:
```
SOAP_USER=              # Username for uthentication against the CBS Soap service
REST_USER=              # Username for users accessing this middleware
SOAP_PASS=              # Password for CBS authentication
REST_PASS=              # Password for users accessing this middleware
SOAP_URL=               # Core Banking Soap Service endpoint, e.g. http://localhost:8004
```

### Create virtual environment
`python3 -m venv .venv`

`source .venv/bin/activate`
### Install dependencies
`pip install -r requirements.txt`

### Start the service
`flask run --host=0.0.0.0 --port=8002`

## Testing this middleware transactions API
GET `<HOST_URL>/api/v1/transactions/<customer_number>` including Basic Auth credentials.

Response:
```json
{
    "customerNumber": "234774784",
    "transactions": [
        {
            "accountNumber": "332216783322167555621628",
            "alternativechanneltrnscrAmount": 27665.6889301,
            "alternativechanneltrnscrNumber": 0,
            "alternativechanneltrnsdebitAmount": 29997265.951905,
            "alternativechanneltrnsdebitNumber": 114,
            "atmTransactionsNumber": 36934417,
            "atmtransactionsAmount": 192538.94,
            "axmonthlycredittransactions": 0.0,
            "bouncedChequesDebitNumber": 535,
            "bouncedchequescreditNumber": 0,
            "bouncedchequetransactionscrAmount": 1.37,
            "bouncedchequetransactionsdrAmount": 2602.4,
            "chequeDebitTransactionsAmount": 2765.57,
            "chequeDebitTransactionsNumber": 6.0,
            "createdAt": 1401263420000,
            "createdDate": 1350538588000,
            "credittransactionsAmount": 0.0,
            "debitcardpostransactionsAmount": 117347.063,
            "debitcardpostransactionsNumber": 931309756.0,
            "fincominglocaltransactioncrAmount": 2552389.4,
            "id": 5,
            "incominginternationaltrncrAmount": 76.160425,
            "incominginternationaltrncrNumber": 285700400.0,
            "incominglocaltransactioncrNumber": 1.0,
            "intrestAmount": 22,
            "lastTransactionDate": 554704439000,
            "lastTransactionType": "Null",
            "lastTransactionValue": 1.0,
            "maxAtmTransactions": 0.0,
            "maxMonthlyBebitTransactions": 78272009.0,
            "maxalternativechanneltrnscr": 0.0,
            "maxalternativechanneltrnsdebit": 0.0,
            "maxbouncedchequetransactionscr": 0.0,
            "maxchequedebittransactions": 0.0,
            "maxdebitcardpostransactions": 5468080253826023.0,
            "maxincominginternationaltrncr": 0.0,
            "maxincominglocaltransactioncr": 0.0,
            "maxmobilemoneycredittrn": 0.0,
            "maxmobilemoneydebittransaction": 0.0,
            "maxoutgoinginttrndebit": 0.0,
            "maxoutgoinglocaltrndebit": 0.0,
            "maxoverthecounterwithdrawals": 609866462.0,
            "minAtmTransactions": 0.0,
            "minMonthlyDebitTransactions": 0.0,
            "minalternativechanneltrnscr": 0.0,
            "minalternativechanneltrnsdebit": 0.0,
            "minbouncedchequetransactionscr": 0.0,
            "minchequedebittransactions": 0.0,
            "mindebitcardpostransactions": 4716295906413.0,
            "minincominginternationaltrncr": 0.0,
            "minincominglocaltransactioncr": 0.0,
            "minmobilemoneycredittrn": 0.0,
            "minmobilemoneydebittransaction": 0.0,
            "minmonthlycredittransactions": 29624.78,
            "minoutgoinginttrndebit": 0.0,
            "minoutgoinglocaltrndebit": 0.0,
            "minoverthecounterwithdrawals": 100927826.0,
            "mobilemoneycredittransactionAmount": 349693.8071922,
            "mobilemoneycredittransactionNumber": 4092,
            "mobilemoneydebittransactionAmount": 18738282.3746,
            "mobilemoneydebittransactionNumber": 0,
            "monthlyBalance": 2205.0,
            "monthlydebittransactionsAmount": 295.6677,
            "outgoinginttransactiondebitAmount": 9.561730814,
            "outgoinginttrndebitNumber": 0,
            "outgoinglocaltransactiondebitAmount": 56.03,
            "outgoinglocaltransactiondebitNumber": 0,
            "overdraftLimit": 7.0,
            "overthecounterwithdrawalsAmount": 372849038.239,
            "overthecounterwithdrawalsNumber": 546382904.0,
            "transactionValue": 3500.0
        }
    ]
}
```