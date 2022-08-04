

## 修改

- ### get_user_model

```
\venv\Lib\site-packages\django\contrib\auth\__init__.py
```

```python
def get_user_model(flag=None):
    """
    Return the User model that is active in this project.
    """
    try:
        if flag == 1:
            return django_apps.get_model(settings.AUTH_USER_MODEL2, require_ready=False)
        else:
            return django_apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
        )


```



- ### authentication

```
E:\kifFile\tangkang\tangkang_backend\venv\Lib\site-packages\rest_framework_simplejwt\authentication.py
```

```python
 def authenticate(self, request):
        header = self.get_header(request)
        
        isMiniapp = re.search('miniapp', request.path)
        print('isMiniapp', isMiniapp)
        if isMiniapp:
            self.user_model = get_user_model(flag=1)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
```

