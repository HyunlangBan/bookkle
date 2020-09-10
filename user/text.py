def message(domain, uidb64, token):
    return f'안녕하세요, 북끌에 가입해주셔서 감사합니다. 아래 링크를 클릭하면 회원가입 인증이 완료됩니다. \n\n http://{domain}/accounts/activate/{uidb64}/{token}'
