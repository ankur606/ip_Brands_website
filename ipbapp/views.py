from django.shortcuts import render
from django.views import View
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.
class HomePageView(View):
    def get(self, request):
        context = {}
        service_id_get  = request.GET.get('service_id')
        print(service_id_get)
  
        if service_id_get is not None:
            service_sub_headinhg = AddServiceSubHeading.objects.filter(service=service_id_get)

        elif service_id_get is  None:
            service_ids = Services.objects.filter().first()
            service_sub_headinhg = AddServiceSubHeading.objects.filter(service=service_ids.id)
    
        company_address = GetInTouch.objects.all()
        banner = HomeBanner.objects.all()
        about_section = AboutUsPage.objects.all()
        scope_section = ScopePage.objects.all()
        where_section = WherePage.objects.all()
        geographic_section = GeographicalModel.objects.all()
        industries_section = IndustriesSection.objects.all()
        how_section = HowSection.objects.all()
        whyusSection = WhyUsSection.objects.all()
        whyusSections = WhyUsSection.objects.all().first()
        why_us_instance = WhyUsSection.objects.get(id=whyusSections.id)
        why_us_heading = AddWhyUsSectionSubHeading.objects.filter(whyus=why_us_instance.id)
        references_section = References.objects.all()
        service = Services.objects.all() 

        project_overview_1995_1999 = ManagementProjects.objects.get(year_durations="1995-1999")
        project_overview_2000_2005 = ManagementProjects.objects.get(year_durations="2000-2005")
        project_overview_2006_2010 = ManagementProjects.objects.get(year_durations="2006-2010")
        project_overview_2011_2014 = ManagementProjects.objects.get(year_durations="2011-2014")
        project_overview_2015_2019 = ManagementProjects.objects.get(year_durations="2015-2019")
        project_overview_2020_2022 = ManagementProjects.objects.get(year_durations="2020-2022")

        
        usp_section = UspSection.objects.all().first()
        usp_section_heading = UspSectionSubHeading.objects.filter(ups=usp_section.id)
        context = {"company_address": company_address,
                   'banner': banner,
                   'about':about_section,
                   'scope':scope_section,
                   'where':where_section,
                   'geographic':geographic_section,
                   'industries':industries_section,
                   'how':how_section,
                   'WhyUs':whyusSection,
                   'why_us_heading':why_us_heading,
                   'references':references_section,
                   'service':service,
         
                   'service_sub_headinhg':service_sub_headinhg,
                   'usp':usp_section,
                   'usp_heading':usp_section_heading,
                   '1995_1999':project_overview_1995_1999,
                   '2000_2005':project_overview_2000_2005,
                   '2006_2010':project_overview_2006_2010,
                   '2011_2014':project_overview_2011_2014,
                   '2011_2014':project_overview_2011_2014,
                   '2015_2019':project_overview_2015_2019,
                   '2020_2022':project_overview_2020_2022,
                   }
                    
        return render(request, 'website/index.html', context)

    def post(self, request):
        data = ContactInquiry()
        name = request.POST.get('full_name')
        email = request.POST.get("email")
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        data.full_name = name
        data.email = email
        data.subject = subject
        data.message = message
        data.save()
        success = 'User Inquiry Forms Submit Successfully...!!'
        return HttpResponse(success)
