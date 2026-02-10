from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from datetime import datetime, timedelta
import os
import sqlite3
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Dictionary-based "database" with 4 user types (email-based)
users_db = {
    'demo@user.com': {
        'username': 'demo',
        'password': generate_password_hash('demo123'),
        'role': 'user'
    },
    'admin@crypto.com': {
        'username': 'admin',
        'password': generate_password_hash('demo123'),
        'role': 'admin'
    },
    'analyst@crypto.com': {
        'username': 'analyst',
        'password': generate_password_hash('demo123'),
        'role': 'analyst'
    },
    'mod@crypto.com': {
        'username': 'moderator',
        'password': generate_password_hash('demo123'),
        'role': 'moderator'
    }
}

# Tracked coins database - expanded list
tracked_coins = [
    'bitcoin', 'ethereum', 'solana', 'cardano', 'polkadot', 
    'chainlink', 'litecoin', 'bitcoin-cash', 'stellar', 'dogecoin',
    'polygon', 'avalanche-2', 'cosmos', 'algorand', 'tezos',
    'filecoin', 'vechain', 'theta-token', 'elrond-erd-2', 'hedera-hashgraph'
]

# Supported fiat currencies
supported_currencies = {
    'usd': {'symbol': '$', 'name': 'US Dollar'},
    'eur': {'symbol': '€', 'name': 'Euro'},
    'gbp': {'symbol': '£', 'name': 'British Pound'},
    'jpy': {'symbol': '¥', 'name': 'Japanese Yen'},
    'cad': {'symbol': 'C$', 'name': 'Canadian Dollar'},
    'aud': {'symbol': 'A$', 'name': 'Australian Dollar'},
    'chf': {'symbol': 'CHF', 'name': 'Swiss Franc'},
    'cny': {'symbol': '¥', 'name': 'Chinese Yuan'},
    'inr': {'symbol': '₹', 'name': 'Indian Rupee'},
    'krw': {'symbol': '₩', 'name': 'South Korean Won'}
}

# User portfolios - each user starts with $10,000 fake money
user_portfolios = {}

# Price alerts
price_alerts = {}

# Transaction history
transaction_history = {}

def get_crypto_prices(coin_ids, currency='usd'):
    """Fetch current prices from CoinGecko API in specified currency"""
    try:
        ids = ','.join(coin_ids)
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={currency}&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true'
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return {}

def get_historical_data(coin_id, days=7, currency='usd'):
    """Fetch historical price data for charts in specified currency"""
    try:
        url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={currency}&days={days}'
        print(f"Fetching from URL: {url}")
        response = requests.get(url, timeout=10)
        print(f"API response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"API error: {response.text}")
            return generate_mock_data(coin_id, days, currency)
            
        data = response.json()
        print(f"API response keys: {data.keys() if data else 'No data'}")
        
        # Format data for Chart.js
        prices = []
        for timestamp, price in data.get('prices', []):
            prices.append({
                'x': timestamp,
                'y': round(price, 6)
            })
        
        print(f"Formatted {len(prices)} price points")
        return prices if prices else generate_mock_data(coin_id, days, currency)
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return generate_mock_data(coin_id, days, currency)

def generate_mock_data(coin_id, days=7, currency='usd'):
    """Generate mock historical data for testing"""
    import random
    from datetime import datetime, timedelta
    
    # Base prices for different coins in USD
    base_prices_usd = {
        'bitcoin': 45000,
        'ethereum': 2500,
        'solana': 100,
        'cardano': 0.5,
        'polkadot': 7,
        'chainlink': 15,
        'litecoin': 70,
        'dogecoin': 0.08
    }
    
    # Currency conversion rates (mock)
    currency_rates = {
        'usd': 1,
        'eur': 0.85,
        'gbp': 0.73,
        'jpy': 110,
        'cad': 1.25,
        'aud': 1.35,
        'chf': 0.92,
        'cny': 6.45,
        'inr': 74,
        'krw': 1180
    }
    
    base_price_usd = base_prices_usd.get(coin_id, 1000)
    conversion_rate = currency_rates.get(currency, 1)
    base_price = base_price_usd * conversion_rate
    
    prices = []
    
    # Generate data points for the specified number of days
    now = datetime.now()
    for i in range(days * 24):  # Hourly data points
        timestamp = int((now - timedelta(hours=days * 24 - i)).timestamp() * 1000)
        # Add some random variation (±5%)
        variation = random.uniform(-0.05, 0.05)
        price = base_price * (1 + variation)
        prices.append({
            'x': timestamp,
            'y': round(price, 6)
        })
    
    print(f"Generated {len(prices)} mock data points for {coin_id} in {currency}")
    return prices

def initialize_user_portfolio(username):
    """Initialize a new user's portfolio with starting balance"""
    if username not in user_portfolios:
        user_portfolios[username] = {
            'balance': 10000.0,  # Starting with $10,000 fake money
            'holdings': {}  # {coin_id: quantity}
        }
    if username not in transaction_history:
        transaction_history[username] = []

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Get user's preferred currency from session or default to USD
    currency = session.get('currency', 'usd')
    prices = get_crypto_prices(tracked_coins, currency)
    
    # Get user portfolio
    initialize_user_portfolio(username)
    portfolio = user_portfolios.get(username, {'balance': 10000, 'holdings': {}})
    
    # Calculate portfolio values
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
                         currency_symbol=supported_currencies[currency]['symbol'],
                         supported_currencies=supported_currencies)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form['password']
        
        # Check if user exists by email
        if email not in users_db:
            flash('Invalid email or password')
            return redirect(url_for('login'))
        
        user_data = users_db[email]
        
        # Verify password
        if not check_password_hash(user_data['password'], password):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        
        # Get user role
        user_role = user_data.get('role', 'user')
        username = user_data.get('username', email.split('@')[0])
        
        # Set session data
        session['email'] = email
        session['username'] = username
        session['role'] = user_role
        
        # Initialize portfolio for regular users
        if user_role == 'user':
            initialize_user_portfolio(username)
        
        # Redirect based on role
        if user_role == 'admin':
            flash(f'Welcome back, Admin {username}!')
            return redirect(url_for('admin_dashboard'))
        elif user_role == 'analyst':
            flash(f'Welcome back, Analyst {username}!')
            return redirect(url_for('analyst_dashboard'))
        elif user_role == 'moderator':
            flash(f'Welcome back, Moderator {username}!')
            return redirect(url_for('moderator_dashboard'))
        else:  # user role
            flash(f'Welcome back, {username}!')
            return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/user_login', methods=['POST'])
def user_login():
    # Redirect to main login handler
    return login()

@app.route('/admin_login', methods=['POST'])
def admin_login():
    # Redirect to main login handler
    return login()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email'].lower().strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))
        
        # Check if email already exists
        if email in users_db:
            flash('Email already registered')
            return redirect(url_for('signup'))
        
        # Create new user account (always as 'user' role for signup)
        users_db[email] = {
            'username': username,
            'password': generate_password_hash(password),
            'role': 'user'
        }
        
        initialize_user_portfolio(username)
        flash(f'Account created successfully! Please login with {email}')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'username' not in session or session.get('role') != 'admin':
        flash('Admin access required')
        return redirect(url_for('login') + '?type=admin')
    
    return render_template('admin.html', tracked_coins=tracked_coins, users=list(users_db.keys()))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        flash('Admin access required')
        return redirect(url_for('login') + '?type=admin')
    
    # Admin-specific dashboard with enhanced features
    admin_stats = {
        'total_users': len(users_db),
        'admin_users': len([u for u in users_db.values() if u.get('role') == 'admin']),
        'regular_users': len([u for u in users_db.values() if u.get('role') == 'user']),
        'analysts': len([u for u in users_db.values() if u.get('role') == 'analyst']),
        'moderators': len([u for u in users_db.values() if u.get('role') == 'moderator']),
        'tracked_coins': len(tracked_coins),
        'total_portfolios': len(user_portfolios),
        'total_transactions': sum(len(transactions) for transactions in transaction_history.values())
    }
    
    return render_template('admin_dashboard.html', 
                         tracked_coins=tracked_coins, 
                         users=list(users_db.keys()),
                         stats=admin_stats)

@app.route('/analyst_dashboard')
def analyst_dashboard():
    if 'username' not in session or session.get('role') != 'analyst':
        flash('Analyst access required')
        return redirect(url_for('login') + '?type=analyst')
    
    username = session['username']
    currency = session.get('currency', 'usd')
    
    # Get market data for analysis
    prices = get_crypto_prices(tracked_coins, currency)
    
    # Calculate market statistics
    analyst_stats = {
        'total_coins_tracked': len(tracked_coins),
        'coins_up_24h': len([c for c, p in prices.items() if p.get(f'{currency}_24h_change', 0) > 0]),
        'coins_down_24h': len([c for c, p in prices.items() if p.get(f'{currency}_24h_change', 0) < 0]),
        'total_market_cap': sum([p.get(f'{currency}_market_cap', 0) for p in prices.values()]),
        'avg_24h_change': sum([p.get(f'{currency}_24h_change', 0) for p in prices.values()]) / len(prices) if prices else 0
    }
    
    # Get top gainers and losers
    sorted_by_change = sorted(prices.items(), key=lambda x: x[1].get(f'{currency}_24h_change', 0), reverse=True)
    top_gainers = sorted_by_change[:5]
    top_losers = sorted_by_change[-5:]
    
    return render_template('analyst_dashboard.html',
                         username=username,
                         stats=analyst_stats,
                         prices=prices,
                         tracked_coins=tracked_coins,
                         top_gainers=top_gainers,
                         top_losers=top_losers,
                         currency=currency,
                         currency_symbol=supported_currencies[currency]['symbol'])

@app.route('/moderator_dashboard')
def moderator_dashboard():
    if 'username' not in session or session.get('role') != 'moderator':
        flash('Moderator access required')
        return redirect(url_for('login') + '?type=moderator')
    
    username = session['username']
    
    # Get user activity data
    moderator_stats = {
        'total_users': len(users_db),
        'active_portfolios': len(user_portfolios),
        'total_transactions': sum(len(transactions) for transactions in transaction_history.values()),
        'users_by_role': {
            'user': len([u for u in users_db.values() if u.get('role') == 'user']),
            'admin': len([u for u in users_db.values() if u.get('role') == 'admin']),
            'analyst': len([u for u in users_db.values() if u.get('role') == 'analyst']),
            'moderator': len([u for u in users_db.values() if u.get('role') == 'moderator'])
        }
    }
    
    # Get recent transactions for monitoring
    recent_transactions = []
    for user, transactions in transaction_history.items():
        for tx in transactions[-5:]:  # Last 5 transactions per user
            recent_transactions.append({
                'username': user,
                'type': tx['type'],
                'coin_id': tx['coin_id'],
                'amount': tx['amount'],
                'timestamp': tx['timestamp']
            })
    
    # Sort by timestamp
    recent_transactions.sort(key=lambda x: x['timestamp'], reverse=True)
    recent_transactions = recent_transactions[:20]  # Top 20 recent
    
    return render_template('moderator_dashboard.html',
                         username=username,
                         stats=moderator_stats,
                         users=users_db,
                         recent_transactions=recent_transactions)

@app.route('/test_chart')
def test_chart():
    return render_template('test_chart.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/news')
def news():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Fetch crypto news (using a simple news API or placeholder)
    news_data = get_crypto_news()
    return render_template('news.html', news=news_data)

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_settings = get_user_settings(username)
    return render_template('settings.html', settings=user_settings)

def get_crypto_news():
    """Fetch cryptocurrency news"""
    try:
        # Using CoinGecko's news endpoint or placeholder data
        news_items = [
            {
                'title': 'Bitcoin Reaches New All-Time High',
                'description': 'Bitcoin surges past previous records as institutional adoption continues.',
                'url': '#',
                'published_at': '2024-02-01T10:00:00Z',
                'source': 'CryptoNews'
            },
            {
                'title': 'Ethereum 2.0 Staking Rewards Increase',
                'description': 'Ethereum staking rewards see significant increase following network upgrade.',
                'url': '#',
                'published_at': '2024-02-01T08:30:00Z',
                'source': 'BlockchainDaily'
            },
            {
                'title': 'Solana Network Sees Record Transaction Volume',
                'description': 'Solana processes record number of transactions as DeFi activity surges.',
                'url': '#',
                'published_at': '2024-01-31T16:45:00Z',
                'source': 'DeFiPulse'
            }
        ]
        return news_items
    except:
        return []

def get_user_settings(username):
    """Get user settings"""
    return {
        'theme': 'light',
        'notifications': True,
        'email_alerts': False,
        'default_currency': 'USD',
        'refresh_interval': 30
    }

@app.route('/portfolio')
def portfolio():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    initialize_user_portfolio(username)
    
    portfolio = user_portfolios[username]
    prices = get_crypto_prices(tracked_coins)
    
    # Calculate portfolio value
    total_value = portfolio['balance']
    holdings_value = 0
    
    for coin_id, quantity in portfolio['holdings'].items():
        if coin_id in prices:
            coin_value = prices[coin_id]['usd'] * quantity
            holdings_value += coin_value
            total_value += coin_value
    
    # Get recent transactions
    recent_transactions = transaction_history.get(username, [])[-10:]  # Last 10 transactions
    
    return render_template('portfolio.html', 
                         portfolio=portfolio, 
                         prices=prices, 
                         total_value=total_value,
                         holdings_value=holdings_value,
                         transactions=recent_transactions,
                         tracked_coins=tracked_coins)

@app.route('/charts')
@app.route('/charts/<coin_id>')
def charts(coin_id=None):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    currency = session.get('currency', 'usd')
    
    # Get all prices for the chart page
    prices = get_crypto_prices(tracked_coins, currency)
    
    # If a specific coin is requested, get its historical data
    historical_data = None
    current_price = {}
    days = request.args.get('days', 7, type=int)
    
    if coin_id:
        historical_data = get_historical_data(coin_id, days, currency)
        current_price = prices.get(coin_id, {})
    
    return render_template('charts.html', 
                         coin_id=coin_id,
                         historical_data=historical_data,
                         current_price=current_price,
                         prices=prices,
                         tracked_coins=tracked_coins,
                         days=days,
                         currency=currency,
                         currency_symbol=supported_currencies[currency]['symbol'])

@app.route('/api/prices')
def api_prices():
    """API endpoint for real-time price updates"""
    currency = request.args.get('currency', 'usd').lower()
    if currency not in supported_currencies:
        currency = 'usd'
    
    prices = get_crypto_prices(tracked_coins, currency)
    return jsonify({
        'prices': prices,
        'currency': currency,
        'currency_symbol': supported_currencies[currency]['symbol']
    })

@app.route('/api/currencies')
def api_currencies():
    """API endpoint for supported currencies"""
    return jsonify(supported_currencies)

@app.route('/api/set_currency', methods=['POST'])
def set_currency():
    """Set user's preferred currency"""
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

@app.route('/api/add_coin', methods=['POST'])
def add_coin():
    if 'username' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    coin_id = request.json.get('coin_id')
    if coin_id and coin_id not in tracked_coins:
        tracked_coins.append(coin_id)
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid coin ID'}), 400

@app.route('/api/remove_coin', methods=['POST'])
def remove_coin():
    if 'username' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    coin_id = request.json.get('coin_id')
    if coin_id in tracked_coins:
        tracked_coins.remove(coin_id)
        return jsonify({'success': True})
    return jsonify({'error': 'Coin not found'}), 400

@app.route('/api/buy_coin', methods=['POST'])
def buy_coin():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    username = session['username']
    initialize_user_portfolio(username)
    
    coin_id = request.json.get('coin_id')
    amount_usd = float(request.json.get('amount', 0))
    
    if amount_usd <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    
    # Get current price
    prices = get_crypto_prices([coin_id])
    if coin_id not in prices:
        return jsonify({'error': 'Coin not found'}), 400
    
    current_price = prices[coin_id]['usd']
    quantity = amount_usd / current_price
    
    # Check if user has enough balance
    portfolio = user_portfolios[username]
    if portfolio['balance'] < amount_usd:
        return jsonify({'error': 'Insufficient balance'}), 400
    
    # Execute trade
    portfolio['balance'] -= amount_usd
    if coin_id in portfolio['holdings']:
        portfolio['holdings'][coin_id] += quantity
    else:
        portfolio['holdings'][coin_id] = quantity
    
    # Record transaction
    transaction = {
        'type': 'buy',
        'coin_id': coin_id,
        'quantity': quantity,
        'price': current_price,
        'amount': amount_usd,
        'timestamp': datetime.now().isoformat()
    }
    transaction_history[username].append(transaction)
    
    return jsonify({'success': True, 'transaction': transaction})

@app.route('/api/sell_coin', methods=['POST'])
def sell_coin():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    username = session['username']
    initialize_user_portfolio(username)
    
    coin_id = request.json.get('coin_id')
    quantity = float(request.json.get('quantity', 0))
    
    if quantity <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    # Check if user has enough holdings
    portfolio = user_portfolios[username]
    if coin_id not in portfolio['holdings'] or portfolio['holdings'][coin_id] < quantity:
        return jsonify({'error': 'Insufficient holdings'}), 400
    
    # Get current price
    prices = get_crypto_prices([coin_id])
    if coin_id not in prices:
        return jsonify({'error': 'Coin not found'}), 400
    
    current_price = prices[coin_id]['usd']
    amount_usd = quantity * current_price
    
    # Execute trade
    portfolio['holdings'][coin_id] -= quantity
    if portfolio['holdings'][coin_id] == 0:
        del portfolio['holdings'][coin_id]
    portfolio['balance'] += amount_usd
    
    # Record transaction
    transaction = {
        'type': 'sell',
        'coin_id': coin_id,
        'quantity': quantity,
        'price': current_price,
        'amount': amount_usd,
        'timestamp': datetime.now().isoformat()
    }
    transaction_history[username].append(transaction)
    
    return jsonify({'success': True, 'transaction': transaction})

@app.route('/api/historical/<coin_id>')
def api_historical(coin_id):
    """API endpoint for historical price data"""
    days = request.args.get('days', 7, type=int)
    currency = request.args.get('currency', 'usd').lower()
    
    if currency not in supported_currencies:
        currency = 'usd'
        
    print(f"Fetching historical data for {coin_id} with {days} days in {currency}")
    data = get_historical_data(coin_id, days, currency)
    print(f"Historical data length: {len(data)}")
    if data:
        print(f"Sample data point: {data[0] if data else 'None'}")
    
    return jsonify({
        'data': data,
        'currency': currency,
        'currency_symbol': supported_currencies[currency]['symbol']
    })

def get_crypto_news():
    """Fetch cryptocurrency news"""
    try:
        # Using CoinGecko's news endpoint or placeholder data
        news_items = [
            {
                'title': 'Bitcoin Reaches New All-Time High',
                'description': 'Bitcoin surges past previous records as institutional adoption continues.',
                'url': '#',
                'published_at': '2024-02-01T10:00:00Z',
                'source': 'CryptoNews'
            },
            {
                'title': 'Ethereum 2.0 Staking Rewards Increase',
                'description': 'Ethereum staking rewards see significant increase following network upgrade.',
                'url': '#',
                'published_at': '2024-02-01T08:30:00Z',
                'source': 'BlockchainDaily'
            },
            {
                'title': 'Solana Network Sees Record Transaction Volume',
                'description': 'Solana processes record number of transactions as DeFi activity surges.',
                'url': '#',
                'published_at': '2024-01-31T16:45:00Z',
                'source': 'DeFiPulse'
            }
        ]
        return news_items
    except:
        return []

def get_user_settings(username):
    """Get user settings"""
    return {
        'theme': 'light',
        'notifications': True,
        'email_alerts': False,
        'default_currency': 'USD',
        'refresh_interval': 30
    }

@app.route('/api/toggle_favorite', methods=['POST'])
def toggle_favorite():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    username = session['username']
    coin_id = request.json.get('coin_id')
    
    if username not in user_favorites:
        user_favorites[username] = []
    
    if coin_id in user_favorites[username]:
        user_favorites[username].remove(coin_id)
        return jsonify({'success': True, 'action': 'removed'})
    else:
        user_favorites[username].append(coin_id)
        return jsonify({'success': True, 'action': 'added'})

@app.route('/api/market_stats')
def market_stats():
    """Get market statistics"""
    try:
        # Fetch global market data
        url = 'https://api.coingecko.com/api/v3/global'
        response = requests.get(url, timeout=10)
        data = response.json()
        
        return jsonify({
            'total_market_cap': data['data']['total_market_cap']['usd'],
            'total_volume': data['data']['total_volume']['usd'],
            'market_cap_change_24h': data['data']['market_cap_change_percentage_24h_usd'],
            'active_cryptocurrencies': data['data']['active_cryptocurrencies'],
            'bitcoin_dominance': data['data']['market_cap_percentage']['btc']
        })
    except:
        return jsonify({'error': 'Failed to fetch market stats'}), 500

@app.route('/api/trending')
def trending():
    """Get trending cryptocurrencies"""
    try:
        url = 'https://api.coingecko.com/api/v3/search/trending'
        response = requests.get(url, timeout=10)
        data = response.json()
        
        trending_coins = []
        for coin in data['coins'][:5]:  # Top 5 trending
            trending_coins.append({
                'id': coin['item']['id'],
                'name': coin['item']['name'],
                'symbol': coin['item']['symbol'],
                'market_cap_rank': coin['item']['market_cap_rank']
            })
        
        return jsonify(trending_coins)
    except:
        return jsonify([])

@app.route('/api/fear_greed')
def fear_greed():
    """Get Fear & Greed Index"""
    try:
        # This would typically use the Alternative.me API
        # For demo, returning mock data
        return jsonify({
            'value': 65,
            'value_classification': 'Greed',
            'timestamp': datetime.now().isoformat()
        })
    except:
        return jsonify({'error': 'Failed to fetch Fear & Greed Index'}), 500

if __name__ == '__main__':
    app.run(debug=True)