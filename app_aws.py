from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import boto3
import uuid
import requests
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import json
from decimal import Decimal

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# AWS Configuration
REGION = os.environ.get('AWS_REGION', 'us-east-1')
dynamodb = boto3.resource('dynamodb', region_name=REGION)
sns = boto3.client('sns', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)

# DynamoDB Tables
users_table = dynamodb.Table('CryptoPulse_Users')
portfolios_table = dynamodb.Table('CryptoPulse_Portfolios')
transactions_table = dynamodb.Table('CryptoPulse_Transactions')
price_alerts_table = dynamodb.Table('CryptoPulse_PriceAlerts')

# SNS Topic ARN
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:216989138822:capestone_project')

# S3 Bucket for file storage
S3_BUCKET = os.environ.get('S3_BUCKET', 'cryptopulse-files')

# Supported currencies and cryptocurrencies
supported_currencies = {
    'usd': {'name': 'US Dollar', 'symbol': '$'},
    'eur': {'name': 'Euro', 'symbol': '€'},
    'gbp': {'name': 'British Pound', 'symbol': '£'},
    'jpy': {'name': 'Japanese Yen', 'symbol': '¥'},
    'cad': {'name': 'Canadian Dollar', 'symbol': 'C$'},
    'aud': {'name': 'Australian Dollar', 'symbol': 'A$'},
    'chf': {'name': 'Swiss Franc', 'symbol': 'CHF'},
    'cny': {'name': 'Chinese Yuan', 'symbol': '¥'},
    'inr': {'name': 'Indian Rupee', 'symbol': '₹'},
    'krw': {'name': 'South Korean Won', 'symbol': '₩'}
}

tracked_coins = [
    'bitcoin', 'ethereum', 'solana', 'cardano', 'polkadot', 'chainlink',
    'litecoin', 'bitcoin-cash', 'stellar', 'dogecoin', 'ripple', 'avalanche-2',
    'polygon', 'uniswap', 'cosmos', 'algorand', 'tezos', 'filecoin',
    'internet-computer', 'vechain', 'theta-token', 'elrond-erd-2'
]

def send_notification(subject, message):
    """Send SNS notification"""
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
    except ClientError as e:
        print(f"Error sending notification: {e}")

def decimal_default(obj):
    """JSON serializer for DynamoDB Decimal types"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def get_crypto_prices(coin_ids=None, currency='usd'):
    """Fetch cryptocurrency prices from CoinGecko API"""
    if coin_ids is None:
        coin_ids = tracked_coins
    
    try:
        coins_str = ','.join(coin_ids)
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': coins_str,
            'vs_currencies': currency,
            'include_24hr_change': 'true',
            'include_market_cap': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Error: {response.status_code}")
            return generate_mock_prices(coin_ids, currency)
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return generate_mock_prices(coin_ids, currency)

def generate_mock_prices(coin_ids, currency='usd'):
    """Generate mock prices for testing"""
    import random
    mock_prices = {}
    base_prices = {
        'bitcoin': 45000, 'ethereum': 3000, 'solana': 100, 'cardano': 0.5,
        'polkadot': 25, 'chainlink': 15, 'litecoin': 150, 'bitcoin-cash': 300,
        'stellar': 0.12, 'dogecoin': 0.08, 'ripple': 0.6, 'avalanche-2': 35
    }
    
    for coin_id in coin_ids:
        base_price = base_prices.get(coin_id, random.uniform(1, 100))
        variation = random.uniform(-0.1, 0.1)
        price = base_price * (1 + variation)
        change_24h = random.uniform(-10, 10)
        
        mock_prices[coin_id] = {
            currency: price,
            f'{currency}_24h_change': change_24h,
            f'{currency}_market_cap': price * random.randint(1000000, 100000000)
        }
    
    return mock_prices

def initialize_user_portfolio(username):
    """Initialize user portfolio in DynamoDB"""
    try:
        portfolios_table.get_item(Key={'username': username})
    except ClientError:
        # Portfolio doesn't exist, create it
        portfolios_table.put_item(Item={
            'username': username,
            'balance': Decimal('10000.00'),  # Starting balance
            'holdings': {},
            'created_at': datetime.now().isoformat()
        })

def get_user_portfolio(username):
    """Get user portfolio from DynamoDB"""
    try:
        response = portfolios_table.get_item(Key={'username': username})
        if 'Item' in response:
            return response['Item']
        else:
            initialize_user_portfolio(username)
            return get_user_portfolio(username)
    except ClientError as e:
        print(f"Error getting portfolio: {e}")
        return {'balance': Decimal('10000.00'), 'holdings': {}}

def get_user_transactions(username, limit=10):
    """Get user transactions from DynamoDB"""
    try:
        response = transactions_table.query(
            KeyConditionExpression=Key('username').eq(username),
            ScanIndexForward=False,  # Sort by timestamp descending
            Limit=limit
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error getting transactions: {e}")
        return []

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form.get('user_type', 'user')
        
        try:
            response = users_table.get_item(Key={'username': username})
            if 'Item' in response:
                user = response['Item']
                if check_password_hash(user['password'], password):
                    if user_type == 'admin' and user.get('role') != 'admin':
                        return render_template('login.html', error='Access denied. Admin credentials required.')
                    
                    session['username'] = username
                    session['role'] = user.get('role', 'user')
                    
                    # Initialize portfolio for regular users
                    if user.get('role') != 'admin':
                        initialize_user_portfolio(username)
                    
                    send_notification("User Login", f"User {username} logged in as {user_type}")
                    
                    if user_type == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    return redirect(url_for('home'))
                else:
                    return render_template('login.html', error='Invalid credentials')
            else:
                return render_template('login.html', error='User not found')
        except ClientError as e:
            print(f"Login error: {e}")
            return render_template('login.html', error='Login failed')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')
        
        try:
            # Check if user exists
            response = users_table.get_item(Key={'username': username})
            if 'Item' in response:
                return render_template('signup.html', error='Username already exists')
            
            # Create new user
            hashed_password = generate_password_hash(password)
            users_table.put_item(Item={
                'username': username,
                'password': hashed_password,
                'email': email,
                'role': 'user',
                'created_at': datetime.now().isoformat()
            })
            
            # Initialize portfolio
            initialize_user_portfolio(username)
            
            send_notification("New User Signup", f"User {username} has signed up")
            return redirect(url_for('login'))
            
        except ClientError as e:
            print(f"Signup error: {e}")
            return render_template('signup.html', error='Signup failed')
    
    return render_template('signup.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    currency = session.get('currency', 'usd')
    username = session['username']
    
    # Get cryptocurrency prices
    prices = get_crypto_prices(tracked_coins, currency)
    
    # Get user portfolio
    portfolio = get_user_portfolio(username)
    
    # Calculate portfolio value
    total_value = float(portfolio['balance'])
    holdings_value = 0
    
    for coin_id, quantity in portfolio.get('holdings', {}).items():
        if coin_id in prices:
            coin_price = prices[coin_id][currency]
            holdings_value += float(quantity) * coin_price
    
    total_value += holdings_value
    
    return render_template('home.html', 
                         prices=prices, 
                         tracked_coins=tracked_coins,
                         portfolio=portfolio,
                         total_value=total_value,
                         holdings_value=holdings_value,
                         currency=currency,
                         currency_symbol=supported_currencies[currency]['symbol'])

@app.route('/portfolio')
def portfolio():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    currency = session.get('currency', 'usd')
    
    # Get user data
    portfolio = get_user_portfolio(username)
    transactions = get_user_transactions(username, 20)
    prices = get_crypto_prices(tracked_coins, currency)
    
    # Calculate portfolio metrics
    total_value = float(portfolio['balance'])
    holdings_value = 0
    
    for coin_id, quantity in portfolio.get('holdings', {}).items():
        if coin_id in prices:
            coin_price = prices[coin_id][currency]
            holdings_value += float(quantity) * coin_price
    
    total_value += holdings_value
    
    return render_template('portfolio.html',
                         portfolio=portfolio,
                         transactions=transactions,
                         prices=prices,
                         tracked_coins=tracked_coins,
                         total_value=total_value,
                         holdings_value=holdings_value,
                         currency=currency,
                         currency_symbol=supported_currencies[currency]['symbol'])

@app.route('/charts')
@app.route('/charts/<coin_id>')
def charts(coin_id=None):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    currency = session.get('currency', 'usd')
    prices = get_crypto_prices(tracked_coins, currency)
    
    return render_template('charts.html',
                         prices=prices,
                         tracked_coins=tracked_coins,
                         selected_coin=coin_id,
                         currency=currency,
                         currency_symbol=supported_currencies[currency]['symbol'])

@app.route('/news')
def news():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('news.html')

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('settings.html',
                         supported_currencies=supported_currencies,
                         current_currency=session.get('currency', 'usd'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Admin Routes
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    try:
        # Get system statistics
        users_response = users_table.scan()
        portfolios_response = portfolios_table.scan()
        transactions_response = transactions_table.scan()
        
        users = users_response.get('Items', [])
        portfolios = portfolios_response.get('Items', [])
        transactions = transactions_response.get('Items', [])
        
        # Calculate statistics
        total_users = len([u for u in users if u.get('role') != 'admin'])
        total_admins = len([u for u in users if u.get('role') == 'admin'])
        total_transactions = len(transactions)
        total_portfolio_value = sum(float(p.get('balance', 0)) for p in portfolios)
        
        # Recent activity
        recent_transactions = sorted(transactions, 
                                   key=lambda x: x.get('timestamp', ''), 
                                   reverse=True)[:10]
        
        return render_template('admin_dashboard.html',
                             total_users=total_users,
                             total_admins=total_admins,
                             total_transactions=total_transactions,
                             total_portfolio_value=total_portfolio_value,
                             recent_transactions=recent_transactions,
                             users=users,
                             tracked_coins=tracked_coins)
    except ClientError as e:
        print(f"Admin dashboard error: {e}")
        return render_template('admin_dashboard.html', error='Failed to load dashboard data')

# API Routes
@app.route('/api/buy_coin', methods=['POST'])
def buy_coin():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    username = session['username']
    coin_id = request.json.get('coin_id')
    amount_usd = float(request.json.get('amount', 0))
    
    if amount_usd <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    
    try:
        # Get current price
        prices = get_crypto_prices([coin_id])
        if coin_id not in prices:
            return jsonify({'error': 'Coin not found'}), 400
        
        current_price = prices[coin_id]['usd']
        quantity = amount_usd / current_price
        
        # Get current portfolio
        portfolio = get_user_portfolio(username)
        
        if float(portfolio['balance']) < amount_usd:
            return jsonify({'error': 'Insufficient balance'}), 400
        
        # Update portfolio
        new_balance = float(portfolio['balance']) - amount_usd
        holdings = portfolio.get('holdings', {})
        
        if coin_id in holdings:
            holdings[coin_id] = float(holdings[coin_id]) + quantity
        else:
            holdings[coin_id] = quantity
        
        # Update in DynamoDB
        portfolios_table.update_item(
            Key={'username': username},
            UpdateExpression='SET balance = :balance, holdings = :holdings',
            ExpressionAttributeValues={
                ':balance': Decimal(str(new_balance)),
                ':holdings': {k: Decimal(str(v)) for k, v in holdings.items()}
            }
        )
        
        # Record transaction
        transaction_id = str(uuid.uuid4())
        transaction = {
            'username': username,
            'transaction_id': transaction_id,
            'type': 'buy',
            'coin_id': coin_id,
            'quantity': Decimal(str(quantity)),
            'price': Decimal(str(current_price)),
            'amount': Decimal(str(amount_usd)),
            'timestamp': datetime.now().isoformat()
        }
        
        transactions_table.put_item(Item=transaction)
        
        send_notification("Crypto Purchase", 
                         f"User {username} bought {quantity:.6f} {coin_id.upper()} for ${amount_usd:.2f}")
        
        return jsonify({'success': True, 'transaction': json.loads(json.dumps(transaction, default=decimal_default))})
        
    except ClientError as e:
        print(f"Buy coin error: {e}")
        return jsonify({'error': 'Transaction failed'}), 500

@app.route('/api/sell_coin', methods=['POST'])
def sell_coin():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    username = session['username']
    coin_id = request.json.get('coin_id')
    quantity = float(request.json.get('quantity', 0))
    
    if quantity <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    try:
        # Get current portfolio
        portfolio = get_user_portfolio(username)
        holdings = portfolio.get('holdings', {})
        
        if coin_id not in holdings or float(holdings[coin_id]) < quantity:
            return jsonify({'error': 'Insufficient holdings'}), 400
        
        # Get current price
        prices = get_crypto_prices([coin_id])
        if coin_id not in prices:
            return jsonify({'error': 'Coin not found'}), 400
        
        current_price = prices[coin_id]['usd']
        amount_usd = quantity * current_price
        
        # Update portfolio
        new_balance = float(portfolio['balance']) + amount_usd
        holdings[coin_id] = float(holdings[coin_id]) - quantity
        
        if holdings[coin_id] <= 0:
            del holdings[coin_id]
        
        # Update in DynamoDB
        portfolios_table.update_item(
            Key={'username': username},
            UpdateExpression='SET balance = :balance, holdings = :holdings',
            ExpressionAttributeValues={
                ':balance': Decimal(str(new_balance)),
                ':holdings': {k: Decimal(str(v)) for k, v in holdings.items()}
            }
        )
        
        # Record transaction
        transaction_id = str(uuid.uuid4())
        transaction = {
            'username': username,
            'transaction_id': transaction_id,
            'type': 'sell',
            'coin_id': coin_id,
            'quantity': Decimal(str(quantity)),
            'price': Decimal(str(current_price)),
            'amount': Decimal(str(amount_usd)),
            'timestamp': datetime.now().isoformat()
        }
        
        transactions_table.put_item(Item=transaction)
        
        send_notification("Crypto Sale", 
                         f"User {username} sold {quantity:.6f} {coin_id.upper()} for ${amount_usd:.2f}")
        
        return jsonify({'success': True, 'transaction': json.loads(json.dumps(transaction, default=decimal_default))})
        
    except ClientError as e:
        print(f"Sell coin error: {e}")
        return jsonify({'error': 'Transaction failed'}), 500

@app.route('/api/set_currency', methods=['POST'])
def set_currency():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    currency = request.json.get('currency', 'usd').lower()
    if currency not in supported_currencies:
        return jsonify({'error': 'Unsupported currency'}), 400
    
    session['currency'] = currency
    return jsonify({
        'success': True,
        'currency': currency,
        'currency_symbol': supported_currencies[currency]['symbol']
    })

@app.route('/api/historical/<coin_id>')
def api_historical(coin_id):
    """API endpoint for historical price data"""
    days = request.args.get('days', 7, type=int)
    currency = request.args.get('currency', 'usd').lower()
    
    if currency not in supported_currencies:
        currency = 'usd'
    
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': currency,
            'days': days,
            'interval': 'daily' if days > 30 else 'hourly'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            # Return mock data if API fails
            mock_data = generate_mock_historical_data(days)
            return jsonify(mock_data)
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        mock_data = generate_mock_historical_data(days)
        return jsonify(mock_data)

def generate_mock_historical_data(days):
    """Generate mock historical data for charts"""
    import random
    from datetime import datetime, timedelta
    
    prices = []
    base_price = random.uniform(100, 50000)
    
    for i in range(days * 24):  # Hourly data
        timestamp = (datetime.now() - timedelta(hours=days*24-i)).timestamp() * 1000
        price = base_price * (1 + random.uniform(-0.05, 0.05))
        prices.append([int(timestamp), price])
        base_price = price
    
    return {
        'prices': prices,
        'market_caps': [[p[0], p[1] * random.randint(1000000, 100000000)] for p in prices],
        'total_volumes': [[p[0], p[1] * random.randint(10000, 1000000)] for p in prices]
    }

# Admin API Routes
@app.route('/api/admin/create_user', methods=['POST'])
def admin_create_user():
    if 'username' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        role = request.json.get('role', 'user')
        
        # Check if user exists
        response = users_table.get_item(Key={'username': username})
        if 'Item' in response:
            return jsonify({'error': 'User already exists'}), 400
        
        # Create user
        hashed_password = generate_password_hash(password)
        users_table.put_item(Item={
            'username': username,
            'password': hashed_password,
            'role': role,
            'created_at': datetime.now().isoformat()
        })
        
        if role != 'admin':
            initialize_user_portfolio(username)
        
        send_notification("Admin User Creation", f"Admin created user: {username}")
        return jsonify({'success': True})
        
    except ClientError as e:
        print(f"Admin create user error: {e}")
        return jsonify({'error': 'Failed to create user'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
