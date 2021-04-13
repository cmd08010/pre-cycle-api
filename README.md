[![General Assembly Logo](https://camo.githubusercontent.com/1a91b05b8f4d44b5bbfb83abac2b0996d8e26c92/687474703a2f2f692e696d6775722e636f6d2f6b6538555354712e706e67)](https://generalassemb.ly/education/web-development-immersive)

# Django Auth Template

This template contains a project, `django_auth_template`, and an app, `api`,
which are set up complete with user authentication and an example resource,
`Mango`, which has an example user ownership implementation.

## Preparation

1. [Download](../../archive/master.zip) this template.
1. Move the .zip file to your `sei/projects/` directory and Unzip it (creating a
   folder) -- **NOTE:** if the folder was already unzipped, use the `mv` command
   line to move it to the `sei/projects/` directory.
1. Empty [`README.md`](README.md) and fill with your own content.
1. Move into the new project and `git init`.
1. Create and checkout to a new branch, `training`, for your work.
1. Create a `.env` file
1. Add a key `ENV` with the value `development` **exactly**.
    1. Note: When you deploy, you will create this key on Heroku the value `production`. This will distinguish the development and production settings set in this template.
1. Run `pipenv shell` to start up your virtual environment **in the `django-env` folder**.
1. Run `pipenv install django-rest-auth django-cors-headers python-dotenv dj-database-url` **in the `django-env` folder**.
     1. Note: Any future Django projects you build in the `django-env` folder will have access to these packages.
2. Create a psql database for your project
    1. Edit `settings.sql` then run `psql -U postgres -f settings.sql`
    OR:
    1. Run `createdb "project_db_name"`
    OR:
    1. Type `psql` to get into interactive shell.
    2. Run `CREATE DATABASE "project_db_name";` where `project_db_name` is the name you want for your database.
1. Add the database name to the `.env` file using the key `DB_NAME_DEV`.
1. Replace all instances of `django_auth_template` with your application name. **This includes the folder included in this repository.**
2. Generate a secret key using [this tool](https://djecrety.ir) and add it to the `.env` file using the key `SECRET`.
1. Open the repository in Atom with `atom .`
2. Make sure to read the [Connecting Client](#connecting-client) section
for connecting with your `browser-template` or `react-auth-template` based
project.

### The `.env` File

After following the steps above, your `.env` file should look _something_ like
the following, replacing `project_db_name` with your database name and
`secret_key` with your secret key.

```sh
ENV=development
DB_NAME_DEV=project_db_name
SECRET=secret_key
```

## Structure

This template includes a project `django_auth_template` which should be renamed
as part of the set-up steps. It includes the `settings.py` file with special
settings to be able to run both locally and on production. **DO NOT ADD A NEW
OR MODIFY THE CURRENT `DATABASES` DEFINITION UNLESS INSTRUCTED TO DO SO.**

There is also an app `api` which can be renamed if necessary. The `api` app
includes folders for models and view files, which can then be imported into
`urls.py` for use.

## Commands

Commands are run with the syntax `python3 manage.py <command>`:

| command | action |
|---------|--------|
| `runserver`  |  Run the server |
| `makemigrations`  | Generate migration files based on changes to models  |
| `migrate`  | Run migration files to migrate changes to db  |
| `startapp`  | Create a new app  |

## Deployment

Before deploying, make sure you have renamed your project folder and replaced
all instances of `django_auth_template` with your app's name.

Once ready, you can follow the steps in the [django-heroku-deployment-guide](https://git.generalassemb.ly/ga-wdi-boston/django-heroku-deployment-guide).

## Connecting Client

This template is intentionally minimal, and does not override many of Django's
defaults. This means connecting either the `browser-template` or `react-auth-template` clients to this backend involves updating that client code slightly.

Ultimately, Django and any other backend API framework should be able to build
standalone backend APIs that can talk to any client. We just have to make sure
the client is following some of the expectations that Django has by default.

### Port

When working on our "local" computer, we work on the `localhost` location. This
is paired with a port number to identify where our server is running on our
local machine. Our client templates use port `7165`, for example, and run at
`http://localhost:7165`.

These templates also talk to a backend at a certain port, which is set to `4147`
in the client templates. **We need to change the port in the URL the client
application uses when running locally.**

In the `browser-template` this means modifying the `config.js` file, and in the
`react-auth-template` the `apiConfig.js` file.

This django template uses the port `8000` by default, so any client speaking to
this template's default server location would be `http://localhost:8000`.

### URL Syntax

Django defaults to expecting (and requiring) trailing forward slashes `/` on
requests. You'll need to make sure any requests you make from a client to this
template look something like `http://localhost:8000/books/`.

### Token Syntax

We've gotten used to the token syntax that the Express framework expects:

```
Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

However, the DRF [`TokenAuthentication`](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) class in this template is what defines
what our token syntax should look like when the client make an authenticated
request to our Django application.

When making authenticated requests from any client, make sure your tokens
follow this pattern:

```
Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Incoming Request Data

Our JavaScript conventions are to use `camelCase` when defining almost everything, however Python conventions (and therefore Django conventions) use
`snake_case` instead. We have to keep this in mind when sending data from a
client to a Django application.

### Handle JSON Data

> Note: This section is only necessary if you are connecting this template to
> the `browser-template` and/or using the `$.ajax` method.

### Stringify Your Request Data

When sending data with AJAX, we must stringify it with `JSON.stringify`. See the below example:

```js
const create = function (data) {
  return $.ajax({
    url: config.apiUrl + '/mangos/',
    method: 'POST',
    headers: {
      Authorization: 'Token ' + store.user.token
    },
    data: JSON.stringify(data)
  })
}
```

### Have Django Load the JSON Data

The `request.data` object becomes a QueryDict, and generally doesn't look the way we expect.

Instead of `request.data`, you must use `request.body`. We can then load the body as JSON with `json.loads`.

See the below (focusing on just the data) example:

```py
# Import the `json` module
import json

....

class Mangos(APIView):
    def post(self, request):
        # Create variable to store readable JSON data
        data = json.loads(request.body)
        # pass the now Dictionary to the serializer, doing whatever you need
        serializer = MySerializer(data=data['resource'])
.....

```

## Debugging

`pipenv shell` moved me into a different directory!

> Pipenv wants to be in the root directory, so if it thinks it's not then it
> will move you to what it thinks is the root of your repository. Exit out
> of the shell with `exit`, then check if the folder it moved you to is a git
> repository. If you see a `.git` folder inside of the `trainings` folder,
> for example, delete that folder so that `trainings` is no longer a "git repo."
> Then, you can change back into your project directory and try running
> `pipenv shell` again.

`pipenv shell` is complaining about my python version not matching

> Our python version is defined in the `Pipfile`. Simply replace the current
> `python_version = "x.x"` statement with the appropriate version.

SyntaxError pointing to `manage.py` when trying to run the server, migrate, etc.

> Double-check your python version with `python --version`. If you see a "2.x.x"
> version, then you need to use the command `python3` when running python
> scripts. You can also follow these guides to replace your `python` command so
> it always uses python3.
>
> Mac: https://stackoverflow.com/questions/49704364/make-python3-as-my-default-python-on-mac/49711594
>
> Linux: https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux

Error: No module named <my-projects-name> when trying to run the server

> If Python can't find the module that is your project name, then very likely
> you forgot a very important piece of the preparation steps. You need to
> make sure you rename the project folder as well.

I made changes to my models & ran my migrations but it says "No migrations to apply"

> Double-check that you **generated** the migration files before you tried
> to run them. This means running `makemigrations` before `migrate`.

Errors with `psycopg2`

> There's a lot to read about this issue if you want:
> https://github.com/psycopg/psycopg2/issues/674
> https://www.psycopg.org/articles/2018/02/08/psycopg-274-released/
>
> This template uses `psycopg2-binary` to minimize errors during project
> development. If you have errors with `psycopg2` anyway, notify an instructor.

## Additional Resources

- [Django Rest Framework Tutorial: Authentication](https://www.django-rest-framework.org/api-guide/authentication)

## [License](LICENSE)

1.  All content is licensed under a CC­BY­NC­SA 4.0 license.
1.  All software code is licensed under GNU GPLv3. For commercial use or
    alternative licensing, please contact legal@ga.co.
