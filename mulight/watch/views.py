from collections import Counter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from watch.models import Watch


@api_view(['POST'])
def do_checkout(request):
    """Take a list of watch ids and return total price.
    """
    counter = Counter([int(ele.lstrip('0')) for ele in request.data])
    total_price = 0
    for k, quantity in counter.items():
        if not Watch.objects.filter(id=k).exists():
            # Specific id should not be returned for security reason.
            return Response({'err_msg': 'watch id does not exist'})

        # Calculate price for current watch and add the result to total.
        curr_watch = Watch.objects.get(id=k)
        price = curr_watch.price
        tmp_total = 0
        base = curr_watch.discount_base
        if base:
            tmp_total += curr_watch.discount_amount * (quantity // base)
            tmp_total += price * (quantity % base)
        else:
            tmp_total += price * quantity

        total_price += tmp_total

    return Response({'price': total_price})
