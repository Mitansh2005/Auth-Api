from .models import CustomUser
from rest_framework import serializers
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from .utils import Util

class UserRegisterationSerializer(serializers.ModelSerializer):
  password2=serializers.CharField(style={'input_type':'password'},write_only=True)
  class Meta:
    model=CustomUser
    fields=['email','name','password','password2','tc']
    extra_kwargs={
      'password':{'write_only':True}
    }
  def validate(self, data):
    password=data.get('password')
    password2=data.get('password2')
    if password !=password2:
      raise serializers.ValidationError('Password and Confirm Password does not match')

    return data
  
  def create(self, validated_data):
   return CustomUser.objects.create_user(**validated_data)

class CustomUserLoginSerializer(serializers.ModelSerializer):
  email=serializers.EmailField(max_length=255)
  class Meta:
    model=CustomUser
    fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model=CustomUser
    fields=['id','email','name']

class UserChangePasswordSerializer(serializers.Serializer):
  password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
  password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
  class Meta:
    fields=['password','password2']
  def validate(self,data):
    user=self.context.get('user')
    password=data.get('password')
    password2=data.get('password2')
    if password !=password2:
     raise serializers.ValidationError('Password and Confirm Password does not match')
    user.set_password(password)
    user.save()
    return data
  
class UserChangePasswordEmailSerializer(serializers.Serializer):
  email=serializers.EmailField(max_length=255)
  class Meta:
    field=['email']

  def validate(self,data):
    email=data.get('email')
    if CustomUser.objects.filter(email=email).exists():
      user=CustomUser.objects.get(email=email)
      uid= urlsafe_base64_encode(force_bytes(user.id))
      token=PasswordResetTokenGenerator().make_token(user)
      link="http://localhost:3000/api/user/reset/"+uid+"/"+token
      print("uid"+uid)
      print('token:'+token)
      print('link:'+link)
      # body="Reset your password by clicking the below mentioned link "+ link
      # data={
      #   "subject":"Reset your password",
      #   "body":body,
      #   "to_email":user.email,
      # }
      # Util.send_email(data)
      return data
    else:
      raise serializers.ValidationError('You are not a registered User')
    
# class UserPasswordResetSerializer(serializers.Serializer):
#   password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
#   password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
#   class Meta:
#     fields=['password','password2']
#   def validate(self,data):
#     try:
#       password=data.get('password')
#       password2=data.get('password2')
#       uid=self.context.get('uid')
#       token=self.context.get('token')
#       if password !=password2:
#        raise serializers.ValidationError('Password and Confirm Password does not match')
#       id=smart_str(urlsafe_base64_decode(uid))
#       user=CustomUser.objects.get(id=id)
#       if not PasswordResetTokenGenerator().check_token(user,token):
#         raise serializers.ValidationError('Token is not Valid or Expired')
#       user.set_password(password)
#       user.save()
#       return data
#     except DjangoUnicodeDecodeError as identifier:
#       PasswordResetTokenGenerator().check_token(user,token)
#       raise serializers.ValidationError('Token is not Valid or Expired')
