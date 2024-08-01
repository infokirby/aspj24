import sklearn 
import joblib
model = joblib.load('fraud_detection_model.pkl')

def is_fraudulent_order(current_order, past_orders):
    # Implement logic to check if the current order is fraudulent based on past orders
    current_total = current_order['Total']
    past_totals = [order['Total'] for order in past_orders]
    
    if not past_totals:
        return False  # No past orders to compare with
    
    average_past_total = sum(past_totals) / len(past_totals)
    
    # Example threshold: If the current total is more than 3 times the average past total, flag as fraudulent
    if current_total > 3 * average_past_total:
        return True
    
    return False