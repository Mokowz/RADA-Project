from django.core.mail import send_mail
from users.models import User

def send_combined_alert_email(flood_risks, drought_risks):
    subject = "⚠️ Flood & Drought Risk Alert for Baringo County"
    lines = ["Dear Resident,\n"]
    
    if flood_risks:
        lines.append("⚠️ Flood risks have been identified on the following days:")
        for date, prob in flood_risks:
            lines.append(f"• {date}: {prob}% probability")
        lines.append("")

    if drought_risks:
        lines.append("🌾 Drought risks have been identified on the following days:")
        for date, prob in drought_risks:
            lines.append(f"• {date}: {prob}% probability")
        lines.append("")

    lines.append("We advise taking necessary precautions to protect your home, crops, and livestock.")
    lines.append("Stay safe,\nEarly Alert System Team")

    message = "\n".join(lines)
    recipients = list(User.objects.values_list("email", flat=True))


    send_mail(subject, message, from_email='ronniemokaya30@gmail.com', recipient_list=recipients)
