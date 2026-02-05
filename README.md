# CryptoPulse - Real-time Cryptocurrency Tracker

A Flask-based web application for tracking cryptocurrency prices in real-time with user authentication, price alerts, and admin management features.

## Features

### Core Functionality
- **Real-time Price Tracking**: Live updates for Bitcoin, Ethereum, Solana, and more
- **User Authentication**: Secure login/signup system with Flask sessions
- **Price Alerts**: Set custom price thresholds with visual and browser notifications
- **Live Search**: Filter and search through tracked cryptocurrencies
- **Admin Panel**: Manage tracked coins and view user statistics

### User Interface
- Clean, responsive design using Bootstrap 5
- Real-time price updates without page refresh
- Interactive price alert system
- Mobile-friendly responsive layout

## Technology Stack

### Backend
- **Python Flask** - Web framework
- **Flask Sessions** - User authentication
- **Werkzeug** - Password hashing
- **Requests** - API calls to CoinGecko

### Frontend
- **HTML5 & CSS3**
- **Bootstrap 5** - UI framework
- **JavaScript** - Dynamic interactions
- **Chart.js** - Ready for data visualization

### Data Source
- **CoinGecko API** - Real-time cryptocurrency data

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CryptoPulse
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Use demo credentials: `admin` / `admin123` for admin access
   - Or create a new user account

## Project Structure

```
CryptoPulse/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   ├── home.html         # Dashboard
│   ├── admin.html        # Admin panel
│   └── about.html        # About page
└── static/               # Static assets
    ├── style.css         # Custom styles
    └── script.js         # JavaScript functionality
```

## Usage

### For Regular Users
1. **Sign up** for a new account or use existing credentials
2. **View Dashboard** to see live cryptocurrency prices
3. **Set Price Alerts** by clicking "Set Alert" next to any coin
4. **Search Coins** using the search bar to filter results
5. **Monitor Alerts** - get visual and browser notifications when price thresholds are met

### For Administrators
1. **Login** with admin credentials (`admin` / `admin123`)
2. **Access Admin Panel** from the navigation menu
3. **Add/Remove Coins** to customize which cryptocurrencies are tracked
4. **View User Statistics** to see registered users and system usage

## API Endpoints

- `GET /` - Dashboard (requires authentication)
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /signup` - Registration page
- `POST /signup` - Process registration
- `GET /admin` - Admin panel (admin only)
- `GET /about` - About page
- `GET /api/prices` - JSON API for current prices
- `POST /api/add_coin` - Add coin to tracking (admin only)
- `POST /api/remove_coin` - Remove coin from tracking (admin only)

## Features in Detail

### Real-time Price Updates
- Automatic refresh every 30 seconds
- Manual refresh button available
- Color-coded 24-hour change indicators
- Responsive price formatting

### Price Alert System
- Set alerts above or below current price
- Visual notifications with color-coded table rows
- Browser notifications (with user permission)
- Persistent alerts stored in localStorage

### User Management
- Secure password hashing with Werkzeug
- Session-based authentication
- Role-based access control (admin/user)
- Dictionary-based user storage (easily replaceable with database)

### Admin Features
- Add/remove tracked cryptocurrencies
- View all registered users
- Real-time coin management
- User statistics dashboard

## Future Enhancements

- **Portfolio Tracker**: Virtual trading with fake money
- **Historical Charts**: Price history visualization with Chart.js
- **Database Integration**: Replace dictionary storage with SQLite/PostgreSQL
- **WebSocket Support**: Real-time price streaming
- **Email Alerts**: Send price alerts via email
- **Mobile App**: React Native companion app

## Demo Credentials

- **Admin Access**: Username: `admin`, Password: `admin123`
- **Regular User**: Create new account via signup page

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.