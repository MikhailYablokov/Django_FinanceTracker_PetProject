from apps.transaction.services import get_or_create_balances

def balances_context(request):
    if request.user.is_authenticated:
        balances = get_or_create_balances(request.user)
        return {'balances': balances.values()}
    return {'balances': []}