# from django.db import models

# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# GENDER = (('Male','Male'), ('Female','Female'))
# STATUS = (('Pending','Pending'), ('Email_Confirmation', 'Email_Confirmation'), ('Email_Verified', 'Email_Verified'), ('Active', 'Active'))


# class UserAccountManager(BaseUserManager):
#     def create_account (self, email, password, full_name): # things listed in REQUIRED_FIELDS
#         if not email:
#             raise ValueError("must have an email")
#         account = self.model(email=self.normalize_email(email), full_name = full_name)
#         account.set_password(password)
#         account.save(using=self.db)
#         return account


#     def create_superuser(self, email, password, full_name):
#         account = self.create_account(email, password, full_name)
#         account.is_staff = True
#         account.is_active = True
#         account.is_superuser = True
#         account.status = "Active"
#         account.save(using = self.db)
#         return account


# class UserAccount(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=200)
#     gender = models.CharField(max_length=50, choices=GENDER, default='Male')
#     profile = models.ImageField(upload_to='Profile', blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     # is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     # is_superuser = models.BooleanField(default=False)
#     status = models.CharField(max_length=100, choices=STATUS, default='Pending')
#     created_date = models.DateTimeField(auto_now_add=True, editable=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['full_name'] # will appear at py manage.py createsuperuser thingy

#     objects = UserAccountManager()

#     def __str__(self):
#         return self.full_name
    
#     class Meta:
#         ordering = ('-id',)

#     @property
#     def get_full_name (self):
#         return self.full_name # get name fast 
#     def get_staff (self):
#         return self.account_set.filter(is_staff = True) # get staff list fast 
#     def get_viewer (self):
#         return self.account_set.filter(is_staff = False) # get viewers list fast 
