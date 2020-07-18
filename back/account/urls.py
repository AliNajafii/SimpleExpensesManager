from django.urls import path,include
from . import account_views
urlpatterns = [

    path('<str:username>/<str:account_name>',
    account_views.AccountProfileView.as_view(),
    name='account_profile'
     ),

    path('<str:username>/<str:account_name>/update',
    account_views.AccountUpdateView.as_view(),
    name='account_update'
    ),

    path('<str:username>/account/lists',
    account_views.AccountListView.as_view(),
    name='account_lists'
    ),

    path('<str:username>/<str:account_name>/transactions',
    account_views.AccountListView.as_view(),
    name='transaction_list'
    ),

    # path('<str:username>/<str:account_name>/tag',
    # include('account.tag_urls')
    # ),
    #
    # path('<str:username>/<str:account_name>/<str:cat_name>',
    # include('account.cat_urls'),
    # name='category_detail'

    # ),

    # path('<str:username>/<str:account_name>/categorys',
    # include('account.cat_urls'),
    # name='category_list'
    #
    # ),


]
