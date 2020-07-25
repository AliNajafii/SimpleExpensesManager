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

    path('<str:account_name>/transactions/<int:transaction_id>',
    account_views.TransactionView.as_view(),
    name='transaction-detail'
    ),

    path('<str:account_name>/transactions/create',
    account_views.TransactionCreateView.as_view(),
    name='transaction-create'
    ),

    path('<str:account_name>/transactions/update',
    account_views.TransactionUpdateView.as_view(),
    name='transaction-update'
    ),

    path('<str:account_name>/transactions/create',
    account_views.TransactionDeleteView.as_view(),
    name='transaction-delete'
    ),

    path('tag/',
    include('account.tag_urls')
    ),

    path('category/',
    include('account.cat_urls'),
    ),



]
