"""Fictional, non-personal examples used by tests and the demo."""

SAMPLE_MESSAGES: dict[str, str] = {
    "Routine appointment (lower risk)": (
        "Reminder: your appointment is tomorrow at 3 pm. "
        "Please open the provider's usual app if you need to make a change."
    ),
    "Ambiguous account note": "Please check your account when you have a moment.",
    "Delivery fee": (
        "Your parcel could not be delivered today. Pay the $2.14 redelivery fee "
        "now at https://delivery-review-example.test/pay or it will be returned."
    ),
    "Bank verification": (
        "Security alert: your bank account has been locked. Confirm your login "
        "and one-time code immediately at https://secure-bank-example.test."
    ),
    "Marketplace courier": (
        "I want to buy the camera today. The courier needs you to pay a "
        "refundable insurance fee first through this payment link."
    ),
    "Crypto investment": (
        "Guaranteed daily crypto returns: send $300 to this wallet today and "
        "I will turn it into $3,000 by next week."
    ),
    "Job offer": (
        "You have been selected for a remote job paying $95 per hour with no "
        "interview. Buy gift cards and send the codes to activate payroll."
    ),
    "Rental deposit": (
        "The apartment is available but I am overseas. Send the bond today "
        "before viewing to reserve the property."
    ),
    "Family emergency": (
        "Mum, this is my temporary number. I am in trouble. Do not call; "
        "transfer $1,800 right now and I will explain later."
    ),
    "Tax refund": (
        "ATO tax refund pending. Enter your bank details at "
        "https://mygov-refund-example.test immediately to receive it."
    ),
}
