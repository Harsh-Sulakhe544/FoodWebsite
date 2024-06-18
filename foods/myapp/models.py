from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Custom user model
class User(models.Model):
    id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.name

# Model for authentication purpose
class UserAuth(models.Model):
    id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    email= models.EmailField(max_length=254, unique=True)
    password= models.CharField(max_length=128, unique=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email

# Food related models
class Dessert(models.Model):
    id= models.BigAutoField(auto_created=True, primary_key=True,serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    description = models.TextField()
    brand_name = models.CharField(default='Unknown Brand', max_length=100)
    image = models.ImageField(default='NULL', upload_to='dessert_images/')
    price = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    product_id = models.CharField(default='N/A', max_length=20)
    rating = models.DecimalField(decimal_places=1, default=0.0, max_digits=3)
    
    def __str__(self):
        return self.name

class MainCourse(models.Model):
    id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name= models.CharField(max_length=100)
    description = models.TextField(),
    brand_name = models.CharField(default='Unknown Brand', max_length=100)
    image = models.ImageField(default='NULL', upload_to='main_course_images/')
    price = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    product_id = models.CharField(default='N/A', max_length=20)
    rating = models.DecimalField(decimal_places=1, default=0.0, max_digits=3)
    
    def __str__(self):
        return self.name

class Starter(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    description = models.TextField()
    brand_name = models.CharField(default='Unknown Brand', max_length=100)
    image = models.ImageField(default='NULL', upload_to='dessert_images/')
    price = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    product_id = models.CharField(default='N/A', max_length=20)
    rating = models.DecimalField(decimal_places=1, default=0.0, max_digits=3)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
    session_id = models.CharField(max_length=255),
    created_at = models.DateTimeField(auto_now_add=True),

    def __str__(self):
        return self.session_id

class CartItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    product_type =  models.CharField(max_length=50)
    product_id =  models.PositiveIntegerField()
    quantity =  models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(on_delete=models.CASCADE, to='myapp.cart'),

    def __str__(self):
        return f'{self.product_type} - {self.product_id}'

    def get_product(self):
        if self.product_type == 'dessert':
            return Dessert.objects.get(id=self.product_id)
        elif self.product_type == 'main_course':
            return MainCourse.objects.get(id=self.product_id)
        elif self.product_type == 'starter':
            return Starter.objects.get(id=self.product_id)
        return None
