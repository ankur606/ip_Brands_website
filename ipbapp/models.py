from django.db import models

# Create your models here.
class HomeBanner(models.Model):
    heading = models.CharField(max_length=400, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
   

class AboutUsPage(models.Model):
    image = models.FileField(null=True, blank=True)
    title_name = models.CharField(max_length=400, null=True, blank=True) 
    heading = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    year_name = models.IntegerField(null=True, blank=True)
    year_title = models.CharField(max_length=400, null=True, blank=True) 
    

class ScopePage(models.Model):
    image = models.FileField(null=True, blank=True)
    page_title = models.CharField(max_length=400, null=True, blank=True) 
    heading = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

 
class WherePage(models.Model):
    image = models.FileField(null=True, blank=True)
    page_title = models.CharField(max_length=400, null=True, blank=True) 
    heading = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class GeographicalModel(models.Model):
    image = models.FileField(null=True, blank=True)
    page_title = models.CharField(max_length=400, null=True, blank=True) 
    description = models.TextField(null=True, blank=True)
        

class IndustriesSection(models.Model):
    image = models.FileField(null=True, blank=True)
    page_title = models.CharField(max_length=400, null=True, blank=True) 
    heading = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)        

class HowSection(models.Model):
    page_title = models.CharField(max_length=400, null=True, blank=True) 
    description = models.TextField(null=True, blank=True)
    heading = models.TextField(null=True, blank=True)
    flexible_set_up = models.CharField(max_length=400, null=True, blank=True)
    sub_heading = models.TextField(null=True, blank=True)    

class ServicesSection(models.Model):
    image = models.FileField(null=True, blank=True)
    heading = models.CharField(max_length=400, null=True, blank=True) 
      
class ContactInquiry(models.Model):
    full_name = models.CharField(max_length=400, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True )
    subject = models.CharField(max_length=400, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

class GetInTouch(models.Model):
    IPBrandsGmbH = models.CharField(max_length=400, null=True, blank=True) 
    address = models.TextField(null=True, blank=True)
    GermanyOffice_title = models.CharField(max_length=400, null=True, blank=True) 
    GermanyOfficeAddress = models.TextField(null=True, blank=True)

class Services(models.Model):
    service_name = models.CharField(max_length=400, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)        

class AddServiceSubHeading(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE )
    sub_heading_name = models.CharField(max_length=500, null=True, blank=True)

class WhyUsSection(models.Model):
    page_title = models.CharField(max_length=400, null=True, blank=True)
    image = models.FileField(null=True, blank=True)

class AddWhyUsSectionSubHeading(models.Model):
    whyus = models.ForeignKey(WhyUsSection, on_delete=models.CASCADE )
    sub_heading_name = models.TextField(null=True, blank=True)

class References(models.Model):
    image = models.FileField(null=True, blank=True)
    resources_heading_name = models.CharField(max_length=400, null=True, blank=True)
    resources_description = models.TextField(null=True, blank=True)
    user_image = models.FileField(null=True, blank=True)
    user_name = models.FileField(null=True, blank=True)
    user_designation =  models.CharField(max_length=400, null=True, blank=True)
    user_description = models.TextField(null=True, blank=True)
    user_about_us = models.TextField(null=True, blank=True)
  
class ManagementProjects(models.Model):
    image_first = models.FileField(null=True, blank=True)
    image_second = models.FileField(null=True, blank=True)
    image_third = models.FileField(null=True, blank=True)
    image_fourth = models.FileField(null=True, blank=True)
    year_durations = models.CharField(max_length=400, null=True, blank=True)
    description_first = models.TextField(null=True, blank=True, default="")
    description_second = models.TextField(null=True, blank=True, default="")
    description_third = models.TextField(null=True, blank=True, default="")
    description_fourth = models.TextField(null=True, blank=True, default="")


class UspSection(models.Model):
    page_title = models.CharField(max_length=400, null=True, blank=True)
    heading = models.CharField(max_length=800, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)        

class UspSectionSubHeading(models.Model):
    ups = models.ForeignKey(UspSection, on_delete=models.CASCADE )
    sub_heading_name = models.CharField(max_length=500, null=True, blank=True)