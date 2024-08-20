import razorpay


KEY = 'rzp_test_0Soma3GGNGgA8f'


ID= 'EHYe9nNtZFgOPfG1PBAI7c0G'




def create_payment(amount,receipt):
    """create order payment using razor pay API,
    Parameters:amount->amount get from total_price value in orders table,
    receipt->receipt value get from orders invoice id into orders table"""
    client = razorpay.Client(auth=(KEY,ID))
    if client :
        data = {
        "amount": amount,
        "currency": "INR",
        "receipt": receipt
        }
        payment = client.order.create(data=data)
       
    return payment
