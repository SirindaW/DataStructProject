from django.db import models
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


# class AllProduct(models.Model):
#     title = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=200, decimal_places=2)
#     description = models.TextField(default="")

#     def __str__(self):
#         return self.title


class IphoneModel(models.Model):
    title = models.CharField(max_length=400)

    def __str__(self):
        return self.title

    def is_model(self,o):
        if o.lower().replace(' ','') == str(self.title).replace(' ','').lower():
            return True
        return False

class CollectionFeature(models.Model):
    title = models.CharField(max_length=400)
    def __str__(self) :
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=400)
    image = models.ImageField(
        upload_to="product_imgs", blank=True, null=True)
    detail = models.TextField(default='',null=True,blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    model = models.ForeignKey(IphoneModel,on_delete=SET_NULL,null=True) 
    collection = models.ForeignKey(CollectionFeature,on_delete=SET_NULL, blank=True,null=True)
    slug = models.SlugField(unique = True)

    class Meta:
        unique_together = ('title','slug')

    def has_collection(self):
        return self.collection != None

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)
