# from django.db.models.signals import post_delete, m2m_changed
# from tasks.models import Task
# from django.dispatch import receiver
# from django.core.mail import send_mail

# @receiver(m2m_changed, sender=Task.assigned_to.through) #post save signal
# def notify_employee_on_task_creations(sender, instance, action, **kwargs):
#     if action == "post_add":
#         assigned_emails = [emp.email for emp in instance.assigned_to.all()]
#         print(assigned_emails)
#         send_mail(
#             "New Task Assigned",
#             f"You have been assigned to the Task : {instance.title}.",
#             "eng.tuhin77@gmail.com",
#             assigned_emails,
#             fail_silently=False,
#         )

# @receiver(post_delete, sender=Task) #post delete signal
# def delete_associate_delete(sender, instance, **kwargs):
#     if hasattr(instance, 'details'):
#         print(instance)
#         instance.details.delete()
#         print("Associated TaskDetails deleted successfully")     