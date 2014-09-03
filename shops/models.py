from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from core import modelFieldChoicesManager as MCM

# Create your models here.



class Shop(models.Model):

    #Shop Details
    shop_name = models.CharField(max_length=128)
    shop_address = models.CharField(max_length=256, null = True) # TODO change to incorporate multiple address lines
    shop_category = models.CharField(max_length=2,choices = MCM.SHOP_CATEGORY_CHOICES(), default = 'GS')
    shop_location = models.CommaSeparatedIntegerField(max_length=20, null = True)
    shop_contact_no = models.CharField(max_length=15, null = True) # TODO multiple nos
    shop_email = models.EmailField(max_length=30, null = True) # TODO multiple emails
    #shop_image_path = models.FilePathField(null = True) # TODO change to store paths only
    shop_info_text = models.CharField(max_length=2048, null = True)#TODO change to hold file
    #Shop Admin
    shop_admin = models.ForeignKey(User)

    def __str__(self):
        return self.shop_name


class Catalog(models.Model):

    shop = models.ForeignKey(Shop)
    product = models.ForeignKey(Product)
    price = models.IntegerField(null = True)

    def __str__(self):
        return self.product

class ProductOffer(models.Model):
    offer_name = models.CharField(max_length=128)
    offer_info = models.CharField(max_length=1024, null = True)
    points_needed = models.IntegerField(default = 0)#TODO make this flexible
    offer_catalog_item = models.ForeignKey(Catalog, null = True)
    is_eligible = False

    def eligibilityCheck(self, user, shop):
        relation, created = ShopUserRelation.objects.get_or_create(user_id=user.id, shop_id=shop.id)
        points = relation.loyalty_points
        if self.points_needed > points:
            self.is_eligible = False
        else:
            self.is_eligible = True

    def __str__(self):
        return self.offer_name


class ShopUserRelation(models.Model):

    shop = models.ForeignKey(Shop)
    user = models.ForeignKey(User)

    shop_review = models.CharField(max_length=2048, blank=True)

    loyalty_points = models.IntegerField(default = 0)

    user_like = models.BooleanField(default = False)
    visited = models.BooleanField(default = False)


    def __str__(self):
        return "Shop User Relation Item " + str(self.id)

class ShopOffer(models.Model):
    offer_name = models.CharField(max_length=128)
    offer_info = models.CharField(max_length=1024, null = True)
    points_needed = models.IntegerField(default = 0)#TODO make this flexible
    offer_category = models.CharField(max_length=5 ,choices = MCM.PRODUCT_CATEGORY_CHOICES())
    offer_shop = models.ForeignKey(Shop, null = True)
    is_eligible = False

    def eligibilityCheck(self, user):
        relation, created = ShopUserRelation.objects.get_or_create(user_id=user.id, shop_id=self.offer_shop.id)
        points = relation.loyalty_points
        if self.points_needed > points:
            self.is_eligible = False
        else:
            self.is_eligible = True

    def __str__(self):
        return self.offer_name

class ProductUserRelation(models.Model):

    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    product_review = models.CharField(max_length=2048)

    def __str__(self):
        return "Product User Relation Item " + str(self.id)

class History(models.Model):

    date = models.DateField()
    product = models.ForeignKey(Product)
    #offer_availed = models.ForeignKey(Offer, null = True)#TODO multiple
    shop_user_relation = models.ForeignKey(ShopUserRelation)

    def __str__(self):
        return "History Item " + str(self.id)
