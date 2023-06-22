from django.contrib.auth.base_user import BaseUserManager


class ManagerUser(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, password,
                     **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password,
                    **extra_fields):
        return self._create_user(email,
                                 first_name,
                                 last_name,
                                 password,
                                 **extra_fields)

    def create_superuser(self, email, first_name, last_name, password,
                         **extra_fields):
        user = self._create_user(email,
                                 first_name,
                                 last_name,
                                 password,
                                 **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
