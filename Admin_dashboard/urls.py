from django import views
from django.urls import path
from . import views



urlpatterns = [
    
    path('admin-dashboard/', views.IndexPageDashboard.as_view(), name="homePageDashboard"),
    path('admin-login/', views.login , name="adminLogin"),
    path('user-logout/', views.userlogout, name ='logouts'),
    path('user-details/', views.ShowUserView.as_view(), name ='showUser'),
    path('user-profile/', views.AdminProfile.as_view(), name ='profile'),
    path('add-new-user/', views.AddNewUserView.as_view(), name ='addUser'),
    path("delete-user/<int:id>", views.UserDeleteView.as_view(), name="deleteUser" ),
    path('update-user-profile/<int:id>', views.UpdateUserProfileView.as_view(), name="editUser"),
    path("admin-forget-password/",views.forgetPassword, name='forgetPassword'),
    path('add-new-banner/', views.AddHomeBanner.as_view(), name="addBanner" ),
    path('show-banner-lists/', views.ShowBannerView.as_view(), name="bannerLists"),
    path('banner-delete/<int:id>/', views.DeleteBanner.as_view(), name="bannerDelete"),
    path('edit-banner/<int:id>', views.EditBanner.as_view(), name="Editbanner"),
    path('add-new-about-us-page-content/', views.AboutsPage.as_view(), name="addAbouts" ),
    path('show-about-us-page-content/', views.ShowAboutUsPageContent.as_view(), name="about_page_content"),
    path('edit-about-us-page/<int:id>', views.EditAboutPageContent.as_view(), name="EditAboutsPage"),
    path('delete-about_page/<int:id>/', views.DeleteAboutPageContent.as_view(), name="AboutDelete"),
    path('add-scope-page-content/', views.AddScopePage.as_view(), name="addScope" ),
    path('show-scope-page-content/', views.ShowScopePageContent.as_view(), name="showScope" ),
    path('edit-scope-page/<int:id>', views.EditScopePageContent.as_view(), name="EditscopePage"),
    path('delete-scope-page/<int:id>/', views.DeleteScopePageContent.as_view(), name="scopeDelete"),
    path('add-where-page-content/', views.AddWherePageContent.as_view(), name="addWhere" ),
    path('show-where-page-content/', views.ShowWherePageContent.as_view(), name="showWhere" ),
    path('edit-where-page/<int:id>', views.EditWherePageContent.as_view(), name="EditWherePage"),
    path('delete-where-page/<int:id>/', views.DeleteWherePageContent.as_view(), name="WhereDelete"),
    
    path('add-geographical-page-content/', views.AddGeographicalPageContent.as_view(), name="addGeographical" ),
    path('show-geographical-page-content/', views.ShowGeographicalPageContent.as_view(), name="showGeographical" ),
    path('edit-geographical-page/<int:id>', views.EditGeographicalPageContent.as_view(), name="EditGeographicalPage"),
    path('delete-geographical-page/<int:id>/', views.DeleteGeographicalPageContent.as_view(), name="GeographicalDelete"),

    path('add-industries-page-content/', views.AddIndustriesPageContent.as_view(), name="addIndustries" ),
    path('show-industries-page-content/', views.ShowIndustriesPageContent.as_view(), name="showIndustries" ),
    path('edit-industries-page/<int:id>', views.EditIndustriesPageContent.as_view(), name="EditIndustries"),
    path('delete-industries-page/<int:id>/', views.DeleteIndustriesPageContent.as_view(), name="industriesDelete"),

    path('add-how-page-content/', views.AddHowPageContent.as_view(), name="addHowPageContent" ),
    path('show-how-page-content/', views.ShowHowPageContent.as_view(), name="showHowPageContent" ),
    path('edit-how-page/<int:id>', views.EditHowPageContent.as_view(), name="EditHowPageContent"),
    path('delete-how-page/<int:id>/', views.DeleteHowPageContent.as_view(), name="HowPageContentDelete"),

    path('show-contact-inquiry-forms-lists/', views.ShowContactInquiryLists.as_view(), name="showContactLists" ),
    path('delete-contact-inquiry-forms/<int:id>/', views.DeleteContactInquiryForms.as_view(), name="DeleteInquiryForms"),

    path('add-company-address/', views.AddCompanyAddress.as_view(), name="addCompanyAddress" ),
    path('show-company-address/', views.ShowCompanyAddress.as_view(), name="showCompanyAddress" ),
    path('edit-company-address/<int:id>', views.EditCompanyAddress.as_view(), name="editCompanyAddress"),
    path('delete-company-address/<int:id>/', views.DeleteCompanyAddress.as_view(), name="DeleteCompanyAddress"),


    path('add-new-services/', views.AddNewService.as_view(), name="addService"),
    path('show-services-lists/', views.ShowServicesLists.as_view(), name="showService"),
    path('edit-service/<int:id>', views.EditServices.as_view(), name="editService"),
    path('delete-services/<int:id>', views.DeleteServices.as_view(), name="deleteServies"),

    path('add-service-sub-heading/<int:id>', views.ServiceSubHeading.as_view(), name="AddServiceSubHeading" ),
    path('show-services-sub-heading-lists/<int:id>', views.ShowServiceSubHeadingLists.as_view(), name="ServiceSubHeadingLists"),
    path('edit-services-sub-heading/<int:id>', views.EditServiceSubheading.as_view(), name="EditServiceSubHeadingLists"),
    path('delete-service-sub-heading/<int:id>', views.DeleteServiceSubHeading.as_view(), name="DeleteServiceSubHeading"),


    path('add-why-us-section-content/', views.AddWhyUsPageContent.as_view(), name="addWhyUsContent" ),
    path('show-why-us-recoard-lists/', views.ShowWhyUsPageContent.as_view(), name="showWhyUsRecoardLists" ),
    path('edit-why-us-section/<int:id>', views.EditWhyUsPageContent.as_view(), name="editWhyUsSection"),
    path('delete-why-us-page-content/<int:id>/', views.DeleteWhyUsPageContent.as_view(), name="DeleteWhyUsPage"),

    path('add-why-us-sub-heading/<int:id>', views.AddWhyUsSubHeading.as_view(), name="AddWhyUsSubHeading" ),
    path('show-why-us-sub-heading-lists/<int:id>', views.ShowWhyUsSubHeadingLists.as_view(), name="ShowWhyUsSubHeading"),
    path('edit-why-us-sub-heading/<int:id>', views.EditWhyUsSubheading.as_view(), name="EditWhyUsSubHeadingLists"),
    path('delete-why-us-sub-heading/<int:id>', views.DeleteWhyUsSubHeading.as_view(), name="DeleteWhyUsSubHeading"),
    
    path('add-reference-page-content', views.AddReferencePageContent.as_view(), name="AddReferencePageContent"),
    path('show-reference-page-content', views.ShowReferencePageContent.as_view(), name="ShowReferenceContent"),
    path('edit-reference-page-content/<int:id>', views.EditReferenceContent.as_view(), name="EditReferenceContent"),
    path('delete-reference-content/<int:id>', views.DeleteReferencePageContent.as_view(), name="DeleteReferenceContent"),

    path('add-usp-section-content', views.AddUspPageContent.as_view(), name="AddUspPageContent"),
    path('show-usp-section-content', views.ShowUspSectioneContent.as_view(), name="ShowUspContent"),
    path('edit-usp-section-content/<int:id>', views.EditUspSectionContent.as_view(), name="EditUspContent"),
    path('delete-usp-content/<int:id>', views.DeleteUspSectionContent.as_view(), name="DeleteUspContent"),

    path('add-usp-sub-heading-section-content/<int:id>', views.AddUspSubHeading.as_view(), name="AddUspSubHeading"),
    path('show-usp-sub-heading-section-content/<int:id>', views.ShowUspSubHeadingLists.as_view(), name="ShowUspSubHeadingContent"),
    path('edit-usp-sub-heading-section-content/<int:id>', views.EditUspSubheading.as_view(), name="EditUspSubHeadingContent"),
    path('delete-usp-sub-heading-content/<int:id>', views.DeleteUspSubHeading.as_view(), name="DeleteUspSubHeadingContent"),

    path('add-project-overview-page-content', views.ManagementProjectsOverview.as_view(), name="AddProjectOverviewContent"),
    path('show-project-overview-page-content-lists', views.ShowProjectsOverviewLists.as_view(), name="ShowProjectOverviewContent"),
    path('edit-project-overview/<int:id>', views.EditProjectsOverview.as_view(), name="editProjectOverview"),
    path('delete-project-overview/<int:id>', views.DeleteProjectOverview.as_view(), name="DeleteProjectOverview")


   
    
]