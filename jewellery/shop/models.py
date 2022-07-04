from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return str(self.name)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


class product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category ,on_delete=models.CASCADE, default=1)
    price = models.PositiveIntegerField(default=0)
    purity = models.IntegerField(default=0)
    jewellery_type = models.CharField(max_length=50, default="")
    weight = models.FloatField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateTimeField()
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return str(self.product_name)

    @staticmethod
    def get_all_products():
        return product.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return product.objects.filter(category=category_id)
        else:
            return product.objects.all()

    @staticmethod
    def get_products_by_id(product_id):
        return product.objects.filter(id=product_id)


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return str(self.email)

    def register(self):
        self.save()


    @staticmethod
    def get_all_customer_by_email(email):
        return Customer.objects.filter(email=email)

    @staticmethod
    def get_customer_by_email(email):
        try:
          return Customer.objects.get(email=email)
        except:
          return False

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False


class cart(models.Model):
    email = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE,default="1")
    quantity = models.PositiveIntegerField(default="1")

    def __str__(self):
        return str(self.email)

    @property
    def total_cost(self):
        return self.quantity * self.product.price


class Appointment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField(default=9)
    purpose = models.CharField(max_length=500)
    date = models.DateTimeField()


class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField(default=9)
    feedback = models.CharField(max_length=5000)


STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)


class Order(models.Model):
    email = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE, default="1")
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=10000000000000000, default="")
    status = models.CharField(max_length=50 , choices=STATUS_CHOICES, default='pending')


    @property
    def total_cost(self):
        return self.quantity * self.product.price
