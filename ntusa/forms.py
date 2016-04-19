from django.contrib.auth.forms import AuthenticationForm

class HintedAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(HintedAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = '使用者名稱'
        self.fields['password'].widget.attrs['placeholder'] = '密碼'
