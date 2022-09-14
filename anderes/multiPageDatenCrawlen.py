from urllib.request import Request, urlopen
from urllib.parse import urlencode

url='https://www.google.com/search?'

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Cookie' :'CONSENT=YES+srp.gws-20220509-0-RC1.zh-CN+FX+340; HSID=Ah2820kyYT3ddtjUs; SSID=ALHR8bCMC0cPARCH1; APISID=TWzENw-H9VE8XtoM/A0r13wz98VBddqj3D; SAPISID=feqruknNjL-CVSOa/Ao4AG5qpwB_62R5IY; __Secure-1PAPISID=feqruknNjL-CVSOa/Ao4AG5qpwB_62R5IY; __Secure-3PAPISID=feqruknNjL-CVSOa/Ao4AG5qpwB_62R5IY; S=billing-ui-v3=lIe_bEhIWlEU2kSUATuJFox7Q_NaFUq0:billing-ui-v3-efe=lIe_bEhIWlEU2kSUATuJFox7Q_NaFUq0; OTZ=6593137_48_52_123900_48_436380; SEARCH_SAMESITE=CgQI-JUB; SID=MQjDydNE18LciDTOP7IxE09qc9q5JyuH_nhEqkVa56uSru0ag5SJeD6m_507SP8RD2oPYw.; __Secure-1PSID=MQjDydNE18LciDTOP7IxE09qc9q5JyuH_nhEqkVa56uSru0a0TwAfZfOuboc4D02HP6Kpw.; __Secure-3PSID=MQjDydNE18LciDTOP7IxE09qc9q5JyuH_nhEqkVa56uSru0a1PSPEXPjT7xmd20uXKFsbg.; OGPC=19022552-1:; AEC=AakniGPmywQycKcxeRlWvnFx7FHfOP4QFXaFbcYLbNhBvA5qntgS8Rv-uZA; NID=511=B_kWSdC6jtTwxwb1o4KWz987uJ5y3C3jMoJCyAoGFkHw-mEvlyYNplCD7RUNU_guN8oj56kz9_6HXKErTknD2FnrrQqKgsZ6FVjYspme-6IlFFTe4IrsjtjZxBaEYGnEEPrNBz5-Z5KpotwIfsIfIaaU-V9KccO6Okl8cSZDbs8fi7ikcI2G5x-4JsotnMD0vI3XNk9se0yAKZtQYYi3TK2EgeTFGWUZa4U2SfDzBhCGKcW31MEoFYun2AUOLFwdqSVVEKtG-rOInwt7d_K4wptSpjYQcDCK4FyAlUb21xJXvtY4v-GVeU9SFr9zchOM9I83CP1C7usP0JhCDgWrIqHrjwF9R5_YT8y8wG8rSqHoUjtcW74czInU0iVsK46AKRrQo3WgPFzGL35Pz7x7xYso4AfZfmjgs0NHuYZPJHQ; 1P_JAR=2022-08-12-21; DV=g-2ffUFBHa1V4NEdj8dT9Xj6q0c_KRgb7zvUO_7MSAAAACAcuD9TMkTrcAAAAICIXxvmwpdnMwAAAHxNtg6drFzxFwAAAA; SIDCC=AEf-XMRoFdG-IGlQQEy5f492pU3jKKgCVZQ0ayI8YzsoRyhuXBvM5wWGe2t3ZTCuMAdzMorccno; __Secure-1PSIDCC=AEf-XMQE8xeeRXG1cR-Pp9tnxf0BEo799mdLD1YosnNmzH7CcsGI216rOMgysBOt67eqXW2fIkQ; __Secure-3PSIDCC=AEf-XMRfhn9ahMjAN6ngYpGoMT9CtDfD9JqaKLQTX9DqcI3nJ66P5u7oAQBhlffPY1HeI8KdhyQ'
}
params = {
    'q' : '',
    'start' : 0 #0, 10, 20,30...
}

def page_get(q):
    params['q']= q
    for page in range(1, 11):
        params['start'] = (page-1)*10
        page_url = url+ urlencode(params)
        req =Request(page_url,
                     headers=headers)
        response = urlopen(req)

        assert response.code == 200
        with open('pages/%s-%s.html' %(q, page), 'wb') as file:
            bytes_ = response.read()
            file.write(bytes_)

        print('download %s %s erfolgreich' %(q, page))

page_get('python 3.6')

