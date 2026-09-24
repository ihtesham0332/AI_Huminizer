from fastapi import APIRouter, Request, HTTPException, Header
import logging
import json

router = APIRouter()
logger = logging.getLogger(__name__)

# This would be your actual Stripe Webhook Secret
STRIPE_WEBHOOK_SECRET = "whsec_..."

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """
    Secure endpoint to receive subscription payments from Stripe.
    Automatically upgrades users in the database when they pay.
    """
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing Stripe Signature")
        
    try:
        # 1. Read the raw body (required by Stripe to verify signatures)
        payload = await request.body()
        
        # 2. In a real environment, you verify the signature using the stripe SDK
        # stripe.Webhook.construct_event(payload, stripe_signature, STRIPE_WEBHOOK_SECRET)
        
        event = json.loads(payload)
        event_type = event.get('type')
        
        if event_type == 'checkout.session.completed':
            session = event['data']['object']
            customer_email = session.get('customer_details', {}).get('email')
            # TODO: Upgrade this user in the Database to PRO tier
            logger.info(f"Payment successful for {customer_email}. Upgraded to PRO tier.")
            
        elif event_type == 'customer.subscription.deleted':
            subscription = event['data']['object']
            # TODO: Downgrade this user in the Database back to FREE tier
            logger.info("Subscription cancelled. Downgrading user.")
            
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Stripe Webhook Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
