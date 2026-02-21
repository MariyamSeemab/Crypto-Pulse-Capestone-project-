# CRYPTOPULSE - Architecture & Database Diagrams

## Project Overview

**CryptoPulse** is a real-time cryptocurrency tracking and virtual trading platform with multi-role authentication, providing users with live price updates, portfolio management, and transaction notifications through AWS services.

---

## AWS ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CRYPTOPULSE AWS ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────────────────┘

                                    Internet
                                       │
                                       ▼
                            ┌──────────────────┐
                            │   Route 53 DNS   │
                            │  (Optional CDN)  │
                            └────────┬─────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │     Application Load Balancer  │
                    │         (Optional)             │
                    └────────────┬───────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                ▼                ▼                ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │   EC2 (AZ1)  │ │   EC2 (AZ2)  │ │   EC2 (AZ3)  │
        │              │ │              │ │              │
        │  Flask App   │ │  Flask App   │ │  Flask App   │
        │  (app_aws.py)│ │  (app_aws.py)│ │  (app_aws.py)│
        └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
               │                │                │
               └────────────────┼────────────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
                    ▼           ▼           ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │   DynamoDB   │ │   SNS Topic  │ │   S3 Bucket  │
        │              │ │              │ │              │
        │ • Users      │ │ Email Alerts │ │ Static Files │
        │ • Portfolios │ │ Transaction  │ │ (Optional)   │
        │ • Transactions│ │ Notifications│ │              │
        │ • PriceAlerts│ └──────────────┘ └──────────────┘
        └──────────────┘
               │
               ▼
        ┌──────────────┐
        │  IAM Role    │
        │ custom_user_ │
        │    role      │
        │              │
        │ • EC2 Full   │
        │ • SNS Full   │
        │ • DynamoDB   │
        │   Full       │
        └──────────────┘

External API:
        ┌──────────────┐
        │  CoinGecko   │
        │     API      │
        │              │
        │ Real-time    │
        │ Crypto Prices│
        └──────────────┘
```

---

## ENTITY RELATIONSHIP (ER) DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CRYPTOPULSE DATABASE SCHEMA (DynamoDB)                  │
└─────────────────────────────────────────────────────────────────────────────┘


    ┌─────────────────────────┐
    │        USERS            │
    │─────────────────────────│
    │ PK: username (String)   │◄──────────┐
    │─────────────────────────│           │
    │ • email (String)        │           │ 1 to Many
    │ • password (String)     │           │
    │ • role (String)         │           │
    │   - user                │           │
    │   - admin               │           │
    │   - analyst             │           │
    │   - moderator           │           │
    │ • created_at (String)   │           │
    └─────────────────────────┘           │
                                          │
                                          │
    ┌─────────────────────────┐           │
    │      PORTFOLIOS         │           │
    │─────────────────────────│           │
    │ PK: username (String)   │◄──────────┤
    │─────────────────────────│           │
    │ • balance (Decimal)     │           │
    │ • holdings (Map)        │           │
    │   {                     │           │
    │     coin_id: quantity   │           │
    │   }                     │           │
    │ • created_at (String)   │           │
    └─────────────────────────┘           │
                                          │
                                          │
    ┌─────────────────────────┐           │
    │     TRANSACTIONS        │           │
    │─────────────────────────│           │
    │ PK: username (String)   │◄──────────┤
    │ SK: timestamp (String)  │           │
    │─────────────────────────│           │
    │ • transaction_id (UUID) │           │
    │ • type (String)         │           │
    │   - buy                 │           │
    │   - sell                │           │
    │ • coin_id (String)      │           │
    │ • quantity (Decimal)    │           │
    │ • price (Decimal)       │           │
    │ • amount (Decimal)      │           │
    └─────────────────────────┘           │
                                          │
                                          │
    ┌─────────────────────────┐           │
    │      PRICE_ALERTS       │           │
    │─────────────────────────│           │
    │ PK: username (String)   │◄──────────┘
    │ SK: alert_id (UUID)     │
    │─────────────────────────│
    │ • coin_id (String)      │
    │ • target_price (Decimal)│
    │ • condition (String)    │
    │   - above               │
    │   - below               │
    │ • active (Boolean)      │
    │ • created_at (String)   │
    └─────────────────────────┘


RELATIONSHIPS:
═══════════════
• One User → One Portfolio (1:1)
• One User → Many Transactions (1:N)
• One User → Many Price Alerts (1:N)
```

---

## DATA FLOW DIAGRAMS

### 1. USER LOGIN FLOW

```
┌──────────┐
│  User    │
└────┬─────┘
     │
     │ 1. Enter email & password
     ▼
┌─────────────────┐
│  Login Page     │
│ (login.html)    │
└────┬────────────┘
     │
     │ 2. POST /login
     ▼
┌─────────────────────────┐
│  Flask App (app_aws.py) │
│                         │
│  • Validate credentials │
│  • Check DynamoDB       │
│  • Detect user role     │
└────┬────────────────────┘
     │
     │ 3. Query Users table
     ▼
┌─────────────────┐
│   DynamoDB      │
│   Users Table   │
└────┬────────────┘
     │
     │ 4. Return user data
     ▼
┌─────────────────────────┐
│  Flask App              │
│  • Create session       │
│  • Set role             │
│  • Redirect by role     │
└────┬────────────────────┘
     │
     │ 5. Redirect based on role
     ├──────────┬──────────┬──────────┐
     ▼          ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│  User   │ │  Admin  │ │ Analyst │ │Moderator│
│Dashboard│ │Dashboard│ │Dashboard│ │Dashboard│
└─────────┘ └─────────┘ └─────────┘ └─────────┘
```

### 2. BUY CRYPTOCURRENCY FLOW

```
┌──────────┐
│  User    │
└────┬─────┘
     │
     │ 1. Click "Buy" button
     ▼
┌─────────────────┐
│  Portfolio Page │
│ (portfolio.html)│
│                 │
│ • Select coin   │
│ • Enter amount  │
└────┬────────────┘
     │
     │ 2. POST /api/buy_coin
     ▼
┌─────────────────────────┐
│  Flask App              │
│                         │
│  • Validate amount      │
│  • Check balance        │
│  • Get current price    │
└────┬────────────────────┘
     │
     │ 3. Fetch live price
     ▼
┌─────────────────┐
│  CoinGecko API  │
│                 │
│  Return price   │
└────┬────────────┘
     │
     │ 4. Price data
     ▼
┌─────────────────────────┐
│  Flask App              │
│                         │
│  • Calculate quantity   │
│  • Update portfolio     │
└────┬────────────────────┘
     │
     │ 5. Update Portfolios table
     ▼
┌─────────────────┐
│   DynamoDB      │
│ Portfolios Table│
│                 │
│ • Deduct balance│
│ • Add holdings  │
└────┬────────────┘
     │
     │ 6. Record transaction
     ▼
┌─────────────────┐
│   DynamoDB      │
│Transactions Tbl │
│                 │
│ • Save buy tx   │
└────┬────────────┘
     │
     │ 7. Send notification
     ▼
┌─────────────────┐
│   AWS SNS       │
│                 │
│ • Email alert   │
│ • Transaction   │
│   confirmation  │
└────┬────────────┘
     │
     │ 8. Email sent
     ▼
┌──────────┐
│  User    │
│  Email   │
└──────────┘
```

### 3. SELL CRYPTOCURRENCY FLOW

```
┌──────────┐
│  User    │
└────┬─────┘
     │
     │ 1. Click "Sell" button
     ▼
┌─────────────────┐
│  Portfolio Page │
│                 │
│ • Select coin   │
│ • Enter quantity│
└────┬────────────┘
     │
     │ 2. POST /api/sell_coin
     ▼
┌─────────────────────────┐
│  Flask App              │
│                         │
│  • Validate quantity    │
│  • Check holdings       │
│  • Get current price    │
└────┬────────────────────┘
     │
     │ 3. Fetch live price
     ▼
┌─────────────────┐
│  CoinGecko API  │
└────┬────────────┘
     │
     │ 4. Price data
     ▼
┌─────────────────────────┐
│  Flask App              │
│                         │
│  • Calculate amount     │
│  • Update portfolio     │
└────┬────────────────────┘
     │
     │ 5. Update Portfolios table
     ▼
┌─────────────────┐
│   DynamoDB      │
│ Portfolios Table│
│                 │
│ • Add balance   │
│ • Remove holding│
└────┬────────────┘
     │
     │ 6. Record transaction
     ▼
┌─────────────────┐
│   DynamoDB      │
│Transactions Tbl │
│                 │
│ • Save sell tx  │
└────┬────────────┘
     │
     │ 7. Send notification
     ▼
┌─────────────────┐
│   AWS SNS       │
│                 │
│ • Email alert   │
└────┬────────────┘
     │
     │ 8. Email sent
     ▼
┌──────────┐
│  User    │
│  Email   │
└──────────┘
```

### 4. VIEW PORTFOLIO FLOW

```
┌──────────┐
│  User    │
└────┬─────┘
     │
     │ 1. Navigate to Portfolio
     ▼
┌─────────────────┐
│  Flask App      │
│  GET /portfolio │
└────┬────────────┘
     │
     │ 2. Get user portfolio
     ▼
┌─────────────────┐
│   DynamoDB      │
│ Portfolios Table│
└────┬────────────┘
     │
     │ 3. Portfolio data
     ▼
┌─────────────────┐
│  Flask App      │
│                 │
│ • Get holdings  │
└────┬────────────┘
     │
     │ 4. Fetch current prices
     ▼
┌─────────────────┐
│  CoinGecko API  │
└────┬────────────┘
     │
     │ 5. Price data
     ▼
┌─────────────────┐
│  Flask App      │
│                 │
│ • Calculate P&L │
│ • Total value   │
└────┬────────────┘
     │
     │ 6. Get transactions
     ▼
┌─────────────────┐
│   DynamoDB      │
│Transactions Tbl │
└────┬────────────┘
     │
     │ 7. Transaction history
     ▼
┌─────────────────┐
│  Flask App      │
│                 │
│ • Render page   │
└────┬────────────┘
     │
     │ 8. Display portfolio
     ▼
┌─────────────────┐
│  Portfolio Page │
│                 │
│ • Holdings      │
│ • Balance       │
│ • Transactions  │
│ • P&L           │
└─────────────────┘
```

---

## USER ROLE ACCESS MATRIX

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ROLE-BASED ACCESS CONTROL                            │
└─────────────────────────────────────────────────────────────────────────────┘

Feature/Page              │ User │ Admin │ Analyst │ Moderator │
──────────────────────────┼──────┼───────┼─────────┼───────────┤
Login                     │  ✓   │   ✓   │    ✓    │     ✓     │
Signup                    │  ✓   │   ✓   │    ✓    │     ✓     │
Dashboard (Home)          │  ✓   │   ✗   │    ✗    │     ✗     │
Admin Dashboard           │  ✗   │   ✓   │    ✗    │     ✗     │
Analyst Dashboard         │  ✗   │   ✗   │    ✓    │     ✗     │
Moderator Dashboard       │  ✗   │   ✗   │    ✗    │     ✓     │
Portfolio Management      │  ✓   │   ✗   │    ✗    │     ✗     │
Buy Cryptocurrency        │  ✓   │   ✗   │    ✗    │     ✗     │
Sell Cryptocurrency       │  ✓   │   ✗   │    ✗    │     ✗     │
View Charts               │  ✓   │   ✓   │    ✓    │     ✓     │
View News                 │  ✓   │   ✓   │    ✓    │     ✓     │
Settings                  │  ✓   │   ✓   │    ✓    │     ✓     │
About Page                │  ✓   │   ✓   │    ✓    │     ✓     │
Add/Remove Coins          │  ✗   │   ✓   │    ✗    │     ✗     │
View All Users            │  ✗   │   ✓   │    ✗    │     ✓     │
System Statistics         │  ✗   │   ✓   │    ✓    │     ✓     │
Market Analysis           │  ✗   │   ✗   │    ✓    │     ✗     │
User Activity Monitor     │  ✗   │   ✗   │    ✗    │     ✓     │
Transaction History (Own) │  ✓   │   ✗   │    ✗    │     ✗     │
Transaction History (All) │  ✗   │   ✓   │    ✗    │     ✓     │
Email Notifications       │  ✓   │   ✓   │    ✓    │     ✓     │
Price Alerts              │  ✓   │   ✗   │    ✗    │     ✗     │
Currency Selection        │  ✓   │   ✓   │    ✓    │     ✓     │
```

---

## SECURITY ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SECURITY LAYERS                                    │
└─────────────────────────────────────────────────────────────────────────────┘

Layer 1: Network Security
═════════════════════════
┌─────────────────────────┐
│  VPC (Virtual Private   │
│       Cloud)            │
│                         │
│  • Public Subnet (EC2)  │
│  • Security Groups      │
│  • Network ACLs         │
└─────────────────────────┘

Layer 2: Application Security
══════════════════════════════
┌─────────────────────────┐
│  Flask Application      │
│                         │
│  • HTTPS/TLS            │
│  • Session Management   │
│  • CSRF Protection      │
│  • Input Validation     │
└─────────────────────────┘

Layer 3: Authentication
═══════════════════════
┌─────────────────────────┐
│  User Authentication    │
│                         │
│  • Password Hashing     │
│    (Werkzeug)           │
│  • Email-based Login    │
│  • Session Cookies      │
│  • Role-based Access    │
└─────────────────────────┘

Layer 4: Data Security
══════════════════════
┌─────────────────────────┐
│  DynamoDB               │
│                         │
│  • Encryption at Rest   │
│  • Encryption in Transit│
│  • IAM Policies         │
│  • Backup & Recovery    │
└─────────────────────────┘

Layer 5: API Security
═════════════════════
┌─────────────────────────┐
│  External APIs          │
│                         │
│  • Rate Limiting        │
│  • API Key Management   │
│  • Error Handling       │
│  • Timeout Controls     │
└─────────────────────────┘
```

---

## SCALABILITY ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      HORIZONTAL SCALING STRATEGY                             │
└─────────────────────────────────────────────────────────────────────────────┘

                        ┌──────────────────┐
                        │  Auto Scaling    │
                        │     Group        │
                        └────────┬─────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
            ┌──────────┐  ┌──────────┐  ┌──────────┐
            │  EC2-1   │  │  EC2-2   │  │  EC2-N   │
            │          │  │          │  │          │
            │ Flask App│  │ Flask App│  │ Flask App│
            └────┬─────┘  └────┬─────┘  └────┬─────┘
                 │             │             │
                 └─────────────┼─────────────┘
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
            ┌──────────┐  ┌──────────┐  ┌──────────┐
            │ DynamoDB │  │   SNS    │  │    S3    │
            │          │  │          │  │          │
            │ Auto-    │  │ Unlimited│  │ Unlimited│
            │ Scaling  │  │ Capacity │  │ Storage  │
            └──────────┘  └──────────┘  └──────────┘

Scaling Triggers:
• CPU Utilization > 70%
• Request Count > 1000/min
• Response Time > 2 seconds
```

---

## DEPLOYMENT WORKFLOW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD PIPELINE                                       │
└─────────────────────────────────────────────────────────────────────────────┘

1. Development
   ┌──────────────┐
   │  Local Dev   │
   │  (app.py)    │
   └──────┬───────┘
          │
          │ git push
          ▼
2. Version Control
   ┌──────────────┐
   │   GitHub     │
   │  Repository  │
   └──────┬───────┘
          │
          │ webhook
          ▼
3. Build & Test
   ┌──────────────┐
   │  CI Server   │
   │  (Optional)  │
   │              │
   │ • Run tests  │
   │ • Lint code  │
   └──────┬───────┘
          │
          │ deploy
          ▼
4. AWS Deployment
   ┌──────────────┐
   │  EC2 Instance│
   │              │
   │ • Pull code  │
   │ • Install    │
   │ • Restart    │
   └──────┬───────┘
          │
          │ configure
          ▼
5. AWS Services
   ┌──────────────┐
   │ • DynamoDB   │
   │ • SNS        │
   │ • S3         │
   │ • IAM        │
   └──────────────┘
```

---

## PRE-REQUISITES

### 1. AWS Account Setup
   - Create AWS account
   - Configure billing alerts
   - Set up IAM users

### 2. Understanding IAM Basics
   - IAM roles and policies
   - Security best practices
   - Access key management

### 3. Amazon EC2 Basics
   - EC2 instance types
   - Security groups
   - SSH key pairs
   - Elastic IPs

### 4. DynamoDB Basics
   - NoSQL concepts
   - Partition keys and sort keys
   - Read/write capacity units
   - Global secondary indexes

### 5. Python & Flask
   - Python 3.8+
   - Flask framework
   - Virtual environments
   - pip package management

### 6. Git & GitHub
   - Version control basics
   - Repository management
   - Branch strategies
   - Pull/push operations

---

## MONITORING & LOGGING

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      MONITORING ARCHITECTURE                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│ CloudWatch   │
│  Metrics     │
│              │
│ • CPU Usage  │
│ • Memory     │
│ • Network    │
│ • Disk I/O   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ CloudWatch   │
│    Logs      │
│              │
│ • App Logs   │
│ • Error Logs │
│ • Access Logs│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ CloudWatch   │
│   Alarms     │
│              │
│ • High CPU   │
│ • Errors     │
│ • Latency    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│     SNS      │
│ Notifications│
│              │
│ • Email      │
│ • SMS        │
└──────────────┘
```

---

## COST OPTIMIZATION

```
Service          │ Free Tier              │ Estimated Monthly Cost
─────────────────┼────────────────────────┼────────────────────────
EC2 (t2.micro)   │ 750 hours/month        │ $0 - $10
DynamoDB         │ 25 GB storage          │ $0 - $5
                 │ 25 WCU, 25 RCU         │
SNS              │ 1,000 emails/month     │ $0 - $2
S3               │ 5 GB storage           │ $0 - $1
Data Transfer    │ 1 GB/month             │ $0 - $5
─────────────────┼────────────────────────┼────────────────────────
TOTAL            │                        │ $0 - $23/month
```

---

**Document Version**: 1.0  
**Last Updated**: February 11, 2026  
**Project**: CryptoPulse - Cryptocurrency Trading Platform
