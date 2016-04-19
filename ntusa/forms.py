from django.contrib.auth.forms import AuthenticationForm

class HintedAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(HintedAuthenticationForm, self).__init__(*args, **kwargs)
        username_widget = self.fields['username'].widget
        username_widget.attrs['placeholder'] = '使用者名稱'
        username_widget.attrs['required'] = True

        password_widget = self.fields['password'].widget
        password_widget.attrs['placeholder'] = '密碼'
        password_widget.attrs['required'] = True
