===============
Online Exam
===============

Online test application lets user(student) take an online programming test.
A special user called moderator can add questions, create question paper, 
conduct online test and monitor the test.


Quick start
------------

1. In your terminal run the following command::
    $ easy_install git+https://github.com/FOSSEE/online_test.git#egg=django_exam-0.1

2. Add "testapp.exam", "taggit" and "taggit_autocomplete_modified" apps 
   to your INSTALLED_APPS setting as follows::

    INSTALLED_APPS =(
        'testapp.exam',
        'taggit',
        'taggit_autocomplete_modified',
    )

3. In project settings, add AUTH_PROFILE_MODULE = 'testapp.exam.Profile'
   You can change the testapp.exam.Profile to your desired app user profile.

4. Include the "testapp.exam" and taggit_autocomplete_modified URL configuration
   in your project urls.py as follows::

    url(r'^exam/', include('testapp.exam.urls')),
    url(r'^taggit_autocomplete_modified/', include\
                                        ('taggit_autocomplete_modified.urls'))


5. Run 'python manage.py syncdb' to create models for the new installed apps.

6. Run 'python manage.py runserver' to start the development server
   and visit http://localhost:8000/exam/

7. Run code_server command as superuser as follows::

       $ sudo code_server

   Note: If you are using virtual python environment, then activate the environment
         using sudo. Then simply run the code_server command as follows::

         $ code_server
