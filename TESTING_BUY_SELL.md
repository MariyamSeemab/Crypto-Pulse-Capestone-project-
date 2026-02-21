# Testing Buy/Sell Functionality

## Steps to Test Buy Feature:

1. **Login as Regular User**
   - Email: `demo@user.com`
   - Password: `demo123`

2. **Navigate to Portfolio**
   - Click "Portfolio" in the navigation menu

3. **Try to Buy a Coin**
   - Click the green "Buy Crypto" button
   - Select a coin from the dropdown (e.g., "Bitcoin")
   - Enter an amount (e.g., 100)
   - Click "Buy"

4. **Check for Errors**
   - If you see an error, note the message
   - Check the browser console (F12 → Console tab)

## Common Issues:

### Issue 1: Coin not found
- **Cause**: The coin ID might not match what CoinGecko API expects
- **Solution**: Try these coins that are definitely tracked:
  - bitcoin
  - ethereum
  - solana
  - cardano

### Issue 2: Invalid amount
- **Cause**: Amount is 0 or negative
- **Solution**: Enter a positive number (e.g., 10, 50, 100)

### Issue 3: Insufficient balance
- **Cause**: Trying to buy more than $10,000 (starting balance)
- **Solution**: Enter an amount less than your available balance

## Debug Information:

The server now logs detailed information when you try to buy/sell:
- Request data received
- Coin ID and amount
- Prices fetched from API
- Any errors encountered

Check the terminal/console where the Flask app is running to see these logs.

## Expected Behavior:

When buy/sell works correctly:
1. You should see a success message
2. The page should reload
3. Your portfolio should update with the new holdings
4. Your balance should decrease (buy) or increase (sell)
5. A mock email notification will be logged to the console

## Browser Console Check:

Open browser developer tools (F12) and check:
1. **Console tab**: Look for JavaScript errors
2. **Network tab**: Check the /api/buy_coin request
   - Status should be 200 (success) not 400 (error)
   - Response should show transaction details
