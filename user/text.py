def message(domain, uidb64, token):
    return f'안녕하세요, 북끌에 가입해주셔서 감사합니다. 아래 링크를 클릭하면 회원가입 인증이 완료됩니다. \n\n 이 인증 링크는 일회성으로, 로딩중에 페이지를 나가면 인증이 되지 않습니다. 로딩이 긴 경우 조금만 기다려주시면 감사하겠습니다. \n\n  http://{domain}/accounts/activate/{uidb64}/{token}'
