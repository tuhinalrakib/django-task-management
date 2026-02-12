from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model) :
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Task(models.Model) :
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("INPROGRESS", "In Progress"),
        ("COMPLETED", "Completed")
    ]
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE,
        related_name= "project_tasks",
        default=1
        )
    assigned_to = models.ManyToManyField(User, related_name="tasks")
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15,choices=STATUS_CHOICES, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.title

class TaskDetails(models.Model) :
    HIGH = "H"
    MEDIUM = "M"
    LOW = "L"

    PRIORITY_OPTIONS = (
        (HIGH, "HIGH"),
        (MEDIUM, "MEDIUM"),
        (LOW, "LOW")
    )
    task = models.OneToOneField(
        Task, 
        on_delete= models.DO_NOTHING,
        related_name= "details"
        )
    asset = models.ImageField(upload_to="task_assets", blank=True,  default="task_assets/default.jpg")
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices= PRIORITY_OPTIONS, default= LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Detail from task {self.task.title}"

# Many To Many realation
# task = onekgulo empoyee ekta task korse
# employee = onekgulo task er jonn employee assign ase

#signals
 