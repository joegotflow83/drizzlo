from final_project.celery import app
import requests
import uuid
from twilio.rest import TwilioRestClient
from django.contrib.auth.models import User

from .models import ActivateKey
from cookbook.models import Recipe


# Email Verify Send Function
def send_verify_mail(pk):
    user = User.objects.get(pk=pk)
    new_key = ActivateKey(user=user, key=uuid.uuid4())
    new_key.save()
    activation = ActivateKey.objects.get(pk=new_key.pk)
    return requests.post(
        "https://api.mailgun.net/v3/sandbox4ad1b1d33eab43bfa034ce1dd326c25f.mailgun.org/messages",
        auth=("api", "key-cb25e64ad0416c9fe40189d8cc420e3a"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox4ad1b1d33eab43bfa034ce1dd326c25f.mailgun.org>",
              "to": "{} <{}>".format(user.username, user.email),
              "subject": "Hello {}".format(user.username),
              "text": """Welcome {}! To verify your account please enter the key below to be able to log in to your account.
                      We hope you enjoy our product and site.
                      Key: {}
                      The Joegotflow Product Team""".format(user.username, activation.key)})


# Email Recipe Function
def send_recipe_mail(recipe_pk, user_pk, creator, ingredients, instructions):
    recipe = Recipe.objects.get(pk=recipe_pk)
    user = User.objects.get(pk=user_pk)
    return requests.post(
        "https://api.mailgun.net/v3/sandbox4ad1b1d33eab43bfa034ce1dd326c25f.mailgun.org/messages",
        auth=("api", "key-cb25e64ad0416c9fe40189d8cc420e3a"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox4ad1b1d33eab43bfa034ce1dd326c25f.mailgun.org>",
              "to": "{} <{}>".format(user.username, user.email),
              "subject": "Recipe: {}".format(recipe.title),
              "text": """Name: {}
                      Created By: {}
                      Type: {}
                      Prep Time: {}
                      Cook Time: {}
                      Ingredients: {}

                      Instructions: {}""".format(recipe.title, creator, recipe.tags, recipe.prep_time, recipe.cook_time,
                                                 ingredients, instructions)})


# SMS Send Function
def sms(shoppinglist, number):
    account_sid = "ACfced82b13f94fceb03015f0fb54ecc82"
    auth_token = "59a55a9b816da5118b7ced398790ffd2"
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body="Your shopping list is {}".format(shoppinglist),
                                     to="+1{}".format(number),
                                     from_="+17573356907"),
    return message


@app.task
def send_verify_email(pk):
    print('I sent the email!')
    return send_verify_mail(pk)


@app.task
def send_recipe_email(recipe_pk, user_pk, creator, ingredients, instructions):
    print('I send the email!')
    return send_recipe_mail(recipe_pk, user_pk, creator, ingredients, instructions)


@app.task
def send_sms(shoppinglist,  number):
    print('I sent the sms!')
    return sms(shoppinglist, number)
