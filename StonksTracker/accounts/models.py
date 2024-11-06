from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    UserID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.username


class Watchlist(models.Model):
    WatchlistID = models.AutoField(primary_key=True)  # Automatically incrementing primary key
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Foreign key referencing User model

    class Meta:
        db_table = 'watchlists'  # Use lowercase and plural form for consistency

    def __str__(self):
        return f"Watchlist ID: {self.WatchlistID} for User: {self.UserID.username}"


class PriceHistory(models.Model):
    historyID = models.AutoField(primary_key=True)  # Automatically incrementing primary key
    itemName = models.CharField(max_length=100)  # Item name field
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price field
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is created

    class Meta:
        db_table = "price_history"  # Use lowercase and plural form for consistency

    def __str__(self):
        return f"PriceHistory ID: {self.historyID}, Item: {self.itemName}, Price: {self.price}"