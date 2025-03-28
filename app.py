import os
from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree as ET
from functools import wraps
from flask_caching import Cache
from dotenv import load_dotenv


load_dotenv()

# Create Flask app
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

REST_USERS = {
    os.getenv('REST_USER'): os.getenv('REST_PASS')
}
# SOAP Service Configuration
SOAP_URL = os.getenv('SOAP_URL')
SOAP_USER = os.getenv('SOAP_USER')
SOAP_PASS = os.getenv('SOAP_PASS')


def soap_to_rest_transaction(soap_response):
    """Convert SOAP response to REST JSON format"""
    ns = {'ns': 'http://credable.io/cbs/transaction'}
    root = ET.fromstring(soap_response)

    transactions = []
    for txn in root.findall('.//ns:transactionData', ns):
        transaction = {
            'accountNumber': txn.findtext('ns:accountNumber', '', ns),
            'alternativechanneltrnscrAmount': float(txn.findtext('ns:alternativechanneltrnscrAmount', '', ns)),
            'alternativechanneltrnscrNumber': int(txn.findtext('ns:alternativechanneltrnscrNumber', '0', ns)),
            'alternativechanneltrnsdebitAmount': float(txn.findtext('ns:alternativechanneltrnsdebitAmount', '0', ns)),
            'alternativechanneltrnsdebitNumber': int(txn.findtext('ns:alternativechanneltrnsdebitNumber', '0', ns)),
            'atmTransactionsNumber': int(txn.findtext('ns:atmTransactionsNumber', '0', ns)),
            'atmtransactionsAmount': float(txn.findtext('ns:atmtransactionsAmount', '0', ns)),
            'bouncedChequesDebitNumber': int(txn.findtext('ns:bouncedChequesDebitNumber', '0', ns)),
            'bouncedchequescreditNumber': int(txn.findtext('ns:bouncedchequescreditNumber', '0', ns)),
            'bouncedchequetransactionscrAmount': float(txn.findtext('ns:bouncedchequetransactionscrAmount', '0', ns)),
            'bouncedchequetransactionsdrAmount': float(txn.findtext('ns:bouncedchequetransactionsdrAmount', '0', ns)),
            'chequeDebitTransactionsAmount': float(txn.findtext('ns:chequeDebitTransactionsAmount', '0', ns)),
            'chequeDebitTransactionsNumber': float(txn.findtext('ns:chequeDebitTransactionsNumber', '0', ns)),
            'credittransactionsAmount': float(txn.findtext('ns:credittransactionsAmount', '0', ns)),
            'createdAt': int(txn.findtext('ns:createdAt', '0', ns)),
            'createdDate': int(txn.findtext('ns:createdDate', '0', ns)),
            'debitcardpostransactionsAmount': float(txn.findtext('ns:debitcardpostransactionsAmount', '0', ns)),
            'debitcardpostransactionsNumber': float(txn.findtext('ns:debitcardpostransactionsNumber', '0', ns)),
            'fincominglocaltransactioncrAmount': float(txn.findtext('ns:fincominglocaltransactioncrAmount', '0', ns)),
            'id': int(txn.findtext('ns:id', '0', ns)),
            'incominginternationaltrncrAmount': float(txn.findtext('ns:incominginternationaltrncrAmount', '0', ns)),
            'incominginternationaltrncrNumber': float(txn.findtext('ns:incominginternationaltrncrNumber', '0', ns)),
            'incominglocaltransactioncrNumber': float(txn.findtext('ns:incominglocaltransactioncrNumber', '0', ns)),
            'intrestAmount': int(txn.findtext('ns:intrestAmount', '0', ns)),
            'lastTransactionDate': int(txn.findtext('ns:lastTransactionDate', '0', ns)),
            'lastTransactionType': txn.findtext('ns:lastTransactionType', '0', ns),
            'lastTransactionValue': float(txn.findtext('ns:lastTransactionValue', '0', ns)),
            'maxAtmTransactions': float(txn.findtext('ns:maxAtmTransactions', '0', ns)),
            'maxMonthlyBebitTransactions': float(txn.findtext('ns:maxMonthlyBebitTransactions', '0', ns)),
            'maxalternativechanneltrnscr': float(txn.findtext('ns:maxalternativechanneltrnscr', '0', ns)),
            'maxalternativechanneltrnsdebit': float(txn.findtext('ns:maxalternativechanneltrnsdebit', '0', ns)),
            'maxbouncedchequetransactionscr': float(txn.findtext('ns:maxbouncedchequetransactionscr', '0', ns)),
            'maxchequedebittransactions': float(txn.findtext('ns:maxchequedebittransactions', '0', ns)),
            'maxdebitcardpostransactions': float(txn.findtext('ns:maxdebitcardpostransactions', '0', ns)),
            'maxincominginternationaltrncr': float(txn.findtext('ns:maxincominginternationaltrncr', '0', ns)),
            'maxincominglocaltransactioncr': float(txn.findtext('ns:maxincominglocaltransactioncr', '0', ns)),
            'maxmobilemoneycredittrn': float(txn.findtext('ns:maxmobilemoneycredittrn', '0', ns)),
            'maxmobilemoneydebittransaction': float(txn.findtext('ns:maxmobilemoneydebittransaction', '0', ns)),
            'axmonthlycredittransactions': float(txn.findtext('ns:axmonthlycredittransactions', '0', ns)),
            'maxoutgoinginttrndebit': float(txn.findtext('ns:maxoutgoinginttrndebit', '0', ns)),
            'maxoutgoinglocaltrndebit': float(txn.findtext('ns:maxoutgoinglocaltrndebit', '0', ns)),
            'maxoverthecounterwithdrawals': float(txn.findtext('ns:maxoverthecounterwithdrawals', '0', ns)),
            'minAtmTransactions': float(txn.findtext('ns:minAtmTransactions', '0', ns)),
            'minMonthlyDebitTransactions': float(txn.findtext('ns:minMonthlyDebitTransactions', '0', ns)),
            'minalternativechanneltrnscr': float(txn.findtext('ns:minalternativechanneltrnscr', '0', ns)),
            'minalternativechanneltrnsdebit': float(txn.findtext('ns:minalternativechanneltrnsdebit', '0', ns)),
            'minbouncedchequetransactionscr': float(txn.findtext('ns:minbouncedchequetransactionscr', '0', ns)),
            'minchequedebittransactions': float(txn.findtext('ns:minchequedebittransactions', '0', ns)),
            'mindebitcardpostransactions': float(txn.findtext('ns:mindebitcardpostransactions', '0', ns)),
            'minincominglocaltransactioncr': float(txn.findtext('ns:minincominglocaltransactioncr', '0', ns)),
            'minincominginternationaltrncr': float(txn.findtext('ns:minincominginternationaltrncr', '0', ns)),
            'minmobilemoneycredittrn': float(txn.findtext('ns:minmobilemoneycredittrn', '0', ns)),
            'minmobilemoneydebittransaction': float(txn.findtext('ns:minmobilemoneydebittransaction', '0', ns)),
            'minmonthlycredittransactions': float(txn.findtext('ns:minmonthlycredittransactions', '0', ns)),
            'minoutgoinginttrndebit': float(txn.findtext('ns:minoutgoinginttrndebit', '0', ns)),
            'minoutgoinglocaltrndebit': float(txn.findtext('ns:minoutgoinglocaltrndebit', '0', ns)),
            'minoverthecounterwithdrawals': float(txn.findtext('ns:minoverthecounterwithdrawals', '0', ns)),
            'mobilemoneycredittransactionAmount': float(txn.findtext('ns:mobilemoneycredittransactionAmount', '0', ns)),
            'mobilemoneycredittransactionNumber': int(txn.findtext('ns:mobilemoneycredittransactionNumber', '0', ns)),
            'mobilemoneydebittransactionAmount': float(txn.findtext('ns:mobilemoneydebittransactionAmount', '0', ns)),
            'mobilemoneydebittransactionNumber': int(txn.findtext('ns:mobilemoneydebittransactionNumber', '0', ns)),
            'monthlyBalance': float(txn.findtext('ns:monthlyBalance', '0', ns)),
            'monthlydebittransactionsAmount': float(txn.findtext('ns:monthlydebittransactionsAmount', '0', ns)),
            'outgoinginttransactiondebitAmount': float(txn.findtext('ns:outgoinginttransactiondebitAmount', '0', ns)),
            'outgoinginttrndebitNumber': int(txn.findtext('ns:outgoinginttrndebitNumber', '0', ns)),
            'outgoinglocaltransactiondebitAmount': float(txn.findtext('ns:outgoinglocaltransactiondebitAmount', '0', ns)),
            'outgoinglocaltransactiondebitNumber': int(txn.findtext('ns:outgoinglocaltransactiondebitNumber', '0', ns)),
            'overdraftLimit': float(txn.findtext('ns:overdraftLimit', '0', ns)),
            'overthecounterwithdrawalsAmount': float(txn.findtext('ns:overthecounterwithdrawalsAmount', '0', ns)),
            'overthecounterwithdrawalsNumber': float(txn.findtext('ns:overthecounterwithdrawalsNumber', '0', ns)),
            'transactionValue': float(txn.findtext('ns:transactionValue', '0', ns)),
        }
        transactions.append(transaction)

    return transactions


def requires_auth(f):
    """Decorator to enforce Basic Authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_credentials(auth.username, auth.password):
            return jsonify({
                "error": "Unauthorized",
                "message": "Please provide valid credentials"
            }), 401, {'WWW-Authenticate': 'Basic realm="REST API"'}
        return f(*args, **kwargs)
    return decorated


def check_credentials(username, password):
    """Verify username/password against our user store"""
    return REST_USERS.get(username) == password


@app.route('/api/v1/transactions/<customer_number>', methods=['GET'])
@cache.cached(timeout=300)
@requires_auth
def get_transactions(customer_number):
    """REST endpoint to get transactions for a customer"""
    # Build SOAP request
    soap_request = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                      xmlns:tran="http://credable.io/cbs/transaction">
       <soapenv:Header/>
       <soapenv:Body>
          <tran:TransactionsRequest>
             <tran:customerNumber>{customer_number}</tran:customerNumber>
          </tran:TransactionsRequest>
       </soapenv:Body>
    </soapenv:Envelope>"""

    # Call SOAP service
    headers = {'Content-Type': 'text/xml'}
    try:
        response = requests.post(
            f'{SOAP_URL}/service/transaction-data',
            data=soap_request,
            headers=headers,
            auth=HTTPBasicAuth(SOAP_USER, SOAP_PASS)
        )

        if response.status_code != 200:
            return jsonify({'error': 'SOAP service error'}), 502

        # Convert SOAP to JSON
        transactions = soap_to_rest_transaction(response.text)
        return jsonify({
            'customerNumber': customer_number,
            'transactions': transactions
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    # Run on different port than SOAP service
    app.run(port=8094, debug=True)