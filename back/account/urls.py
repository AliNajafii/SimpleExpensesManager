from django.urls import path,include
from . import account_views
urlpatterns = [

    path('<str:account_name>/',
    account_views.AccountProfileView.as_view(),
    name='account-profile'
     ),

    path('<str:account_name>/update',
    account_views.AccountUpdateView.as_view(),
    name='account-update'
    ),

    path('<str:account_name>/delete',
    account_views.AccountDeleteView.as_view(),
    name='account-delete'
    ),

    path('list',
    account_views.UserAccountListView.as_view(),
    name='account-list'
    ),

    path('create',
    account_views.AccountCreateView.as_view(),
    name='account-create'
    ),

    path('<str:account_name>/transactions',
    account_views.TransactionListView.as_view(),
    name='transaction-list'
    ),

    path('tag/',
    include('account.tag_urls')
    ),

    path('category/',
    include('account.cat_urls'),
    ),



]
