# Description

A simple test application using python backend and angular frontend.
This is just for illustration purpose for an Aalam cloud developer.


# How to start

1. Create the resources folder and installed @angular/cli using
```
npm install @angular/cli
```
2. Next create a new angular app using
```
cd resources && ng new --dir .  --routing py-ang-testapp
```

4. Modify the src/index.html to have the proper base URL
```
<base href="/aalam/py-ang-testapp"/>
```

5. Add the build.sh to build a ahead-of-time compiled app so that it will
be optimized to run faster when loaded.  Notice the build.sh modifies
path of the javascript files to point to the static URL prefix.

6. Whenever a change is made to the angular app, run ```./build.sh```. This will
keep the dist folder ready


# REDIS or MYSQL Database

In app.py, if you set ```USE_REDISDB``` to ```True``` it will use the redis database,
else it will use MYSQL database using sqlalchemy.
