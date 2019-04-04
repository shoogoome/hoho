from server.account.models import Account
import requests
from faker import Faker

fake = Faker(locale='zh_CN')

for i in range(100):
    p = fake.profile()
    Account.objects.create(
        nickname=p.get('username'),
        realname=p.get('username'),
        temp_access_token=i
    )

    s = requests.session()
    s.post("hoho.server.net/accounts/register/this/is/jiekou/useing/to/kaifa", data={
        "token": i
    })

    s.get("hoho.server.net/schools/1/associations/1/apply?debug=1&choosing_code=20535904")
