# CryptoPulse Login Credentials

## 🔐 Unified Email-Based Login System

CryptoPulse now uses a **single login form** that automatically detects your role based on your email address and redirects you to the appropriate dashboard.

---

## 📧 Demo Accounts

### 1. 👤 Regular User
**Email**: `demo@user.com`  
**Password**: `demo123`  
**Auto-Redirect**: User Dashboard

**Features:**
- View cryptocurrency prices
- Buy and sell cryptocurrencies
- Manage portfolio ($10,000 starting balance)
- View charts and analytics
- Track profit/loss
- Multi-currency support

---

### 2. 🛡️ Administrator
**Email**: `admin@crypto.com`  
**Password**: `demo123`  
**Auto-Redirect**: Admin Dashboard

**Features:**
- View system statistics
- Manage all users
- Add/remove tracked coins
- View all transactions
- System configuration
- User role management

---

### 3. 📊 Analyst
**Email**: `analyst@crypto.com`  
**Password**: `demo123`  
**Auto-Redirect**: Analyst Dashboard

**Features:**
- Advanced market analytics
- Top gainers/losers tracking
- Market cap analysis
- Technical indicators
- Export market data
- Generate analysis reports
- View all coin statistics

---

### 4. ⚙️ Moderator
**Email**: `mod@crypto.com`  
**Password**: `demo123`  
**Auto-Redirect**: Moderator Dashboard

**Features:**
- Monitor user activity
- View all transactions
- Manage user accounts
- Review flagged content
- Generate user reports
- Track user statistics
- Community management

---

## 🌐 Access URLs

- **Application**: http://127.0.0.1:5000
- **Login Page**: http://127.0.0.1:5000/login
- **Signup Page**: http://127.0.0.1:5000/signup

---

## 🔄 How It Works

1. **Single Login Form**: All users use the same login page
2. **Email Detection**: System reads your email address
3. **Role Identification**: Automatically determines your role from the database
4. **Smart Redirect**: Sends you to the correct dashboard:
   - `@user.com` → User Dashboard
   - `admin@crypto.com` → Admin Dashboard
   - `analyst@crypto.com` → Analyst Dashboard
   - `mod@crypto.com` → Moderator Dashboard

---

## 📋 Role Comparison

| Feature | User | Admin | Analyst | Moderator |
|---------|------|-------|---------|-----------|
| Trading | ✅ | ❌ | ❌ | ❌ |
| Portfolio | ✅ | ❌ | ❌ | ❌ |
| View Prices | ✅ | ✅ | ✅ | ✅ |
| Charts | ✅ | ✅ | ✅ | ✅ |
| System Management | ❌ | ✅ | ❌ | ❌ |
| Market Analysis | ❌ | ❌ | ✅ | ❌ |
| User Management | ❌ | ✅ | ❌ | ✅ |
| Reports | ❌ | ✅ | ✅ | ✅ |

---

## 🆕 Creating New Users

### Via Signup (Regular Users Only)
1. Go to http://127.0.0.1:5000/signup
2. Enter username, email, and password
3. Account created with 'user' role
4. Starting balance: $10,000 virtual money
5. Email domain determines access level

### Via Code (For Special Roles)
Add to `users_db` in `app.py`:
```python
'newanalyst@crypto.com': {
    'username': 'newanalyst',
    'password': generate_password_hash('password123'),
    'role': 'analyst'
}
```

---

## 🎯 Email Domain Guidelines

- **@user.com**: Regular user accounts (trading & portfolio)
- **@crypto.com**: Staff accounts (admin, analyst, moderator)
- **Custom domains**: Can be configured in the database

---

## 🔒 Security Features

1. **Password Hashing**: All passwords securely hashed with Werkzeug
2. **Email Validation**: Proper email format required
3. **Role-Based Access**: Automatic role detection and routing
4. **Session Management**: Secure session handling
5. **No Access Codes**: Simplified authentication process

---

## 💡 Quick Start Guide

### For New Users:
1. Visit http://127.0.0.1:5000
2. Click "Sign Up"
3. Fill in your details (use @user.com email)
4. Login with your email and password
5. Start trading with $10,000 virtual balance

### For Demo Testing:
1. Visit http://127.0.0.1:5000/login
2. Choose any demo email from the list
3. Enter password: `demo123`
4. System automatically redirects to your dashboard

---

## 🐛 Troubleshooting

### Can't Login?
- ✅ Check email spelling (case-insensitive)
- ✅ Verify password is correct
- ✅ Ensure email is registered in the system

### Wrong Dashboard?
- ✅ Check your email domain
- ✅ Verify your role in the database
- ✅ Clear browser cache and try again

### Email Already Exists?
- ✅ Use a different email address
- ✅ Try password recovery (if implemented)
- ✅ Contact administrator

---

## 📊 System Architecture

```
Login Flow:
1. User enters email + password
2. System validates credentials
3. Looks up user role in database
4. Creates session with role info
5. Redirects to appropriate dashboard

Email → Role → Dashboard
demo@user.com → user → /home
admin@crypto.com → admin → /admin_dashboard
analyst@crypto.com → analyst → /analyst_dashboard
mod@crypto.com → moderator → /moderator_dashboard
```

---

## 🔄 Recent Changes

### v2.0 - Email-Based Login
- ✅ Unified login form for all user types
- ✅ Automatic role detection from email
- ✅ Smart dashboard redirection
- ✅ Removed access code requirements
- ✅ Simplified authentication flow
- ✅ Enhanced user experience

---

*Last Updated: February 2026*
*Version: 2.0 - Email-Based Authentication*