
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView as RetrieveAPIView

from ..models import CustomUser as User, UserWallet
from ..serializers import UserWalletSerializer

class UserWalletDashboardAPIView(RetrieveAPIView):
    queryset = UserWallet.objects.all()
    serializer_class = UserWalletSerializer
    lookup_field = "user_id"

    def get_object(self):
        try:
            return UserWallet.objects.get(user_id=self.request.user.id)
        except UserWallet.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        selected_wallet = self.get_object()
        if selected_wallet is None:
            return Response(
                {"message": "This wallet does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UserWalletSerializer(selected_wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)