from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey("ProductCategory", on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images", blank=True, null=True)

    
    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    CATEGORIES = [
        ("Digital", "Digital"),
        ("Physical", "Physical"),
        ("Other", "Other")
    ]
    name = models.CharField(max_length=255, choices=CATEGORIES, default="Other")
