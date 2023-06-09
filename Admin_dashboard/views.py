from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, HttpResponseRedirect,  HttpResponse
from django.contrib.auth import authenticate, login as dj_login, logout
from .models import *
from .forms import *
from ipbapp.models import*
# Create your views here.
class IndexPageDashboard(View):

    def get(self, request):
        user = User.objects.all()
        super_user = User.objects.filter(is_superuser=True)
        counter=0
        superuser=0
        staff=0
        active = 0
        for i in user:
            counter+=1
            if i.is_superuser == True:
                superuser+=1

            if i.is_staff == True:
                staff+=1
        
            if i.is_active == True:
                active+=1
        d = { "user":super_user,
          "counter_user":counter,
          "superuser":superuser,
          'staff':staff,
          'user':user,
          "active":active,
        }
        if request.user.is_superuser == True:
            return render(request, 'dashboard/index.html', d)
        else:
            return redirect("adminLogin")


# =============Admin LOGIN=============

def login(request):
    if request.method == 'POST':
        email_id = request.POST.get('email')
        passwords = request.POST.get('password')

        user = authenticate(
            request=request, email=email_id, password=passwords)

        if user is not None:
            if User.objects.filter(email=email_id, is_superuser=True):
                dj_login(request, user)
                return redirect('homePageDashboard')
            else:
                messages.error(request, 'You Are Not Admin User')
        else:
            messages.error(request, 'Invalid Email or Password')

    return render(request, 'dashboard/samples/login.html')


# =============LOGOUT=============

def userlogout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully..!!')
    return redirect('adminLogin')

# ===== Show All Users In Admin Dashboard =======#


class ShowUserView(View):
    def get(self, request):
        user = User.objects.all()
        return render(request,  'dashboard/show-user.html', {'data': user})


class AddNewUserView(View):
    def get(self, request):
        return render(request,  'dashboard/add_user.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        password = request.POST.get('password')
        con_password = request.POST.get('password1')
        print(email, phone_number, password, name)
        if password == con_password:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User Email  Already Exist.. ')
            else:
                user = User.objects.create_user(
                    name=name, email=email, password=password, phone_number=phone_number)

                user.save()
                messages.success(request, 'User Added Successfully..!!')
                return redirect('showUser')
            messages.error(request, 'Password Not Match ..!!')
        if request.user.is_superuser == True:
            return render(request, 'dasboard/add_user.html')

        else:
            return redirect("/")


# =============delete User=============
class UserDeleteView(View):
    def get(self, request, id):
        a = User.objects.get(pk=id)
        a.delete()
        messages.success(request, 'User Deleted Successfully..!!')
        return redirect('showUser')


# ====== Edit User Profile =========#
class UpdateUserProfileView(View):

    def get(self, request, id):
        if request.user.is_superuser == True:
            return render(request, 'dashboard/edit_user.html', {"user": User.objects.get(pk=id)})
        else:
            return HttpResponseRedirect('/')

    def post(self, request, id):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        super = request.POST.get('super')
        staff = request.POST.get('staff')
        active = request.POST.get('active')
        checklist = [False, False, False]

        if super == 'True':
            checklist[0] = True
        if staff == 'True':
            checklist[1] = True
        if active == 'True':
            checklist[2] = True

        user = User.objects.get(id=id)
        user.name = name
        user.email = email
        user.phone_number = phone_number
        user.is_superuser = checklist[0]
        user.is_admin = checklist[1]
        user.is_active = checklist[2]
        user.save()
        messages.success(request, 'User Edit Successfully..!!')
        return redirect('showUser')


def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            password = request.POST.get('password')
            v = User.objects.get(email=email)
            if v.is_superuser == True:
                v.set_password(password)
                v.save()

                messages.success(request, 'Password Forget Successfully..!!')
                return redirect('adminLogin')
            else:
                messages.error(
                    request, "Sorry! You Are Not Admin User . You Can't  Forget Password! ")
        else:
            messages.error(request, 'Invalid Email..')
    return render(request, 'dashboard/samples/forget-password.html')

class AdminProfile(View):
    def get(self, request):
        return render(request, 'dashboard/profile.html')

########   Home Banner View  ###############

class AddHomeBanner(View):
    def get(self, request):
        return render(request, 'dashboard/add_banner.html')
    def post(self, request):
        data = HomeBanner()
        image = request.FILES.get('banner_image')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
        data.image = image
        data.heading = heading
        data.description = description
        data.save()
        messages.success(request, 'Home Banner Add Successfully..!!')
        return redirect('bannerLists')


class ShowBannerView(View):
    def get(self, request):
        data = HomeBanner.objects.all()
        return render(request, 'dashboard/show_banner.html', {'data':data})

class EditBanner(View):
    def get(self, request, id):
        data = HomeBanner.objects.get(id=id)
        return render(request, 'dashboard/edit_banner.html', {'data':data})

    def post(self, request, id):
        data = HomeBanner.objects.filter(id=id)
        image = request.FILES.get('banner_image')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
        if image is not None:
            HomeBanner(id=id, image=image, heading=heading, description=description).save()
            messages.success(request, 'Home Banner Edit Successfully..!!')
            return redirect('bannerLists')
        else:
             for banner_data in data:
                HomeBanner(id=id, image=banner_data.image, heading=heading, description=description).save()
                messages.success(request, 'Home Banner Edit Successfully..!!')
                return redirect('bannerLists')

class DeleteBanner(View):
    def get(self, request, id):
        data = HomeBanner.objects.get(id=id)
        data.delete()
        messages.success(request, 'Home Banner Delete Successfully..!!')
        return redirect('bannerLists')

########  About us Page Views #########

class AboutsPage(View):
    def get(self, request):
        return render(request, 'dashboard/add_about_us_content.html')
    def post(self, request):
        data = AboutUsPage()
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
        year = request.POST.get('year_name')
        year_title = request.POST.get('title_year')

        data.image = image
        data.title_name = title_name
        data.heading = heading
        data.description = description
        data.year_name = year
        data.year_title = year_title
        data.save()
        messages.success(request, 'About Us Page  Content Add Successfully..!!')
        return redirect('about_page_content')

class ShowAboutUsPageContent(View):
    def get(self, request):
        data = AboutUsPage.objects.all()
        return render(request, 'dashboard/show_about_page_content.html', {'data':data})

class EditAboutPageContent(View):
    def get(self, request, id):
        data = AboutUsPage.objects.get(id=id)
        return render(request, 'dashboard/edit_about_page_content.html', {'data':data})

    def post(self, request, id):
        data = AboutUsPage.objects.filter(id=id)
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
        year = request.POST.get('year_name')
        year_title = request.POST.get('title_year')
        if image is not None:
            AboutUsPage(id=id, image=image, title_name=title_name, heading=heading, description=description, year_name=year, year_title=year_title ).save()
            messages.success(request, 'About us page content Edit Successfully..!!')
            return redirect('about_page_content')
        else:
             for data in data:
                AboutUsPage(id=id, image=data.image, title_name=title_name, heading=heading, description=description, year_name=year, year_title=year_title).save()
                messages.success(request, 'About us page content Edit Successfully..!!')
                return redirect('about_page_content')        
class DeleteAboutPageContent(View):
    def get(self, request, id):
        data = AboutUsPage.objects.get(id=id)
        data.delete()
        messages.success(request, 'About Page Content Delete Successfully..!!')
        return redirect('about_page_content')

#########  Scope Page Views ##############
class AddScopePage(View):
    def get(self, request):
        return render(request, 'dashboard/add_scope_page_content.html')
    def post(self, request):
        data = ScopePage()
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
    
        data.image = image
        data.page_title = title_name
        data.heading = heading
        data.description = description
        data.save()
        messages.success(request, 'Scope  Page  Content Add Successfully..!!')
        return redirect('showScope')

class ShowScopePageContent(View):
    def get(self, request):
        data = ScopePage.objects.all()
        return render(request, 'dashboard/show_scope_page_content.html', {'data':data})        

class EditScopePageContent(View):
    def get(self, request, id):
        data = ScopePage.objects.get(id=id)
        return render(request, 'dashboard/edit_scope_page_content.html', {'data':data})

    def post(self, request, id):
        data = ScopePage.objects.filter(id=id)
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
    
        if image is not None:
            ScopePage(id=id, image=image, page_title=title_name, heading=heading, description=description).save()
            messages.success(request, 'Scope Page content Edit Successfully..!!')
            return redirect('showScope')
        else:
             for data in data:
                ScopePage(id=id, image=data.image, page_title=title_name, heading=heading, description=description).save()
                messages.success(request, 'Scope page content Edit Successfully..!!')
                return redirect('showScope') 

class DeleteScopePageContent(View):
    def get(self, request, id):
        data = ScopePage.objects.get(id=id)
        data.delete()
        messages.success(request, 'Scope Page Content Delete Successfully..!!')
        return redirect('showScope')       

#########  Where Page Views ##############  
class AddWherePageContent(View):
    def get(self, request):
        return render(request, 'dashboard/add_where_page_content.html')
    def post(self, request):
        data = WherePage()
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
    
        data.image = image
        data.page_title = title_name
        data.heading = heading
        data.description = description
        data.save()
        messages.success(request, 'Where  Page  Content Add Successfully..!!')
        return redirect('showWhere')

class ShowWherePageContent(View):
    def get(self, request):
        data = WherePage.objects.all()
        return render(request, 'dashboard/show_where_page_content.html', {'data':data})        

class EditWherePageContent(View):
    def get(self, request, id):
        data = WherePage.objects.get(id=id)
        return render(request, 'dashboard/edit_where_page_content.html', {'data':data})

    def post(self, request, id):
        data = WherePage.objects.filter(id=id)
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
    
        if image is not None:
            WherePage(id=id, image=image, page_title=title_name, heading=heading, description=description).save()
            messages.success(request, 'Where Page content Edit Successfully..!!')
            return redirect('showWhere')
        else:
             for data in data:
                WherePage(id=id, image=data.image, page_title=title_name, heading=heading, description=description).save()
                messages.success(request, 'Where page content Edit Successfully..!!')
                return redirect('showWhere') 

class DeleteWherePageContent(View):
    def get(self, request, id):
        data = WherePage.objects.get(id=id)
        data.delete()
        messages.success(request, 'Where Page Content Delete Successfully..!!')
        return redirect('showWhere')       


#########  GeoGraphical Page Views ##############  
class AddGeographicalPageContent(View):
    def get(self, request):
        return render(request, 'dashboard/add_geographical_content.html')
    def post(self, request):
        data = GeographicalModel()
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        description = request.POST.get('description')
    
        data.image = image
        data.page_title = title_name
        data.description = description
        data.save()
        messages.success(request, 'Geographical  Page  Content Add Successfully..!!')
        return redirect('showGeographical')

class ShowGeographicalPageContent(View):
    def get(self, request):
        data = GeographicalModel.objects.all()
        return render(request, 'dashboard/show_geographical_content.html', {'data':data})        

class EditGeographicalPageContent(View):
    def get(self, request, id):
        data = GeographicalModel.objects.get(id=id)
        return render(request, 'dashboard/edit_geographical_content.html', {'data':data})

    def post(self, request, id):
        data = GeographicalModel.objects.filter(id=id)
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
 
        description = request.POST.get('description')
    
        if image is not None:
            GeographicalModel(id=id, image=image, page_title=title_name,  description=description).save()
            messages.success(request, 'Geographical Page content Edit Successfully..!!')
            return redirect('showGeographical')
        else:
             for data in data:
                GeographicalModel(id=id, image=data.image, page_title=title_name, description=description).save()
                messages.success(request, 'Geographical page content Edit Successfully..!!')
                return redirect('showGeographical') 

class DeleteGeographicalPageContent(View):
    def get(self, request, id):
        data = GeographicalModel.objects.get(id=id)
        data.delete()
        messages.success(request, 'Geographical Page Content Delete Successfully..!!')
        return redirect('showGeographical') 


#########  Industries Page Views ##############  

class AddIndustriesPageContent(View):
    def get(self, request):
        return render(request, 'dashboard/add_Industries_content.html')
    def post(self, request):
        data = IndustriesSection()
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
    
        data.image = image
        data.page_title = title_name
        data.heading = heading
        data.description = description
        data.save()
        messages.success(request, 'Industries  Page  Content Add Successfully..!!')
        return redirect('showIndustries')

class ShowIndustriesPageContent(View):
    def get(self, request):
        data = IndustriesSection.objects.all()
        return render(request, 'dashboard/show_indutries_content.html', {'data':data})        

class EditIndustriesPageContent(View):
    def get(self, request, id):
        data = IndustriesSection.objects.get(id=id)
        return render(request, 'dashboard/edit_industries_content.html', {'data':data})

    def post(self, request, id):
        data = IndustriesSection.objects.filter(id=id)
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
    
        if image is not None:
            IndustriesSection(id=id, image=image, page_title=title_name, heading=heading, description=description).save()
            messages.success(request, 'Industries Page content Edit Successfully..!!')
            return redirect('showIndustries')
        else:
             for data in data:
                IndustriesSection(id=id, image=data.image, page_title=title_name, heading=heading, description=description).save()
                messages.success(request, 'Industries page content Edit Successfully..!!')
                return redirect('showIndustries') 

class DeleteIndustriesPageContent(View):
    def get(self, request, id):
        data = IndustriesSection.objects.get(id=id)
        data.delete()
        messages.success(request, 'Industries Page Content Delete Successfully..!!')
        return redirect('showIndustries')         


#########  How Page Views ##############  

class AddHowPageContent(View):
    def get(self, request):
        return render(request, 'dashboard/add_how_page_content.html')
    def post(self, request):
        data = HowSection()
        title_name = request.POST.get('title_name')
        description = request.POST.get('description')
        heading = request.POST.get('heading')
        flexible_set_up = request.POST.get('flexible_set_up')
        sub_heading = request.POST.get('sub_heading')

    
        data.page_title = title_name
        data.description = description
        data.heading = heading
        data.flexible_set_up = flexible_set_up
        data.sub_heading = sub_heading
        
        data.save()
        messages.success(request, 'How Section  Page  Content Add Successfully..!!')
        return redirect('showHowPageContent')

class ShowHowPageContent(View):
    def get(self, request):
        data = HowSection.objects.all()
        return render(request, 'dashboard/show_how_page_content.html', {'data':data})        

class EditHowPageContent(View):
    def get(self, request, id):
        data = HowSection.objects.get(id=id)
        return render(request, 'dashboard/edit_how_page_content.html', {'data':data})

    def post(self, request, id):
        data = HowSection.objects.filter(id=id)
   
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
        sub_heading = request.POST.get('sub_heading')
        
      
        HowSection(id=id,  page_title=title_name, description=description,  heading=heading, sub_heading = sub_heading  ).save()
        messages.success(request, 'How Section Page content Edit Successfully..!!')
        return redirect('showHowPageContent')
        

class DeleteHowPageContent(View):
    def get(self, request, id):
        data = HowSection.objects.get(id=id)
        data.delete()
        messages.success(request, 'How Section Page Content Delete Successfully..!!')
        return redirect('showHowPageContent')         



#########  Services Page Views ##############  

class AddNewServices(View):
    def get(self, request):
        return render(request, 'dashboard/add_how_page_content.html')
    def post(self, request):
        data = HowSection()
        title_name = request.POST.get('title_name')
        description = request.POST.get('description')
        heading = request.POST.get('heading')
        sub_heading = request.POST.get('sub_heading')

    
        data.page_title = title_name
        data.description = description
        data.heading = heading
        data.sub_heading = sub_heading
        
        data.save()
        messages.success(request, 'How Section  Page  Content Add Successfully..!!')
        return redirect('showHowPageContent')

class ShowHowPageContent(View):
    def get(self, request):
        data = HowSection.objects.all()
        return render(request, 'dashboard/show_how_page_content.html', {'data':data})        

class EditHowPageContent(View):
    def get(self, request, id):
        data = HowSection.objects.get(id=id)
        return render(request, 'dashboard/edit_how_page_content.html', {'data':data})

    def post(self, request, id):
        data = HowSection.objects.filter(id=id)
   
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
        sub_heading = request.POST.get('sub_heading')
        flexible_set_up = request.POST.get('flexible_set_up')
        
      
        HowSection(id=id,  page_title=title_name, description=description,  heading=heading, flexible_set_up=flexible_set_up, sub_heading = sub_heading  ).save()
        messages.success(request, 'How Section Page content Edit Successfully..!!')
        return redirect('showHowPageContent')
        

class DeleteHowPageContent(View):
    def get(self, request, id):
        data = HowSection.objects.get(id=id)
        data.delete()
        messages.success(request, 'How Section Page Content Delete Successfully..!!')
        return redirect('showHowPageContent')                 


class ShowContactInquiryLists(View):
    def get(self, request):
        data = ContactInquiry.objects.all()
        return render(request, 'dashboard/contact_inquiry_lists.html', {'data':data}) 

class DeleteContactInquiryForms(View):
    def get(self, request, id):
        data = ContactInquiry.objects.get(id=id)
        data.delete()
        messages.success(request, 'User Contact Inquiry Forms Delete Successfully..!!')
        return redirect('showContactLists')  

######## Contact Inquiry view ########

class AddCompanyAddress(View):
    def get(self, request):
        return render(request, 'dashboard/add_company_address.html')
    def post(self, request):
        data = GetInTouch()
        title_name = request.POST.get('title_name')
        address = request.POST.get('address')
        germany = request.POST.get('germany')
        Germany_office_address = request.POST.get('Germany_office_address')

        data.IPBrandsGmbH = title_name
        data.address = address
        data.GermanyOffice_title = germany
        data.GermanyOfficeAddress = Germany_office_address
        
        data.save()
        messages.success(request, 'Company Address Add Successfully..!!')
        return redirect('showCompanyAddress')

class ShowCompanyAddress(View):
    def get(self, request):
        data = GetInTouch.objects.all()
        return render(request, 'dashboard/show_company_address.html', {'data':data})        

class EditCompanyAddress(View):
    def get(self, request, id):
        data = GetInTouch.objects.get(id=id)
        return render(request, 'dashboard/edit_company_address.html', {'data':data})

    def post(self, request, id):
        data = GetInTouch.objects.filter(id=id)
   
        title_name = request.POST.get('title_name')
        address = request.POST.get('address')
        germany = request.POST.get('germany')
        Germany_office_address = request.POST.get('Germany_office_address')

        GetInTouch(id=id,  IPBrandsGmbH=title_name, address=address,  GermanyOffice_title=germany, GermanyOfficeAddress = Germany_office_address  ).save()
        messages.success(request, 'Company Address Edit Successfully..!!')
        return redirect('showCompanyAddress')
        

class DeleteCompanyAddress(View):
    def get(self, request, id):
        data = GetInTouch.objects.get(id=id)
        data.delete()
        messages.success(request, 'Company Address Delete Successfully..!!')
        return redirect('showCompanyAddress')         


class AddNewService(View):
    def get(self, request):
        return render(request, 'dashboard/add_new_services.html')

    def post(self, request):
        service_data = Services()
        service_name = request.POST.get('service_name')
        image = request.FILES.get('image')
        description = request.POST.get('description')

        service_data.service_name = service_name
        service_data.image = image
        service_data.description = description
        service_data.save()
        messages.success(request, 'New Service Add Successfully..!!')
        return redirect("showService")

class ShowServicesLists(View):
    def get(self, request):
        data = Services.objects.all()
        return render(request, 'dashboard/show_services_lists.html',{'data':data})            


class EditServices(View):
    def get(self, request, id):
        data = Services.objects.get(id=id)
        return render(request, 'dashboard/edit_services.html', {'data':data})
    
    def post(self, request, id):
        data = Services.objects.filter(id=id)
        service_name = request.POST.get('service_name')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        if image is not None:
            Services(id=id, service_name = service_name, image = image, description = description ).save()
            messages.success(request, 'Edit Service  Successfully..!!')
            return redirect("showService")
        else:
            for data in data:
                Services(id=id, service_name = service_name, image = data.image, description = description ).save()
                messages.success(request, 'Edit Service  Successfully..!!')
        return redirect("showService")

class DeleteServices(View):
    def get(self, request, id):
        data = Services.objects.get(id=id)
        data.delete()
        messages.success(request, 'Delete Service  Successfully..!!')
        return redirect("showService")

######### Services Sub Heading ###########

class ServiceSubHeading(View):
    def get(self, request, id):
        data = Services.objects.get(id=id)
        return render(request, 'dashboard/add_services_sub_heading.html', {'data':data})
    def post(self, request, id):
        data = AddServiceSubHeading()
        service_data = Services.objects.get(id=id)
        service_id = request.POST.get('service_id')
        sub_heading = request.POST.get('sub_heading')
        data.service = service_data
        data.sub_heading_name = sub_heading
        data.save()
        messages.success(request, 'Service Sub Heading Add Successfully..!!')
        return redirect('ServiceSubHeadingLists', id)

class ShowServiceSubHeadingLists(View):
    def get(self, request,id):
        service_id = Services.objects.get(id=id)
        data = AddServiceSubHeading.objects.filter(service=id)
        return render(request, 'dashboard/show_services_sub_headings_lists.html', {'data':data, 'service_id':service_id})        

class EditServiceSubheading(View):
    def get(self, request, id):
        data = AddServiceSubHeading.objects.get(id=id)

        return render(request, 'dashboard/edit_services_sub_heading.html', {'data':data})

    def post(self, request, id):
        data = AddServiceSubHeading.objects.filter(id=id)
        service_id = request.POST.get("service_id")
        sub_heading = request.POST.get('sub_heading')
        if service_id is None:
            for data in data:
                AddServiceSubHeading(id=id, service=data.service, sub_heading_name=sub_heading).save()
                messages.success(request, 'Service Sub Heading Edit Successfully..!!')
                return redirect('showService')
        else:
            messages.success(request, 'Service Sub Heading Not Edited..!!')
            return redirect('showService')

class DeleteServiceSubHeading(View):
    def get(self, request, id):
        data = AddServiceSubHeading.objects.get(id=id) 
        data.delete()
        messages.success(request, 'Service Sub Heading Delete Successfully..!!')
        return redirect('showService')    



#########  Why us Section Views ##############  

class AddWhyUsPageContent(View):
    def get(self, request):
        return render(request, 'dashboard/add_why_us_page_content.html')
    def post(self, request):
        data = WhyUsSection()
        image = request.FILES.get('image')
        title_name = request.POST.get('title_name')
 
    
        data.image = image
        data.page_title = title_name
        data.save()
        messages.success(request, 'New  Why Us Section Content Add Successfully..!!')
        return redirect('showWhyUsRecoardLists')

class ShowWhyUsPageContent(View):
    def get(self, request):
        data = WhyUsSection.objects.all()
        return render(request, 'dashboard/show_why_us_recoard_lists.html', {'data':data})        

class EditWhyUsPageContent(View):
    def get(self, request, id):
        data = WhyUsSection.objects.get(id=id)
        return render(request, 'dashboard/edit_why_us_section.html', {'data':data})

    def post(self, request, id):
        data = WhyUsSection.objects.filter(id=id)
        image = request.FILES.get('image')
        title_name = request.POST.get('page_title')

    
        if image is not None:
            WhyUsSection(id=id, image=image, page_title=title_name).save()
            messages.success(request, 'Why Us  Page content Edit Successfully..!!')
            return redirect('showWhyUsRecoardLists')
        else:
             for data in data:
                WhyUsSection(id=id, image=data.image, page_title=title_name).save()
                messages.success(request, 'Why Us page content Edit Successfully..!!')
                return redirect('showWhyUsRecoardLists') 

class DeleteWhyUsPageContent(View):
    def get(self, request, id):
        data = WhyUsSection.objects.get(id=id)
        data.delete()
        messages.success(request, 'Why Us  Page Content Delete Successfully..!!')
        return redirect('showWhyUsRecoardLists')   

#######   Why Us Page Sub Heading ###########

class AddWhyUsSubHeading(View):
    def get(self, request, id):
        data = WhyUsSection.objects.get(id=id)
        return render(request, 'dashboard/add_why_us_sub_heading.html', {'data':data})
    def post(self, request, id):
        data = AddWhyUsSectionSubHeading()
        why_us_data = WhyUsSection.objects.get(id=id)

        sub_heading = request.POST.get('sub_heading')
        data.whyus = why_us_data
        data.sub_heading_name = sub_heading
        data.save()
        messages.success(request, 'Why Us Page Sub Heading Add Successfully..!!')
        return redirect('ShowWhyUsSubHeading', id)

class ShowWhyUsSubHeadingLists(View):
    def get(self, request,id):
        why_us_id = WhyUsSection.objects.get(id=id)
        data = AddWhyUsSectionSubHeading.objects.filter(whyus=id)
        
        return render(request, 'dashboard/show_why_us_sub_heading_lists.html', {'data':data, 'service_id':why_us_id})        

class EditWhyUsSubheading(View):
    def get(self, request, id):
        data = AddWhyUsSectionSubHeading.objects.get(id=id)
        return render(request, 'dashboard/edit_why_us_sub_heading.html', {'data':data})

    def post(self, request, id):
        data = AddWhyUsSectionSubHeading.objects.filter(id=id)
        why_us_id = request.POST.get("why_us_id")
        sub_heading = request.POST.get('sub_heading')
        if why_us_id is None:
            for data in data:
                AddWhyUsSectionSubHeading(id=id, whyus=data.whyus, sub_heading_name=sub_heading).save()
                messages.success(request, 'Why Us  Sub Heading Edit Successfully..!!')
                return redirect('showWhyUsRecoardLists')
        else:
            messages.success(request, 'Why Us Sub Heading Not Edited..!!')
            return redirect('showWhyUsRecoardLists')

class DeleteWhyUsSubHeading(View):
    def get(self, request, id):
        data = AddWhyUsSectionSubHeading.objects.get(id=id) 
        data.delete()
        messages.success(request, 'Why Us  Sub Heading Delete Successfully..!!')
        return redirect('showWhyUsRecoardLists')    

#########   Reference Section Content ##########

class AddReferencePageContent(View):
    def get(self, request):
        return render(request, 'dashboard/add_reference_content.html') 

    def post(self, request):
            data = References()
            image = request.FILES.get('banner_image')
            resources_heading_name = request.POST.get('resource_heading')
            resources_description = request.POST.get('resource_description')
            user_image = request.FILES.get('user_image')
            user_name  = request.POST.get('user_name')
            user_designation  = request.POST.get('name_designation')
            user_description = request.POST.get('user_abouts')
            user_about_us = request.POST.get('description')

            data.image = image
            data.resources_heading_name = resources_heading_name
            data.resources_description = resources_description
            data.user_image = user_image
            data.user_name = user_name
            data.user_designation = user_designation
            data.user_description = user_description
            data.user_about_us = user_about_us
            data.save()
            messages.success(request, 'Reference Section content Add Successfully..!!')
            return redirect('ShowReferenceContent')
class EditReferenceContent(View):
    def get(self, request, id):
        data = References.objects.get(id=id)
        return render(request, 'dashboard/edit_reference_content.html', {'data':data})        

    def post(self, request, id):
            data = References.objects.filter(id=id)
            image = request.FILES.get('banner_image')
            resources_heading_name = request.POST.get('resource_heading')
            resources_description = request.POST.get('resource_description')
            user_image = request.FILES.get('user_image')
            user_name  = request.POST.get('user_name')
            user_designation  = request.POST.get('name_designation')
            user_description = request.POST.get('description')
            user_about_us = request.POST.get('user_abouts')    
            if image or user_image is  None:
                for ref_data in data:
                    References(id=id, image=ref_data.image, resources_heading_name=resources_heading_name, resources_description=resources_description, user_image=ref_data.user_image, user_name=user_name, user_designation=user_designation,user_description=user_description, user_about_us=user_about_us ).save()
                    messages.success(request, 'Reference Section content Edit Successfully..!!')
                    return redirect('ShowReferenceContent')
            elif image is None: 
                for data in data:
                    References(id=id, image=data.image, resources_heading_name=resources_heading_name, resources_description=resources_description, user_image=user_image, user_name=user_name, user_designation=user_designation,user_description=user_description, user_about_us=user_about_us ).save()  
                    messages.success(request, 'Reference Section content Edit Successfully..!!')
                    return redirect('ShowReferenceContent')
            elif user_image is None:         
                for data in data:
                    References(id=id, image=image, resources_heading_name=resources_heading_name, resources_description=resources_description, user_image=data.user_image, user_name=user_name, user_designation=user_designation,user_description=user_description, user_about_us=user_about_us ).save()  
                    messages.success(request, 'Reference Section content Edit Successfully..!!')
                    return redirect('ShowReferenceContent')
            else:
                References(id=id, image=image, resources_heading_name=resources_heading_name, resources_description=resources_description, user_image=user_image, user_name=user_name, user_designation=user_designation,user_description=user_description, user_about_us=user_about_us ).save()                                
                messages.success(request, 'Reference Section content Edit Successfully..!!')
                return redirect('ShowReferenceContent')
class ShowReferencePageContent(View):
    def get(self, request):
        data = References.objects.all()
        return render(request, 'dashboard/show_reference_content.html', {'data':data})      

class DeleteReferencePageContent(View):
    def get(self, request, id):
        data = References.objects.get(id=id)
        data.delete()
        messages.success(request, 'Reference Section content Delete Successfully..!!')
        return redirect('ShowReferenceContent')             

######## Management Projects Overview #########

class ManagementProjectsOverview(View):
    def get(self, request):
        ManagementProjects.objects.all()
        return render(request, 'dashboard/add_project_overview.html')
    def post(self, request):
        data = ManagementProjects()
        image_first = request.FILES.get('image_first')
        image_second = request.FILES.get('image_second')
        image_third = request.FILES.get('image_third')
        image_fourth = request.FILES.get('image_fourth')
        year_durations = request.POST.get('year_durations')
        description_first = request.POST.get('description_first')
        description_second = request.POST.get('description_second')
        description_third = request.POST.get('description_third')
        description_fourth = request.POST.get('description_fourth')
        data.image_first = image_first
        data.image_second = image_second
        data.image_third = image_third
        data.image_fourth = image_fourth
        data.description_first = description_first
        data.description_second = description_second
        data.description_third = description_third
        data.description_fourth = description_fourth
        data.year_durations = year_durations
        data.save()
        messages.success(request, 'Project Overview  Content Add Successfully..!!')
        return redirect('ShowProjectOverviewContent')  

class ShowProjectsOverviewLists(View):
    def get(self, request):
        project_overview = ManagementProjects.objects.all()
        return render(request, 'dashboard/show_project_overview_lists.html', {'data':project_overview})

class EditProjectsOverview(View):
    def get(self, request, id):
        data = ManagementProjects.objects.get(id=id)
        return render(request, 'dashboard/edit_project_overview.html', {'data':data})
    def post(self, request, id):
        data = ManagementProjects.objects.filter(id=id)
        image_first = request.FILES.get('image_first')
        image_second = request.FILES.get('image_second')
        image_third = request.FILES.get('image_third')
        image_fourth = request.FILES.get('image_fourth')
        year_durations = request.POST.get('year_durations')
        description_first = request.POST.get('description_first')
        description_second = request.POST.get('description_second')
        description_third = request.POST.get('description_third')
        description_fourth = request.POST.get('description_fourth')
        if image_first or image_second or image_third or image_fourth is not None:
            for data in data:
                ManagementProjects(id=id,image_first=data.image_first, image_second=data.image_second, image_third=data.image_third, image_fourth=data.image_fourth, year_durations=year_durations, description_first=description_first, description_second=description_second, description_third=description_third, description_fourth=description_fourth  ).save()
                messages.success(request, 'Project Overview  Content Edit Successfully..!!')
                return redirect('ShowProjectOverviewContent') 
        elif image_first is None:
            for data in data:
                ManagementProjects(id=id,image_first=data.image_first, image_second=image_second, image_third=image_third, image_fourth=image_fourth, year_durations=year_durations, description_first=description_first, description_second=description_second, description_third=description_third, description_fourth=description_fourth).save()
                messages.success(request, 'Project Overview  Content Edit Successfully..!!')
                return redirect('ShowProjectOverviewContent') 
        elif image_second is None:
            for data in data:
                ManagementProjects(id=id,image_first=image_first, image_second=data.image_second, image_third=image_third, image_fourth=image_fourth, year_durations=year_durations, description_first=description_first, description_second=description_second, description_third=description_third, description_fourth=description_fourth).save()
                messages.success(request, 'Project Overview  Content Edit Successfully..!!')
                return redirect('ShowProjectOverviewContent') 
        elif image_third is None:
            for data in data:
                ManagementProjects(id=id,image_first=image_first, image_second=image_second, image_third=data.image_third, image_fourth=image_fourth, year_durations=year_durations, description_first=description_first, description_second=description_second, description_third=description_third, description_fourth=description_fourth).save()
                messages.success(request, 'Project Overview  Content Edit Successfully..!!')
                return redirect('ShowProjectOverviewContent') 
        
        elif image_fourth is None:
            for data in data:
                ManagementProjects(id=id,image_first=image_first, image_second=image_second, image_third=data.image_third, image_fourth=data.image_fourth, year_durations=year_durations, description_first=description_first, description_second=description_second, description_third=description_third, description_fourth=description_fourth).save()
                messages.success(request, 'Project Overview  Content Edit Successfully..!!')
                return redirect('ShowProjectOverviewContent') 
        else:
            ManagementProjects(id=id,image_first=image_first, image_second=image_second, image_third=image_third, image_fourth=data.image_fourth, year_durations=year_durations, description_first=description_first, description_second=description_second, description_third=description_third, description_fourth=description_fourth  ).save()
            messages.success(request, 'Project Overview  Content Edit Successfully..!!')
            return redirect('ShowProjectOverviewContent') 
class DeleteProjectOverview(View):
    def get(self, request, id):
        ManagementProjects.objects.get(id=id).delete()
        messages.success(request, 'Project Overview  Content Delete Successfully..!!')
        return redirect('ShowProjectOverviewContent') 

########  U S P Section View ############
class AddUspPageContent(View):
    def get(self, request):
        return render(request, 'dashboard/add_usp_section_content.html')
    def post(self, request):
        data = UspSection()
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
    
        data.image = image
        data.page_title = title_name
        data.heading = heading
        data.description = description
        data.save()
        messages.success(request, 'UspSection  Page  Content Add Successfully..!!')
        return redirect('ShowUspContent')

class ShowUspSectioneContent(View):
    def get(self, request):
        data = UspSection.objects.all()
        return render(request, 'dashboard/show_usp_section_content.html', {'data':data})        

class EditUspSectionContent(View):
    def get(self, request, id):
        data = UspSection.objects.get(id=id)
        return render(request, 'dashboard/edit_usp_section.html', {'data':data})

    def post(self, request, id):
        data = UspSection.objects.filter(id=id)
        image = request.FILES.get('banner_image')
        title_name = request.POST.get('title_name')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
    
        if image is not None:
            UspSection(id=id, image=image, page_title=title_name, heading=heading, description=description).save()
            messages.success(request, 'UspSection Page content Edit Successfully..!!')
            return redirect('ShowUspContent')
        else:
             for data in data:
                UspSection(id=id, image=data.image, page_title=title_name, heading=heading, description=description).save()
                messages.success(request, 'UspSection page content Edit Successfully..!!')
                return redirect('ShowUspContent') 

class DeleteUspSectionContent(View):
    def get(self, request, id):
        data = UspSection.objects.get(id=id)
        data.delete()
        messages.success(request, 'UspSection Page Content Delete Successfully..!!')
        return redirect('ShowUspContent')   

########## Usp Sub Heading View #######     

class AddUspSubHeading(View):
    def get(self, request, id):
        data = UspSection.objects.get(id=id)
        return render(request, 'dashboard/add_usp_section_sub_heading.html', {'data':data})
    def post(self, request, id):
        data = UspSectionSubHeading()
        usp_data = UspSection.objects.get(id=id)

        sub_heading = request.POST.get('sub_heading')
        data.ups = usp_data
        data.sub_heading_name = sub_heading
        data.save()
        messages.success(request, 'Usp Section Sub Heading Add Successfully..!!')
        return redirect('ShowUspSubHeadingContent', id)

class ShowUspSubHeadingLists(View):
    def get(self, request,id):
        usp_id = UspSection.objects.get(id=id)
        data = UspSectionSubHeading.objects.filter(ups=id)
        
        return render(request, 'dashboard/show_usp_sub_heading_lists.html', {'data':data, 'service_id':usp_id})        

class EditUspSubheading(View):
    def get(self, request, id):
        data = UspSectionSubHeading.objects.get(id=id)
        return render(request, 'dashboard/edit_usp_sub_heading.html', {'data':data})

    def post(self, request, id):
        data = UspSectionSubHeading.objects.filter(id=id)
        usp_id = request.POST.get("why_us_id")
        sub_heading = request.POST.get('sub_heading')
        if usp_id is None:
            for data in data:
                UspSectionSubHeading(id=id, ups=data.ups, sub_heading_name=sub_heading).save()
                messages.success(request, 'Usp Sub Heading Edit Successfully..!!')
                return redirect('ShowUspContent')
        else:
            messages.success(request, 'Usp Sub Heading Not Edited..!!')
            return redirect('ShowUspContent')

class DeleteUspSubHeading(View):
    def get(self, request, id):
        data = UspSectionSubHeading.objects.get(id=id) 
        data.delete()
        messages.success(request, ' Usp  Sub Heading Delete Successfully..!!')
        return redirect('ShowUspContent')    