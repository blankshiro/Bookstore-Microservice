import stripe

stripe.api_key = 'sk_test_51JkVJRCTtIsYSaGSDUsqTW0aMtUv9wy95QGqyTQOKCZ\
    2WF9M0SS9Z18Jee5hbhBf2Pn7gmcHiowr342LUgD5gKVW00LNxnpyVD'


def createCard(cardNumber, expiryMonth, expiryYear, cvv):
    card = {
        "number": str(cardNumber),
        "exp_month": int(expiryMonth),
        "exp_year": int(expiryYear),
        "cvc": str(cvv),
    }
    return card


def generateCardToken(card):
    data = stripe.Token.create(card=card)
    cardToken = data['id']
    return cardToken


def createPayment(amount, currency, description, tokenid):
    payment = stripe.Charge.create(
        amount=int(amount)*100,
        currency=currency,
        description=description,
        source=tokenid,
    )

    payment_check = payment['paid']    # return True for successfull payment
    print(payment)
    return payment_check


def processPayment(amount, description, cardNumber, expiryMonth, expiryYear,
                   cvv):
    card = createCard(cardNumber, expiryMonth, expiryYear, cvv)
    paymentIntent = generateCardToken(card)

    paymentStatus = createPayment(amount, "SGD", description, paymentIntent)
    if(paymentStatus):
        return True
    else:
        return False
