"""Quickstart example."""

from time import sleep

from supersetapiclient import SupersetClient

client = SupersetClient(
    host="http://localhost:8088",
    username="admin",
    password="admin",
)

guest_token = client.guest_token(uuid="15700569-4271-4294-93b9-cbda6bdae021")
print(guest_token)

sleep(30)

guest_token = client.guest_token(uuid="15700569-4271-4294-93b9-cbda6bdae021")
print(guest_token)


sleep(30)

guest_token = client.guest_token(uuid="15700569-4271-4294-93b9-cbda6bdae021")
print(guest_token)

sleep(30)

guest_token = client.guest_token(uuid="15700569-4271-4294-93b9-cbda6bdae021")
print(guest_token)

sleep(60 * 2)

guest_token = client.guest_token(uuid="15700569-4271-4294-93b9-cbda6bdae021")
print(guest_token)
