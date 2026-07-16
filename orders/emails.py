import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)

def send_order_confirmation_email(order):
    """Send a premium HTML order confirmation email to the user"""
    if not order or not order.user or not order.user.email:
        logger.warning(f"Skipping order confirmation email: Order, User or User Email is missing.")
        return False
    
    try:
        subject = f"Order Confirmed - {order.order_id}"
        
        # Render HTML content
        context = {
            'order': order,
        }
        html_content = render_to_string('emails/order_confirmation.html', context)
        
        # Render plain-text fallback
        text_content = (
            f"Hi {order.user.username.title()},\n\n"
            f"Thank you for your order! Your order {order.order_id} has been received.\n\n"
            f"Order Summary:\n"
        )
        for item in order.items.all():
            variant_str = f" ({item.variant.size} / {item.variant.color})" if item.variant else ""
            text_content += f"- {item.product.name}{variant_str} x {item.quantity} (₹{item.price} each)\n"
        
        text_content += (
            f"\nTotal Price: ₹{order.total_price}\n"
            f"Shipping Address: {order.shipping_address}\n\n"
            f"We are preparing your package. Thank you for shopping with us!\n"
            f"DripShop Support"
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"Order confirmation email sent successfully for {order.order_id} to {order.user.email}")
        return True
    except Exception as e:
        logger.exception(f"Failed to send order confirmation email for {order.order_id}: {str(e)}")
        return False
